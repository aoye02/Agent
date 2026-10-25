import asyncio
from PySide6.QtCore import Qt, QTimer, QEvent, QObject
from PySide6.QtWidgets import QVBoxLayout
from bubble import Bubble, LoadingBubble
from scrollarea import AutoScrollArea
from worker import AgentWorker
import time
class ChatPage(QObject):
    """对话页逻辑：气泡显示、发送消息、滚动"""
    def __init__(self, ui, main_window, db):
        super().__init__()
        self.ui = ui
        self.main = main_window
        self.db = db
        self.is_replying = False
        self.loading = None

        # 动态添加垂直布局
        self.chat_layout = self.ui.chatContainer.layout()
        if self.chat_layout is None:
            self.chat_layout = QVBoxLayout(self.ui.chatContainer)
        self.chat_layout.addStretch()

        # ★ 懒加载状态变量
        self._is_loading_more = False

        self.ui.chatScroll.reached_top.connect(self._load_older_messages)

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
        if self.ui.chatScroll.is_user_at_bottom:
            QTimer.singleShot(100, self.ui.chatScroll.scroll_to_bottom)

    def on_send(self):
        text = self.ui.inputLine.toPlainText().strip()
        if not text:
            return

        # 1. 禁用发送按钮
        self.ui.sendButton.setEnabled(False)
        self.is_replying = True

        # ★ 2. 恢复你原本的对话逻辑
        is_first_message = False
        if self.main.current_conv_id is None:
            self.main.current_conv_id = self.db.new_conversation(
                self.main.current_user, "新对话"
            )
            is_first_message = True
        else:
            if self.db.count_messages(self.main.current_conv_id) == 0:
                is_first_message = True

        # 存用户消息
        self.db.add_message(self.main.current_conv_id, "user", text)

        # 如果是第一条 → 更新标题
        if is_first_message:
            title = text[:10] + ("..." if len(text) > 10 else "")
            self.db.update_title(self.main.current_conv_id, title)
            QTimer.singleShot(10, self.main.refresh_history)

        # 3. 显示到 UI
        self.ui.chatScroll.is_user_at_bottom = True
        self.add_bubble(text, is_user=True)
        self.ui.inputLine.clear()

        # 4. 准备流式变量
        self.full_reply = ""
        self.ai_bubble = None
        self._last_scroll_time = 0

        self.loading = LoadingBubble()
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.loading)

        # ★ 5. 启动真实的 Worker（传入 agent 和 conv_id）
        self.worker = AgentWorker(self.main.agent, text, self.main.current_conv_id)
        self.worker.chunk_received.connect(self._on_chunk_received)
        self.worker.error_occurred.connect(self._on_stream_error) # 绑定错误信号
        self.worker.finished_stream.connect(self._on_stream_finished)
        self.worker.start()

    def _on_chunk_received(self, chunk):
        self._last_scroll_time = 0
        """主线程接收子线程的文字，并更新 UI"""
        if self.ai_bubble is None:
            self._destroy_loading()
            self.ai_bubble = Bubble("", is_user=False)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.ai_bubble)
            if self.ui.chatScroll.is_user_at_bottom:
                QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

        # 1. 拦截工具提示
        if chunk.startswith("__TOOL__"):
            tool_msg = chunk.replace("__TOOL__", "")
            self.ai_bubble.update_text(tool_msg)
            return

        # 2. 处理正常文字
        if not self.full_reply:
            self.ai_bubble.label.setText("")

        self.full_reply += chunk

        # 节流更新 UI
        now = time.time()
        if now - self._last_scroll_time > 0.1:
            self._last_scroll_time = now
            self.ai_bubble.update_text(self.full_reply)
            if self.ui.chatScroll.is_user_at_bottom:
                QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    def _on_stream_error(self, err_msg):
        print("流式出错:", err_msg)
        if getattr(self, "ai_bubble", None):
            self.ai_bubble.update_text(f"出错了：{err_msg}")

    def _on_stream_finished(self):
        """接收完毕，清理现场"""
        self._destroy_loading()

        if getattr(self, "full_reply", "") and self.main.current_conv_id:
            self.db.add_message(self.main.current_conv_id, "assistant", self.full_reply)

        if getattr(self, "ai_bubble", None):
            self.ai_bubble.update_text(self.full_reply)
            if self.ui.chatScroll.is_user_at_bottom:
                QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

        self.is_replying = False
        self.ui.sendButton.setEnabled(True)
        self.ui.inputLine.setFocus()
        self.ai_bubble = None

    # def on_send(self):
    #     """点击发送 / 按回车时执行"""
    #     # 1. 读用户输入
    #     text = self.ui.inputLine.toPlainText().strip()
    #     if not text:
    #         return

    #     # ⚠️ 禁用发送按钮 + 输入框，防止"连续发"
    #     self.ui.sendButton.setEnabled(False)
    #     self.is_replying = True          # ★ 标记"回复中"

    #     # 是否"刚建的新对话"（还没发过消息）
    #     is_first_message = False

    #     if self.main.current_conv_id is None:
    #         # 没有当前对话 → 建新对话
    #         self.main.current_conv_id = self.db.new_conversation(
    #             self.main.current_user, "新对话"
    #         )
    #         is_first_message = True
    #     else:
    #         # 已有对话，检查"是不是第一条消息"
    #         if self.db.count_messages(self.main.current_conv_id) == 0:
    #             is_first_message = True

    #     # 存用户消息
    #     self.db.add_message(self.main.current_conv_id, "user", text)

    #     # 如果是第一条 → 更新标题
    #     if is_first_message:
    #         title = text[:10] + ("..." if len(text) > 10 else "")
    #         self.db.update_title(self.main.current_conv_id, title)
    #         QTimer.singleShot(10, self.main.refresh_history)      # 刷新列表，标题变了

    #     self.ui.chatScroll.is_user_at_bottom = True   # ★ 发消息 = 想看最新
    #     # 2. 显示到对话区
    #     self.add_bubble(text, is_user=True)

    #     # 5. 清空输入框
    #     self.ui.inputLine.clear()
    #     # 原本的：asyncio.create_task(self._async_ask(text))
    #     # 替换成延迟 50 毫秒启动，把主线程彻底让出来
    #     QTimer.singleShot(50, lambda: asyncio.create_task(self._async_ask(text)))
    #     # asyncio.create_task(self._async_ask(text))

    def eventFilter(self, obj, event):
        """回车发送，Shift+回车换行；AI 回复中，回车无效"""
        if obj is self.ui.inputLine and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                # AI 空闲 → 正常逻辑
                if event.modifiers() & Qt.ShiftModifier:
                    return False        # Shift+回车 → 换行
                # ★ AI 正在回复 → 吞掉回车，什么也不做
                if self.is_replying:
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

    # async def _async_ask(self, text):
    #     """异步调 agent，结果回主线程显示"""
    #     if self.main.agent is None or self.main.agent.agent is None:
    #         self.add_bubble("智能体还在初始化，请稍等几秒再试…", is_user=False)
    #         self.is_replying = False
    #         self.ui.sendButton.setEnabled(True)
    #         self.ui.inputLine.setFocus()
    #         return

    #     # 加"思考中"气泡
    #     self.loading = LoadingBubble()
    #     self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.loading)
    #     if self.ui.chatScroll.is_user_at_bottom:
    #         QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    #     ai_bubble = None
    #     full_reply = ""
    #     self._last_scroll_time = 0

    #     try:
    #         conv_id = self.main.current_conv_id
    #         async for chunk in self.main.agent.ask(text, conv_id):
    #             # 1. 收到工具调用状态
    #             if chunk.startswith("__TOOL__"):
    #                 tool_msg = chunk.replace("__TOOL__", "")

    #                 # 如果没有 AI 气泡，把 loading 换成 AI 气泡
    #                 if ai_bubble is None:
    #                     self._destroy_loading()
    #                     ai_bubble = Bubble("", is_user=False)
    #                     self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_bubble)
    #                     if self.ui.chatScroll.is_user_at_bottom:
    #                         QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    #                 # 在气泡里显示提示
    #                 ai_bubble.update_text(tool_msg)
    #                 continue

    #             # 2. 收到正常的逐字文本流
    #             if ai_bubble is None:
    #                 self._destroy_loading()
    #                 ai_bubble = Bubble("", is_user=False)
    #                 self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_bubble)
    #                 if self.ui.chatScroll.is_user_at_bottom:
    #                     QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    #             # ★ 如果是第一段正文到来，说明工具跑完了，清空之前的工具提示文字
    #             if not full_reply:
    #                 ai_bubble.label.setText("")

    #             full_reply += chunk
    #             # ★ 必须加节流，每 0.1 秒才允许重绘和滚动一次
    #             now = time.time()
    #             if now - self._last_scroll_time > 0.1:
    #                 self._last_scroll_time = now
    #                 ai_bubble.update_text(full_reply)
    #                 if self.ui.chatScroll.is_user_at_bottom:
    #                     QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    #     except Exception as e:
    #         print("流式出错:", e)
    #         if ai_bubble is None:
    #             self._destroy_loading()
    #             ai_bubble = Bubble("", is_user=False)
    #             self.chat_layout.insertWidget(self.chat_layout.count() - 1, ai_bubble)
    #         ai_bubble.update_text(f"出错了：{e}")
    #     finally:
    #         # 3. 存数据库
    #         if full_reply:
    #             if self.main.current_conv_id:
    #                 self.db.add_message(self.main.current_conv_id, "assistant", full_reply)
    #             if ai_bubble is not None:
    #                 ai_bubble.update_text(full_reply)   # 保证最终文本完整
    #                 if self.ui.chatScroll.is_user_at_bottom:
    #                     QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    #         # 恢复状态
    #         self.is_replying = False
    #         self.ui.sendButton.setEnabled(True)
    #         self.ui.inputLine.setFocus()

    def _destroy_loading(self):
        """安全销毁加载气泡"""
        if self.loading is not None:
            try:
                self.loading.deleteLater()
            except RuntimeError:
                pass
            self.loading = None

    def load_conversation(self, conv_id):
        self.clear_chat_display()

        # 强制重置滚动状态
        self._is_loading_more = False
        self.ui.chatScroll.is_user_at_bottom = True

        messages = self.db.get_messages(conv_id, before_id=None, limit=15)
        for msg_id, role, content in messages:
            bubble = Bubble(content, is_user=(role == "user"), msg_id=msg_id)
            self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        self.chat_layout.activate()          # 催布局
        self.ui.chatContainer.updateGeometry()
        QTimer.singleShot(0, self.ui.chatScroll.scroll_to_bottom)

    def _load_older_messages(self):
        if self._is_loading_more:
            return
        self._is_loading_more = True

        first_item = self.chat_layout.itemAt(0)
        if not first_item or not first_item.widget():
            self._is_loading_more = False
            return
        anchor_bubble = first_item.widget()
        oldest_msg_id = anchor_bubble.msg_id

        older_messages = self.db.get_messages(
            self.main.current_conv_id, before_id=oldest_msg_id, limit=15)
        if not older_messages:
            self._is_loading_more = False
            return

        self.ui.chatScroll.is_user_at_bottom = False

        # ★ 用视口坐标系，不是 chatContainer
        viewport = self.ui.chatScroll.viewport()
        anchor_y_before = anchor_bubble.mapTo(
            viewport, anchor_bubble.rect().topLeft()).y()

        for msg_id, role, content in reversed(older_messages):
            bubble = Bubble(content, is_user=(role == "user"), msg_id=msg_id)
            self.chat_layout.insertWidget(0, bubble)

        bar = self.ui.chatScroll.verticalScrollBar()
        old_max = bar.maximum()

        def _restore(_min, new_max):
            if new_max <= old_max:
                return
            try:
                bar.rangeChanged.disconnect(_restore)
            except (RuntimeError, TypeError):
                pass
            try:
                self.chat_layout.activate()
                self.ui.chatContainer.updateGeometry()
                y_after = anchor_bubble.mapTo(
                    viewport, anchor_bubble.rect().topLeft()).y()
                bar.setValue(bar.value() + (y_after - anchor_y_before))
                self.ui.chatScroll.ensureWidgetVisible(anchor_bubble, 0, 0)
            finally:
                self._is_loading_more = False

        bar.rangeChanged.connect(_restore)

    def clear_chat_display(self):
        """清空对话区所有气泡"""
        while self.chat_layout.count() > 1:      # 保留最后的弹簧
            item = self.chat_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()