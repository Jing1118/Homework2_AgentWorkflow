import time
import os
from typing import List
from workflow.base_agent import BaseAgent

class WorkflowEngine:
    """工作流编排引擎：负责管理Agent执行顺序、状态共享、日志记录、错误重试"""
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents  # 按顺序排列的Agent列表
        self.context = {}     # 全流程共享的状态字典（Agent通信的核心）
        self.logs = []        # 执行日志，用于追踪状态
        self.max_retry = 1    # 单步失败最大重试次数（错误恢复机制）

    def add_log(self, level: str, message: str):
        """记录执行日志"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)  # 同时打印到控制台

    def save_logs_to_file(self, log_dir: str = "logs"):
        """
        将执行日志保存到本地文件
        自动创建logs文件夹，文件名按时间生成，方便回溯历史执行记录
        """
        # 自动创建日志文件夹
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 按时间生成日志文件名
        file_name = time.strftime("workflow_%Y%m%d_%H%M%S.log", time.localtime())
        file_path = os.path.join(log_dir, file_name)

        # 写入日志
        with open(file_path, "w", encoding="utf-8") as f:
            for log in self.logs:
                f.write(log + "\n")
        
        self.add_log("INFO", f"执行日志已保存到文件: {file_path}")

    def run(self, initial_context: dict = None) -> dict:
        """
        启动工作流，按顺序执行所有Agent
        新增：单步耗时统计、失败自动重试、更细致的状态管理
        """
        # 初始化上下文
        if initial_context:
            self.context.update(initial_context)
        
        self.context["status"] = "running"
        self.context["step_durations"] = {}  # 记录每一步的执行耗时
        self.add_log("INFO", "工作流启动，开始执行")
        self.add_log("INFO", f"初始输入: {self.context.get('user_topic', '无')}")
        self.add_log("INFO", f"单步最大重试次数: {self.max_retry}")

                # 顺序执行每个Agent（核心：流程控制 + 重试机制 + 耗时统计）
        for index, agent in enumerate(self.agents):
            step_name = f"第{index+1}步_{agent.name}"
            start_time = time.time()
            retry_count = 0
            step_success = False

            self.add_log("INFO", f"第{index+1}步：开始执行 [{agent.name}]")

            while retry_count <= self.max_retry:
                try:
                    self.context = agent.run(self.context)
                    step_success = True
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count > self.max_retry:
                        self.context["status"] = "failed"
                        self.context["error_msg"] = str(e)
                        self.add_log("ERROR", f"[{agent.name}] 执行失败，已重试{self.max_retry}次，最终错误: {str(e)}")
                        self.add_log("ERROR", "工作流异常终止")
                        return self.context
                    
                    self.add_log("WARN", f"[{agent.name}] 执行失败，正在进行第{retry_count}次重试...")
                    time.sleep(1)

            # 条件分支与循环控制：如果当前是写作Agent，检查字数
            if agent.name == "写作Agent" and step_success:
                word_count = len(self.context.get("draft_content", ""))
                self.add_log("INFO", f"写作字数检测：当前生成 {word_count} 字")
                
                # 如果字数少于300，且重写次数小于2次，则触发循环重写
                if word_count < 300 and self.context.get("rewrite_count", 0) < 2:
                    self.context["rewrite_count"] = self.context.get("rewrite_count", 0) + 1
                    self.add_log("WARN", f"字数不达标（<300字），触发条件循环！第 {self.context['rewrite_count']} 次打回重写...")
                    
                    # 再次调用写作Agent
                    self.context = agent.run(self.context)
                    # 重新统计耗时
                    start_time = time.time()

            # 统计本步耗时
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.context["step_durations"][step_name] = duration

            if step_success:
                self.add_log("INFO", f"第{index+1}步：[{agent.name}] 执行完成，耗时 {duration} 秒")
                self.add_log("INFO", f"当前状态: {self.context.get('current_step', '未知')}")

        # 全部执行完成
        self.context["status"] = "completed"
        # 计算总耗时
        total_duration = round(sum(self.context["step_durations"].values()), 2)
        self.context["total_duration"] = total_duration
        
        self.add_log("INFO", f"工作流全部执行完成，总耗时 {total_duration} 秒")
        return self.context

    def get_logs(self) -> list:
        """获取全部执行日志"""
        return self.logs
