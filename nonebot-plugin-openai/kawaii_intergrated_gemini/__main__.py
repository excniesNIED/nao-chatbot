# __main__.py (最终修复版 - 移除 ClientOptions)

import configparser
import google.generativeai as genai
from pathlib import Path

from nonebot import on_message
from nonebot.params import Depends
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent

from nonebot_plugin_uninfo import get_session, Session
from .data_source import LOADED_REPLY_DICT
from .utils import search_reply_dict, choice_reply_from_ev, finish_multi_msg

# --- 1. 加载 Gemini 配置 ---
try:
    config_path = Path(__file__).parent / "gemini_config.ini"
    if not config_path.exists():
        logger.warning("插件配置文件 'gemini_config.ini' 不存在，将无法使用 AI 对话功能。")
        gemini_model = None
    else:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        gemini_api_key = config.get('gemini', 'gemini_api_key')
        gemini_model_name = config.get('gemini', 'gemini_model_name')
        model_name = config.get('gemini', 'model_name')
        system_prompt = config.get('gemini', 'system_prompt')

        if not all([gemini_api_key, gemini_model_name]):
            raise ValueError("gemini_config.ini 中的 gemini_api_key 和 gemini_model_name 不能为空。")

        # --- 2. 初始化 Gemini 客户端 ---
        # Gemini 库会自动通过环境变量读取代理设置
        genai.configure(api_key=gemini_api_key)
        
        gemini_model = genai.GenerativeModel(
            model_name=gemini_model_name,
            system_instruction=system_prompt + f"你的名字是{model_name}。"
        )
        logger.info(f"Google Gemini 客户端初始化成功, 模型: {gemini_model_name}")

except Exception as e:
    logger.error(f"加载 Gemini 配置失败，将无法使用 AI 对话功能: {e}")
    gemini_model = None


# --- 3. 创建响应器 ---
search_matcher = on_message(
    rule=to_me(), 
    priority=10, 
    block=True
)


async def get_gemini_response(prompt: str) -> str:
    """
    异步调用 Google Gemini API 获取回复。
    """
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
    
    # 2. 如果未命中，则调用 Gemini
    else:
        response_text = await get_gemini_response(msg)
        
        if not response_text:
            logger.warning("AI 功能未启用或未能生成回复，已跳过。")
            await search_matcher.finish()

        reply_template = "{at}\n" + response_text
        formatted_messages = await choice_reply_from_ev(ss, [reply_template])
        await finish_multi_msg(formatted_messages)