from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import QSizePolicy

class Sidebar:
    def __init__(self, ui, main_window, settings_page):
        self.ui = ui
        self.main = main_window
        self.settings_page = settings_page
        self.settings = QSettings("MyCompany", "MyAgent")
        # 点用户区 → 设置
        self.ui.userArea.mousePressEvent = self.open_settings
        self.ui.userArea.setMouseTracking(True)     # 支持 hover

    def set_username(self, username):
        """登录后调用：设置用户 + 加载历史"""
        self.ui.username.setText(username)

    def open_settings(self, event):
        """点用户区 → 切到设置页"""
        self.settings_page.load()                   # 加载用户信息
        self.ui.stackedWidget.setCurrentIndex(1)

    def update_sidebar_avatar(self,avatar_path=None):
        """更新 sidebar 底部头像。不传路径就从 QSettings 读"""
        if not hasattr(self.ui, "avatar"):
            return

        # 如果没传路径，从 QSettings 读
        if avatar_path is None:
            avatar_path = self.settings_page.settings.value("avatar", "")

        if not avatar_path:
            return

        self.settings_page.apply_avatar(
            self.ui.avatar, avatar_path, size=40
        )

