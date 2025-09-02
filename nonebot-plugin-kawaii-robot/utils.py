import asyncio
import random
import re
from collections.abc import Iterable
from typing import TypedDict

from nonebot.matcher import current_bot, current_event, current_matcher
from nonebot_plugin_alconna.uniseg import At, Image, Reply, UniMessage, get_message_id
from nonebot_plugin_uninfo import Member, Session, User

from .config import config
from .const import NICKNAME, ReplyDictType

SEG_SAMPLE = "{segment}"
SEG_REGEX = re.compile(r"(?P<h>[^\{])" + re.escape(SEG_SAMPLE) + r"(?P<t>[^\}])")
# 正则表达式，用于手动匹配和提取图片标签及其URL
IMAGE_TAG_REGEX = re.compile(r'\{:Image\(url=\"([^\"]+)\"\)\}')

DEFAULT_USER_CALLING = "你"


def split_seg(text: str) -> list[str]:
    text = text.removeprefix(SEG_SAMPLE)
    text = text.removesuffix(SEG_SAMPLE)

    results = list(re.finditer(SEG_REGEX, text))
    if not results:
        return [text]

    parts = []
    last_index = 0
    for match in results:
        h = match.group("h")
        t = match.group("t")
        now_index = match.start() + (len(h) if h else 0)
        if now_index > last_index:
            parts.append(text[last_index:now_index])
        last_index = match.end() - (len(t) if t else 0)

    if last_index < len(text):
        parts.append(text[last_index:])

    return parts


def flatten_list(li: Iterable[Iterable[str]]) -> list[str]:
    """
    展平二维列表
    """
    return [x for y in li for x in y]


def full_to_half(text: str) -> str:
    """
    全角转半角
    """
    return "".join(
        chr(ord(char) - 0xFEE0) if "\uff01" <= char <= "\uff5e" else char
        for char in text
    )


def search_reply_dict(reply_dict: ReplyDictType, text: str) -> list[str] | None:
    """
    在词库中搜索回复
    """
    text = full_to_half(text.lower())

    if config.leaf_match_pattern == 0:
        return reply_dict.get(text)

    if config.leaf_search_max > 0 and len(text) > config.leaf_search_max:
        return None

    generator = (reply_dict[key] for key in reply_dict if key in text)
    if config.leaf_match_pattern == 1:
        return next(generator, None)

    return flatten_list(list(generator)) or None


def format_sender_username(username: str | None) -> str:
    """
    格式化发送者的昵称，如果昵称过长则截断
    """
    username = username or "你"
    if len(username) > 10:
        username = username[:2] + random.choice(["酱", "亲", "ちゃん", "同志", "老师"])
    return username


def get_username(info: User | Member) -> str:
    if isinstance(info, Member):
        if info.nick:
            return format_sender_username(info.nick)
        info = info.user
    return format_sender_username(info.nick or info.name or "你")


class BuiltInVarDict(TypedDict):
    user_id: str
    username: str
    message_id: str | None
    bot_nickname: str
    at: At
    reply: Reply | None


def format_vars(
    string: str,
    builtin: BuiltInVarDict,
    **extra,
) -> list[UniMessage]:
    """
    【已修改】
    重写此函数以手动处理Image标签，绕过alconna模板解析器的bug。
    """
    final_messages = []
    for seg in split_seg(string):
        # 使用正则表达式分割字符串，将文本和图片URL分开
        # 例如: "文本1{:Image(url="URL")}文本2" -> ['文本1', 'URL', '文本2']
        parts = IMAGE_TAG_REGEX.split(seg)

        if len(parts) == 1:  # 没有找到图片，按原方式处理
            final_messages.append(UniMessage.template(seg).format(**builtin, **extra))
            continue

        # 找到了图片，手动构建UniMessage
        current_message = UniMessage()
        for i, part in enumerate(parts):
            if i % 2 == 0:  # 偶数索引是文本部分
                if part:
                    # 文本部分仍然使用模板格式化，以支持 {username} 等变量
                    current_message.extend(
                        UniMessage.template(part).format(**builtin, **extra)
                    )
            else:  # 奇数索引是正则表达式捕获到的URL部分
                current_message.append(Image(url=part))

        if current_message:
            final_messages.append(current_message)

    return final_messages


async def get_builtin_vars_from_ev(ss: Session) -> BuiltInVarDict:
    bot = current_bot.get()
    event = current_event.get()
    user_id = event.get_user_id()
    try:
        message_id = get_message_id(event=event, bot=bot)
    except Exception:
        message_id = None
    return {
        "user_id": user_id,
        "username": get_username(ss.member or ss.user),
        "message_id": message_id,
        "bot_nickname": NICKNAME,
        "at": At("user", user_id),
        "reply": Reply(message_id) if message_id else None,
    }


async def choice_reply_from_ev(
    ss: Session,
    reply_list: list[str],
    **kwargs,
) -> list[UniMessage]:
    """
    从提供的回复列表中随机选择一条回复并格式化
    """
    raw_reply = random.choice(reply_list)
    return format_vars(raw_reply, await get_builtin_vars_from_ev(ss), **kwargs)


def check_percentage(need_percent: float, percentage: float | None = None) -> bool:
    """
    检查概率
    """
    if need_percent <= 0:
        return False
    if need_percent >= 100:
        return True

    if not percentage:
        percentage = random.random() * 100
    return percentage <= need_percent


async def finish_multi_msg(msg_list: list[UniMessage]):
    first_msg = msg_list.pop(0)
    await first_msg.send()

    for msg in msg_list:
        await asyncio.sleep(random.uniform(*config.leaf_multi_reply_delay))
        await msg.send()

    await current_matcher.get().finish()
