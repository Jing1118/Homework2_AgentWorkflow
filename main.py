from workflow.agents.planner_agent import PlannerAgent
from workflow.agents.writer_agent import WriterAgent
from workflow.agents.reviewer_agent import ReviewerAgent
from workflow.workflow_engine import WorkflowEngine
# from workflow.agents.title_optimizer_agent import TitleOptimizerAgent


if __name__ == "__main__":
    # 1. 定义用户输入（可以改成任意你想测试的主题）
    user_input = {
        "user_topic": "学生党平价防晒霜，防晒时间长，价格实惠"
    }

    # 2. 按顺序组装Agent（工作流的节点）
    agent_list = [
        PlannerAgent(),
        WriterAgent(),

        # TitleOptimizerAgent(),

        ReviewerAgent()
    ]

    # 3. 创建工作流引擎
    workflow = WorkflowEngine(agent_list)

    # 4. 运行工作流
    result = workflow.run(user_input)

    # 5. 输出最终结果
    print("\n" + "="*50)
    print("📝 最终生成的种草文案：")
    print("="*50)
    if result["status"] == "completed":
        print(result["final_content"])
    else:
        print(f"执行失败：{result.get('error_msg', '未知错误')}")

    # 6. 输出执行日志
    print("\n" + "="*50)
    print("📋 完整执行日志：")
    print("="*50)
    for log in workflow.get_logs():
        print(log)

    # 保存日志到本地文件
    workflow.save_logs_to_file()
