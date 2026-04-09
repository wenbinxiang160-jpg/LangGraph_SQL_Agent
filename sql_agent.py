from sqlalchemy import text

from agent_state import AgentState
from dbconfig import engine

from llm import llm



SQL_PROMPT = """你是 MySQL 专家。
当前问题涉及的表结构：
{schema_context}
依据上述涉及得表结构输出sql语句满足以下3点规则
规则：
1. 只生成 SELECT 语句
2. 必须使用聚合函数，结果加 LIMIT
3. 只输出 SQL

"""

def sql_agent(state: AgentState) -> AgentState:
    # 1. 让 LLM 生成 SQL
    sql = llm.invoke(SQL_PROMPT.format(schema_context=state["schema_context"])).content.strip()

    # 2. 安全检查（面试可以提这个点）
    if any(kw in sql.upper() for kw in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        return {"sql": sql, "query_result": [{"error": "危险操作被拦截"}]}

    # 3. 执行 SQL
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result.fetchall()]
            print(f"sql: {sql}, query_result: {rows}")
        return {"sql": sql, "query_result": rows}
    except Exception as e:
        # SQL 出错，告诉 Supervisor 重试（面试可以讲这个容错机制）
        return {"sql": sql, "query_result": [{"error": str(e)}]}


if __name__ == '__main__':
    state = {
        "question": "哪个商家的创建时间最晚？",
        "sql": "",
        "query_result": [],
        "analysis": "",
        "report": "",
        "next": ""
    }
    result = sql_agent(state=state)
    print("生成的 SQL:", result["sql"])
    print("查询结果:", result["query_result"])
