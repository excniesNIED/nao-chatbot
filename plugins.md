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
- 戳一戳、非词库内容修改 `const.py` ，然后替换到 `/root/Lagrange.OneBot/nao/.venv/lib/python3.11/site-packages/nonebot_plugin_kawaii_robot` 下的对应文件。

#### 编写

参考 [Kyomotoi/AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus) 的 json 字典格式，键是关键词字符串，值是回复列表

**注意：词库要符合 json 格式 如果报解码错误（`UnicodeDecodeError`）先检查自己的词库是不是 无 BOM 的 UTF-8 编码格式**

回复里可以写变量，目前用 `UniMessage.template().format()` 格式化；可以往里写 [Alconna 的扩展控制符](https://nonebot.dev/docs/best-practice/alconna/uniseg#使用消息模板)。
如果回复中需要用到 `{` 或 `}`，请用 `{{` 或 `}}` 代替。
插件内建的一些的变量：

- `{user_id}`：发送者 QQ 号
- `{username}`：发送者昵称（获取失败则默认为 `你`）
- `{bot_nickname}`：机器人昵称（没有设置则默认为 `可爱的咱`）
- `{message_id}`: 消息 ID，在戳一戳回复中为 None
- `{segment}`：用于分割消息，该变量前的文本将会单独为一条消息发送
- `{at}`: At 消息发送者，是 `{:At(user, user_id)}` 的简写
- `{reply}`: 回复发送者的消息，是 `{:Reply(message_id)}` 的简写，在戳一戳回复中为 None

### 特殊问题

将`utils.py`、`__main__.py` 替换到 `/root/Lagrange.OneBot/nao/.venv/lib/python3.11/site-packages/nonebot_plugin_kawaii_robot` 下的对应文件。

### 程序崩溃（收不到回复）问题的根源与修复

从你提供的NoneBot日志中，我定位到了一个关键错误：

```
nonebot_plugin_alconna.uniseg.constraint.SerializeFailed: 在没有机器人实例的情况下无法将通用消息转为对应的适配器消息
```

这个错误发生在你发送“@小Nao help”之后，源于插件的**复读姬（repeater）功能**。具体来说，问题出在 `nonebot_plugin_kawaii_robot/__main__.py` 文件的 `repeat_rule` 函数中。

#### 问题分析

这个函数在判断消息是否为复读时，尝试将消息转换为 `UniMessage` 格式，但此时程序无法获取到机器人实例（Bot Instance），导致序列化失败并抛出异常。这个异常中断了后续的程序流程，使得你最终收不到或只收到不完整的回复。

#### 解决方案

你需要修改 `nonebot_plugin_kawaii_robot/__main__.py` 文件来修复这个Bug。

**请打开以下文件:**
`lgc-nb2dev/nonebot-plugin-kawaii-robot/nonebot-plugin-kawaii-robot-4de3a1cf76d24ca34c8a112fa4c519ba6a1a5d80/nonebot_plugin_kawaii_robot/__main__.py`

**找到 `repeat_rule` 函数（大约在第186行）：**

```python
async def repeat_rule(event: BaseEvent, ss: Uninfo) -> bool:
    try:
        raw = event.get_message()
    except ValueError:
        return False
    msg = repr(UniMessage.of(raw)) # <--- 问题行
    return RepeatInfo.get(ss.scene_path).count(event.get_user_id(), msg)
```

**将 `msg = repr(UniMessage.of(raw))` 这一行修改为：**

```python
    msg = str(raw)
```

修改后的函数如下所示：

```python
async def repeat_rule(event: BaseEvent, ss: Uninfo) -> bool:
    try:
        raw = event.get_message()
    except ValueError:
        return False
    msg = str(raw) # <--- 修改这里
    return RepeatInfo.get(ss.scene_path).count(event.get_user_id(), msg)
```

这样修改后，程序将使用更简单的方式获取消息的字符串内容进行复读判断，避免了导致崩溃的序列化错误。

### 问题根源：URL解析冲突

你遇到的新问题是一个非常隐蔽的Bug，它**不在你的词库文件中**（你修改后的JSON文件是完全正确的！），而是在插件处理URL的方式上。

我来为你详细解释一下这次的报错：

```
ValueError: too many values to unpack (expected 2)
```

这个错误发生在插件的依赖库 `nonebot-plugin-alconna` 尝试解析你的图片消息时。

- **问题所在**：你的图片URL中包含了`=`符号（例如：`.../xxx.jpg?sign=...`）。
- **触发过程**：插件的模板功能在解析 `{:Image(url="...")}` 时，会用 `=` 来分割参数名（`url`）和参数值（`"..."`）。但它使用了一个过于简单的分割方法，导致它把你URL里的 `sign=` 也当作了参数分隔符。
- **导致崩溃**：因此，它试图将 `url="...jpg?sign=..."` 分割成 `键` 和 `值` 两部分，但因为有多个 `=`，分割后得到了超过两部分，程序不知道如何处理，于是就崩溃了。

简单来说，这是插件所依赖的一个底层库在处理带参数的URL时存在的一个缺陷。

#### 解决方案：修改插件代码以绕过此Bug

幸运的是，我们可以通过修改 `nonebot-plugin-kawaii-robot` 插件自身的一个文件来“聪明地”绕过这个Bug，而不需要去动更底层的库。

我们需要修改 `utils.py` 文件，让它在把消息交给底层库之前，手动将图片URL单独处理好。

我将为你提供完整的、已修改好的 `utils.py` 文件。你只需要用下面的内容**完整替换**掉你原来的 `nonebot_plugin_kawaii_robot/utils.py` 文件即可。

## [nonebot_plugin_group_welcome](https://github.com/excniesNIED/nonebot_plugin_group_welcome)

### 使用方法

将 `welcome.py` 放置在 NoneBot 项目的 `src/plugins` 目录下。修改第8行白名单、第23行的图片显示和第34行的欢迎语即可。

### 注意事项

-  本插件依赖于 `GroupIncreaseNoticeEvent` (群成员增加事件)，请确保你的 OneBot 实现可以正确上报该事件。
- 图片路径必须是 **绝对路径**，并且Lagrange.OneBot容器或进程需要有该路径的 **读权限**。如果使用 Docker 部署，请确保路径映射正确。

<img src="https://gastigado.cnies.org/d/project_nonebot_plugin_group_welcome/PixPin_2025_08_31_19_45_52.png?sign=kjsczdNeTe5BdbOm1tU-rX5Ls5XefHSDgqOjLsvKnvE=:0" alt="效果图预览" style="zoom: 33%;" />

## [nonebot_plugin_ban_word_detector](https://github.com/excniesNIED/nonebot_plugin_ban_word_detector)

### ✨ 功能

- **多词库支持**: 可通过配置文件同时加载多个本地词库文件。
- **分级惩罚机制**:
  - **第一次**检测到违规消息：撤回该消息并发送警告。
  - **第二次**检测到同一用户的违规消息：撤回消息并禁言该用户30分钟。
  - **第三次**检测到同一用户的违规消息：将该用户踢出群聊。
  - 踢出群聊后，检测次数重置。
- **持久化记录**: 用户违规次数会被记录在本地，即使机器人重启也不会丢失。
- **管理员豁免**: 自动忽略群主和管理员的消息，防止误判。
- **详细日志**: 所有检测和处理操作都会以Unix日志风格记录到本地文件 `noadpls.txt` 中，方便追溯。
- `recomendgroupban.py` 可以检测推荐群聊、推荐联系人卡片

### 🔧 配置

在使用前，请在您的 NoneBot 项目根目录下创建 `config.json` 文件，并根据您的实际情况进行配置。

**1. `config.json` 文件**

```json
{
    "monitored_groups": [
        123456789,
        987654321
    ],
    "word_files": [
        "D:\\path\\to\\your\\wordlist1.txt",
        "C:\\Users\\bot\\Desktop\\wordlist2.txt"
    ]
}
```

- `monitored_groups`: (必需) 一个包含群号的列表，插件将只在这些群聊中生效。
- `word_files`: (必需) 一个包含词库文件绝对路径的列表。

**2. 词库文件 (`.txt`)**

请根据 `config.json` 中填写的路径创建对应的 `.txt` 文件。每个违禁词占一行，例如：

```
违禁词1
违禁词2
广告内容
...
```

**3. 用户违规记录 (自动生成)**

插件会自动创建 `user_violations.json` 文件来存储用户的违规计数，您通常无需手动修改它。

### 安装

将 `textban.py` 放置在 NoneBot 项目的 `src/plugins` 目录下。修改第23行的图片显示和第34行的欢迎语即可。

违禁词库可以使用本人根据 [cleanse-speech](https://github.com/TelechaBot/cleanse-speech) 转换的词库 [清谈词库](https://github.com/excniesNIED/nao-chatbot/tree/main/nonebot-plugin-kawaii-robot/outer)：

- `advertisement`：默认中文广告词库
- `pornographic`：默认中文色情词库
- `politics`: 默认中文敏感词库
- `general`: 默认中文通用词库
- `netease`: 网易屏蔽词库

针对校园新生群、班级群等校园场景，可以使用本人整理的基于校园迎新群真实广告样本整理的广告检测词库 [campus-ad-detection-words](https://github.com/excniesNIED/campus-ad-detection-words)。

### 📖 使用

插件没有任何主动触发的命令。一旦配置完成并启动机器人，它将自动监控指定群聊中的消息。

当有用户（非管理员）发送的消息包含任意一个词库中的违禁词时，插件将根据其历史违规次数自动执行相应的惩罚操作。

### 📝 日志格式

所有操作都将被记录在 NoneBot 根目录下的 `noadpls.txt` 文件中。格式如下：

`[时间] [群号] [用户名] [消息内容] [处理结果]`

**示例:**

```log
[2025-09-01 10:12:20] [123456789] [张三] [这是一条广告消息] [撤回消息]
[2025-09-01 10:15:30] [123456789] [张三] [这是第二条广告] [撤回消息并禁言30分钟]
[2025-09-01 10:20:05] [987654321] [李四] [这是违规内容] [撤回消息]
```

<img src="https://gastigado.cnies.org/d/project_nonebot_plugin_group_welcome/PixPin_2025_09_01_18_15_05.png?sign=85TMwzimoUlY7A10RaTTQUYIf4uky-SJmFypuO-_oS8=:0" alt="效果图预览" style="zoom:50%;" />

## nonebot-plugin-openai

接入兼容 OpenAI 的 LLM，分为独立版和集成 [nonebot-plugin-kawaii-robot](https://github.com/lgc-NB2Dev/nonebot-plugin-kawaii-robot) 版本。

LLM 相关配置详见 `config.ini`。使用前需要指定URL、API Key、Model ID、System Prompt和群聊白名单等。

独立版直接放在 `src/plugins` 即可。

集成版需要将相关文件放在 `/root/Lagrange.OneBot/nao/.venv/lib/python3.11/site-packages/nonebot_plugin_kawaii_robot`。LLM 调用优先级低于词库回答。

Gemini 版本可以使用免费的API。安装Gemini API调用库：

```bash
pip install google-generativeai
```

| 特性                              | Gemini 2.5 Flash                                        | Gemini 2.5 Flash-Lite                                 | 关键差异分析                                                 |
| --------------------------------- | ------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| **核心描述**                      | 价格与性能的最佳平衡                                    | 极致的成本效益和低延迟                                | Flash 是“全能选手”，Flash-Lite 是“速度与成本专家”。          |
| **输入/输出 Token 限制**          | 输入: 1,048,576<br>输出: 65,536                         | 输入: 1,048,576<br>输出: 65,536                       | **没有区别**。两者都保持了巨大的100万Token上下文窗口，这点非常出色。 |
| **支持的能力**                    | 支持思考 (Thinking)、代码执行、函数调用、上下文缓存等   | 支持思考 (Thinking)、代码执行、函数调用、上下文缓存等 | **能力上几乎完全相同**。Flash-Lite 并没有因为更轻量而牺牲核心功能。 |
| **免费套餐速率限制 (Free Tier)**  | **RPM: 10** (每分钟请求数)<br>**RPD: 250** (每天请求数) | **RPM: 15**<br>**RPD: 1,000**                         | **Flash-Lite 的免费额度更慷慨**。它允许更高的请求频率和多达4倍的每日请求量，明确鼓励大规模调用。 |
| **价格 (付费套餐, 每100万Token)** | 输入: **$0.30**<br>输出: **$2.50**                      | 输入: **$0.10**<br>输出: **$0.40**                    | **这是最核心的区别**。Flash-Lite 的成本极低，输入价格仅为 Flash 的 1/3，输出价格更是不到 Flash 的 1/6。 |
| **上下文缓存价格**                | 每100万Token **$0.075**                                 | 每100万Token **$0.025**                               | Flash-Lite 的缓存价格同样只有 Flash 的 1/3，进一步降低了连续对话或分析的成本。 |
| **知识截止日期**                  | 2025年1月                                               | 2025年1月                                             | **没有区别**。                                               |

为 Gemini API 设置代理或自定义接入点的标准方法**不是**在代码中传入 URL，而是通过设置系统**环境变量**来实现的。Python 库会自动识别并使用这些环境变量。

**如何使用自定义 URL (代理)**

如果您需要通过代理访问 Gemini API，请在**启动 NoneBot 之前**，在您的终端中设置环境变量。

**在 Linux / macOS 系统中:**

```
export HTTPS_PROXY="http://your-proxy-address:port"
# 然后在同一个终端窗口中启动你的 NoneBot
nb run
```

**在 Windows (CMD) 中:**

```
set HTTPS_PROXY=http://your-proxy-address:port
# 然后在同一个 CMD 窗口中启动你的 NoneBot
nb run
```

**在 Windows (PowerShell) 中:**

```
$env:HTTPS_PROXY="http://your-proxy-address:port"
# 然后在同一个 PowerShell 窗口中启动你的 NoneBot
nb run
```

这样修改后，代码本身不再处理 URL，而是交由 Python 和 `google-generativeai` 库通过标准方式自动处理，既修复了报错，也让配置更加规范。





https://github.com/LagrangeDev/Lagrange.Core

https://github.com/LagrangeDev/Lagrange.Core/issues/715

https://github.com/LagrangeDev/Lagrange.Core/issues/891

https://github.com/sealdice/sealdice-core/issues/1168#issuecomment-2566279137

https://github.com/sealdice/sealdice-core/pull/1388

https://lagrangedev.github.io/Lagrange.Doc/v1/Lagrange.OneBot/Config/

https://lagrangedev.github.io/lagrange-config-generator/
