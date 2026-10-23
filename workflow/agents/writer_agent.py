from workflow.base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """写作Agent：接收规划结果，生成小红书风格的完整种草文案"""
    def __init__(self):
        super().__init__("写作Agent")

    def run(self, context: dict) -> dict:
        plan_result = context.get("plan_result", "")
        user_topic = context.get("user_topic", "")
        if not plan_result:
            raise ValueError("未收到规划结果，无法写作")

        # 检查是否是重写请求
        rewrite_count = context.get("rewrite_count", 0)
        rewrite_tip = ""
        if rewrite_count > 0:
            rewrite_tip = f"\n【警告】上次生成的文案字数太少，请务必扩充内容，字数一定要在300-500字之间！这是第{rewrite_count}次重写。"

        prompt = f"""
        你是资深小红书种草博主，根据下面的规划方案，写一篇完整的种草文案。
        主题：{user_topic}
        规划方案：
        {plan_result}
        {rewrite_tip}

        要求：
        1. 语气亲切接地气，像和闺蜜分享一样
        2. 开头要有吸引力,带合适的emoji
        3. 正文分点清晰，多用口语化表达
        4. 字数必须在300-500字之间
        5. 结尾带互动引导
        """

        draft_content = self.call_llm(prompt)
        
        context["draft_content"] = draft_content
        context["current_step"] = "写作完成"
        
        return context