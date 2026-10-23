import requests
import os
from dotenv import load_dotenv

# 加载环境变量里的API Key
load_dotenv()

class BaseAgent:
    """所有Agent的基类，定义统一的接口和通用能力"""
    def __init__(self, name: str):
        self.name = name  # Agent的名字
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def call_llm(self, prompt: str) -> str:
        """通用方法：调用大模型，所有Agent都能用"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # 请求失败就抛出异常
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"[{self.name}] 调用大模型失败: {str(e)}")

    def run(self, context: dict) -> dict:
        """
        每个Agent必须实现的核心方法
        context：全流程共享的状态字典，Agent间通过它传递消息
        返回更新后的context
        """
        raise NotImplementedError("子类必须实现run方法")
