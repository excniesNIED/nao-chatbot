# __main__.py (Definitive Final Version - Removed "Thinking" Message)

import configparser
import openai
import random
from pathlib import Path

from nonebot import on_message
from nonebot.params import Depends
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent

# Import the necessary components from the plugin's ecosystem
from nonebot_plugin_uninfo import get_session, Session
from .data_source import LOADED_REPLY_DICT
from .utils import search_reply_dict, choice_reply_from_ev, finish_multi_msg


# --- Load OpenAI Configuration ---
try:
    config_path = Path(__file__).parent / "openai_config.ini"
    if not config_path.exists():
        logger.warning("Plugin configuration file 'openai_config.ini' not found. AI chat functionality will be disabled.")
        client = None
    else:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        
        api_url = config.get('openai', 'api_url')
        api_key = config.get('openai', 'api_key')
        model_id = config.get('openai', 'model_id')
        model_name = config.get('openai', 'model_name')
        system_prompt = config.get('openai', 'system_prompt')

        if not all([api_url, api_key, model_id]):
            raise ValueError("api_url, api_key, and model_id in openai_config.ini cannot be empty.")

        # --- Initialize OpenAI Client ---
        client = openai.AsyncOpenAI(
            base_url=api_url,
            api_key=api_key,
        )
        logger.info("OpenAI client initialized successfully.")

except Exception as e:
    logger.error(f"Failed to load OpenAI configuration. AI chat functionality will be disabled: {e}")
    client = None


# --- Create Matcher ---
search_matcher = on_message(
    rule=to_me(), 
    priority=10, 
    block=True
)


async def get_openai_response(prompt: str) -> str:
    """
    Asynchronously get a response from the OpenAI compatible API.
    """
    if not client:
        return ""
        
    try:
        messages = [
            {"role": "system", "content": system_prompt + f"Your name is {model_name}."},
            {"role": "user", "content": prompt}
        ]

        logger.info(f"Local dictionary not hit, calling OpenAI API (Model: {model_id})")
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "唔... 我好像不知道该怎么回答了..."

    except Exception as e:
        logger.error(f"An unexpected error occurred while calling OpenAI: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"


# --- Main Handler ---
@search_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    msg = event.get_plaintext().strip()

    if not msg:
        return

    # 1. Check local dictionary
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"Message hit in local dictionary: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)
    
    # 2. If not found, call OpenAI
    else:
        # ========================================================
        # The "thinking" message below has been removed.
        # await search_matcher.send("唔...让我想想~ 🤔")
        # ========================================================
        response_text = await get_openai_response(msg)
        
        if not response_text:
            logger.warning("AI is disabled or failed to generate a response. Execution stopped.")
            await search_matcher.finish()

        reply_template = "{at}\n" + response_text
        formatted_messages = await choice_reply_from_ev(ss, [reply_template])
        await finish_multi_msg(formatted_messages)