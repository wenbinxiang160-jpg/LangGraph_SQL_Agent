
# 项目名

基于 LangGraph 构建的多 Agent 协作数据分析平台。⽤⼾以⾃然语⾔提问，系统⾃动编排 SQL ⽣成、数据查询、趋势分析与报告⽣成四个阶段，输出结构化分析报告并附带溯源 SQL，实现从⾃然语⾔到数据洞察的完整闭环。

## 项目架构图
# AgentState 定义 ├── llm.py            
# LLM 初始化 ├── agents/ │   ├── sql_agent.py      
# SQL Agent 类 │   ├── analyst_agent.py  
# Analyst Agent 类 │   ├── report_agent.py   
# Report Agent 类 │   └── supervisor.py     
# Supervisor 类 ├── graph.py          
# LangGraph 组装 └── app.py            
# Streamlit 入口
## 快速启动
streamlit run app.py       

