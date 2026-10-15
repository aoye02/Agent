import math
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class Bubble(QWidget):
    """聊天气泡：可选中复制"""

    def __init__(self, text: str, is_user: bool = False):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)    # 气泡外间距

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setStyleSheet("""
            background: %s;
            padding: 8px;
            border-radius: 8px;
            font-size: 13px;
        """% ("#DCF8C6" if is_user else "#F0F0F0")
        )
        MAX_WIDTH = 600
        metrics = label.fontMetrics()
        flat_text = text.replace("\n", "")
        total_width = metrics.horizontalAdvance(flat_text)
        lines = math.ceil(total_width / MAX_WIDTH)   # 需要几行

        if lines <= 1:
            # 1 行 → 按内容
            label.setFixedWidth(total_width + 50)
        else:
            # 多行 → 固定 600
            label.setFixedWidth(MAX_WIDTH)

        print(f"total_width={total_width}, lines={lines}, label.width={label.width()}")

        if is_user:
            layout.addStretch()
            layout.addWidget(label)
        else:
            layout.addWidget(label)
            layout.addStretch()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


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