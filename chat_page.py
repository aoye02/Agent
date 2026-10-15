import asyncio
from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QKeyEvent
from bubble import Bubble, LoadingBubble
from agent import MyAgent
# from worker import AgentWorker      # 把 AgentWorker 也拆出去

class ChatPage(QObject):
    """对话页逻辑：气泡显示、发送消息、滚动"""
    def __init__(self, ui, main_window, db):
        super().__init__()
        self.ui = ui
        self.main = main_window
        self.db = db

        # self.worker = None
        self.loading = None

        # 动态添加垂直布局
        self.chat_layout = self.ui.chatContainer.layout()
        if self.chat_layout is None:
            self.chat_layout = QVBoxLayout(self.ui.chatContainer)
        self.chat_layout.addStretch()

        # ★ 输入框内容变化时，调整高度
        self.ui.inputLine.textChanged.connect(self.adjust_input_height)

        # 信号
        self.ui.sendButton.clicked.connect(self.on_send)
        self.ui.inputLine.installEventFilter(self)
        self.ui.inputLine.setStyleSheet("QTextEdit { font-size: 13px; }")
        # ★ 延迟调一次，让初始高度 = 20
        QTimer.singleShot(0, self.adjust_input_height)

    def add_bubble(self, text, is_user):
        """加一个气泡"""
        bubble = Bubble(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        # 用 QTimer.singleShot 延迟滚
        QTimer.singleShot(0, self.scroll_to_bottom)
        QTimer.singleShot(80, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """彻底滚到底"""
        self.chat_layout.activate()
        self.ui.chatContainer.updateGeometry()
        self.ui.chatScroll.updateGeometry()
        bar = self.ui.chatScroll.verticalScrollBar()
        bar.setValue(bar.maximum())         # 这段本身对

    def on_send(self):
        """点击发送 / 按回车时执行"""
        # 1. 读用户输入
        text = self.ui.inputLine.toPlainText().strip()
        if not text:
            return

        # ⚠️ 禁用发送按钮 + 输入框，防止"连续发"
        self.ui.sendButton.setEnabled(False)

        # 是否"刚建的新对话"（还没发过消息）
        is_first_message = False

        if self.main.current_conv_id is None:
            # 没有当前对话 → 建新对话
            self.main.current_conv_id = self.db.new_conversation(
                self.main.current_user, "新对话"
            )
            is_first_message = True
        else:
            # 已有对话，检查"是不是第一条消息"
            msgs = self.db.get_messages(self.main.current_conv_id)
            if len(msgs) == 0:
                is_first_message = True

        # 存用户消息
        self.db.add_message(self.main.current_conv_id, "user", text)

        # 如果是第一条 → 更新标题
        if is_first_message:
            title = text[:10] + ("..." if len(text) > 10 else "")
            self.db.update_title(self.main.current_conv_id, title)
            self.main.refresh_history()      # 刷新列表，标题变了

        # 2. 显示到对话区
        self.add_bubble(text, is_user=True)

        # 5. 清空输入框
        self.ui.inputLine.clear()

        # 加"思考中"气泡
        self.loading = LoadingBubble()
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.loading)

        asyncio.create_task(self._async_ask(text))

    def eventFilter(self, obj, event):
        """回车发送，Shift+回车换行；AI 回复中，回车无效"""
        if obj is self.ui.inputLine and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                # AI 空闲 → 正常逻辑
                if event.modifiers() & Qt.ShiftModifier:
                    return False        # Shift+回车 → 换行
                # ★ AI 正在回复 → 吞掉回车，什么也不做
                if self.loading is not None:
                    return True
                self.on_send()
                return True             # 回车 → 发送
        return False

    def adjust_input_height(self):
        """根据内容调整输入框高度，最小 20，最大 120"""
        doc = self.ui.inputLine.document()
        # 文档高度 = 内容高度（含边距）
        height = int(doc.size().height()) + 12      # +12 是边距/padding
        height = max(20, min(height, 120))          # 限制在 20~120
        self.ui.inputLine.setFixedHeight(height)

    async def _async_ask(self, text):
        """异步调 agent，结果回主线程显示"""
        if self.main.agent is None or self.main.agent.agent is None:
            self.on_reply("智能体还在初始化，请稍等几秒再试…")
            return
        reply = await self.main.agent.ask(text)   # ← 用主窗口的 agent
        self.on_reply(reply)

    def on_reply(self, reply):
        # 恢复按钮
        self.ui.sendButton.setEnabled(True)
        self.ui.inputLine.setFocus()      # 焦点回到输入框

        """后台线程完成后，回到主线程显示"""
        if self.loading:
            self.loading.deleteLater()
            self.loading = None
        # 存 AI 回复
        self.db.add_message(self.main.current_conv_id, "assistant", reply)
        self.add_bubble(reply, is_user=False)

    def load_conversation(self, conv_id):
        """加载某个对话的消息"""
        self.clear_chat_display()
        messages = self.db.get_messages(conv_id)
        for role, content in messages:
            self.add_bubble(content, is_user=(role == "user"))
        QTimer.singleShot(500, self.scroll_to_bottom)
        QTimer.singleShot(1500, self.scroll_to_bottom)

    def clear_chat_display(self):
        """清空对话区所有气泡"""
        while self.chat_layout.count() > 1:      # 保留最后的弹簧
            item = self.chat_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    # def close(self):
    #     """程序关闭前清理线程"""
    #     pass