# My Agent — 基于 LangGraph 的智能体助手

一个桌面端 AI 聊天助手，集成 MCP 工具调用、多会话管理、本地文件操作。

## 功能
- 💬 多轮对话（LangGraph + 智谱 GLM）
- 🛠 MCP 工具调用（Filesystem、DuckDuckGo 搜索、天气）
- 📁 多会话管理（SQLite 持久化）
- 🔐 用户登录（PBKDF2 密码哈希）
- 🎨 PySide6 桌面 UI

## 技术栈
- Python 3.12 / PySide6
- LangChain / LangGraph
- MCP（Model Context Protocol）
- SQLite

## 快速开始
1. 克隆项目
2. 安装依赖：`uv sync`
3. 配置 `.env`（参考 `.env.example`）
4. 运行：`python mainwindow.py`

## 项目结构
（简单列一下关键文件）

## License
MIT
