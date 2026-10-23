from workflow.base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    """审校Agent：检查文案、优化表达、补充话题标签，输出终稿"""
    def __init__(self):
        super().__init__("审校Agent")

    def run(self, context: dict) -> dict:
        # 取出写作Agent生成的初稿
        draft_content = context.get("draft_content", "")
        user_topic = context.get("user_topic", "")
        if not draft_content:
            raise ValueError("未收到文案初稿，无法审校")

        # 构造提示词，审校优化
        prompt = f"""
        你是专业的小红书内容审校师，请对下面的种草文案进行优化：
        主题：{user_topic}
        待优化文案：
        {draft_content}

        优化要求：
        1. 修正错别字和不通顺的句子
        2. 优化语气，更有种草感和感染力
        3. 在文案末尾添加5个精准的小红书话题标签（#开头）
        4. 保留原文的核心内容和结构，不要大幅改写
        
        直接输出优化后的完整文案，不要多余说明。
        """

        # 调用大模型生成终稿
        final_content = self.call_llm(prompt)
        
        # 把最终结果写回共享状态
        context["final_content"] = final_content
        context["current_step"] = "审校完成"
        context["status"] = "success"
        
        return context
