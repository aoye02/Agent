from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class Bubble(QWidget):
    """聊天气泡：可选中复制"""

    def __init__(self, text: str, is_user: bool = False, msg_id: int = None):
        super().__init__()
        self.msg_id = msg_id  # ★ 记住数据库 ID
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)    # 气泡外间距

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setStyleSheet("""
            background: %s;
            padding: 8px;
            border-radius: 8px;
            font-size: 13px;
        """% ("#DCF8C6" if is_user else "#F0F0F0")
        )

        if is_user:
            layout.addStretch()
            layout.addWidget(self.label)
        else:
            layout.addWidget(self.label)
            layout.addStretch()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # ★ 只调一次 adjust_width，不用重复写计算
        self.adjust_width()

    def update_text(self, text: str):
            """流式更新文本"""
            self.label.setText(text)
            # 重新算宽度（可选，长文本会到 600）
            self.adjust_width()

    def adjust_width(self):
        """根据文本宽度调整气泡宽度"""
        text = self.label.text()
        if not text:
            return

        metrics = self.label.fontMetrics()
        flat_text = text.replace("\n", "")
        total_width = metrics.horizontalAdvance(flat_text)

        MAX_WIDTH = 600
        PADDING = 16

        if total_width + PADDING < MAX_WIDTH:
            self.label.setFixedWidth(total_width + PADDING + 10)
        else:
            self.label.setFixedWidth(MAX_WIDTH)


class LoadingBubble(QWidget):
    """思考中的气泡"""

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel("正在思考...")
        self.label.setStyleSheet(
            "background: #F0F0F0; padding: 8px; border-radius: 8px;"
        )
        layout.addWidget(self.label)
        layout.addStretch()