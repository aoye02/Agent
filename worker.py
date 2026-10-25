import asyncio
from PySide6.QtCore import QThread, Signal
import traceback  # ★ 引入追踪模块

class AgentWorker(QThread):
    chunk_received = Signal(str)
    error_occurred = Signal(str) # ★ 新增错误信号
    finished_stream = Signal()

    # ★ 构造参数改回真实的 agent, text, conv_id
    def __init__(self, agent, text, conv_id):
        super().__init__()
        self.agent = agent
        self.text = text
        self.conv_id = conv_id

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def _run():
            try:
                # ★ 真实调用流式生成器
                async for chunk in self.agent.ask(self.text, self.conv_id):
                    self.chunk_received.emit(chunk)
            except Exception as e:
                # 如果底层 MCP 或 SQLite 报错，打印详细堆栈，并通知 UI
                error_detail = traceback.format_exc()
                print("\n【!!! 后台线程死因 !!!】\n", error_detail)
                self.error_occurred.emit(str(e))
            finally:
                self.finished_stream.emit()

        loop.run_until_complete(_run())
        loop.close()