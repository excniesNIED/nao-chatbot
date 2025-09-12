# create_embeddings_db.py
import google.generativeai as genai
import pandas as pd
import pypdf2
import markdown
import re
from pathlib import Path
import configparser
from nonebot.log import logger

# --- 配置 ---

# ↓↓↓ 在这个列表中指定你要向量化的知识库文件名 ↓↓↓
DOCUMENTS_TO_PROCESS = [
    "q&a.md",
    "reference.pdf"
    # 如果有更多文件，继续在这里添加，例如: "another_doc.md"
]

CONFIG_PATH = Path(__file__).parent / "gemini_config.ini"
DOCS_PATH = Path(__file__).parent
DB_SAVE_PATH = Path(__file__).parent / "embeddings_database.pkl"
MODEL_ID = "embedding-001"


# --- 文本处理函数 ---
def read_pdf(file_path: Path) -> str:
    """读取PDF文件内容"""
    try:
        with open(file_path, 'rb') as f:
            reader = pypdf2.PdfReader(f)
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
            # 移除HTML标签以获取纯文本
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
    # 1. 加载API Key
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH, encoding='utf-8')
        gemini_api_key = config.get('gemini', 'gemini_api_key')
        if not gemini_api_key or gemini_api_key == "YOUR_GEMINI_API_KEY":
            logger.error("请在 gemini_config.ini 中配置你的 gemini_api_key。")
            return
        genai.configure(api_key=gemini_api_key)
        logger.info("Gemini API Key 配置成功。")
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return

    # 2. 读取所有指定文档并分块
    all_chunks = []
    doc_files_to_process = [DOCS_PATH / f for f in DOCUMENTS_TO_PROCESS]

    if not doc_files_to_process:
        logger.warning("文件处理列表 'DOCUMENTS_TO_PROCESS' 为空，未创建任何 Embeddings。")
        return

    for doc_file in doc_files_to_process:
        if not doc_file.exists():
            logger.warning(f"在配置中指定的文件 '{doc_file.name}' 未找到，已跳过。")
            continue

        content = ""
        if doc_file.suffix == '.pdf':
            content = read_pdf(doc_file)
        elif doc_file.suffix == '.md':
            content = read_md(doc_file)
        # 你可以根据需要添加对其他文件类型（如 .txt）的支持
        # elif doc_file.suffix == '.txt':
        #     content = read_txt(doc_file)

        if content:
            chunks = split_text_into_chunks(content)
            all_chunks.extend(chunks)
            logger.info(f"文件 '{doc_file.name}' 已被分割成 {len(chunks)} 个文本块。")

    if not all_chunks:
        logger.error("未能从指定文档中提取任何文本内容，Embeddings 数据库创建失败。")
        return

    # 3. 为每个块生成Embeddings
    logger.info(f"开始为 {len(all_chunks)} 个文本块生成 Embeddings，这可能需要一些时间...")
    try:
        result = genai.embed_content(
            model=MODEL_ID,
            content=all_chunks,
            task_type="retrieval_document"
        )
        embeddings = result['embedding']
        logger.success(f"成功生成 {len(embeddings)} 条 Embeddings。")

        # 4. 创建DataFrame并保存
        df = pd.DataFrame({
            'text': all_chunks,
            'embeddings': list(embeddings)
        })
        df.to_pickle(DB_SAVE_PATH)
        logger.success(f"Embeddings 数据库已成功创建并保存至: {DB_SAVE_PATH}")

    except Exception as e:
        logger.error(f"生成 Embeddings 或保存数据库时发生错误: {e}")

if __name__ == "__main__":
    # 直接运行此脚本
    create_and_save_embeddings()