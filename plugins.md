# 插件列表和使用方法

**安装插件前，务必激活虚拟环境！**

```bash
source myenv/bin/activate
```

## [nonebot-plugin-kawaii-robot](https://github.com/lgc-NB2Dev/nonebot-plugin-kawaii-robot)

### 安装

```bash
nb plugin install nonebot_plugin_kawaii_robot
```

### 配置

在 NoneBot2 项目的 `.env` 文件中按需添加下面的配置项

```
# 机器人昵称
NICKNAME=[]

# 词库回复权限，`ALL` 就是全部聊天都会触发回复，`GROUP` 就是仅群聊
LEAF_PERMISSION=ALL

# 忽略词，指令以本列表中的元素开头不会触发回复
# 例：[".", "#", "你好"]
LEAF_IGNORE=[]

# 回复模式，`-1` 关闭全部 at 回复，`0` 仅启用词库回复，`1` 开启所有回复
LEAF_REPLY_TYPE=1

# 戳一戳回复文字概率，范围 `0` ~ `100`，`-1` 关闭戳一戳回复，`0` 代表始终戳回去
LEAF_POKE_RAND=20

# 复读、打断复读时是否按复读的用户数计算次数
LEAF_FORCE_DIFFERENT_USER=True

# 触发复读或打断次数，群内复读 `{0}` ~ `{1}` 次数后触发复读或打断
LEAF_REPEATER_LIMIT=[2, 6]

# 复读后，群友继续复读达到指定次数时是否继续参与复读或打断
LEAF_REPEAT_CONTINUE=False

# 打断概率，范围 `0` ~ `100`，`0` 关闭打断
LEAF_INTERRUPT=20

# 打断复读后，群友继续复读达到指定次数时是否继续参与复读或打断
LEAF_INTERRUPT_CONTINUE=True

# 词库回复匹配模式，
# `0` 是整句话精确匹配关键词（不推荐）；
# `1` 是按从长到短的顺序遍历词库中的关键词，遇到匹配的就停止遍历并选取对应回复；
# `2` 与 `1` 的遍历方式相同，但是会遍历所有词库中的关键词，然后从匹配到的所有项目中随机选取一个回复
LEAF_MATCH_PATTERN=1

# 当 `LEAF_MATCH_PATTERN` >= 1 时，消息长度大于此数值则不从词库中匹配回复，设为 `0` 则禁用此功能
LEAF_SEARCH_MAX=20

# 词库回复是否需要 @机器人 或包含机器人昵称
LEAF_NEED_AT=True

# 当 `LEAF_NEED_AT` 为 `False` 时，非 @机器人 时的词库回复触发概率，范围 `0` ~ `100`
LEAF_TRIGGER_PERCENT=5

# 戳一戳回复延时，单位秒
LEAF_POKE_ACTION_DELAY=[0.5, 1.5]

# 当回复存在多条消息时，发送消息的间隔时间，单位秒
LEAF_MULTI_REPLY_DELAY=[1.0, 3.0]

# 是否载入内置回复词库
# 内置了 Kyomotoi/AnimeThesaurus 词库（data.json），还有咱自制的 bot 的词库（leaf.json）
LEAF_LOAD_BUILTIN_DICT=True

# 是否载入内置特殊回复词库
LEAF_LOAD_BUILTIN_SPECIAL=True

# 是否注册 重载词库 指令
LEAF_REGISTER_RELOAD_COMMAND=True
```

### 词库位置

在 Linux 系统中，`nonebot-plugin-kawaii-robot` 插件的词库位置分为两种：**自定义附加词库（包括特殊词库）** 和 **内置词库**，具体路径如下：


#### 1. 自定义附加词库（包括特殊词库）

自定义词库（如用户自己添加的 json 词库）和特殊词库（`_hello.json`、`_poke.json` 等）存储在插件的配置目录中，该目录由 `nonebot-plugin-localstore` 管理，遵循 Linux 系统的 XDG 规范，默认路径为：  

```bash
~/.config/nonebot2/plugins/nonebot-plugin-kawaii-robot/
```

- 该目录下的 `*.json` 文件（除文件名以 `_` 开头的特殊词库外）会被加载为普通附加词库。
- 特殊词库（`_hello.json`、`_poke.json`、`_unknown.json`、`_interrupt.json`）也存储在此目录，用于特定场景的回复。


#### 2. 内置词库

插件自带的内置词库（如 `leaf.json`、`data.json`）存储在插件安装目录的 `resource` 文件夹中。

具体路径取决于你的 Python 环境和插件安装位置，通常为：  

```bash
# 假设插件安装在 Python 环境的 site-packages 目录下
{你的 Python 环境路径}/site-packages/nonebot_plugin_kawaii_robot/resource/
```

- 例如，若使用虚拟环境，路径可能类似：`~/venv/lib/python3.x/site-packages/nonebot_plugin_kawaii_robot/resource/`。
- 内置词库是否加载由配置项 `LEAF_LOAD_BUILTIN_DICT` 控制（默认启用）。


#### 说明

- 日志中提到的 `_hello.json`、`_poke.json` 等特殊词库，以及用户添加的自定义词库，均位于上述 **自定义附加词库目录**。
- 内置词库 `leaf.json`、`data.json` 位于插件安装目录的 `resource` 文件夹，属于插件自带文件。