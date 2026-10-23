import streamlit as st
from workflow.agents.planner_agent import PlannerAgent
from workflow.agents.writer_agent import WriterAgent
from workflow.agents.reviewer_agent import ReviewerAgent
from workflow.workflow_engine import WorkflowEngine

# 页面配置
st.set_page_config(page_title="多Agent文案生成工作流", page_icon="✍️", layout="wide")

st.title("多Agent协作小红书种草文案生成工作流")
st.markdown("基于**规划 -> 写作 -> 审校**流水线，支持**字数检测与自动重写循环**。")

# 输入区域
with st.form("input_form"):
    user_topic = st.text_input("请输入你想种草的产品主题：", 
                               value="学生党平价防晒霜，防晒时间长，价格实惠")
    submit_button = st.form_submit_button("🚀 启动工作流生成")

if submit_button:
    if not user_topic:
        st.error("请输入主题！")
    else:
        with st.spinner("工作流执行中，请稍候（涉及多次大模型调用，约需10-15秒）..."):
            # 初始化工作流
            user_input = {"user_topic": user_topic}
            agent_list = [
                PlannerAgent(),
                WriterAgent(),
                ReviewerAgent()
            ]
            workflow = WorkflowEngine(agent_list)
            
            # 运行
            result = workflow.run(user_input)
            
            # 保存日志
            workflow.save_logs_to_file()

        st.success("工作流执行完成！")
        
        # 分栏展示
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 最终生成的文案")
            if result["status"] == "completed":
                st.info(result["final_content"])
            else:
                st.error(f"执行失败：{result.get('error_msg')}")
                
        with col2:
            st.subheader("📋 执行日志与状态追踪")
            log_text = "\n".join(workflow.get_logs())
            st.text_area("执行详情", log_text, height=400)
            
            # 显示耗时状态
            st.write(f"⏱️ **总耗时**: {result.get('total_duration', 0)} 秒")
            st.write(f"🔄 **重写次数**: {result.get('rewrite_count', 0)} 次")