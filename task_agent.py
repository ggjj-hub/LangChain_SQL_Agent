import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
import sys
print(f"当前使用的 Python 解释器路径: {sys.executable}")
print(f"当前使用的 Python 版本: {sys.version}")
# 1. 加载环境变量 (确保你的 .env 里有 API_KEY 和 DATABASE_URL)
load_dotenv()

# 2. 连接数据库
# 格式: mysql+pymysql://用户名:密码@localhost:3306/数据库名
db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"))

# 3. 初始化大模型 (这里以 DeepSeek 为例，性价比极高)
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0  # 设为0，让 AI 生成 SQL 时更严谨，不瞎编
)

# 4. 创建 SQL Agent
# 它会自动理解表结构，并把自然语言转成 SQL 执行
agent_executor = create_sql_agent(
    llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,  # 开启后，你能在控制台看到 AI 思考和写 SQL 的全过程
    max_iterations=15,  # 允许它多想几步
    handle_parsing_errors=True # 处理解析错误
)

# 5. 测试指令：生成周报数据
#prompt = "查询员工'张三'在本周（2026-03-30至今）的所有销售订单，汇总总金额，并列出前三条订单详情。"
prompt = """
你是公司的财务周报助手。请为员工'张三'生成本周（2026-03-30至今）的销售周报：
1. 统计销售总额和订单数量。
2. 列出金额最高的前三笔订单。
3. 结合 weekly_tasks 表，简述该员工本周的工作进展。
如果本周没有订单，请明确说明，但仍需汇总其工作任务进展。
"""

try:
    print("🚀 Agent 正在思考中...")
    response = agent_executor.invoke({"input": prompt})
    print("\n--- AI 生成的周报草稿 ---")
    print(response["output"])
except Exception as e:
    print(f"❌ 运行出错了: {e}")