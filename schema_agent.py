# 连接你的 MySQL（本地生活平台的库）
from sqlalchemy import create_engine, inspect

from agent_state import AgentState
from dbconfig import TABLE_NAMES, TABLE_DDL
from llm import llm



SCHEMA_LINKING_PROMPT = """
数据库有以下表：
{table_names}

用户问题：{question}

请判断回答这个问题需要用到哪些表，只输出表名列表，用逗号分隔，不要有其他内容。
例如：tb_shop,tb_voucher_order...
"""


def schema_agent(state: AgentState) -> AgentState:
    prompt = SCHEMA_LINKING_PROMPT.format(
        table_names="\n".join(TABLE_NAMES),
        question=state["question"]
    )
    result = llm.invoke(prompt).content.strip()

    # 解析 LLM 返回的表名列表
    selected_tables = [t.strip() for t in result.split(",")]

    # 只取相关表的 DDL 拼接进上下文
    relevant_ddl = "\n\n".join([
        TABLE_DDL[t] for t in selected_tables
        if t in TABLE_DDL
    ])
    print({"schema_context": relevant_ddl})
    return {"schema_context": relevant_ddl}


if __name__ == '__main__':
    state = {
        "question": "哪个商家的创建时间最晚？",
        "schema_context": "",
        "sql": "",
        "query_result": [],
        "analysis": "",
        "report": "",
        "next": ""
    }
    result = schema_agent(state=state)
    print("涉及表单:", result["schema_context"])
