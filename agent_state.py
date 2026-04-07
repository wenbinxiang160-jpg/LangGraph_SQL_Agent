from typing import TypedDict, Annotated, Optional
import operator


class AgentState(TypedDict):
    question: str  # 用户原始问题
    sql: str  # SQL Agent 写的 SQL
    query_result: Optional[list]  # MySQL 执行结果
    analysis: str  # Analyst Agent 的分析
    report: str  # 最终报告
    next: str  # Supervisor 决定下一步去哪个 Agent


