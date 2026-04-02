# SQL Agent 周报助手 🚀

这是一个基于 LangChain 和 DeepSeek 的智能化数据库助手。

## 功能特性
- **自然语言查库**：直接输入中文，Agent 自动生成 SQL 并执行。
- **自动周报生成**：根据数据库销售数据，生成 PDF 格式周报。
- **邮件自动发送**：集成 SMTP 协议，一键送达邮箱。

## 环境要求
- Python 3.12 (推荐)
- MySQL 8.0+

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `.env` 文件（包含 API_KEY 和 DATABASE_URL）
3. 运行 `task_agent.py`
