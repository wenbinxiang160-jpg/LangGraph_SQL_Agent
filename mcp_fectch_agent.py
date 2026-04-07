import asyncio
import sys
from langchain_classic.agents import create_react_agent, AgentExecutor
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from llm import llm
from langchain_core.prompts import PromptTemplate


async def run_fetch_agent(question: str) -> str:
    # 1. 启动 MCP fetch 服务，自动发现它提供的工具
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server_fetch"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. 自动发现 MCP 服务提供的所有工具
            tools = await load_mcp_tools(session)
            print(f">>> 发现的 MCP 工具: {[t.name for t in tools]}")
            # 输出类似: ['fetch']

            # 3. 让 Agent 使用这些工具回答问题
            prompt = PromptTemplate.from_template("""
            你是一个网页内容助手。你必须严格按照以下格式回答问题：

Thought: 你应该思考接下来要做什么。
Action: 调用的工具名称，必须是 [{tool_names}] 中的一个。
Action Input: 工具的输入参数。
Observation: 工具返回的结果（你不需要写这一行，系统会自动填充）。
... (这个 Thought/Action/Action Input/Observation 循环可以重复)
Thought: 我现在知道最终答案了。
Final Answer: 最终的总结结果。

注意：严禁输出任何多余的解释、开场白或 Markdown 代码块。

工具列表:
{tools}

用户问题: {input}

{agent_scratchpad}
            """)

            agent = create_react_agent(llm, tools, prompt)
            executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

            result = await executor.ainvoke({"input": question})
            return result["output"]


def fetch_webpage(question: str) -> str:
    """对外暴露的同步调用入口"""
    return asyncio.run(run_fetch_agent(question))


if __name__ == "__main__":
    # 测试
    result = fetch_webpage(
        "帮我抓取 https://www.msn.cn/zh-cn/news/other/%E5%91%A8%E6%B6%A6%E5%8F%91%E6%A2%81%E5%AE%B6%E8%BE%89%E5%87%BA%E5%B1%B1-%E9%98%B5%E5%AE%B9%E7%82%B8%E8%A3%82-%E8%BF%99%E6%B8%AF%E7%89%87%E6%8B%BF%E4%B8%8B30%E4%BA%BF%E7%A5%A8%E6%88%BF%E4%B8%8D%E6%98%AF%E6%B2%A1%E5%8F%AF%E8%83%BD/ar-AA1ZZsiz?ocid=BingNewsSerp 的内容并总结")
    print(result)
