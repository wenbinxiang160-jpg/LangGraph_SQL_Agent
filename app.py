import streamlit as st

from start import run_query

st.set_page_config(page_title="运营数据智能助手", page_icon="🤖", layout="wide")
st.title("🤖 运营数据智能分析助手")
st.caption("基于 LangGraph 多 Agent 架构 | 数据来源：本地生活平台")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("📌 溯源 SQL"):
                st.code(msg["sql"], language="sql")

# 用户输入
if question := st.chat_input("例如：上个月销售额最高的商户是哪些？"):
    # 展示用户消息
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # 执行 Agent
    with st.chat_message("assistant"):
        with st.spinner("🔄 Agent 分析中..."):
            result = run_query(question)

        # 展示报告
        st.markdown(result["report"])

        # 溯源 SQL
        with st.expander("📌 溯源 SQL"):
            st.code(result["sql"], language="sql")

    # 存入历史
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["report"],
        "sql": result["sql"]
    })
