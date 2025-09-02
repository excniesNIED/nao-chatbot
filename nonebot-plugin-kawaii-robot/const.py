from .config import config

ReplyDictType = dict[str, list[str]]

NICKNAME = next(iter(config.nickname)) if config.nickname else "可爱的咱"

# hello之类的回复
BUILTIN_HELLO_REPLY = [
    "你好喵~",
    "呜喵..？！",
    "你好OvO",
    "喵呜 ~ ，叫小Nao做什么呢☆",
    "怎么啦qwq",
    "呜喵 ~ ，干嘛喵？",
    "呼喵 ~ 叫可爱的咱有什么事嘛OvO",
]

# 戳一戳消息
BUILTIN_POKE_REPLY = [
    "小Nao在呢！有什么事就问小Nao吧！",
    "呜喵？",
    "喵！",
    "请不要戳小Nao了 >_<",
    "喵 ~ ！ 戳我干嘛喵！",
    "戳坏了，你赔！",
    "呜......戳坏了",
    "呜呜......不要乱戳",
    "怎么了喵？",
    "有什么吩咐喵？",
    "呼喵 ~ 叫可爱的咱有什么事嘛OvO",
]

# 不明白的消息
BUILTIN_UNKNOWN_REPLY = [
    "小Nao不懂捏...",
    "没有听懂喵...",
    "小Nao没有理解呢...",
]

# 打断复读
BUILTIN_INTERRUPT_MSG = [
    "打断！",
    "打断复读！",
    "你们这群入机能不能别刷屏了喵",
]
