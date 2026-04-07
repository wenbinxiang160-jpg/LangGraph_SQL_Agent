from agent_state import AgentState
from llm import llm


def report_agent(state: AgentState) -> AgentState:
    prompt = f"""
    生成一份数据分析报告，格式如下：

    ## 分析结论
    {state['analysis']}

    ## 数据明细
    （把 {state['query_result']} 整理成表格形式）

    ## 溯源 SQL
```sql
    {state['sql']}
```
    """
    report = llm.invoke(prompt).content
    print(f"report:{report}")
    return {"report": report}