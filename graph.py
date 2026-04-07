import agent_state

from llm import llm

SUPERVISOR_PROMPT = """你是一个数据分析任务的调度者。
根据当前任务状态，决定下一步该做什么。

当前状态：
- 用户问题：{question}
- SQL是否已生成：{has_sql}
- 数据是否已查询：{has_data}
- 分析是否完成：{has_analysis}
- 报告是否已生成：{has_report}

只能回答以下之一（不要有其他内容）：
- sql_agent    （需要生成并执行SQL）
- analyst      （SQL已执行，需要分析数据）
- report       （分析完成，需要生成报告）
- FINISH       （报告已完成，结束任务）
"""


def supervisor_agent(state: agent_state.AgentState) -> agent_state.AgentState:
    prompt = SUPERVISOR_PROMPT.format(
        question=state["question"],
        has_sql=bool(state.get("sql")),
        has_data=bool(state.get("query_result")),
        has_analysis=bool(state.get("analysis")),
        has_report=bool(state.get("report"))
    )
    next_step = llm.invoke(prompt).content.strip()
    print(f"next:{next_step}")
    return {"next": next_step}


if __name__ == '__main__':
    state = {
        "question": "哪个商家的创建时间最晚？",
        "sql": "SELECT `name` FROM `tb_shop` ORDER BY `create_time` DESC LIMIT 1",
        "query_result": [{'name': '星聚会KTV(拱墅区万达店)'}],
        "analysis": "星聚会KTV(拱墅区万达店)是创建时间最晚的商户",
        "report": "",
        "next": ""
    }
    result = supervisor_agent(state=state)
    print(result)  # 期望: {'next': 'analyst'}
