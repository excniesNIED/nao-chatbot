# create_embeddings_db.py (使用 OpenAI 兼容 API 版本)
from openai import OpenAI
import pandas as pd
import PyPDF2
import markdown
import re
from pathlib import Path
import configparser
from nonebot.log import logger
import time

# --- 配置 ---

# ↓↓↓ 在这个列表中指定你要向量化的知识库文件名 ↓↓↓
DOCUMENTS_TO_PROCESS = [
    "q_a.md",
    "reference1.pdf",
    "reference2.pdf"
]

# 使用新的配置文件
CONFIG_PATH = Path(__file__).parent / "openai_config.ini"
DOCS_PATH = Path(__file__).parent
DB_SAVE_PATH = Path(__file__).parent / "embeddings_database.pkl"

# --- 文本处理函数 (这部分无需改变) ---
def read_pdf(file_path: Path) -> str:
    """读取PDF文件内容"""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = "".join(page.extract_text() for page in reader.pages)
        logger.info(f"成功读取 PDF 文件: {file_path.name}")
        return text
    except Exception as e:
        logger.error(f"读取 PDF 文件 {file_path.name} 失败: {e}")
        return ""

def read_md(file_path: Path) -> str:
    """读取Markdown文件内容并转换为纯文本"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = markdown.markdown(f.read())
            text = re.sub(r'<[^>]+>', '', html)
        logger.info(f"成功读取 Markdown 文件: {file_path.name}")
        return text
    except Exception as e:
        logger.error(f"读取 Markdown 文件 {file_path.name} 失败: {e}")
        return ""

def split_text_into_chunks(text: str, max_chunk_size=1000, overlap=100) -> list[str]:
    """将长文本分割成带有重叠部分的块"""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        chunks.append(text[start:end])
        start += max_chunk_size - overlap
    return chunks

# --- 主函数 ---
def create_and_save_embeddings():
    """主函数，用于创建和保存文本嵌入"""
    # 1. 加载 OpenAI 配置并初始化客户端
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH, encoding='utf-8')
        api_url = config.get('openai', 'api_url')
        api_key = config.get('openai', 'api_key')
        embedding_model_id = config.get('openai', 'embedding_model_id')

        if not all([api_url, api_key, embedding_model_id]):
            logger.error("请确保 openai_config.ini 中已正确配置 api_url, api_key, 和 embedding_model_id。")
            return

        client = OpenAI(base_url=api_url, api_key=api_key)
        logger.info(f"OpenAI 客户端初始化成功，将使用模型: {embedding_model_id}")

    except Exception as e:
        logger.error(f"加载 OpenAI 配置或初始化客户端失败: {e}")
        return

    # 2. 读取所有指定文档并分块 (与之前相同)
    all_chunks = []
    doc_files_to_process = [DOCS_PATH / f for f in DOCUMENTS_TO_PROCESS]

    for doc_file in doc_files_to_process:
        if not doc_file.exists():
            logger.warning(f"在配置中指定的文件 '{doc_file.name}' 未找到，已跳过。")
            continue
        content = ""
        if doc_file.suffix == '.pdf': content = read_pdf(doc_file)
        elif doc_file.suffix == '.md': content = read_md(doc_file)
        if content:
            chunks = split_text_into_chunks(content)
            all_chunks.extend(chunks)
            logger.info(f"文件 '{doc_file.name}' 已被分割成 {len(chunks)} 个文本块。")

    if not all_chunks:
        logger.error("未能从指定文档中提取任何文本内容，Embeddings 数据库创建失败。")
        return

    # 3. 为每个块生成Embeddings (使用 OpenAI API)
    logger.info(f"开始为 {len(all_chunks)} 个文本块生成 Embeddings...")
    try:
        # OpenAI API 支持批量处理，效率更高
        response = client.embeddings.create(
            input=all_chunks,
            model=embedding_model_id
        )
        embeddings_list = [item.embedding for item in response.data]
        logger.info(f"成功生成 {len(embeddings_list)} 条 Embeddings。")

        # 4. 创建DataFrame并保存
        df = pd.DataFrame({
            'text': all_chunks,
            'embeddings': embeddings_list
        })
        df.to_pickle(DB_SAVE_PATH)
        logger.info(f"Embeddings 数据库已成功创建并保存至: {DB_SAVE_PATH}")

    except Exception as e:
        logger.error(f"调用 OpenAI Embeddings API 或保存数据库时发生错误: {e}")
        logger.error("请检查 API Key 是否有效、网络连接是否正常，以及账户是否可用。")


if __name__ == "__main__":
    create_and_save_embeddings()