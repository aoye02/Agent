# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QSettings, Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtWidgets import QFileDialog, QMessageBox, QStyle, QSizePolicy
from password_utils import hash_password


class SettingsPage:
    """设置页逻辑：管用户设置、换头像、保存、返回"""

    def __init__(self, ui, main_window):
        self.ui = ui
        self.main = main_window          # 主窗口引用（用于切页）
        self.settings = QSettings("MyCompany", "MyAgent")

        self.init_ui()

    def init_ui(self):
        """初始化：连信号、设样式、加载数据"""
        # 1. 返回按钮（QToolButton）→ 回对话页
        icon = self.main.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowBack
        )
        self.ui.backBtn.setIcon(icon)
        self.ui.backBtn.setIconSize(QSize(20, 20))
        self.ui.backBtn.clicked.connect(self.go_back)

        # 2. 左侧列表 → 右侧切换
        self.ui.settingList.currentRowChanged.connect(
            self.ui.settingStack.setCurrentIndex
        )
        self.ui.settingList.setCurrentRow(0)

        # 3. 用户设置页按钮
        self.ui.changeAvatarBtn.clicked.connect(self.change_avatar)
        self.ui.saveUserBtn.clicked.connect(self.save_user_settings)
        self.ui.editInfoBtn.clicked.connect(self.enable_edit)

        # 4. 默认：用户名"只读"
        self.ui.nameInput.setReadOnly(True)

    # ========== 页面加载（每次进设置页时调） ==========
    def load(self):
        """进入设置页时，加载用户信息"""
        # 用户名
        username = self.settings.value("username", "")
        self.ui.nameInput.setText(username)

        # 头像
        avatar_path = self.settings.value("avatar", "")
        if avatar_path:
            self.set_circular_avatar(avatar_path)

        # 恢复"只读"
        self.ui.nameInput.setReadOnly(True)

    # ========== 返回对话页 ==========
    def go_back(self):
        """返回对话页"""
        self.main.ui.stackedWidget.setCurrentIndex(0)

    # ========== 换头像 ==========
    def change_avatar(self):
        """选图片 + 圆形显示"""
        file, _ = QFileDialog.getOpenFileName(
            self.main, "选择头像", "",
            "图片 (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file:
            return
        # 1. 更新设置页自己的大头像（80×80）
        self.set_circular_avatar(file)

        # 2. 更新主窗口 sidebar 的小头像（40×40）
        self.main.update_avatar(file)   # ← 传路径过去
        self.settings.setValue("avatar", file)

    def set_circular_avatar(self, image_path, size=80):
        self.apply_avatar(self.ui.avatarLabel, image_path, size)

    def make_circular_pixmap(self, image_path, size=80):
        """只负责生成圆形 pixmap，不设置到任何控件"""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return None

        pixmap = pixmap.scaled(
            size, size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        x = (size - pixmap.width()) // 2
        y = (size - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        painter.end()

        return rounded


    def apply_avatar(self, label, image_path, size=80):
        """把圆形头像设置到指定 QLabel 上"""
        rounded = self.make_circular_pixmap(image_path, size)
        if rounded is None:
            return
        label.setPixmap(rounded)
        label.setFixedSize(size, size)
        label.setAlignment(Qt.AlignCenter)

        # 让标签在布局里居中（用父布局通用写法）
        parent = label.parent()
        if parent and parent.layout():
            parent.layout().setAlignment(label, Qt.AlignHCenter)

    # ========== 允许修改用户名 ==========
    def enable_edit(self):
        """点'修改信息' → 允许改用户名"""
        self.ui.nameInput.setReadOnly(False)
        self.ui.nameInput.setFocus()
        QMessageBox.information(
            self.main, "提示", "现在可以修改用户名，改完点'保存'"
        )

    # ========== 保存用户设置 ==========
    def save_user_settings(self):
        """保存用户名"""
        new_name = self.ui.nameInput.text().strip()

        if not new_name:
            QMessageBox.warning(self.main, "错误", "用户名不能为空")
            return

        # 更新 QSettings 里的用户名
        self.settings.setValue("username", new_name)

        # 更新 sidebar 底部的用户名
        self.main.ui.username.setText(new_name)

        # 恢复"只读"
        self.ui.nameInput.setReadOnly(True)

        QMessageBox.information(self.main, "成功", "保存成功")