from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import QTimer, Signal

class AutoScrollArea(QScrollArea):
    # ★ 新增：定义一个信号，用来通知外面“该加载历史了”
    reached_top = Signal()
    TOP_TOLERANCE = 10
    BOTTOM_TOLERANCE = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_user_at_bottom = True
        # ★ 兜底：监听滚动条数值变化（专门捕捉鼠标拖拽）
        self.verticalScrollBar().valueChanged.connect(self._on_scrollbar_changed)

    def _on_scrollbar_changed(self, value):
        """当用户直接拖拽滚动条到顶部时触发"""
        bar = self.verticalScrollBar()
        # 同样留出 10 像素的容错空间
        if value <= bar.minimum() + self.TOP_TOLERANCE:
            # 注意：这里直接发信号去加载
            self.reached_top.emit()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        bar = self.verticalScrollBar()

        # 1. 处理往上滑
        if event.angleDelta().y() > 0:
            self.is_user_at_bottom = False
            # ★ 只要在顶部往上拨滚轮，立刻发出信号！
            if bar.value() <= bar.minimum() + self.TOP_TOLERANCE:
                self.reached_top.emit()

        # 2. 处理往下滑
        elif event.angleDelta().y() < 0:
            if bar.maximum() - bar.value() < self.BOTTOM_TOLERANCE:
                self.is_user_at_bottom = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.is_user_at_bottom:
            QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())
        # self.is_user_at_bottom = True