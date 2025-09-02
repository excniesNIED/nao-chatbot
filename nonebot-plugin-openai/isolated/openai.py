# openai.py (独立运行版，不依赖 kawaii-robot)

import configparser
import openai
from pathlib import Path

from nonebot import on_message
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, MessageSegment

# --- 1. 加载 OpenAI 配置 ---
try:
    config_path = Path(__file__).parent / "openai_config.ini"
    if not config_path.exists():
        logger.warning("独立OpenAI插件配置文件 'openai_config.ini' 不存在，插件将不会工作。")
        client = None
        enabled_groups = []
    else:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        api_url = config.get('openai', 'api_url')
        api_key = config.get('openai', 'api_key')
        model_id = config.get('openai', 'model_id')
        model_name = config.get('openai', 'model_name')
        system_prompt = config.get('openai', 'system_prompt')

        # 读取并解析群聊白名单
        enabled_groups_str = config.get('openai', 'enabled_groups', fallback='')
        if enabled_groups_str:
            enabled_groups = [group.strip() for group in enabled_groups_str.split(',')]
            logger.info(f"独立OpenAI插件已加载，将在指定的 {len(enabled_groups)} 个群聊中生效。")
        else:
            enabled_groups = []
            logger.info("独立OpenAI插件已加载，未配置生效群聊，将在所有群聊和私聊中生效。")

        if not all([api_url, api_key, model_id]):
            raise ValueError("api_url, api_key, and model_id in openai_config.ini cannot be empty.")

        # 初始化 OpenAI 客户端
        client = openai.AsyncOpenAI(
            base_url=api_url,
            api_key=api_key,
        )
        logger.info("独立OpenAI插件客户端初始化成功。")

except Exception as e:
    logger.error(f"加载独立OpenAI插件配置失败: {e}")
    client = None
    enabled_groups = []

# --- 2. 创建响应器 ---
# 优先级设为 10，block=True 表示成功响应后不再传递事件
chat_matcher = on_message(
    rule=to_me(),
    priority=10,
    block=True
)

async def get_openai_response(prompt: str) -> str:
    """ 异步调用OpenAI API获取回复 """
    if not client:
        return ""

    try:
        messages = [
            {"role": "system", "content": system_prompt + f" 你的名字是{model_name}。"},
            {"role": "user", "content": prompt}
        ]
        logger.info(f"开始调用 OpenAI API (Model: {model_id})")
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "唔... 我好像不知道该怎么回答了..."

    except Exception as e:
        logger.error(f"调用 OpenAI 时发生错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"

# --- 3. 主处理函数 ---
@chat_matcher.handle()
async def handle_chat(event: MessageEvent, matcher: Matcher):
    # 如果配置加载失败，则直接结束
    if not client:
        await matcher.finish()

    # 检查是否为群聊且不在白名单内
    if isinstance(event, GroupMessageEvent):
        if enabled_groups and str(event.group_id) not in enabled_groups:
            logger.info(f"群聊 {event.group_id} 未在白名单中，独立OpenAI插件已跳过。")
            await matcher.finish() # 直接结束，不响应

    prompt = event.get_plaintext().strip()
    if not prompt:
        return

    # 调用API获取回复
    response_text = await get_openai_response(prompt)

    if response_text:
        # @用户 并发送回复
        await matcher.send(MessageSegment.at(event.get_user_id()) + Message(f"\n{response_text}"))