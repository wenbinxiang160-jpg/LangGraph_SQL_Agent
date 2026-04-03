from langgraph.graph.state import StateGraph, END

from AgentState import AgentState
from SQLAgent import sql_agent
from Supervisor import supervisor_agent
from analystAndReport import analyst_agent, report_agent

# 1. 创建 Graph
workflow = StateGraph(AgentState)

# 2. 注册所有节点
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("sql_agent", sql_agent)
workflow.add_node("analyst_agent", analyst_agent)
workflow.add_node("report_agent", report_agent)

# 3. 设置入口
workflow.set_entry_point("supervisor")

# 4. Supervisor 的条件边（核心路由逻辑）
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],
    {
        "sql_agent": "sql_agent",
        "analyst": "analyst_agent",
        "report": "report_agent",
        "FINISH": END
    }
)

# 5. 其他 Agent 完成后回到 Supervisor 再决策
workflow.add_edge("sql_agent", "supervisor")
workflow.add_edge("analyst_agent", "supervisor")
workflow.add_edge("report_agent", "supervisor")

# 6. 编译成可执行的 App
app = workflow.compile()


def run_query(question: str) -> dict:
    """对外暴露的统一调用入口"""
    return app.invoke({
        "question": question,
        "sql": "",
        "query_result": None,
        "analysis": "",
        "report": "",
        "next": ""
    }, config={"recursion_limit": 15})
