# 基于Lagrange.OneBot协议搭建NoneBot的聊天QQ机器人

Lagrange.Core 是基于 NTQQ 协议的纯 C# 实现，可为 QQ 账号提供协议层支持；NoneBot 则是一款跨平台的 Python 异步聊天机器人框架，具备高扩展性和易用性。本文将详细介绍如何在 Debian 12 系统上部署一套基于 Lagrange.OneBot 协议的 NoneBot QQ 机器人。

## 前置准备

在开始前，请确保你的 Debian 12 服务器满足以下条件：

1. 已安装基础工具：`tar`、`vim`、`python3`（3.9 及以上版本）、`curl`（可选，用于下载文件）；
2. 服务器具备网络连接（需访问 GitHub 下载资源）；
3. 拥有一个可正常登录的 QQ 账号（建议使用非主号，避免风控风险）。

## 第一步：部署 Lagrange.OneBot（协议层）

### 下载运行Lagrange.OneBot

Lagrange.OneBot 负责与 QQ 服务器通信，为 NoneBot 提供消息收发能力，需先完成部署与配置。

访问 [Lagrange.Core 的 GitHub 发行页](https://github.com/LagrangeDev/Lagrange.Core/releases)，下载符合我们需求的`Lagrange.OneBot_linux-x64_net9.0_SelfContained.tar.gz`。

上传到服务器，使用下面命令解压：

```bash
tar -xvzf ./Lagrange.OneBot_linux-x64_net9.0_SelfContained.tar.gz
```

将可执行文件移动到 Lagrange.OneBot 目录：

```bash
cd Lagrange.OneBot
mv ./bin/Release/net9.0/linux-x64/publish/Lagrange.OneBot ./Lagrange.OneBot
```

为可执行文件添加执行权限：

```bash
chmod +x ./Lagrange.OneBot
```

执行以下命令启动程序，首次运行需扫码登录 QQ：

```bash
./Lagrange.OneBot
```

启动成功后，终端会显示二维码链接或图片路径，使用手机 QQ 扫描二维码完成登录。登录成功后，终端会输出 “登录成功” 等提示信息。**此时可先按`Ctrl+C`停止程序，后续配置为系统服务自动运行。**

### 为 Lagrange 配置 systemd 服务

为避免手动启动的繁琐，将 Lagrange.OneBot 配置为 systemd 服务，实现开机自启和崩溃自动重启。

创建服务配置文件：

```bash
vim /lib/systemd/system/lagrange.service
```

写入以下内容（根据实际路径调整，写入前请删除注释）：

```bash
[Unit]
Description=Lagrange.OneBot Service
After=network.target  # 网络启动后再运行

[Service]
Type=simple
User=root  # 运行用户（根据需求修改，如非root需确保权限）
WorkingDirectory=/root/Lagrange.OneBot  # 程序所在目录
ExecStart=/root/Lagrange.OneBot/Lagrange.OneBot  # 程序完整路径
Restart=always  # 程序崩溃时自动重启
RestartSec=5  # 重启间隔（秒）

[Install]
WantedBy=multi-user.target  # 多用户模式下启动
```

保存并退出后，执行以下命令启动并设置开机自启：

```bash
systemctl daemon-reload   # 重新加载 systemd 配置
systemctl enable lagrange # 设置开机自启
systemctl start lagrange  # 启动服务
systemctl status lagrange # 查看服务状态
```

验证服务状态，若显示 “active (running)”，则 Lagrange 服务配置成功。

## 第二步：安装 NoneBot 脚手架（框架层）

### 安装 pipx

`pipx`可在独立环境中安装 Python 命令行工具，两种安装方式任选其一：

#### 方式 1：通过 pip 安装（用户级，推荐，建议使用虚拟环境执行）

```bash
# 确保pip已更新
python3 -m pip install --upgrade pip
# 安装pipx
python3 -m pip install --user pipx
# 配置环境变量（使pipx命令生效）
python3 -m pipx ensurepath
```

**注意**：若输出 “请重启终端” 提示，需关闭当前终端并重新打开。

#### 方式 2：通过 apt 安装（系统级，适合权限充足场景）

```bash
sudo apt update && sudo apt install -y pipx
pipx ensurepath  # 配置环境变量（需重启终端）
```

### 安装 NoneBot 脚手架

```bash
pipx install nb-cli
```

验证安装：

```bash
nb --version
```

若输出版本号，则脚手架安装成功。

## 第三步：创建 NoneBot 项目并连接 Lagrange

### 初始化 NoneBot 项目

执行以下命令启动项目创建向导：

```
nb create
```

按以下步骤完成配置（推荐选项已标注）：

**选择项目模板**：推荐`simple`（简洁模板，适合新手）

![image-20250830215110495](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215110495.png?sign=UDdNg7vf5kUQ3ddtLgNIGYICcBi40RsBRcCOsCvQ5i8=:0)

**输入项目名称**：例如`chatbot`（自定义，小写无空格）

![image-20250830215150320](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215150320.png?sign=AonzoQu93N83sZuDH6l2fPw9V-1VT5CfEifEzgl8uu8=:0)

**选择适配器**：按 <kbd>空格</kbd> 选中`OneBot V11`（必须选，用于连接 Lagrange），然后按 <kbd>Enter</kbd> 下一步

![image-20250830215232794](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215232794.png?sign=n1D0zCMMnggWLWzC-uTfdfcdaXR1KjIjHOk-YVue1iM=:0)

**选择驱动器**：默认`FastAPI`（NoneBot 推荐，性能稳定）

![image-20250830215401640](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215401640.png?sign=hYns5jG6ZD4GglRfxDbQENwySBR-CxFhU6cCM9z410s=:0)

**插件存储位置**：推荐`src`（规范目录结构，便于管理插件）

![image-20250830215525614](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215525614.png?sign=CwR34TOLrfQ0mjTqtLY5x-1CuSJCRH-5WWPexu3mMl8=:0)

**安装依赖**：输入`y`（自动安装项目所需依赖）

![image-20250830215614661](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215614661.png?sign=ViGgVDj2XOd3PcNCAXH4yZoY275O9rx1ixeJ8ojuJgk=:0)

**创建虚拟环境**：

- 若已在独立虚拟环境中操作，输入`n`；
- 若直接在系统环境操作，输入`y`（避免依赖冲突）。

![image-20250830215642893](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215642893.png?sign=LDkj16YJs_8KWrbpChTsdughPsZORyP0TSOZXpjfIlA=:0)

**安装内置插件**：推荐全选便于测试机器人基础功能

![image-20250830215802429](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215802429.png?sign=fHo3ZRZsZmtYy8LMicCJ0W69L0n3apnbp6VnW5dtvEk=:0)

安装成功会出现下面提示：

![image-20250830215859407](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830215859407.png?sign=knoVTfN7CnRS38v1pyRGMFxk1NWUSbMOunL2ES5aO4I=:0)

### 启动 NoneBot 并验证连接

根据提示运行下面命令：

```bash
cd chatbot # 替换为你的项目名称
nb run --reload # 带热重载，修改代码后自动重启
```

出现类似下面命令且没有报错，证明 NoneBot 已经和 Lagrange 握手链

```bash
08-30 01:57:36 [SUCCESS] nonebot | NoneBot is initializing...
08-30 01:57:36 [INFO] nonebot | Current Env: dev
08-30 01:57:36 [DEBUG] nonebot | Loaded Config: {'driver': '~fastapi', 'host': IPv4Address('127.0.0.1'), 'port': 8080, 'log_level': 'DEBUG', 'api_timeout': 30.0, 'superusers': set(), 'nickname': set(), 'command_start': {'/'}, 'command_sep': {'.'}, 'session_expire_timeout': datetime.timedelta(seconds=120), 'environment': 'dev'}
08-30 01:57:36 [DEBUG] nonebot | Succeeded to load adapter "OneBot V11"
08-30 01:57:36 [SUCCESS] nonebot | Running NoneBot...
08-30 01:57:36 [SUCCESS] nonebot | Loaded adapters: OneBot V11
08-30 01:57:36 [INFO] uvicorn | Started server process [548469]
08-30 01:57:36 [INFO] uvicorn | Waiting for application startup.
08-30 01:57:36 [INFO] uvicorn | Application startup complete.
08-30 01:57:36 [INFO] uvicorn | Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
08-30 01:57:40 [INFO] uvicorn | 127.0.0.1:41046 - "WebSocket /onebot/v11/ws" [accepted]
08-30 01:57:40 [INFO] nonebot | OneBot V11 | Bot 2934575117 connected
08-30 01:57:40 [INFO] websockets | connection open
```

## 第四步：配置 NoneBot 后台运行

默认`nb run`在终端关闭后会停止，需配置后台运行方式。以下提供两种常用方案：

### 方案 1：nohup（简单临时方案）

适合短期测试，不支持开机自启，但配置简单：

```bash
# 后台运行并将日志输出到nonebot.log
nohup nb run > /root/nonebot.log 2>&1 &
```

- 查看实时日志：`tail -f /root/nonebot.log`
- 停止进程：先通过`ps aux | grep nb`找到 PID，再执行`kill <PID>`

### 方案 2：systemd（推荐，支持开机自启）

与 Lagrange 配置类似，创建 NoneBot 服务文件：

1. 创建服务文件：

   ```bash
   vim /lib/systemd/system/chatbot.service
   ```

2. 粘贴以下内容（替换项目路径）：

   ```ini
   [Unit]
   Description=NoneBot Service (QQ Robot Framework)
   After=network.target lagrange.service  # 确保Lagrange启动后再启动NoneBot
   
   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/chatbot  # 替换为你的项目目录
   ExecStart=/root/.local/bin/nb run  # 替换为nb命令的绝对路径（可通过which nb查看）
   Restart=always
   RestartSec=5
   StandardOutput=append:/var/log/nonebot.log
   
   [Install]
   WantedBy=multi-user.target
   ```

3. 启动并启用服务：

   ```bash
   systemctl daemon-reload
   systemctl start chatbot
   systemctl enable chatbot
   ```

## 第五步：测试机器人功能测试

如果想要测试机器人是否启动运行，可以在 `src/plugins` 目录下新建 `test.py` 文件写入以下内容：

```python
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message

Test = on_regex(pattern=r'^测试$',priority=1)


@Test.handle()
async def Test_send(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = "测试成功"
    await Test.finish(message=Message(msg))
```

在群聊发送“测试”，如果看到机器人回复，则机器人正常运行：

![image-20250830221108484](https://gastigado.cnies.org/d/halo20250830_lagrange_onebot_nonebot/image_20250830221108484.png?sign=vhHsZ0gH9C2G-INOmGktyy6FpvAGa4UTjAqs44J6cmQ=:0)

此时恭喜你成功搭建了一个QQ聊天机器人。

## 第六步：修改通信端口（可选）

Lagrange默认使用`8080`端口，若该端口被占用（如其他服务使用），需同步修改Lagrange和NoneBot的端口配置。

### 1. 停止相关服务
```bash
systemctl stop lagrange chatbot
```

### 2. 修改Lagrange端口
1. 进入Lagrange目录，编辑配置文件：
   ```bash
   cd /root/Lagrange.OneBot
   vim appsettings.json
   ```
2. 找到`Implementations`下的`Port`字段，修改为空闲端口（如`1145`）：
   ```json
   "Implementations": [
       {
           "Type": "ReverseWebSocket",
           "Host": "127.0.0.1",
           "Port": 1145,  // 修改为空闲端口
           "Suffix": "/onebot/v11/ws",
           "ReconnectInterval": 5000,
           "HeartBeatInterval": 5000,
           "AccessToken": ""
       }
   ]
   ```

### 3. 修改NoneBot端口
1. 进入NoneBot项目目录，编辑`.env`文件：
   ```bash
   cd /root/chatbot
   vim .env
   ```
2. 添加或修改`PORT`字段，与Lagrange端口保持一致：
   ```env
   PORT=1145  # 必须与Lagrange的Port一致
   ```

### 4. 重启服务验证
```bash
systemctl start lagrange nonebot
# 验证端口是否被占用
netstat -tuln | grep 1145
```
若显示 `127.0.0.1:1145` 处于监听状态，则端口修改成功。


## 总结
通过以上步骤，你已成功在Debian 12上搭建了基于Lagrange.OneBot和NoneBot的QQ机器人。接下来可通过开发自定义插件扩展功能（如自动回复、天气查询、群管理等），具体可参考 [NoneBot 官方文档](https://nonebot.dev/docs/) 和 [Lagrange.Doc](https://lagrangedev.github.io/Lagrange.Doc/v2/)。也可以查看 [Awesome NoneBot | NoneBot 相关资源汇总](https://awesome.nonebot.dev)。

注意， QQ 账号可能触发风控，建议避免频繁发送广告或敏感内容。风控相关内容请查看 [NoneBot 社区文档](https://x.none.bot/before/QA#_5-%E5%85%B3%E4%BA%8E%E9%A3%8E%E6%8E%A7) 的相关部分。

