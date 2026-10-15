# This Python file uses the following encoding: utf-8
import sys
import asyncio
import qasync
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from ui_form import Ui_MainWindow
from agent import MyAgent
# from bubble import Bubble, LoadingBubble
from login import LoginDialog
from database import Database
from settings import SettingsPage
# from worker import AgentWorker
from sidebar import Sidebar
from history_page import HistoryPage
from chat_page import ChatPage

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
#     QT自动生成ui_form.py文件，打包前要自己新建一下ui_form.py

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.current_user = ""           # 登录后设置
        self.current_conv_id = None      # 当前对话 ID

        self.chat_page = ChatPage(self.ui, self, self.db)
        self.settings_page = SettingsPage(self.ui, self)    # ← settings 在 settings_page 里
        self.sidebar = Sidebar(self.ui, self, self.settings_page)
        self.history_page = HistoryPage(self.ui, self, self.db)
        self.agent = MyAgent()

    async def init_agent(self):
        """在事件循环启动后，异步初始化 MCP Agent"""
        try:
            await self.agent.setup()
            print("Agent 初始化完成")
            self.chat_page.on_reply("智能体初始化完成")
        except Exception as e:
            print(f"Agent 初始化失败: {e}")

    def set_user(self, username):
        """登录后调用：设置用户 + 加载历史"""
        self.current_user = username
        self.sidebar.set_username(username)
        self.sidebar.update_sidebar_avatar()
        self.history_page.load_history()

    def refresh_history(self):
        """给 chat_page 调用的刷新入口"""
        self.history_page.load_history()

    def update_avatar(self,avatar_path=None):
        self.sidebar.update_sidebar_avatar(avatar_path)

    def closeEvent(self, event):
        # self.chat_page.close()
        event.accept()   # 直接接受关闭，不管线程

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. 创建 qasync 事件循环，包装 Qt 的事件循环
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    # 先弹登录窗口
    login = LoginDialog()
    if login.exec() == QDialog.Accepted:
        widget = MainWindow()
        widget.set_user(login.username)
        widget.show()
        # 3. 关键：在事件循环里用 create_task 异步初始化 Agent
        #    这样 setup() 在后台跑，不会阻塞界面显示
        loop.create_task(widget.init_agent())

        # 4. 启动事件循环
        with loop:
            loop.run_forever()
        sys.exit(0)
    # 登录失败/取消 → 直接退出
