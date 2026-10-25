import os
from langchain_openai import ChatOpenAI
# 这两个是智谱的
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from memory import MemoryManager
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
        # ★ 摘要模型：用更便宜、更快的模型来做历史总结
        self.summary_model = ChatOpenAI(
            model="glm-5.3-flashx",
            api_key=os.getenv("ZHIPU_API_KEY"),
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        self.checkpointer = None
        self.agent = None
        self.memory = None
    async def setup(self, db):         # ← 异步方法，单独拆出来
        # ★ 换成这一行：纯内存状态机
        self.checkpointer = InMemorySaver()
        """异步初始化：连接 MCP，拿工具，创建 agent"""
        # ★ 初始化记忆管理器，把 db 和便宜的摘要模型传进去
        self.memory = MemoryManager(db, self.summary_model)
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
    async def ask(self, question: str, conv_id: int):
        """流式调用，拦截工具事件"""
        messages = self.memory.build_context(conv_id, question)

        # ★ 关键：stream_mode 直接传字符串 "messages"，不要传列表
        async for chunk in self.agent.astream(
            {"messages": messages},
            config={"configurable": {"thread_id": str(conv_id)}},
            stream_mode="messages",
        ):
            # 当 stream_mode 是字符串时，chunk 直接就是一个二元组
            if isinstance(chunk, tuple) and len(chunk) == 2:
                message_chunk, metadata = chunk
            else:
                message_chunk = chunk

            # 1. 拦截工具调用
            if hasattr(message_chunk, "tool_calls") and message_chunk.tool_calls:
                for tool_call in message_chunk.tool_calls:
                    tool_name = tool_call.get("name")
                    zh_name = {
                        "tavily_search": "全网搜索",
                        "get_weather": "查询天气",
                        "read_file": "读取文件",
                        "write_file": "写入文件",
                        "list_directory": "浏览文件夹",
                    }.get(tool_name, tool_name)

                    yield f"__TOOL__🔍 正在使用【{zh_name}】..."

            # 2. 正常的文本流式输出
            if hasattr(message_chunk, "content"):
                content = message_chunk.content
                if isinstance(content, str) and content:
                    yield content
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, str):
                            yield item
                        elif isinstance(item, dict) and item.get("type") == "text":
                            yield item.get("text", "")