
### LangGraph_SQL_Agent

基于 LangGraph 构建的多 Agent 协作数据分析平台。⽤⼾以⾃然语⾔提问，系统⾃动编排 SQL ⽣成、数据查询、趋势分析与报告⽣成四个阶段，输出结构化分析报告并附带溯源 SQL，实现从⾃然语⾔到数据洞察的完整闭环。

### 项目架构图
#### AgentState 定义 ├── agent_state.py            
#### LLM 初始化 ├── llm.py      
#### SQL Agent 类 │   ├── sql_agent.py  
#### Analyst Agent 类 ├── analyst_agent.py   
#### Report Agent 类 ├── report_agent.py     
#### Supervisor 类 ├── graph.py          
#### LangGraph 组装 └──  graph.py           
#### Streamlit 入口
#### mcp测试 ├──mcp_fetch_agent.py
## 快速启动
streamlit run app.py   

## 运行展示
<img width="1277" height="803" alt="image" src="https://github.com/user-attachments/assets/40c1ec79-adbf-499f-8206-014ff15b679c" />
<img width="962" height="1276" alt="image" src="https://github.com/user-attachments/assets/4a92a039-ee48-48c3-94a6-7f7fec7e31a1" />

## 拦截展示
<img width="1912" height="948" alt="image" src="https://github.com/user-attachments/assets/d411bd46-40ef-477f-b2fa-3b86a0f4eb19" />



