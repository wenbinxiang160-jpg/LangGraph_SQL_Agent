from llm import llm
from agent_state import AgentState


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



