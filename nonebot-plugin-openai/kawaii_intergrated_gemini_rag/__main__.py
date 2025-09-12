# __main__.py (整合版 Gemini + kawaii-robot 词库)

import configparser
import google.generativeai as genai
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

# --- 加载 Gemini 配置 ---
try:
    config_path = Path(__file__).parent / "gemini_config.ini"
    if not config_path.exists():
        logger.warning("插件配置文件 'gemini_config.ini' 不存在，将无法使用 AI 对话功能。")
        gemini_model = None
        enabled_groups = []
    else:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        gemini_api_key = config.get('gemini', 'gemini_api_key')
        gemini_model_name = config.get('gemini', 'gemini_model_name')
        system_prompt = config.get('gemini', 'system_prompt')

        # 读取并解析群聊白名单
        enabled_groups_str = config.get('gemini', 'enabled_groups', fallback='')
        if enabled_groups_str:
            enabled_groups = [group.strip() for group in enabled_groups_str.split(',')]
            logger.info(f"Gemini AI对话功能已加载，将在指定的 {len(enabled_groups)} 个群聊中生效。")
        else:
            enabled_groups = []
            logger.info("Gemini AI对话功能已加载，未配置生效群聊，将在所有群聊和私聊中生效。")

        if not all([gemini_api_key, gemini_model_name]):
            raise ValueError("gemini_api_key 和 gemini_model_name 不能为空。")

        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel(
            gemini_model_name,
            system_instruction=system_prompt,
        )
        logger.info(f"Gemini (Model: {gemini_model_name}) 初始化成功。")

except Exception as e:
    logger.error(f"加载 Gemini 配置或初始化模型失败: {e}")
    gemini_model = None
    enabled_groups = []

# --- 创建响应器 ---
search_matcher = on_message(
    rule=to_me(),
    priority=10,
    block=True
)

async def get_gemini_response(prompt: str) -> str:
    """ 异步调用 Google Gemini API 获取回复。 """
    if not gemini_model:
        return ""

    try:
        chat = gemini_model.start_chat(history=[])
        logger.info(f"词库未命中，开始调用 Gemini API (Model: {gemini_model.model_name})")
        response = await chat.send_message_async(prompt)
        return response.text if response.text else "唔... 我好像不知道该怎么回答了..."

    except Exception as e:
        logger.error(f"调用 Gemini 时发生错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"


# --- 主处理函数 ---
@search_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    msg = event.get_plaintext().strip()

    if not msg:
        return

    # 1. 检查本地词库
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"消息在本地词库命中: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)

    # 2. 如果本地词库未命中，则判断是否调用 Gemini
    else:
        # 检查是否为群聊且不在白名单内
        if isinstance(event, GroupMessageEvent):
            if enabled_groups and str(event.group_id) not in enabled_groups:
                logger.info(f"群聊 {event.group_id} 未在AI对话白名单中，已跳过。")
                await search_matcher.finish() # 结束处理

        # 如果检查通过 (是私聊，或在白名单群聊中，或未设置白名单)，则继续调用AI
        response_text = await get_gemini_response(msg)

        if not response_text:
            logger.warning("AI功能未启用或未能生成回复，已跳过。")
            await search_matcher.finish()

        # 使用与可爱机器人插件相同的回复格式发送消息
        reply_template = "{at}\n{ai_response}"
        formatted_messages = await choice_reply_from_ev(
            ss, [reply_template], ai_response=response_text
        )
        await finish_multi_msg(formatted_messages)