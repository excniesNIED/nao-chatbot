import configparser
import openai
from pathlib import Path

from nonebot import on_message
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Event, Message

# --- 1. 加载配置 ---
config_path = Path(__file__).parent / "openai_config.ini"
config = configparser.ConfigParser()

# 检查配置文件是否存在
if not config_path.exists():
    raise FileNotFoundError("插件配置文件 'openai_config.ini' 未找到！请根据说明创建。")

try:
    config.read(config_path, encoding='utf-8')
    api_url = config.get('openai', 'api_url')
    api_key = config.get('openai', 'api_key')
    model_id = config.get('openai', 'model_id')
    model_name = config.get('openai', 'model_name')
    system_prompt = config.get('openai', 'system_prompt')

    # 简单验证配置是否为空
    if not all([api_url, api_key, model_id, model_name, system_prompt]):
        raise ValueError("config.ini 文件中的配置项不能为空。")

except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
    logger.error(f"读取 config.ini 失败: {e}")
    # 可以在这里选择停止插件加载或使用默认值
    raise

# --- 2. 初始化 OpenAI 客户端 ---
# 使用从配置文件读取的信息来初始化客户端
client = openai.AsyncOpenAI(
    base_url=api_url,
    api_key=api_key,
)

# --- 3. 创建 NoneBot 事件响应器 ---
# 优先级设置得比较低 (数字越大优先级越低), 确保在其他词库插件之后执行
# 这样可以实现当其他词库插件未匹配时, 再由本插件进行处理
chat_matcher = on_message(rule=to_me(), priority=99, block=True)


async def get_openai_response(prompt: str) -> str:
    """
    异步调用OpenAI兼容API获取回复, 不包含任何记忆功能。
    """
    try:
        # 构建发送给API的消息列表
        # 每次调用都是一个全新的对话
        messages = [
            {"role": "system", "content": system_prompt + f"你的名字是{model_name}。"},
            {"role": "user", "content": prompt}
        ]

        logger.info(f"向API发送请求: Model={model_id}")

        # 发起API请求
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
            # 其他参数如 temperature, top_p 等可以根据需要添加
        )

        # 提取并返回助手的回复
        content = response.choices[0].message.content
        return content.strip() if content else "嗯...我好像不知道该说什么了。"

    except openai.APIConnectionError as e:
        logger.error(f"无法连接到API服务: {e.__cause__}")
        return "哎呀，我和我的大脑断开连接了，请稍后再试吧！"
    except openai.RateLimitError:
        logger.warning("API请求过于频繁，已达到速率限制。")
        return "你说得太快啦，让我先喘口气！"
    except openai.APIStatusError as e:
        logger.error(f"API返回了错误的状态码: {e.status_code}, 响应: {e.response}")
        return "我的大脑好像出了一点小故障，暂时无法回答你了。"
    except Exception as e:
        logger.error(f"发生了未预料的错误: {e}")
        return "呜...出错了，请联系我的主人检查一下后台日志吧。"


@chat_matcher.handle()
async def handle_chat(event: Event, matcher: Matcher):
    """
    处理@机器人的消息，调用大模型进行回复。
    """
    user_message = event.get_plaintext().strip()

    # 如果用户仅@机器人而没有发送任何有效文本，则不作处理
    if not user_message:
        return

    # 调用大模型API获取回复
    response_text = await get_openai_response(user_message)

    # 将回复发送给用户
    await matcher.finish(Message(response_text))