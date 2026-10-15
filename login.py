# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QSettings
from login_ui import Ui_LoginDialog
from password_utils import hash_password, verify_password


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)

        self.username = ""      # 登录成功后存

        # QSettings：存"用户名 + 哈希密码"
        self.settings = QSettings("MyCompany", "MyAgent")

        # 1. 启动时，自动填充（如果之前"记住我"）
        self.load_saved()

        # 2. 页面切换
        self.ui.goRegisterBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1)
        )
        self.ui.goLoginBtn.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )

        # 3. 登录 / 注册
        self.ui.loginBtn.clicked.connect(self.on_login)
        self.ui.registerBtn.clicked.connect(self.on_register)

    # ========== 自动填充 ==========
    def load_saved(self):
        """启动时，读上次保存的，填到输入框"""
        username = self.settings.value("username", "")
        hashed = self.settings.value("hashed_pwd", "")

        if username:
            self.ui.userInput.setText(username)
            self.ui.pwdInput.setText("")       # 密码不填（因为存的是哈希，不能还原）

        # 勾选"记住我"
        if self.settings.value("remember", False, type=bool):
            self.ui.rememberCheck.setChecked(True)

    # ========== 登录 ==========
    def on_login(self):
        user = self.ui.userInput.text().strip()
        pwd = self.ui.pwdInput.text().strip()

        if not user or not pwd:
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return

        # 从 QSettings 读"存起来的哈希"
        saved_user = self.settings.value("username", "")
        saved_hash = self.settings.value("hashed_pwd", "")

        # 验证
        if user != saved_user or not verify_password(pwd, saved_hash):
            QMessageBox.warning(self, "错误", "用户名或密码不对")
            return

        # 登录成功
        self.username = user

        # 如果勾了"记住我"，保存
        if self.ui.rememberCheck.isChecked():
            self.settings.setValue("remember", True)
        else:
            self.settings.setValue("remember", False)

        self.accept()      # 关闭对话框，返回"成功"

    # ========== 注册 ==========
    def on_register(self):
        user = self.ui.regUserInput.text().strip()
        pwd = self.ui.regPwdInput.text().strip()
        pwd2 = self.ui.regPwd2Input.text().strip()

        if not user or not pwd:
            QMessageBox.warning(self, "错误", "请填写完整")
            return
        if pwd != pwd2:
            QMessageBox.warning(self, "错误", "两次密码不一致")
            return

        # 哈希密码
        hashed = hash_password(pwd)

        # 保存到 QSettings
        self.settings.setValue("username", user)
        self.settings.setValue("hashed_pwd", hashed)

        QMessageBox.information(self, "成功", "注册成功，请登录")

        # 切回登录页，用户名填好
        self.ui.userInput.setText(user)
        self.ui.pwdInput.clear()
        self.ui.stackedWidget.setCurrentIndex(0)