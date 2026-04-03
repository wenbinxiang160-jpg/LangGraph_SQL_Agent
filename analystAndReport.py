from llm import llm
from AgentState import AgentState


def analyst_agent(state: AgentState) -> AgentState:
    prompt = f"""
    用户问题：{state['question']}
    查询数据：{state['query_result']}

    请分析：1. 数据说明了什么 2. 有哪些值得关注的趋势或异常
    用简洁的中文回答，不超过200字。
    """
    analysis = llm.invoke(prompt).content
    print(f"analysis:{analysis}")
    return {"analysis": analysis}


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

