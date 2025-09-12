# __main__.py (混合模式: OpenAI for RAG search, Gemini for Generation, 统一回复格式)

import configparser
import google.generativeai as genai
from openai import OpenAI
import pandas as pd
import numpy as np
from pathlib import Path

from nonebot import on_message
from nonebot.params import Depends
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from nonebot_plugin_uninfo import get_session, Session
from .data_source import LOADED_REPLY_DICT
from .utils import search_reply_dict, choice_reply_from_ev, finish_multi_msg

# --- 全局配置和变量 ---
gemini_config_path = Path(__file__).parent / "gemini_config.ini"
openai_config_path = Path(__file__).parent / "openai_config.ini"
db_path = Path(__file__).parent / "embeddings_database.pkl"

gemini_model = None
openai_client = None
openai_embedding_model = None
df_embeddings = None
enabled_groups = []

# --- 初始化模块 ---
def setup_plugin():
    """在插件加载时执行所有初始化操作"""
    global gemini_model, openai_client, openai_embedding_model, df_embeddings, enabled_groups

    # 1. 加载 Gemini 配置 (用于对话生成)
    try:
        if not gemini_config_path.exists():
            logger.warning("配置文件 'gemini_config.ini' 不存在，AI 对话功能将无法使用。")
        else:
            gemini_config = configparser.ConfigParser()
            gemini_config.read(gemini_config_path, encoding='utf-8')

            gemini_api_key = gemini_config.get('gemini', 'gemini_api_key')
            gemini_model_name = gemini_config.get('gemini', 'gemini_model_name')
            system_prompt = gemini_config.get('gemini', 'system_prompt')
            enabled_groups_str = gemini_config.get('gemini', 'enabled_groups', fallback='')
            enabled_groups = [g.strip() for g in enabled_groups_str.split(',') if g.strip()]

            if not all([gemini_api_key, gemini_model_name]):
                raise ValueError("gemini_api_key 和 gemini_model_name 不能为空。")

            genai.configure(api_key=gemini_api_key)
            gemini_model = genai.GenerativeModel(
                gemini_model_name,
                system_instruction=system_prompt,
            )
            logger.info(f"Gemini (Model: {gemini_model_name}) 初始化成功，用于对话生成。")
    except Exception as e:
        logger.error(f"加载 Gemini 配置或初始化模型失败: {e}")
        gemini_model = None

    # 2. 加载 OpenAI 配置 (用于 RAG 检索)
    try:
        if not openai_config_path.exists():
             logger.warning("配置文件 'openai_config.ini' 不存在，知识库检索功能将无法使用。")
        else:
            openai_config = configparser.ConfigParser()
            openai_config.read(openai_config_path, encoding='utf-8')

            api_url = openai_config.get('openai', 'api_url')
            api_key = openai_config.get('openai', 'api_key')
            openai_embedding_model = openai_config.get('openai', 'embedding_model_id')

            if not all([api_url, api_key, openai_embedding_model]):
                 raise ValueError("请确保 openai_config.ini 中已正确配置 api_url, api_key, 和 embedding_model_id。")

            openai_client = OpenAI(base_url=api_url, api_key=api_key)
            logger.info(f"OpenAI 客户端初始化成功 (Model: {openai_embedding_model})，用于知识库检索。")
    except Exception as e:
        logger.error(f"加载 OpenAI 配置或初始化客户端失败: {e}")
        openai_client = None


    # 3. 加载 Embeddings 数据库
    try:
        if db_path.exists():
            df_embeddings = pd.read_pickle(db_path)
            logger.info(f"成功加载 Embeddings 数据库，共 {len(df_embeddings)} 条知识。")
        else:
            logger.warning(f"Embeddings 数据库 '{db_path.name}' 不存在，知识库问答功能将不可用。")
    except Exception as e:
        logger.error(f"加载 Embeddings 数据库失败: {e}")
        df_embeddings = None

# 在插件加载时执行初始化
setup_plugin()

# --- RAG 和 AI 对话核心函数 ---
def find_best_passage_with_openai(query: str, dataframe: pd.DataFrame, top_k=3):
    """【使用 OpenAI API】在向量数据库中查找与问题最相关的文本块"""
    if dataframe is None or dataframe.empty or openai_client is None:
        return None

    try:
        response = openai_client.embeddings.create(
            input=[query],
            model=openai_embedding_model
        )
        query_embedding = response.data[0].embedding

        dot_products = np.dot(np.stack(dataframe['embeddings']), query_embedding)
        top_indices = np.argsort(dot_products)[-top_k:][::-1]
        context = "\n---\n".join(dataframe.iloc[idx]['text'] for idx in top_indices)
        
        return context
    except Exception as e:
        logger.error(f"使用 OpenAI API 检索知识库时发生错误: {e}")
        return None

async def get_rag_response(prompt: str) -> str | None:
    """获取基于知识库的回答 (RAG)"""
    if df_embeddings is None:
        return None

    logger.info("本地词库未命中，开始在知识库中检索 (using OpenAI Embeddings)...")
    relevant_passage = find_best_passage_with_openai(prompt, df_embeddings)

    if not relevant_passage:
        logger.info("知识库中未找到相关内容。")
        return None

    logger.info("已在知识库中找到相关上下文，开始生成回答 (using Gemini)...")
    
    rag_prompt = f"""
    你是一个问答机器人，请根据下面提供的上下文信息来回答用户的问题。
    请只使用上下文中的信息，如果上下文没有提供足够的信息来回答问题，请直接回复：“根据我现有的知识，我无法回答这个问题。”

    ---
    上下文信息:
    {relevant_passage}
    ---
    用户问题: {prompt}
    回答:
    """
    
    try:
        response = await gemini_model.generate_content_async(rag_prompt)
        return response.text if response.text else None
    except Exception as e:
        logger.error(f"使用 RAG 调用 Gemini 生成回答时发生错误: {e}")
        return "呜...生成回答时出错了，请联系我的主人检查一下后台日志吧。"

async def get_general_gemini_response(prompt: str) -> str:
    """获取通用的 Gemini 对话回复"""
    if not gemini_model:
        return "AI 功能当前不可用哦~"
    
    logger.info("知识库检索无果，开始调用通用对话模型 (using Gemini)...")
    try:
        chat = gemini_model.start_chat(history=[])
        response = await chat.send_message_async(prompt)
        return response.text if response.text else "唔... 我好像不知道该怎么回答了..."
    except Exception as e:
        logger.error(f"调用通用 Gemini 对话时发生错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"

# --- 创建响应器 ---
search_matcher = on_message(
    rule=to_me(),
    priority=10,
    block=True
)

# --- 主处理函数 ---
@search_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    msg = event.get_plaintext().strip()
    if not msg:
        return

    # 步骤 1: 检查本地词库
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"消息在本地词库命中: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)
        return

    # AI 功能的权限检查
    if isinstance(event, GroupMessageEvent):
        if enabled_groups and str(event.group_id) not in enabled_groups:
            logger.info(f"群聊 {event.group_id} 未在AI对话白名单中，已跳过。")
            return

    # 为 API 回复定义一个统一的模板，包含 {at} 变量
    reply_template = "{at}\n{response}"
    response_text = ""

    # 步骤 2: 尝试从知识库 (RAG) 获取回答
    rag_response_text = await get_rag_response(msg)
    if rag_response_text:
        response_text = rag_response_text
    else:
        # 步骤 3: Fallback 到通用对话模型
        response_text = await get_general_gemini_response(msg)

    # 使用与本地词库相同的格式化工具来发送包含 @ 的回复
    formatted_messages = await choice_reply_from_ev(ss, [reply_template], response=response_text)
    await finish_multi_msg(formatted_messages)