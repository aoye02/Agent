#本函数是双线程的子线程，现已不用，做学习用

# import asyncio
# from PySide6.QtCore import QThread, Signal

# class AgentWorker(QThread):
#     """后台线程：跑智能体调用"""
#     result_ready = Signal(str)      # 完成后发信号，带回复内容

#     def __init__(self, agent, question):
#         super().__init__()
#         self.agent = agent
#         self.question = question

#     def run(self):
#         # 在后台线程里调用（不卡界面）
#         reply = asyncio.run(self.agent.ask(self.question))
#         self.result_ready.emit(reply)   # 发信号给主线程