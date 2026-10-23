from workflow.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """规划Agent:接收主题,生成文案大纲、核心卖点、目标人群"""
    def __init__(self):
        super().__init__("规划Agent")

    def run(self, context: dict) -> dict:
        # 从共享状态里取出用户输入的主题
        user_topic = context.get("user_topic", "")
        if not user_topic:
            raise ValueError("用户未输入主题，无法规划")

        # 构造提示词，让大模型生成规划
        prompt = f"""
        你是专业的小红书内容策划师，请针对主题「{user_topic}」,生成种草文案的规划方案,严格按下面3部分输出:
        1. 目标人群：明确这篇文案写给谁看
        2. 核心卖点:列出3个最打动用户的产品亮点
        3. 文案大纲：列出文案的结构框架（开头、正文、结尾分别写什么）
        
        输出要简洁清晰，不要多余废话。
        """

        # 调用大模型，拿到结果
        plan_result = self.call_llm(prompt)
        
        # 把结果写回共享状态，传给下一个Agent
        context["plan_result"] = plan_result
        context["current_step"] = "规划完成"
        
        return context
