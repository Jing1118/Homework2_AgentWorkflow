from workflow.base_agent import BaseAgent

class TitleOptimizerAgent(BaseAgent):
    """
    【扩展示例】标题优化Agent
    职责：对生成的文案优化标题，生成3个爆款标题备选
    证明：新增Agent只需继承BaseAgent、实现run方法，无需修改引擎核心代码
    """
    def __init__(self):
        super().__init__("标题优化Agent")

    def run(self, context: dict) -> dict:
        # 从共享状态读取文案初稿
        draft_content = context.get("draft_content", "")
        user_topic = context.get("user_topic", "")
        
        if not draft_content:
            raise ValueError("未收到文案内容，无法优化标题")

        # 构造提示词
        prompt = f"""
        你是小红书爆款标题专家，请根据下面的文案内容，生成3个不同风格的爆款标题。
        主题：{user_topic}
        文案内容：
        {draft_content}

        要求：
        1. 第一个标题：痛点共鸣型
        2. 第二个标题：效果反差型
        3. 第三个标题：干货安利型
        4. 每个标题控制在20字以内,带emoji
        只输出3个标题,不要多余解释。
        """

        # 调用大模型
        optimized_titles = self.call_llm(prompt)

        # 把结果写回共享状态
        context["optimized_titles"] = optimized_titles
        context["current_step"] = "标题优化完成"

        return context
