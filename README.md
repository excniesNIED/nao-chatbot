# nao-chatbot

## 项目简介
基于NoneBot框架开发的中文聊天机器人，支持QQ平台，提供自动问答、AI对话集成、消息处理等核心功能。

## 功能特性
- ✅ JSON配置化问答系统（支持关键词/模糊匹配）
- 🤖 集成OpenAI/Gemini大模型智能对话
- 🔄 消息去重/打断/戳一戳响应机制
- 🌐 多平台适配（NoneBot全平台支持）

## 技术架构
- **核心框架**：NoneBot2 + Python3.8+
- **数据存储**：JSON配置驱动（custom/internal/outer目录）
- **AI引擎**：OpenAI API + Google Gemini API
- **设计模式**：策略模式（响应策略）+ 观察者模式（事件监听）

## 快速开始
```bash
# 安装依赖
pip install nonebot2
pip install -e nonebot-plugin-kawaii-robot
pip install -e nonebot-plugin-openai

# 启动服务
nonebot run
```

## 插件说明
1. **nonebot-plugin-kawaii-robot** - 核心对话逻辑
   - `custom/`：自定义响应配置（_hello.json/_poke.json）
   - `qa.json`：问答知识库
   - `utils.py`：工具函数库

2. **nonebot-plugin-openai** - AI对话扩展
   - 支持OpenAI和Gemini双引擎
   - 配置文件：openai_config.ini/gemini_config.ini

## 文档导航
- [安装指南](installation.md)
- [插件配置](plugins.md)
- [问答示例](Q&A.md)
- [代码规范](CONTRIBUTING.md)