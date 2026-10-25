from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QListWidgetItem

class HistoryPage:
    def __init__(self, ui, main_window, db):
        self.ui = ui
        self.main = main_window
        self.db = db

        # 点"新建对话"
        self.ui.newChatBtn.clicked.connect(self.on_new_chat)
        # 点历史对话
        self.ui.historyList.itemClicked.connect(self.on_history_click)

    def load_history(self):
        """从数据库加载历史对话列表"""
        self.ui.historyList.clear()
        convs = self.db.get_conversations(self.main.current_user)
        for conv_id, title in convs:
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, conv_id)      # 存 ID
            self.ui.historyList.addItem(item)

    def on_new_chat(self):
        """新建对话"""
        self.main.chat_page.clear_chat_display()
        # 立即建新对话（在数据库里）
        self.main.current_conv_id = self.db.new_conversation(
            self.main.current_user, "新对话"
        )
        self.load_history()      # 刷新列表，新对话出现

    def on_history_click(self, item):
        """点历史对话，加载消息"""
        conv_id = item.data(Qt.UserRole)
        self.main.current_conv_id = conv_id
        QTimer.singleShot(10, lambda: self.main.chat_page.load_conversation(conv_id))