# __main__.py (最终修复版 - 增加群聊白名单功能)

import configparser
import openai
from pathlib import Path

from nonebot import on_message
from nonebot.params import Depends
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
# 导入 GroupMessageEvent 用于判断事件类型
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from nonebot_plugin_uninfo import get_session, Session
from .data_source import LOADED_REPLY_DICT
from .utils import search_reply_dict, choice_reply_from_ev, finish_multi_msg

# --- 加载 OpenAI 配置 ---
try:
    config_path = Path(__file__).parent / "openai_config.ini"
    if not config_path.exists():
        logger.warning("插件配置文件 'openai_config.ini' 不存在，将无法使用 AI 对话功能。")
        client = None
        enabled_groups = [] # 初始化为空列表
    else:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        api_url = config.get('openai', 'api_url')
        api_key = config.get('openai', 'api_key')
        model_id = config.get('openai', 'model_id')
        model_name = config.get('openai', 'model_name')
        system_prompt = config.get('openai', 'system_prompt')

        # === 新增代码：读取并解析群聊白名单 ===
        enabled_groups_str = config.get('openai', 'enabled_groups', fallback='')
        if enabled_groups_str:
            enabled_groups = [group.strip() for group in enabled_groups_str.split(',')]
            logger.info(f"AI对话功能已加载，将在指定的 {len(enabled_groups)} 个群聊中生效。")
        else:
            enabled_groups = []
            logger.info("AI对话功能已加载，未配置生效群聊，将在所有群聊和私聊中生效。")
        # === 新增代码结束 ===

        if not all([api_url, api_key, model_id]):
            raise ValueError("api_url, api_key, and model_id in openai_config.ini cannot be empty.")

        # --- 初始化 OpenAI 客户端 ---
        client = openai.AsyncOpenAI(
            base_url=api_url,
            api_key=api_key,
        )
        logger.info("OpenAI client initialized successfully.")

except Exception as e:
    logger.error(f"加载 OpenAI 配置失败，AI 对话功能将被禁用: {e}")
    client = None
    enabled_groups = [] # 异常时同样初始化为空列表

# --- 创建响应器 ---
# 确保插件优先级低于本地词库插件，作为补充回复
search_matcher = on_message(
    rule=to_me(), 
    priority=10, # 与可爱机器人插件的优先级保持一致或稍低
    block=True
)

async def get_openai_response(prompt: str) -> str:
    """
    异步调用OpenAI兼容API获取回复。
    """
    if not client:
        return ""
        
    try:
        messages = [
            {"role": "system", "content": system_prompt + f"你的名字是{model_name}。"},
            {"role": "user", "content": prompt}
        ]

        logger.info(f"本地词库未命中，开始调用 OpenAI API (Model: {model_id})")
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "唔... 我好像不知道该怎么回答了..."

    except Exception as e:
        logger.error(f"调用 OpenAI 时发生错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"

# --- 主处理函数 ---
@search_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    msg = event.get_plaintext().strip()

    if not msg:
        return

    # 1. 检查本地词库 (kawaii-robot)
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"消息在本地词库命中: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)
    
    # 2. 如果本地词库未命中，则判断是否调用 OpenAI
    else:
        # === 新增代码：检查群聊是否在白名单中 ===
        if isinstance(event, GroupMessageEvent):
            # 如果配置了白名单，并且当前群号不在白名单内
            if enabled_groups and str(event.group_id) not in enabled_groups:
                logger.info(f"群聊 {event.group_id} 未在AI对话白名单中，已跳过。")
                # 直接结束处理，不再响应
                await search_matcher.finish()
        # === 新增代码结束 ===

        # 如果检查通过 (是私聊，或在白名单群聊中，或未设置白名单)，则继续调用AI
        response_text = await get_openai_response(msg)
        
        if not response_text:
            logger.warning("AI功能未启用或未能生成回复，已跳过。")
            await search_matcher.finish()

        # 使用与可爱机器人插件相同的回复格式发送消息
        reply_template = "{at}\n{ai_response}"
        formatted_messages = await choice_reply_from_ev(
            ss, [reply_template], ai_response=response_text
        )
        await finish_multi_msg(formatted_messages)