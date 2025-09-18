# __main__.py (整合 RAG + Gemini + kawaii-robot 词库)

import asyncio
import configparser
import random
import google.generativeai as genai
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict

from nonebot import on_message, on_notice, on_command
from nonebot.params import Depends
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    MessageEvent, 
    GroupMessageEvent, 
    PrivateMessageEvent,
    PokeNotifyEvent,
    Message
)

from nonebot_plugin_uninfo import get_session, Session
from .data_source import (
    LOADED_REPLY_DICT, 
    LOADED_POKE_REPLY, 
    LOADED_UNKNOWN_REPLY,
    LOADED_INTERRUPT_MSG,
    reload_replies
)
from .utils import (
    search_reply_dict, 
    choice_reply_from_ev, 
    finish_multi_msg,
    check_percentage
)
from .config import config

# --- 全局配置和变量 ---
config_path = Path(__file__).parent / "gemini_config.ini"
db_path = Path(__file__).parent / "embeddings_database.pkl"
gemini_model = None
df_embeddings = None
enabled_groups = []

# 复读检测数据结构
group_repeat_data = defaultdict(lambda: {"message": "", "count": 0, "users": set()})
repeat_lock = defaultdict(bool)  # 防止重复触发

# --- 初始化模块 ---
def setup_plugin():
    """在插件加载时执行所有初始化操作"""
    global gemini_model, df_embeddings, enabled_groups

    # 1. 加载 Gemini 配置
    try:
        if not config_path.exists():
            logger.warning("配置文件 'gemini_config.ini' 不存在，AI 功能将无法使用。")
            return

        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        gemini_api_key = config.get('gemini', 'gemini_api_key')
        gemini_model_name = config.get('gemini', 'gemini_model_name')
        system_prompt = config.get('gemini', 'system_prompt')

        enabled_groups_str = config.get('gemini', 'enabled_groups', fallback='')
        enabled_groups = [g.strip() for g in enabled_groups_str.split(',') if g.strip()]

        if not all([gemini_api_key, gemini_model_name]):
            raise ValueError("gemini_api_key 和 gemini_model_name 不能为空。")

        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel(
            gemini_model_name,
            system_instruction=system_prompt,
        )
        logger.info(f"Gemini (Model: {gemini_model_name}) 初始化成功。")
        if enabled_groups:
            logger.info(f"AI 对话功能将在 {len(enabled_groups)} 个指定群聊中生效。")
        else:
            logger.info("AI 对话功能未限制群聊，将在所有群聊和私聊中生效。")

    except Exception as e:
        logger.error(f"加载 Gemini 配置或初始化模型失败: {e}")
        gemini_model = None

    # 2. 加载 Embeddings 数据库
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
def find_best_passage(query: str, dataframe: pd.DataFrame, top_k=3):
    """在向量数据库中查找与问题最相关的文本块"""
    if dataframe is None or dataframe.empty:
        return None

    try:
        query_embedding_result = genai.embed_content(
            model='embedding-001',
            content=query,
            task_type="retrieval_query" # 用于检索的查询
        )
        query_embedding = query_embedding_result['embedding']

        # 计算点积相似度
        dot_products = np.dot(np.stack(dataframe['embeddings']), query_embedding)
        
        # 获取相似度最高的 top_k 个索引
        top_indices = np.argsort(dot_products)[-top_k:][::-1]
        
        # 拼接最相关的文本块作为上下文
        context = "\n---\n".join(dataframe.iloc[idx]['text'] for idx in top_indices)
        
        # 你可以增加一个相似度阈值判断，如果最高的相似度都太低，可以认为没有找到相关内容
        # max_similarity = dot_products[top_indices[0]]
        # if max_similarity < 0.7: # 阈值需要根据你的数据进行调整
        #     return None

        return context
    except Exception as e:
        logger.error(f"检索知识库时发生错误: {e}")
        return None

async def get_rag_response(prompt: str) -> str | None:
    """获取基于知识库的回答 (RAG)"""
    if not gemini_model or df_embeddings is None:
        return None

    logger.info("本地词库未命中，开始在知识库中检索...")
    relevant_passage = find_best_passage(prompt, df_embeddings)

    if not relevant_passage:
        logger.info("知识库中未找到相关内容。")
        return None

    logger.info("已在知识库中找到相关上下文，开始生成回答...")
    
    # 构建包含上下文的 Prompt
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
        logger.error(f"使用 RAG 调用 Gemini 时发生错误: {e}")
        return "呜...生成回答时出错了，请联系我的主人检查一下后台日志吧。"

async def get_general_gemini_response(prompt: str) -> str:
    """获取通用的 Gemini 对话回复"""
    if not gemini_model:
        return "AI 功能当前不可用哦~"
    
    logger.info("知识库检索无果，开始调用通用对话模型...")
    try:
        # 使用原始的 system_prompt 进行通用对话
        chat = gemini_model.start_chat(history=[])
        response = await chat.send_message_async(prompt)
        return response.text if response.text else "唔... 我好像不知道该怎么回答了..."
    except Exception as e:
        logger.error(f"调用通用 Gemini 对话时发生错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"

# --- 戳一戳处理器 ---
poke_matcher = on_notice(priority=5, block=False)

@poke_matcher.handle()
async def _(event: PokeNotifyEvent, ss: Session = Depends(get_session)):
    if config.leaf_poke_rand == -1:
        return
    
    if event.target_id != event.self_id:
        return  # 不是戳机器人的
    
    if not check_percentage(config.leaf_poke_rand):
        return
    
    await asyncio.sleep(random.uniform(*config.leaf_poke_action_delay))
    
    # 选择戳一戳回复
    reply_list = LOADED_POKE_REPLY if LOADED_POKE_REPLY else ["戳我干嘛~"]
    formatted_messages = await choice_reply_from_ev(ss, reply_list)
    await finish_multi_msg(formatted_messages)

# --- 复读检测处理器 ---
repeat_matcher = on_message(priority=20, block=False)

@repeat_matcher.handle()
async def _(event: GroupMessageEvent, ss: Session = Depends(get_session)):
    group_id = str(event.group_id)
    user_id = event.get_user_id()
    message_text = event.get_plaintext().strip()
    
    if not message_text or len(message_text) > 50:  # 忽略空消息和过长消息
        return
    
    # 忽略机器人自己的消息
    if user_id == str(event.self_id):
        return
    
    repeat_data = group_repeat_data[group_id]
    
    # 检查是否为相同消息
    if message_text == repeat_data["message"]:
        if config.leaf_force_different_user:
            if user_id not in repeat_data["users"]:
                repeat_data["count"] += 1
                repeat_data["users"].add(user_id)
        else:
            repeat_data["count"] += 1
    else:
        # 重置复读数据
        repeat_data["message"] = message_text
        repeat_data["count"] = 1
        repeat_data["users"] = {user_id}
        repeat_lock[group_id] = False
    
    # 检查是否触发复读或打断
    min_count, max_count = config.leaf_repeater_limit
    if repeat_data["count"] >= min_count and not repeat_lock[group_id]:
        if repeat_data["count"] <= max_count:
            # 决定是复读还是打断
            if check_percentage(config.leaf_interrupt):
                # 打断复读
                if not config.leaf_interrupt_continue:
                    repeat_lock[group_id] = True
                interrupt_list = LOADED_INTERRUPT_MSG if LOADED_INTERRUPT_MSG else ["打断！"]
                formatted_messages = await choice_reply_from_ev(ss, interrupt_list)
                await finish_multi_msg(formatted_messages)
            else:
                # 参与复读
                if not config.leaf_repeat_continue:
                    repeat_lock[group_id] = True
                await asyncio.sleep(random.uniform(0.5, 2.0))
                await repeat_matcher.send(Message(message_text))

# --- 非@消息处理器 ---
casual_matcher = on_message(priority=99, block=False)

@casual_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    # 检查是否为@消息，如果是则跳过（由主处理器处理）
    if event.is_tome():
        return
    
    # 检查是否需要@才能触发词库回复
    if config.leaf_need_at:
        return
    
    # 检查权限设置
    if config.leaf_permission == "GROUP" and isinstance(event, PrivateMessageEvent):
        return
    
    # 检查忽略词
    msg = event.get_plaintext().strip()
    if not msg:
        return
    
    for ignore_word in config.leaf_ignore:
        if msg.startswith(ignore_word):
            return
    
    # 概率检查
    if not check_percentage(config.leaf_trigger_percent):
        return
    
    # 搜索词库
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"非@消息在本地词库命中: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)

# --- 主@消息处理器 ---
search_matcher = on_message(
    rule=to_me(),
    priority=50,  # 调整优先级，避免与banword等插件冲突
    block=True
)

# --- 主处理函数 ---
@search_matcher.handle()
async def _(event: MessageEvent, ss: Session = Depends(get_session)):
    # 检查回复模式设置
    if config.leaf_reply_type == -1:
        return  # 关闭全部@回复
    
    msg = event.get_plaintext().strip()
    if not msg:
        return

    # 步骤 1: 检查本地词库
    if reply_list := search_reply_dict(LOADED_REPLY_DICT, msg):
        logger.info(f"消息在本地词库命中: '{msg}'")
        formatted_messages = await choice_reply_from_ev(ss, reply_list)
        await finish_multi_msg(formatted_messages)
        return

    # 如果设置为仅启用词库回复，则不进行AI回复
    if config.leaf_reply_type == 0:
        # 使用未知回复
        if LOADED_UNKNOWN_REPLY:
            formatted_messages = await choice_reply_from_ev(ss, LOADED_UNKNOWN_REPLY)
            await finish_multi_msg(formatted_messages)
        return

    # AI 功能的权限检查（仅在启用所有回复时）
    if isinstance(event, GroupMessageEvent):
        if enabled_groups and str(event.group_id) not in enabled_groups:
            logger.info(f"群聊 {event.group_id} 未在AI对话白名单中，已跳过。")
            return # 直接结束，不再响应

    # 步骤 2: 尝试从知识库 (RAG) 获取回答
    rag_response_text = await get_rag_response(msg)
    if rag_response_text:
        await search_matcher.finish(rag_response_text)
        return

    # 步骤 3: Fallback 到通用对话模型
    general_response_text = await get_general_gemini_response(msg)
    await search_matcher.finish(general_response_text)

# --- 重载词库命令处理器 ---
if config.leaf_register_reload_command:
    reload_matcher = on_command("重载词库", priority=1, block=True)
    
    @reload_matcher.handle()
    async def _(event: MessageEvent):
        # 简单的权限检查 - 只允许超级用户或群管理员使用
        user_id = event.get_user_id()
        
        # 检查是否为超级用户
        from nonebot import get_driver
        driver = get_driver()
        superusers = driver.config.superusers
        
        is_superuser = user_id in superusers
        is_admin = False
        
        # 如果是群聊，检查是否为管理员
        if isinstance(event, GroupMessageEvent):
            # 这里可以添加更详细的权限检查逻辑
            # 为了简化，暂时只允许超级用户使用
            pass
        
        if not is_superuser:
            await reload_matcher.finish("只有超级用户可以使用此命令喵~")
            return
        
        try:
            await reload_matcher.send("开始重载词库...")
            await reload_replies()
            await reload_matcher.finish("词库重载完成喵~")
        except Exception as e:
            logger.error(f"重载词库失败: {e}")
            await reload_matcher.finish(f"词库重载失败: {str(e)}")