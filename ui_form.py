# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1027, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.sidebar = QWidget(self.page)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setGeometry(QRect(2, 2, 248, 529))
        self.verticalLayout_3 = QVBoxLayout(self.sidebar)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.newChatBtn = QPushButton(self.sidebar)
        self.newChatBtn.setObjectName(u"newChatBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newChatBtn.sizePolicy().hasHeightForWidth())
        self.newChatBtn.setSizePolicy(sizePolicy)
        self.newChatBtn.setMinimumSize(QSize(0, 50))
        self.newChatBtn.setIconSize(QSize(20, 20))

        self.verticalLayout_3.addWidget(self.newChatBtn)

        self.historyList = QListWidget(self.sidebar)
        self.historyList.setObjectName(u"historyList")
        self.historyList.setStyleSheet(u"QListWidget {\n"
"    background: white;\n"
"    border: none;\n"
"    outline: none;\n"
"}\n"
"QListWidget::item {\n"
"    border-bottom: 1px solid #E0E0E0;\n"
"    padding: 8px;\n"
"    color: black;             /* \u672a\u9009\u4e2d\u6587\u5b57\uff1a\u9ed1 */\n"
"}\n"
"QListWidget::item:selected {\n"
"    background: #D0E0FF;      /* \u9009\u4e2d\u80cc\u666f\uff1a\u6d45\u84dd */\n"
"    color: black;             /* \u9009\u4e2d\u6587\u5b57\uff1a\u9ed1 */\n"
"}\n"
"QListWidget::item:hover {\n"
"    background: #F0F0F0;      /* \u9f20\u6807\u60ac\u505c\uff1a\u6d45\u7070 */\n"
"}")

        self.verticalLayout_3.addWidget(self.historyList)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.userArea = QWidget(self.sidebar)
        self.userArea.setObjectName(u"userArea")
        self.userArea.setMinimumSize(QSize(200, 0))
        self.userArea.setMouseTracking(True)
        self.userArea.setStyleSheet(u"QWidget {\n"
"       background: transparent;\n"
"   }\n"
"   QWidget:hover {\n"
"       background: #E0E0E0;\n"
"   }")
        self.horizontalLayout_3 = QHBoxLayout(self.userArea)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.avatar = QLabel(self.userArea)
        self.avatar.setObjectName(u"avatar")

        self.horizontalLayout_2.addWidget(self.avatar)

        self.username = QLabel(self.userArea)
        self.username.setObjectName(u"username")

        self.horizontalLayout_2.addWidget(self.username)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.userArea)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.setStretch(1, 1)
        self.layoutWidget = QWidget(self.page)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(258, 3, 741, 531))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.chatScroll = QScrollArea(self.layoutWidget)
        self.chatScroll.setObjectName(u"chatScroll")
        self.chatScroll.setWidgetResizable(True)
        self.chatContainer = QWidget()
        self.chatContainer.setObjectName(u"chatContainer")
        self.chatContainer.setGeometry(QRect(0, 0, 737, 390))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chatContainer.sizePolicy().hasHeightForWidth())
        self.chatContainer.setSizePolicy(sizePolicy1)
        self.chatContainer.setMinimumSize(QSize(600, 0))
        self.chatScroll.setWidget(self.chatContainer)

        self.verticalLayout.addWidget(self.chatScroll)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.inputLine = QTextEdit(self.layoutWidget)
        self.inputLine.setObjectName(u"inputLine")
        self.inputLine.setMinimumSize(QSize(0, 20))
        self.inputLine.setMaximumSize(QSize(16777215, 120))

        self.horizontalLayout_4.addWidget(self.inputLine)

        self.sendButton = QPushButton(self.layoutWidget)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout_4.addWidget(self.sendButton)

        self.horizontalLayout_4.setStretch(0, 3)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.layoutWidget1 = QWidget(self.page_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(1, 1, 1001, 541))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.backBtn = QToolButton(self.layoutWidget1)
        self.backBtn.setObjectName(u"backBtn")
        icon = QIcon()
        icon.addFile(u"picture/OIP-C.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.backBtn.setIcon(icon)
        self.backBtn.setIconSize(QSize(50, 30))

        self.verticalLayout_5.addWidget(self.backBtn)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.settingList = QListWidget(self.layoutWidget1)
        font = QFont()
        font.setPointSize(10)
        font.setItalic(True)
        __qlistwidgetitem = QListWidgetItem(self.settingList)
        __qlistwidgetitem.setTextAlignment(Qt.AlignCenter)
        __qlistwidgetitem.setFont(font)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(True)
        font1.setUnderline(False)
        __qlistwidgetitem1 = QListWidgetItem(self.settingList)
        __qlistwidgetitem1.setTextAlignment(Qt.AlignCenter)
        __qlistwidgetitem1.setFont(font1)
        self.settingList.setObjectName(u"settingList")
        self.settingList.setStyleSheet(u"QListWidget {\n"
"    background: white;\n"
"    border: none;\n"
"    outline: none;\n"
"}\n"
"QListWidget::item {\n"
"    border-bottom: 1px solid #E0E0E0;\n"
"    padding: 8px;\n"
"    color: black;             /* \u672a\u9009\u4e2d\u6587\u5b57\uff1a\u9ed1 */\n"
"}\n"
"QListWidget::item:selected {\n"
"    background: #D0E0FF;      /* \u9009\u4e2d\u80cc\u666f\uff1a\u6d45\u84dd */\n"
"    color: black;             /* \u9009\u4e2d\u6587\u5b57\uff1a\u9ed1 */\n"
"}\n"
"QListWidget::item:hover {\n"
"    background: #F0F0F0;      /* \u9f20\u6807\u60ac\u505c\uff1a\u6d45\u7070 */\n"
"}")

        self.horizontalLayout_6.addWidget(self.settingList)

        self.settingStack = QStackedWidget(self.layoutWidget1)
        self.settingStack.setObjectName(u"settingStack")
        self.userSettingPage = QWidget()
        self.userSettingPage.setObjectName(u"userSettingPage")
        self.layoutWidget2 = QWidget(self.userSettingPage)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(0, 2, 751, 481))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.avatarLabel = QLabel(self.layoutWidget2)
        self.avatarLabel.setObjectName(u"avatarLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.avatarLabel.sizePolicy().hasHeightForWidth())
        self.avatarLabel.setSizePolicy(sizePolicy2)
        self.avatarLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatarLabel.setIndent(0)

        self.verticalLayout_4.addWidget(self.avatarLabel)

        self.changeAvatarBtn = QPushButton(self.layoutWidget2)
        self.changeAvatarBtn.setObjectName(u"changeAvatarBtn")

        self.verticalLayout_4.addWidget(self.changeAvatarBtn)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.nameLabel = QLabel(self.layoutWidget2)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.nameLabel)

        self.nameInput = QLineEdit(self.layoutWidget2)
        self.nameInput.setObjectName(u"nameInput")

        self.horizontalLayout_7.addWidget(self.nameInput)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.spacer)

        self.editInfoBtn = QPushButton(self.layoutWidget2)
        self.editInfoBtn.setObjectName(u"editInfoBtn")
        self.editInfoBtn.setStyleSheet(u"QPushButton {\n"
"    color: red;              /* \u6587\u5b57\u989c\u8272 */\n"
"}")

        self.verticalLayout_4.addWidget(self.editInfoBtn)

        self.saveUserBtn = QPushButton(self.layoutWidget2)
        self.saveUserBtn.setObjectName(u"saveUserBtn")

        self.verticalLayout_4.addWidget(self.saveUserBtn)

        self.settingStack.addWidget(self.userSettingPage)
        self.apiSettingPage = QWidget()
        self.apiSettingPage.setObjectName(u"apiSettingPage")
        self.settingStack.addWidget(self.apiSettingPage)

        self.horizontalLayout_6.addWidget(self.settingStack)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.settingStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.newChatBtn.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u5bf9\u8bdd", None))
        self.avatar.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.sendButton.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.backBtn.setText(QCoreApplication.translate("MainWindow", u"...", None))

        __sortingEnabled = self.settingList.isSortingEnabled()
        self.settingList.setSortingEnabled(False)
        ___qlistwidgetitem = self.settingList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u8bbe\u7f6e", None))
        ___qlistwidgetitem1 = self.settingList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"API\u8bbe\u7f6e", None))
        self.settingList.setSortingEnabled(__sortingEnabled)

        self.avatarLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.changeAvatarBtn.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u5934\u50cf", None))
        self.nameLabel.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d\uff1a", None))
        self.editInfoBtn.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u4fe1\u606f", None))
        self.saveUserBtn.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
    # retranslateUi

