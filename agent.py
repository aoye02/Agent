import os
from langchain_openai import ChatOpenAI
# 这两个是智谱的

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


class MyAgent:
    """智能体封装：只管"问问题、拿回答" """

    def __init__(self):
        # model = ChatDeepSeek(model="deepseek-chat")
        self.model = ChatOpenAI(
            model="glm-5.3-flash",
            api_key=os.getenv("ZHIPU_API_KEY"),
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )# 智谱版ai
        self.checkpointer = InMemorySaver()
        self.agent = None
    async def setup(self):         # ← 异步方法，单独拆出来
        """异步初始化：连接 MCP，拿工具，创建 agent"""
        client = MultiServerMCPClient({
            "filesystem": {
                "command": "node",
                "args": [
                    "D:/QT/Agent/My_Agent/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js",
                    "C:/Users/Hasee/Desktop/新建文件夹"
                ],
                "transport": "stdio"
            },
            "weather": {
                  "command": "node",
                  "args": ["D:/QT/Agent/My_Agent/node_modules/weather-open-meteo-mcp/build/index.js"],
                  "transport": "stdio"
            },
            # "duckduckgo": {
            #     "command": "uvx",
            #     "args": ["duckduckgo-mcp-server"],
            #     "transport": "stdio"
            # },
            "tavily": {
                "command": "npx",
                "args": ["-y", "tavily-mcp@0.1.4"],
                "env": {
                    "TAVILY_API_KEY": "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"
                },
                "transport": "stdio"
            }
        })
        tools = await client.get_tools() # 此时智能体有了 read_file 等工具
        self.agent = create_agent(
            model=self.model,
            tools=tools,
            checkpointer=self.checkpointer,
        )
    async def ask(self, question: str) -> str:
        """输入问题，返回回答"""
        result = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": question}]},
            config={"configurable": {"thread_id": "1"}},
        )
        return result["messages"][-1].content