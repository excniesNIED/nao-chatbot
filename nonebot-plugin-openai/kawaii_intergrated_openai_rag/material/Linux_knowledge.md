# 第一节

## 入门

- Linux介绍

- 不同系统之间对比

- 不同发行版介绍

- Linux基本架构和特点

## 安装

- 裸金属和虚拟机
  
  - 发行版选择
  
  - 制作引导盘
  
  - 分区
  
  - 软件源配置
  
  - 必要软件包的安装

## 终端

- 使用终端
  
  - 打开方法
  
  - 补全
  
  - 历史命令
  
  - 常用快捷键

- sudo

- su 切换用户

## 文件操作基础命令

- #### **目录结构与路径**

  - **目录结构**: Linux采用树形目录结构，根目录为`/`，所有文件和目录都从根目录开始。
  - **相对路径与绝对路径**:
    - **相对路径**: 相对于当前工作目录的路径，如`./file`（当前目录下的文件）。
    - **绝对路径**: 从根目录开始的完整路径，如`/home/user/file`。

  #### 文件权限管理
- **chmod**: 修改文件或目录的权限。

  - 示例: `chmod 755 filename`（设置权限为rwxr-xr-x）
  - 示例: `chmod u+x filename`（为所有者添加执行权限）
  - 权限表示:
    - `r`: 读（4）
    - `w`: 写（2）
    - `x`: 执行（1）
    - 所有者、组、其他用户的权限分别用3个数字表示，如`755`。

  #### 目录操作

- **mkdir (make directory)**: 创建新目录。

  - 示例: `mkdir dirname`
  - 常用选项:
    - `-p`: 递归创建目录（如果父目录不存在则一并创建）。
      - 示例: `mkdir -p parent/child`

- **ls (list)**: 列出目录内容。

  - 示例: `ls`
  - 常用选项:
    - `-l`: 显示详细信息（权限、所有者、大小等）。
      - 示例: `ls -l`
    - `-a`: 显示所有文件（包括隐藏文件）。
      - 示例: `ls -a`

- **cd (change directory)**: 切换工作目录。

  - 示例: `cd /path/to/directory`
  - 常用操作:
    - `cd ..`: 返回上级目录。
    - `cd ../../`: 返回上级的上级目录。
    - `cd ~`: 返回当前用户的主目录。
    - `cd -`: 返回上一次所在的目录。

- **pwd (print working directory)**: 显示当前工作目录的绝对路径。

  - 示例: `pwd`

  #### 文件操作

- **cp (copy)**: 复制文件或目录。

  - 示例: `cp file1 file2`（复制文件）
  - 示例: `cp -r dir1 dir2`（递归复制目录）
  - 常用选项:
    - `-r`: 递归复制目录及其内容。

- **rm (remove)**: 删除文件或目录。

  - 示例: `rm filename`（删除文件）
  - 示例: `rm -r dirname`（递归删除目录）
  - 常用选项:
    - `-r`: 递归删除目录及其内容。
    - `-f`: 强制删除，不提示确认。

- **mv (move)**: 移动文件或目录，或重命名文件或目录。

  - 示例: `mv file1 file2`（重命名文件）
  - 示例: `mv file1 /path/to/directory`（移动文件）

- **touch**: 创建空文件或更新文件的时间戳。

  - 示例: `touch filename`

- **echo**: 输出文本或变量内容。

  - 示例: `echo "Hello, World!"`
  - 示例: `echo $PATH`

#### 读取文件

- **od**: 以八进制或其他格式显示文件内容。
  - 示例: `od -c filename`（以字符格式显示）
- **cat**: 显示文件内容。
  - 示例: `cat filename`
- **tac**: 从最后一行开始反向显示文件内容。
  - 示例: `tac filename`
- **less**: 分页显示大文件内容，支持上下滚动。
  - 示例: `less filename`
  - 常用操作:
    - `空格`: 向下翻页。
    - `b`: 向上翻页。
    - `q`: 退出。
- **head**: 显示文件的前几行（默认10行）。
  - 示例: `head -n 20 filename`（显示前20行）
- **tail**: 显示文件的最后几行（默认10行）。
  - 示例: `tail -n 20 filename`（显示最后20行）
  - 常用选项:
    - `-f`: 实时跟踪文件内容的变化（常用于查看日志）。
      - 示例: `tail -f /var/log/syslog`

#### 目录结构与路径

- **目录结构**: Linux采用树形目录结构，根目录为`/`，所有文件和目录都从根目录开始。
- **相对路径与绝对路径**:
  - **相对路径**: 相对于当前工作目录的路径，如`./file`（当前目录下的文件）。
  - **绝对路径**: 从根目录开始的完整路径，如`/home/user/file`。

#### **文件权限管理**

- **chmod**: 修改文件或目录的权限。
  - 示例: `chmod 755 filename`（设置权限为rwxr-xr-x）
  - 示例: `chmod u+x filename`（为所有者添加执行权限）
  - 权限表示:
    - `r`: 读（4）
    - `w`: 写（2）
    - `x`: 执行（1）
    - 所有者、组、其他用户的权限分别用3个数字表示，如`755`。

#### **目录操作**

- **mkdir (make directory)**: 创建新目录。
  - 示例: `mkdir dirname`
  - 常用选项:
    - `-p`: 递归创建目录（如果父目录不存在则一并创建）。
      - 示例: `mkdir -p parent/child`
- **ls (list)**: 列出目录内容。
  - 示例: `ls`
  - 常用选项:
    - `-l`: 显示详细信息（权限、所有者、大小等）。
      - 示例: `ls -l`
    - `-a`: 显示所有文件（包括隐藏文件）。
      - 示例: `ls -a`
- **cd (change directory)**: 切换工作目录。
  - 示例: `cd /path/to/directory`
  - 常用操作:
    - `cd ..`: 返回上级目录。
    - `cd ../../`: 返回上级的上级目录。
    - `cd ~`: 返回当前用户的主目录。
    - `cd -`: 返回上一次所在的目录。
- **pwd (print working directory)**: 显示当前工作目录的绝对路径。
  - 示例: `pwd`

#### **文件操作**

- **cp (copy)**: 复制文件或目录。
  - 示例: `cp file1 file2`（复制文件）
  - 示例: `cp -r dir1 dir2`（递归复制目录）
  - 常用选项:
    - `-r`: 递归复制目录及其内容。
- **rm (remove)**: 删除文件或目录。
  - 示例: `rm filename`（删除文件）
  - 示例: `rm -r dirname`（递归删除目录）
  - 常用选项:
    - `-r`: 递归删除目录及其内容。
    - `-f`: 强制删除，不提示确认。
- **mv (move)**: 移动文件或目录，或重命名文件或目录。
  - 示例: `mv file1 file2`（重命名文件）
  - 示例: `mv file1 /path/to/directory`（移动文件）
- **touch**: 创建空文件或更新文件的时间戳。
  - 示例: `touch filename`
- **echo**: 输出文本或变量内容。
  - 示例: `echo "Hello, World!"`
  - 示例: `echo $PATH`

#### 读取文件

- **od**: 以八进制或其他格式显示文件内容。
  - 示例: `od -c filename`（以字符格式显示）
- **cat**: 显示文件内容。
  - 示例: `cat filename`
- **tac**: 从最后一行开始反向显示文件内容。
  - 示例: `tac filename`
- **less**: 分页显示大文件内容，支持上下滚动。
  - 示例: `less filename`
  - 常用操作:
    - `空格`: 向下翻页。
    - `b`: 向上翻页。
    - `q`: 退出。
- **head**: 显示文件的前几行（默认10行）。
  - 示例: `head -n 20 filename`（显示前20行）
- **tail**: 显示文件的最后几行（默认10行）。
  - 示例: `tail -n 20 filename`（显示最后20行）
  - 常用选项:
    - `-f`: 实时跟踪文件内容的变化（常用于查看日志）。
      - 示例: `tail -f /var/log/syslog`

#### **文件编辑**

- **TUI编辑器**:
  - **Vi/Vim**: 强大的文本编辑器，支持多种模式（命令模式、插入模式等）。
    - 常用快捷键:
      - `i`: 进入插入模式。
      - `Esc`: 返回命令模式。
      - `:wq`: 保存并退出。
      - `:q!`: 不保存并退出。
  - **Nano**: 简单易用的文本编辑器，适合初学者。
    - 常用快捷键:
      - `Ctrl+O`: 保存文件。
      - `Ctrl+X`: 退出编辑器。
  - **Emacs**: 功能强大的编辑器，支持扩展和脚本。
- **GUI编辑器**:
  - **gedit**: Gnome桌面环境的默认文本编辑器。
  - **kate**: KDE桌面环境的默认文本编辑器。
  - **Sublime**: 跨平台的强大文本编辑器。
  - **VSCodium**: 开源的Visual Studio Code版本。
  - **Atom**: GitHub开发的现代化文本编辑器。

#### **man (manual)**

- **man**: 查看命令的手册页。
  - 示例: `man ls`
  - 常用操作:
    - `空格`: 向下翻页。
    - `b`: 向上翻页。
    - `/keyword`: 搜索关键字。
    - `q`: 退出。

# 第二节

## 用户与用户组

- #### **用户管理**

  - **useradd**: 创建新用户。
    - 示例: `useradd username`
    - 常用选项:
      - `-m`: 创建用户主目录。
      - `-s`: 指定用户的默认Shell。
      - `-u`: 指定用户的UID。
      - `-g`: 指定用户的主组。
  - **adduser**: 更友好的用户创建工具（基于`useradd`），提供交互式提示。
    - 示例: `adduser username`
  - **usermod**: 修改用户属性。
    - 示例: `usermod -s /bin/zsh username`（修改用户的默认Shell）
    - 常用选项:
      - `-l`: 修改用户名。
      - `-g`: 修改用户的主组。
      - `-aG`: 将用户添加到附加组。
  - **userdel**: 删除用户。
    - 示例: `userdel username`
    - 常用选项:
      - `-r`: 同时删除用户的主目录和邮件文件。
  - **chfn**: 修改用户的指纹信息（如全名、电话等）。
    - 示例: `chfn username`
  - **chsh**: 修改用户的默认Shell。
    - 示例: `chsh -s /bin/zsh username`
  - **finger**: 显示用户信息（需要安装`finger`工具）。
    - 示例: `finger username`
  - **whoami/id**: 显示当前用户信息。
    - `whoami`: 显示当前用户名。
    - `id`: 显示当前用户的UID、GID及所属组。
      - 示例: `id username`
  - **passwd**: 修改用户密码。
    - 示例: `passwd username`（修改指定用户的密码）
    - 示例: `passwd`（修改当前用户的密码）

  ------

  #### **用户组管理**

  - **groupadd**: 创建新用户组。
    - 示例: `groupadd groupname`
    - 常用选项:
      - `-g`: 指定GID。
  - **groupmod**: 修改用户组属性。
    - 示例: `groupmod -n newgroupname oldgroupname`（修改组名）
    - 常用选项:
      - `-g`: 修改GID。
  - **groupdel**: 删除用户组。
    - 示例: `groupdel groupname`
  - **newgrp**: 切换用户的主组（临时切换）。
    - 示例: `newgrp groupname`
  - **gpasswd**: 管理用户组。
    - 示例: `gpasswd -a username groupname`（将用户添加到组）
    - 示例: `gpasswd -d username groupname`（将用户从组中移除）

  ------

  #### **UID/GID**

  - **UID (User ID)**: 用户的唯一标识符。
    - 系统用户UID通常小于1000，普通用户UID从1000开始。
  - **GID (Group ID)**: 用户组的唯一标识符。
    - 每个用户都有一个主组（Primary Group），可以属于多个附加组（Supplementary Groups）。

  ------

  #### **文件权限管理**

  - **chmod**: 修改文件或目录的权限。
    - 示例: `chmod 755 filename`（设置权限为rwxr-xr-x）
    - 示例: `chmod u+x filename`（为所有者添加执行权限）
    - 权限表示:
      - `r`: 读（4）
      - `w`: 写（2）
      - `x`: 执行（1）
      - 所有者、组、其他用户的权限分别用3个数字表示，如`755`。
  - **chgrp**: 修改文件或目录的所属组。
    - 示例: `chgrp groupname filename`
  - **chown**: 修改文件或目录的所有者和所属组。
    - 示例: `chown username:groupname filename`
    - 常用选项:
      - `-R`: 递归修改目录及其内容的所有者和组。


## 文件层次结构

在根目录下的这些目录的含义，由文件系统层次结构标准 (FHS, Filesystem Hierarchy Standard) 来定义。这个标准定义了 Linux 发行版的标准目录结构。大部分的 Linux 发行版遵循此标准，或由此标准做了细小的调整。以下进行一个简要的介绍。可以在 [FHS 官方文档](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) 中查看标准的具体内容。

- `/bin`：存储必须的程序文件，对所有用户都可用。

- `/boot`：存储在启动系统时需要的文件。

- `/dev`：存储设备文件。

- `/etc`：存储系统和程序的配置文件。

- `/home`：用户的家目录。存储用户自己的信息。

- `/lib`：存放系统运行必须的程序库文件。

- `/media` 和 `/mnt`这两个目录都用于挂载其他的文件系统。`/media` 用于可移除的文件系统（如光盘），而 `/mnt` 用于临时使用。

- `/opt`：存放额外的程序包。一般将一些大型的应用程序放置在这个目录。

- `/root`：root  用户的家目录。

- `/run`系统运行时的数据。在每次启动时，里面的数据都会被删除。

- `/sbin`：存储用于系统管理，以及仅允许 `root` 用户使用的程序。如 `fsck`（文件系统修复程序）、`reboot`（重启系统）等。

- `/srv`：存储网络服务的数据。

- `/tmp`：存放临时文件的目录，所有用户都可使用。

- `/usr`：大多数软件都会安装在此处。其中包含的部分子目录如下：
  - `/usr/include`：存储系统通用的 C 头文件。当然，里面会有你非常熟悉的头文件，如 `stdio.h`。
  - `/usr/local`：存储系统管理员自己安装的程序，这些文件通常不受系统的软件包管理机制（如 `apt`）控制。
  - `/usr/share`：存储程序的数据文件（如 `man` 文档、GUI 程序使用的图片等）。

- `/var`：存储会发生变化的程序相关文件。例如下面的目录：
  - `/var/log`：存储程序的日志文件。
  - `/var/lib`：存储程序自身的状态信息（如 lock file）。
  - `/var/run`：存储程序运行时的数据（部分发行版会将该目录符号链接到 `/run` 目录）。
  - `/var/spool`：存储「等待进一步处理」的程序数据。

## 终端进阶

### CLI, Terminal, Console, TTY 与 Shell

- **CLI (Command Line Interface)**: 命令行界面，用户通过输入文本命令与操作系统交互。
- **Terminal**: 终端，提供用户与CLI交互的界面，可以是物理设备或软件模拟。
- **Console**: 控制台，通常指物理设备上的直接输入输出界面，如服务器上的物理控制台。
- **TTY (Teletypewriter)**: 电传打字机，现代指终端设备或虚拟终端。
- **Shell**: 命令行解释器，负责解析用户输入的命令并执行。

#### 常用 Shell

- **sh (Bourne Shell)**: 早期的Unix Shell，功能较为基础。
- **bash (Bourne Again Shell)**: sh的增强版，Linux系统默认的Shell，功能强大且兼容sh。
- **zsh (Z Shell)**: 功能丰富的Shell，支持插件和主题，用户体验友好。
- **fish (Friendly Interactive Shell)**: 现代化的Shell，提供自动补全和语法高亮等功能。
- **cmd (Command Prompt)**: Windows系统的命令行解释器，功能较为基础。
- **powershell/Windows powershell**: Windows系统的强大命令行工具，支持脚本和对象操作。

### **tty**:

- **用途**: 显示当前终端设备。
- **示例**:
  - 显示终端设备: `tty`

### Shell 机制

- #### 分工

  - **Shell**: 负责解析和执行用户输入的命令。
  - **Kernel**: 操作系统内核，负责管理硬件资源和执行系统调用。

  #### I/O重定向

  - **>**: 重定向输出到文件（覆盖）。
  - **>>**: 重定向输出到文件（追加）。
  - **<**: 从文件读取输入。
  - **2>**: 重定向错误输出到文件。

  #### 管道

  - **|**: 将一个命令的输出作为另一个命令的输入。

  #### alias 别名与 unalias

  - **alias**: 创建命令的别名，简化常用命令的输入。
    - 示例: `alias ll='ls -la'`
  - **unalias**: 删除已定义的别名。
    - 示例: `unalias ll`

  #### 环境变量

  - **env/printenv**: 显示当前的环境变量。
  - **export**: 设置环境变量，使其在当前Shell会话及其子进程中可用。
    - 示例: `export PATH=$PATH:/new/path`
  - **unset**: 删除环境变量。
    - 示例: `unset PATH`

  #### Shell脚本

  - **Shell脚本**: 包含一系列Shell命令的文本文件，可以自动化执行任务。
    - 示例: `#!/bin/bash`
    - 示例: `echo "Hello, World!"`

  #### history和历史命令

  - **history**: 显示当前会话的命令历史。
    - 示例: `history`
  - **!n**: 执行历史记录中第n条命令。
    - 示例: `!100`
  - **!!**: 执行上一条命令。
    - 示例: `!!`
  - **!string**: 执行最近一条以string开头的命令。
    - 示例: `!ls`


## 文件传输

- **scp (Secure Copy)**:
  - **用途**: 在本地和远程系统之间安全地复制文件，基于SSH协议，提供加密传输。
  - **示例**:
    - 从本地复制到远程: `scp file.txt user@remote:/path/to/destination`
    - 从远程复制到本地: `scp user@remote:/path/to/file.txt /local/destination`
    - 递归复制目录: `scp -r dir user@remote:/path/to/destination`
- **rsync**:
  - **用途**: 同步文件和目录，支持增量传输，节省带宽和时间。
  - **示例**:
    - 同步本地目录到远程: `rsync -avz /local/dir user@remote:/path/to/destination`
    - 从远程同步到本地: `rsync -avz user@remote:/path/to/dir /local/destination`
    - 删除目标目录中多余的文件: `rsync -avz --delete /local/dir user@remote:/path/to/destination`
  - **常用选项**:
    - `-a`: 归档模式，保留文件属性和权限。
    - `-v`: 显示详细输出。
    - `-z`: 压缩传输数据。
- **ftp (File Transfer Protocol)**:
  - **用途**: 用于在客户端和服务器之间传输文件。
  - **示例**:
    - 连接FTP服务器: `ftp ftp.example.com`
    - 下载文件: `get file.txt`
    - 上传文件: `put file.txt`
  - **注意**: FTP协议不加密，建议使用SFTP或FTPS替代。
- **wget**:
  - **用途**: 从网络上下载文件，支持HTTP、HTTPS和FTP协议。
  - **示例**:
    - 下载单个文件: `wget https://example.com/file.txt`
    - 递归下载整个网站: `wget -r https://example.com`
    - 断点续传: `wget -c https://example.com/file.txt`
  - **常用选项**:
    - `-O`: 指定输出文件名。
    - `-P`: 指定下载目录。
- **curl**:
  - **用途**: 传输数据，支持多种协议（HTTP、HTTPS、FTP等），常用于API调用和文件下载。
  - **示例**:
    - 下载文件: `curl -O https://example.com/file.txt`
    - 发送POST请求: `curl -X POST -d "param=value" https://example.com/api`
    - 显示响应头: `curl -I https://example.com`
  - **常用选项**:
    - `-o`: 指定输出文件名。
    - `-L`: 自动重定向。
    - `-H`: 添加请求头。

------

#### **图形化工具**

- **WinSCP**:
  - **用途**: Windows下的图形化SCP客户端，支持SFTP和SCP协议。
  - **特点**:
    - 提供直观的界面，支持拖放操作。
    - 支持脚本自动化。
  - **适用场景**: 需要在Windows和Linux服务器之间传输文件。
- **FileZilla**:
  - **用途**: 跨平台的FTP客户端，支持FTP、SFTP和FTPS。
  - **特点**:
    - 支持多平台（Windows、Linux、macOS）。
    - 提供站点管理器，方便管理多个连接。
  - **适用场景**: 需要在不同系统之间传输文件。
- **Xftp**:
  - **用途**: 专为Windows设计的SFTP/FTP客户端，提供图形化界面。
  - **特点**:
    - 支持多标签页和分屏视图。
    - 提供高级文件传输功能。
  - **适用场景**: 需要在Windows和远程服务器之间高效传输文件。

## 文件操作命令

#### **文本搜索与处理**

- **grep**:
  - **用途**: 在文件中搜索指定的字符串或模式。
  - **示例**:
    - 搜索包含"error"的行: `grep "error" file.txt`
    - 忽略大小写: `grep -i "error" file.txt`
    - 递归搜索目录: `grep -r "error" /path/to/dir`
  - **常用选项**:
    - `-v`: 反向匹配（显示不包含模式的行）。
    - `-n`: 显示匹配行的行号。
    - `-c`: 统计匹配行的数量。
- **awk**:
  - **用途**: 强大的文本处理工具，用于模式扫描和处理。
  - **示例**:
    - 打印文件的第二列: `awk '{print $2}' file.txt`
    - 根据条件过滤行: `awk '/error/ {print $0}' file.txt`
    - 计算列的总和: `awk '{sum+=$1} END {print sum}' file.txt`
  - **常用功能**:
    - 支持条件判断、循环、变量等编程特性。
- **sed**:
  - **用途**: 流编辑器，用于对文本进行过滤和转换。
  - **示例**:
    - 替换文本: `sed 's/old/new/g' file.txt`
    - 删除空白行: `sed '/^$/d' file.txt`
    - 打印特定行: `sed -n '5,10p' file.txt`
  - **常用选项**:
    - `-i`: 直接修改文件内容。
    - `-e`: 执行多个编辑命令。

#### **文件排序与统计**

- **sort**:
  - **用途**: 对文件的行进行排序。
  - **示例**:
    - 按字母顺序排序: `sort file.txt`
    - 按数字排序: `sort -n file.txt`
    - 去重: `sort -u file.txt`
  - **常用选项**:
    - `-r`: 逆序排序。
    - `-k`: 按指定列排序。
- **wc**:
  - **用途**: 统计文件的行数、字数和字节数。
  - **示例**:
    - 统计行数: `wc -l file.txt`
    - 统计字数: `wc -w file.txt`
    - 统计字节数: `wc -c file.txt`
  - **常用选项**:
    - `-m`: 统计字符数。

#### **文件对比**

- **diff**:
  - **用途**: 比较两个文件的差异。
  - **示例**:
    - 比较文件: `diff file1.txt file2.txt`
    - 显示上下文: `diff -c file1.txt file2.txt`
  - **常用选项**:
    - `-u`: 生成统一的差异输出。
- **diffstat**:
  - **用途**: 生成`diff`命令的统计信息。
  - **示例**:
    - 统计差异: `diff file1.txt file2.txt | diffstat`
- **cmp**:
  - **用途**: 逐字节比较两个文件。
  - **示例**:
    - 比较文件: `cmp file1.txt file2.txt`

#### **文件查找**

- **find**:
  - **用途**: 在目录树中查找文件。
  - **示例**:
    - 按名称查找: `find /path/to/dir -name "*.txt"`
    - 按类型查找: `find /path/to/dir -type f`
    - 按大小查找: `find /path/to/dir -size +1M`
  - **常用选项**:
    - `-exec`: 对查找到的文件执行命令。
- **locate**:
  - **用途**: 通过数据库快速查找文件。
  - **示例**:
    - 查找文件: `locate file.txt`
  - **注意**: 需要定期更新数据库（`updatedb`）。
- **whereis**:
  - **用途**: 查找二进制文件、源代码和手册页。
  - **示例**:
    - 查找`ls`命令的位置: `whereis ls`
- **which**:
  - **用途**: 查找可执行文件的路径。
  - **示例**:
    - 查找`python`的路径: `which python`

#### **文件链接与类型识别**

- **ln**:
  - **用途**: 创建文件链接（硬链接或符号链接）。
  - **示例**:
    - 创建硬链接: `ln file1.txt file2.txt`
    - 创建符号链接: `ln -s file1.txt file2.txt`
- **file**:
  - **用途**: 确定文件的类型。
  - **示例**:
    - 检查文件类型: `file file.txt`

#### **文件分割**

- **split**:
  - **用途**: 将大文件分割成多个小文件。
  - **示例**:
    - 按行数分割: `split -l 1000 largefile.txt`
    - 按大小分割: `split -b 100M largefile.txt`
  - **常用选项**:
    - `-a`: 指定后缀长度。
    - `-d`: 使用数字后缀。

# 第三节

## 软件包、软件仓库与仓库镜像

#### **常见包管理器**

- **APT (Advanced Package Tool)**:
  - **用途**: Debian/Ubuntu系统的包管理工具，用于管理软件包的安装、更新和删除。
  - **常用命令**:
    - 更新软件包列表: `sudo apt update`
    - 升级已安装的软件包: `sudo apt upgrade`
    - 安装软件包: `sudo apt install package_name`
    - 删除软件包: `sudo apt remove package_name`
    - 搜索软件包: `apt search keyword`
    - 显示软件包信息: `apt show package_name`
- **YUM (Yellowdog Updater Modified)**:
  - **用途**: Red Hat/CentOS系统的包管理工具，用于管理RPM软件包。
  - **常用命令**:
    - 安装软件包: `sudo yum install package_name`
    - 更新软件包: `sudo yum update package_name`
    - 删除软件包: `sudo yum remove package_name`
    - 搜索软件包: `yum search keyword`
    - 显示软件包信息: `yum info package_name`
- **DNF (Dandified YUM)**:
  - **用途**: Fedora系统的包管理工具，YUM的下一代版本，提供更好的性能和依赖解析。
  - **常用命令**:
    - 安装软件包: `sudo dnf install package_name`
    - 更新软件包: `sudo dnf update package_name`
    - 删除软件包: `sudo dnf remove package_name`
    - 搜索软件包: `dnf search keyword`
    - 显示软件包信息: `dnf info package_name`

#### **AppImage**

- **用途**: 一种跨平台的软件打包格式，无需安装即可运行。
- **特点**:
  - 单个文件包含所有依赖，便于分发和使用。
  - 无需管理员权限即可运行。
- **示例**:
  - 下载AppImage文件: `wget https://example.com/appimage`
  - 赋予执行权限: `chmod +x appimage`
  - 运行: `./appimage`

#### **依赖管理**

- **依赖**: 软件包依赖关系管理，确保安装的软件包能够正常运行。
- **常见工具**:
  - **APT**: 自动解决依赖关系。
  - **YUM/DNF**: 自动解决依赖关系。
  - **dpkg**: Debian系统的底层包管理工具，手动解决依赖关系。
  - **rpm**: Red Hat系统的底层包管理工具，手动解决依赖关系。

#### **编译安装**

- **make**:
  - **用途**: 自动化编译工具，根据Makefile文件编译源代码。
  - **示例**:
    - 配置: `./configure`
    - 编译: `make`
    - 安装: `sudo make install`
- **cmake**:
  - **用途**: 跨平台的自动化编译工具，生成Makefile文件。
  - **示例**:
    - 生成Makefile: `cmake .`
    - 编译: `make`
    - 安装: `sudo make install`
- **qmake**:
  - **用途**: Qt项目的自动化编译工具，生成Makefile文件。
  - **示例**:
    - 生成Makefile: `qmake`
    - 编译: `make`
    - 安装: `sudo make install`

## 进程与前后台

#### **进程查看**

- **ps (Process Status)**:
  - **用途**: 显示当前运行的进程。
  - **常用命令**:
    - 显示所有进程: `ps aux`
    - 显示当前用户的进程: `ps -u username`
    - 显示进程树: `ps -e --forest`
  - **输出字段**:
    - `PID`: 进程ID。
    - `USER`: 进程所有者。
    - `%CPU`: CPU占用率。
    - `%MEM`: 内存占用率。
    - `COMMAND`: 进程命令。
- **top**:
  - **用途**: 实时显示系统进程状态。
  - **常用操作**:
    - `k`: 终止指定进程。
    - `P`: 按CPU使用率排序。
    - `M`: 按内存使用率排序。
    - `q`: 退出。
  - **增强版**:
    - **htop**: 提供更友好的界面和更多功能，支持鼠标操作。
    - **btop**: 另一个增强版，提供更丰富的系统监控信息。

#### **进程标识符**

- **PID (Process ID)**:
  - **用途**: 进程的唯一标识符，用于管理和控制进程。
  - **示例**:
    - 查找进程PID: `ps aux | grep process_name`

#### **进程优先级**

1. **nice**:
   - **用途**: 调整进程的优先级（范围：-20到19，值越小优先级越高）。
   - **示例**:
     - 启动进程并设置优先级: `nice -n 10 command`
   - **注意**: 普通用户只能降低优先级（增大nice值）。
2. **renice**:
   - **用途**: 修改已运行进程的优先级。
   - **示例**:
     - 修改进程优先级: `renice -n 5 -p PID`

#### **进程状态**

- **进程状态**:
  - **R (Running)**: 运行中。
  - **S (Sleeping)**: 睡眠中（可中断）。
  - **D (Uninterruptible Sleep)**: 不可中断的睡眠（通常等待I/O）。
  - **Z (Zombie)**: 僵尸进程（已终止但未被父进程回收）。
  - **T (Stopped)**: 已停止。

#### **信号**

- **信号**: 用于向进程发送控制信号。
  - **常用信号**:
    - `SIGKILL (9)`: 强制终止进程。
    - `SIGTERM (15)`: 请求进程终止（允许进程清理资源）。
    - `SIGHUP (1)`: 挂起信号，通常用于重启进程。
  - **示例**:
    - 发送信号: `kill -SIGKILL PID`
    - 终止进程: `kill PID`

#### **nohup**

- **nohup**:
  - **用途**: 使进程在用户退出后继续运行。
  - **示例**:
    - 启动后台进程: `nohup command &`
  - **输出**:
    - 默认输出到`nohup.out`文件。

#### **前后台控制**

- **前后台切换**:
  - **&**: 将进程放到后台运行。
    - 示例: `command &`
  - **fg**: 将后台进程切换到前台。
    - 示例: `fg %job_id`
  - **bg**: 将暂停的后台进程继续运行。
    - 示例: `bg %job_id`
- **jobs**:
  - **用途**: 显示当前会话的后台任务。
  - **示例**:
    - 查看后台任务: `jobs`

#### **内存使用情况**

- **free**:
  - **用途**: 显示系统内存使用情况。
  - **常用选项**:
    - `-h`: 以人类可读的格式显示。
    - `-m`: 以MB为单位显示。
  - **示例**:
    - 查看内存使用: `free -h`

#### **终止进程**

- **kill**:
  - **用途**: 终止指定进程。
  - **示例**:
    - 终止进程: `kill PID`
    - 强制终止: `kill -9 PID`
- **pkill**:
  - **用途**: 根据进程名终止进程。
  - **示例**:
    - 终止进程: `pkill process_name`
- **killall**:
  - **用途**: 终止所有同名进程。
  - **示例**:
    - 终止所有同名进程: `killall process_name`

## 服务与例行性任务

#### **守护进程**

- **守护进程 (Daemon)**:
  - **用途**: 在后台运行的进程，通常用于提供服务（如Web服务器、数据库等）。
  - **特点**:
    - 脱离终端运行，不受用户登录或退出的影响。
    - 通常以`d`结尾命名（如`httpd`, `sshd`）。

#### **服务管理**

- **systemd/systemctl**:
  - **用途**: 现代Linux系统的服务管理工具，用于启动、停止、重启和管理服务。
  - **常用命令**:
    - 启动服务: `sudo systemctl start service_name`
    - 停止服务: `sudo systemctl stop service_name`
    - 重启服务: `sudo systemctl restart service_name`
    - 查看服务状态: `sudo systemctl status service_name`
    - 启用开机自启动: `sudo systemctl enable service_name`
    - 禁用开机自启动: `sudo systemctl disable service_name`
  - **服务文件位置**: `/etc/systemd/system/`
- **SysVinit/service**:
  - **用途**: 传统的服务管理工具，仍在一些旧系统中使用。
  - **常用命令**:
    - 启动服务: `sudo service service_name start`
    - 停止服务: `sudo service service_name stop`
    - 重启服务: `sudo service service_name restart`
    - 查看服务状态: `sudo service service_name status`
  - **服务脚本位置**: `/etc/init.d/`

#### **配置 Nginx 为系统服务**

- **步骤**:

  1. 创建Nginx的systemd服务文件:

     ```
     sudo nano /etc/systemd/system/nginx.service
     ```

  2. 添加以下内容:

     ```
     [Unit]
     Description=A high performance web server and a reverse proxy server
     After=network.target
     
     [Service]
     Type=forking
     PIDFile=/run/nginx.pid
     ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
     ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
     ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
     ExecStop=/bin/kill -s QUIT $MAINPID
     PrivateTmp=true
     
     [Install]
     WantedBy=multi-user.target
     ```

  3. 重新加载systemd配置:

     ```
     sudo systemctl daemon-reload
     ```

  4. 启动并启用Nginx服务:

     ```
     sudo systemctl start nginx
     sudo systemctl enable nginx
     ```

#### **例行性任务**

- **at**:

  - **用途**: 安排一次性定时任务。

  - **示例**:

    - 安排任务: `at 14:00`

    - 输入命令后按`Ctrl+D`保存。

    - 示例任务:

      ```
      echo "Hello, World!" > /tmp/hello.txt
      ```

  - **常用命令**:

    - 查看任务队列: `atq`
    - 删除任务: `atrm job_id`

- **crontab**:

  - **用途**: 安排周期性定时任务。

  - **编辑crontab文件**:

    - 编辑当前用户的crontab: `crontab -e`
    - 查看当前用户的crontab: `crontab -l`

  - **crontab格式**:

    ```
    * * * * * command_to_execute
    - - - - -
    | | | | |
    | | | | +----- Day of the week (0 - 6) (Sunday=0)
    | | | +------- Month (1 - 12)
    | | +--------- Day of the month (1 - 31)
    | +----------- Hour (0 - 23)
    +------------- Minute (0 - 59)
    ```

  - **示例**:

    - 每天凌晨2点执行脚本: `0 2 * * * /path/to/script.sh`
    - 每5分钟执行一次命令: `*/5 * * * * command`

  - **系统级crontab**:

    - 编辑系统级crontab: `sudo nano /etc/crontab`

    - 系统级crontab需要指定用户:

      ```
      * * * * * username command_to_execute
      ```

## 文件压缩与解压缩

#### **压缩工具**

- **bzip2**:
  - **用途**: 使用Burrows-Wheeler算法进行文件压缩，压缩率较高。
  - **示例**:
    - 压缩文件: `bzip2 file.txt`（生成`file.txt.bz2`）
  - **常用选项**:
    - `-k`: 保留原始文件。
      - 示例: `bzip2 -k file.txt`
- **bzip2recover**:
  - **用途**: 恢复损坏的bzip2文件。
  - **示例**:
    - 恢复文件: `bzip2recover file.txt.bz2`
- **zip**:
  - **用途**: 常用的压缩格式，支持多文件压缩。
  - **示例**:
    - 压缩文件: `zip archive.zip file1.txt file2.txt`
    - 压缩目录: `zip -r archive.zip dir/`
  - **常用选项**:
    - `-r`: 递归压缩目录。
    - `-q`: 静默模式（不显示输出）。
- **tar**:
  - **用途**: 归档工具，常与gzip或bzip2结合使用。
  - **示例**:
    - 创建tar归档: `tar -cvf archive.tar file1.txt file2.txt`
    - 压缩为gzip格式: `tar -czvf archive.tar.gz file1.txt file2.txt`
    - 压缩为bzip2格式: `tar -cjvf archive.tar.bz2 file1.txt file2.txt`
  - **常用选项**:
    - `-c`: 创建归档。
    - `-x`: 解压归档。
    - `-v`: 显示详细信息。
    - `-f`: 指定归档文件名。
    - `-z`: 使用gzip压缩。
    - `-j`: 使用bzip2压缩。
- **7z**:
  - **用途**: 高压缩比的压缩格式，支持多种压缩算法。
  - **示例**:
    - 压缩文件: `7z a archive.7z file1.txt file2.txt`
  - **常用选项**:
    - `a`: 添加文件到压缩包。
    - `-t`: 指定压缩格式（如`7z`, `zip`, `tar`）。

#### **解压缩工具**

- **bunzip2**:
  - **用途**: 解压bzip2文件。
  - **示例**:
    - 解压文件: `bunzip2 file.txt.bz2`（生成`file.txt`）
- **unzip**:
  - **用途**: 解压zip文件。
  - **示例**:
    - 解压文件: `unzip archive.zip`
  - **常用选项**:
    - `-d`: 指定解压目录。
      - 示例: `unzip archive.zip -d /path/to/dir`
- **tar**:
  - **用途**: 解压tar归档文件。
  - **示例**:
    - 解压tar归档: `tar -xvf archive.tar`
    - 解压gzip格式: `tar -xzvf archive.tar.gz`
    - 解压bzip2格式: `tar -xjvf archive.tar.bz2`
  - **常用选项**:
    - `-x`: 解压归档。
    - `-v`: 显示详细信息。
    - `-f`: 指定归档文件名。
    - `-z`: 解压gzip格式。
    - `-j`: 解压bzip2格式。
- **7z**:
  - **用途**: 解压7z文件。
  - **示例**:
    - 解压文件: `7z x archive.7z`
  - **常用选项**:
    - `x`: 解压文件。

## 网络通信

#### **远程连接**

- **ssh (Secure Shell)**:
  - **用途**: 安全远程登录协议，提供加密的远程连接。
  - **示例**:
    - 连接远程主机: `ssh user@remote_host`
    - 指定端口: `ssh -p 2222 user@remote_host`
    - 使用密钥登录: `ssh -i /path/to/private_key user@remote_host`
- **telnet**:
  - **用途**: 远程登录协议，不加密，安全性较低。
  - **示例**:
    - 连接远程主机: `telnet remote_host 23`
  - **注意**: 不推荐用于敏感数据传输。
- **cu (Call Up)**:
  - **用途**: 用于串行通信，连接调制解调器或其他串行设备。
  - **示例**:
    - 连接串行设备: `cu -l /dev/ttyS0`
- **nc (Netcat)**:
  - **用途**: 网络工具，用于TCP/UDP连接和端口扫描。
  - **示例**:
    - 监听端口: `nc -l -p 1234`
    - 连接远程主机: `nc remote_host 1234`
    - 端口扫描: `nc -zv remote_host 1-100`

#### **防火墙管理**

- **iptables**:
  - **用途**: Linux内核的防火墙工具，用于配置网络包过滤规则。
  - **示例**:
    - 允许SSH连接: `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`
    - 拒绝所有其他连接: `iptables -A INPUT -j DROP`
  - **常用命令**:
    - 查看规则: `iptables -L`
    - 保存规则: `iptables-save > /etc/iptables/rules.v4`
- **ufw (Uncomplicated Firewall)**:
  - **用途**: 简化的防火墙管理工具，基于iptables。
  - **示例**:
    - 允许SSH连接: `sudo ufw allow 22`
    - 启用防火墙: `sudo ufw enable`
  - **常用命令**:
    - 查看状态: `sudo ufw status`
    - 删除规则: `sudo ufw delete allow 22`

#### **网络诊断**

- **ping**:
  - **用途**: 测试网络连通性。
  - **示例**:
    - 测试连接: `ping remote_host`
    - 指定次数: `ping -c 4 remote_host`
- **netstat**:
  - **用途**: 显示网络连接、路由表、接口统计等信息。
  - **示例**:
    - 显示所有连接: `netstat -a`
    - 显示监听端口: `netstat -l`
    - 显示路由表: `netstat -r`
- **traceroute**:
  - **用途**: 显示数据包到达目标主机的路径。
  - **示例**:
    - 跟踪路径: `traceroute remote_host`
- **tcpdump**:
  - **用途**: 网络抓包工具，用于分析网络流量。
  - **示例**:
    - 抓取所有流量: `tcpdump -i eth0`
    - 抓取特定端口的流量: `tcpdump port 80`

#### **消息通讯**

- **talk**:
  - **用途**: 实时聊天工具，允许两个用户在同一主机上聊天。
  - **示例**:
    - 发起聊天: `talk user@remote_host`
- **wall**:
  - **用途**: 向所有用户发送消息。
  - **示例**:
    - 发送消息: `wall "System will reboot in 5 minutes"`
- **write**:
  - **用途**: 向指定用户发送消息。
  - **示例**:
    - 发送消息: `write username`
- **mail**:
  - **用途**: 发送和接收电子邮件。
  - **示例**:
    - 发送邮件: `echo "Body" | mail -s "Subject" user@example.com`
    - 查看收件箱: `mail`

#### **Web服务**

- **httpd**:
  - **用途**: Apache HTTP服务器，用于提供Web服务。
  - **示例**:
    - 启动服务: `sudo systemctl start httpd`
    - 停止服务: `sudo systemctl stop httpd`
- **apachectl**:
  - **用途**: Apache服务器的控制工具。
  - **示例**:
    - 启动服务: `sudo apachectl start`
    - 重启服务: `sudo apachectl restart`

#### **其他工具**

- **ifconfig/ip addr**:
  - **用途**: 配置网络接口。
  - **示例**:
    - 查看网络接口: `ifconfig` 或 `ip addr`
    - 启用网络接口: `sudo ifconfig eth0 up`
- **arpwatch**:
  - **用途**: 监控ARP活动，检测ARP欺骗攻击。
  - **示例**:
    - 启动监控: `sudo arpwatch -i eth0`

## 系统状态

#### **系统信息**

- **uname**:
  - **用途**: 显示系统信息。
  - **常用选项**:
    - `-a`: 显示所有信息（内核名称、主机名、内核版本、操作系统等）。
      - 示例: `uname -a`
    - `-s`: 显示内核名称。
    - `-r`: 显示内核版本。
    - `-m`: 显示硬件架构。

#### **用户活动**

- **w**:
  - **用途**: 显示当前登录用户及其活动。
  - **输出字段**:
    - `USER`: 登录用户名。
    - `TTY`: 用户使用的终端。
    - `FROM`: 用户登录的来源。
    - `IDLE`: 用户空闲时间。
    - `WHAT`: 用户当前执行的命令。
  - **示例**:
    - 查看当前用户活动: `w`
- **last**:
  - **用途**: 显示用户登录历史。
  - **输出字段**:
    - `USER`: 登录用户名。
    - `TTY`: 用户使用的终端。
    - `FROM`: 用户登录的来源。
    - `LOGIN`: 登录时间。
    - `LOGOUT`: 注销时间。
  - **示例**:
    - 查看登录历史: `last`
- **logname**:
  - **用途**: 显示当前登录用户的名称。
  - **示例**:
    - 显示当前用户: `logname`

#### **服务管理**

- **systemctl**:
  - **用途**: 管理系统服务。
  - **常用命令**:
    - 启动服务: `sudo systemctl start service_name`
    - 停止服务: `sudo systemctl stop service_name`
    - 重启服务: `sudo systemctl restart service_name`
    - 查看服务状态: `sudo systemctl status service_name`
    - 启用开机自启动: `sudo systemctl enable service_name`
    - 禁用开机自启动: `sudo systemctl disable service_name`

#### **系统启动与关闭**

- **shutdown**:
  - **用途**: 关闭或重启系统。
  - **常用选项**:
    - `-h`: 关闭系统。
      - 示例: `sudo shutdown -h now`（立即关机）
    - `-r`: 重启系统。
      - 示例: `sudo shutdown -r +10`（10分钟后重启）
    - `-c`: 取消计划中的关机或重启。
      - 示例: `sudo shutdown -c`
- **reboot**:
  - **用途**: 重启系统。
  - **示例**:
    - 立即重启: `sudo reboot`
- **halt**:
  - **用途**: 停止系统。
  - **示例**:
    - 立即停止: `sudo halt`

#### **终端操作**

- **clear**:
  - **用途**: 清屏。
  - **示例**:
    - 清空终端: `clear`
- **login**:
  - **用途**: 登录系统。
  - **示例**:
    - 登录: `login`
- **logout**:
  - **用途**: 注销当前会话。
  - **示例**:
    - 注销: `logout`

## 磁盘空间管理

#### **磁盘使用情况**

- **df (Disk Free)**:
  - **用途**: 显示磁盘空间使用情况。
  - **常用选项**:
    - `-h`: 以人类可读的格式显示（如KB、MB、GB）。
      - 示例: `df -h`
    - `-T`: 显示文件系统类型。
      - 示例: `df -T`
    - `-i`: 显示inode使用情况。
      - 示例: `df -i`
- **du (Disk Usage)**:
  - **用途**: 显示目录或文件的磁盘使用情况。
  - **常用选项**:
    - `-h`: 以人类可读的格式显示。
      - 示例: `du -h /path/to/dir`
    - `-s`: 显示总大小，不显示子目录。
      - 示例: `du -sh /path/to/dir`
    - `--max-depth=N`: 显示指定层级的目录大小。
      - 示例: `du -h --max-depth=1 /path/to/dir`
- **stat**:
  - **用途**: 显示文件或文件系统的状态信息。
  - **示例**:
    - 查看文件信息: `stat file.txt`
    - 查看文件系统信息: `stat -f /path/to/dir`

#### **文件系统挂载与卸载**

- **mount**:
  - **用途**: 挂载文件系统。
  - **示例**:
    - 挂载设备: `sudo mount /dev/sdb1 /mnt`
    - 查看已挂载的文件系统: `mount`
  - **常用选项**:
    - `-t`: 指定文件系统类型（如`ext4`, `ntfs`）。
      - 示例: `sudo mount -t ext4 /dev/sdb1 /mnt`
- **umount**:
  - **用途**: 卸载文件系统。
  - **示例**:
    - 卸载设备: `sudo umount /mnt`
  - **注意**: 卸载前确保文件系统未被使用。

#### **磁盘配额管理**

- **quota**:
  - **用途**: 显示磁盘配额信息。
  - **示例**:
    - 查看用户配额: `quota -u username`
    - 查看组配额: `quota -g groupname`
- **quotacheck**:
  - **用途**: 检查磁盘配额。
  - **示例**:
    - 检查配额: `sudo quotacheck -avug`
  - **常用选项**:
    - `-a`: 检查所有文件系统。
    - `-v`: 显示详细信息。
    - `-u`: 检查用户配额。
    - `-g`: 检查组配额。
- **quotaon**:
  - **用途**: 启用磁盘配额。
  - **示例**:
    - 启用配额: `sudo quotaon -avug`
- **quotaoff**:
  - **用途**: 禁用磁盘配额。
  - **示例**:
    - 禁用配额: `sudo quotaoff -avug`

#### **符号链接树**

- **lndir**:
  - **用途**: 创建目录的符号链接树。
  - **示例**:
    - 创建符号链接树: `lndir /path/to/source /path/to/destination`

## Docker

#### **1. 基本命令**

- **查看 Docker 版本**:
  ```bash
  docker version
  ```

- **查看 Docker 系统信息**:
  ```bash
  docker info
  ```

---

#### **2. 镜像管理**

- **拉取镜像**:
  ```bash
  docker pull <image_name>:<tag>
  ```
  示例:
  ```bash
  docker pull ubuntu:20.04
  ```

- **查看本地镜像**:
  ```bash
  docker images
  ```

- **删除镜像**:
  ```bash
  docker rmi <image_name>:<tag>
  ```
  示例:
  ```bash
  docker rmi ubuntu:20.04
  ```

- **构建镜像**:
  ```bash
  docker build -t <image_name>:<tag> .
  ```
  示例:
  ```bash
  docker build -t my-app:1.0 .
  ```

- **推送镜像到仓库**:
  ```bash
  docker push <image_name>:<tag>
  ```
  示例:
  ```bash
  docker push my-app:1.0
  ```

---

#### **3. 容器管理**

- **运行容器**:
  ```bash
  docker run [OPTIONS] <image_name>:<tag>
  ```
  常用选项:
  - `-d`: 后台运行容器。
  - `-it`: 交互式运行容器。
  - `--name`: 指定容器名称。
  - `-p`: 端口映射（`host_port:container_port`）。
  - `-v`: 挂载卷（`host_dir:container_dir`）。
  - `--rm`: 容器停止后自动删除。
  - `--env` 或 `-e`: 设置环境变量。

  示例:
  ```bash
  docker run -d -p 8080:80 --name my-container my-app:1.0
  ```

- **查看运行中的容器**:
  ```bash
  docker ps
  ```

- **查看所有容器（包括停止的）**:
  ```bash
  docker ps -a
  ```

- **停止容器**:
  ```bash
  docker stop <container_id_or_name>
  ```
  示例:
  ```bash
  docker stop my-container
  ```

- **启动已停止的容器**:
  ```bash
  docker start <container_id_or_name>
  ```

- **重启容器**:
  ```bash
  docker restart <container_id_or_name>
  ```

- **删除容器**:
  ```bash
  docker rm <container_id_or_name>
  ```
  示例:
  ```bash
  docker rm my-container
  ```

- **进入运行中的容器**:
  ```bash
  docker exec -it <container_id_or_name> /bin/bash
  ```
  示例:
  ```bash
  docker exec -it my-container /bin/bash
  ```

- **查看容器日志**:
  ```bash
  docker logs <container_id_or_name>
  ```

- **查看容器详细信息**:
  ```bash
  docker inspect <container_id_or_name>
  ```

---

#### **4. 网络管理**

- **查看网络列表**:
  ```bash
  docker network ls
  ```

- **创建网络**:
  ```bash
  docker network create <network_name>
  ```

- **查看网络详细信息**:
  ```bash
  docker network inspect <network_name>
  ```

- **删除网络**:
  ```bash
  docker network rm <network_name>
  ```

---

#### **5. 数据卷管理**

- **创建数据卷**:
  ```bash
  docker volume create <volume_name>
  ```

- **查看数据卷列表**:
  ```bash
  docker volume ls
  ```

- **查看数据卷详细信息**:
  ```bash
  docker volume inspect <volume_name>
  ```

- **删除数据卷**:
  ```bash
  docker volume rm <volume_name>
  ```

---

#### **6. Docker Compose**

- **启动服务**:
  ```bash
  docker-compose up
  ```
  后台启动:
  ```bash
  docker-compose up -d
  ```

- **停止服务**:
  ```bash
  docker-compose down
  ```

- **查看服务状态**:
  ```bash
  docker-compose ps
  ```

- **查看服务日志**:
  ```bash
  docker-compose logs
  ```

- **构建镜像并启动服务**:
  ```bash
  docker-compose up --build
  ```

---

#### **7. 其他常用命令**

- **清理未使用的镜像、容器、网络和数据卷**:
  ```bash
  docker system prune
  ```

- **清理所有未使用的资源（包括未使用的镜像）**:
  ```bash
  docker system prune -a
  ```

- **查看 Docker 磁盘使用情况**:
  ```bash
  docker system df
  ```

## Linux 网络进阶

#### **1. 基础概念**

- **以太网**: 用于局域网（LAN）的计算机网络技术。
- **MAC 地址**: 网络接口的唯一标识符，如 `08:00:27:d4:45:68`。
- **TCP/IP**: 互联网协议套件，包含 TCP 和 IP 协议。
- **IP 地址**: 互联网协议地址，如 `10.0.2.15`。
- **ICMP**: 互联网控制消息协议，用于网络诊断（如 `ping`）。
- **TCP**: 传输控制协议，可靠连接（如 SSH、HTTP）。
- **UDP**: 用户数据报协议，无连接（如 DNS）。
- **端口**: 通信端点，如 `80`（HTTP）、`443`（HTTPS）。
- **子网掩码**: 用于划分 IP 网络，如 `/24` 或 `255.255.255.0`。
- **路由**: 选择路径发送网络流量。
- **网关**: 连接不同网络的节点（通常是路由器）。
- **网络接口**: 处理网络任务的硬件和软件组合。

#### **2. 基本工具**

##### **2.1 ifconfig**

- **用途**: 配置和显示网络接口信息。
- **示例**:
  ```bash
  ifconfig eth0
  ```
  - 显示 `eth0` 接口的 IP 地址、MAC 地址、子网掩码等。

##### **2.2 netstat**

- **用途**: 查看网络连接、路由表、接口统计信息。
- **示例**:
  ```bash
  netstat -tuln
  ```
  - 显示所有监听端口。

##### **2.3 ip**

- **用途**: 强大的网络配置工具，替代 `ifconfig` 和 `route`。
- **示例**:
  ```bash
  ip addr show
  ```
  - 显示所有网络接口的详细信息。

##### **2.4 ss**

- **用途**: 显示套接字统计信息，比 `netstat` 更高效。
- **示例**:
  ```bash
  ss -tuln
  ```
  - 显示所有监听端口。

##### **2.5 route**

- **用途**: 查看和配置路由表。
- **示例**:
  ```bash
  route -n
  ```
  - 显示路由表。

#### **3. 防火墙**

##### **3.1 UFW (Uncomplicated Firewall)**

- **用途**: 简化 `iptables` 配置，适合初学者。
- **常用命令**:
  - 启用 UFW:
    ```bash
    sudo ufw enable
    ```
  - 允许 SSH:
    ```bash
    sudo ufw allow ssh
    ```
  - 允许特定端口:
    ```bash
    sudo ufw allow 80/tcp
    ```
  - 查看状态:
    ```bash
    sudo ufw status
    ```

##### **3.2 Firewalld**

- **用途**: 动态管理防火墙规则，支持区域和服务。
- **常用命令**:
  - 启动 Firewalld:
    ```bash
    sudo systemctl start firewalld
    ```
  - 允许 HTTP 服务:
    ```bash
    sudo firewall-cmd --add-service=http --permanent
    ```
  - 允许特定端口:
    ```bash
    sudo firewall-cmd --add-port=8080/tcp --permanent
    ```
  - 重新加载配置:
    ```bash
    sudo firewall-cmd --reload
    ```

##### **3.3 iptables**

- **用途**: 强大的防火墙工具，直接操作内核的 Netfilter。
- **常用命令**:
  - 允许 SSH:
    ```bash
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    ```
  - 阻止特定 IP:
    ```bash
    iptables -A INPUT -s 192.168.1.100 -j DROP
    ```
  - 保存规则:
    ```bash
    iptables-save > /etc/iptables/rules.v4
    ```
