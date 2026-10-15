# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(1039, 590)
        self.stackedWidget = QStackedWidget(LoginDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 10, 1021, 571))
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.layoutWidget = QWidget(self.page_login)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(231, 91, 501, 391))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.loginTitle = QLabel(self.layoutWidget)
        self.loginTitle.setObjectName(u"loginTitle")
        self.loginTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.loginTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.userLabel = QLabel(self.layoutWidget)
        self.userLabel.setObjectName(u"userLabel")

        self.horizontalLayout.addWidget(self.userLabel)

        self.userInput = QLineEdit(self.layoutWidget)
        self.userInput.setObjectName(u"userInput")

        self.horizontalLayout.addWidget(self.userInput)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pwdLabel = QLabel(self.layoutWidget)
        self.pwdLabel.setObjectName(u"pwdLabel")

        self.horizontalLayout_2.addWidget(self.pwdLabel)

        self.pwdInput = QLineEdit(self.layoutWidget)
        self.pwdInput.setObjectName(u"pwdInput")

        self.horizontalLayout_2.addWidget(self.pwdInput)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.loginBtn = QPushButton(self.layoutWidget)
        self.loginBtn.setObjectName(u"loginBtn")

        self.horizontalLayout_6.addWidget(self.loginBtn)

        self.rememberCheck = QCheckBox(self.layoutWidget)
        self.rememberCheck.setObjectName(u"rememberCheck")

        self.horizontalLayout_6.addWidget(self.rememberCheck)

        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.goRegisterBtn = QPushButton(self.layoutWidget)
        self.goRegisterBtn.setObjectName(u"goRegisterBtn")

        self.verticalLayout.addWidget(self.goRegisterBtn)

        self.stackedWidget.addWidget(self.page_login)
        self.page_register = QWidget()
        self.page_register.setObjectName(u"page_register")
        self.layoutWidget1 = QWidget(self.page_register)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(260, 70, 491, 381))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.regTitle = QLabel(self.layoutWidget1)
        self.regTitle.setObjectName(u"regTitle")
        self.regTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.regTitle)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.regUserLabel = QLabel(self.layoutWidget1)
        self.regUserLabel.setObjectName(u"regUserLabel")

        self.horizontalLayout_5.addWidget(self.regUserLabel)

        self.regUserInput = QLineEdit(self.layoutWidget1)
        self.regUserInput.setObjectName(u"regUserInput")

        self.horizontalLayout_5.addWidget(self.regUserInput)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.regPwdLabel = QLabel(self.layoutWidget1)
        self.regPwdLabel.setObjectName(u"regPwdLabel")

        self.horizontalLayout_4.addWidget(self.regPwdLabel)

        self.regPwdInput = QLineEdit(self.layoutWidget1)
        self.regPwdInput.setObjectName(u"regPwdInput")

        self.horizontalLayout_4.addWidget(self.regPwdInput)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.regPwd2Label = QLabel(self.layoutWidget1)
        self.regPwd2Label.setObjectName(u"regPwd2Label")

        self.horizontalLayout_3.addWidget(self.regPwd2Label)

        self.regPwd2Input = QLineEdit(self.layoutWidget1)
        self.regPwd2Input.setObjectName(u"regPwd2Input")

        self.horizontalLayout_3.addWidget(self.regPwd2Input)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.registerBtn = QPushButton(self.layoutWidget1)
        self.registerBtn.setObjectName(u"registerBtn")

        self.verticalLayout_2.addWidget(self.registerBtn)

        self.goLoginBtn = QPushButton(self.layoutWidget1)
        self.goLoginBtn.setObjectName(u"goLoginBtn")

        self.verticalLayout_2.addWidget(self.goLoginBtn)

        self.stackedWidget.addWidget(self.page_register)

        self.retranslateUi(LoginDialog)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"Dialog", None))
        self.loginTitle.setText(QCoreApplication.translate("LoginDialog", u"\u6b22\u8fce\u767b\u9646", None))
        self.userLabel.setText(QCoreApplication.translate("LoginDialog", u"\u7528\u6237\u540d\uff1a", None))
        self.pwdLabel.setText(QCoreApplication.translate("LoginDialog", u"\u5bc6\u7801\uff1a", None))
        self.loginBtn.setText(QCoreApplication.translate("LoginDialog", u"\u767b\u5f55", None))
        self.rememberCheck.setText(QCoreApplication.translate("LoginDialog", u"CheckBox", None))
        self.goRegisterBtn.setText(QCoreApplication.translate("LoginDialog", u"\u6ca1\u6709\u8d26\u53f7\uff0c\u53bb\u6ce8\u518c", None))
        self.regTitle.setText(QCoreApplication.translate("LoginDialog", u"\u6ce8\u518c", None))
        self.regUserLabel.setText(QCoreApplication.translate("LoginDialog", u"\u7528\u6237\u540d\uff1a", None))
        self.regPwdLabel.setText(QCoreApplication.translate("LoginDialog", u"\u5bc6\u7801\uff1a", None))
        self.regPwd2Label.setText(QCoreApplication.translate("LoginDialog", u"\u786e\u8ba4\u5bc6\u7801\uff1a", None))
        self.registerBtn.setText(QCoreApplication.translate("LoginDialog", u"\u6ce8\u518c", None))
        self.goLoginBtn.setText(QCoreApplication.translate("LoginDialog", u"\u4e0d\u60f3\u6ce8\u518c\uff0c\u8fd4\u56de\u767b\u9646", None))
    # retranslateUi

