from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pagesWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.pagesWidget.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.pagesWidget.setObjectName("pagesWidget")

        # вкладка створення ключа (індекс 0)
        self.createKeyPage = QtWidgets.QWidget()
        self.createKeyPage.setObjectName("createKeyPage")
        layout = QtWidgets.QVBoxLayout(self.createKeyPage)
        self.create_label = QtWidgets.QLabel("Create Master Key")
        self.create_label.setAlignment(QtCore.Qt.AlignCenter)
        self.create_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.create_input = QtWidgets.QLineEdit()
        self.create_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_input.setPlaceholderText("Enter new master key")
        self.create_input.setStyleSheet("padding: 10px; font-size: 14pt;")
        self.create_button = QtWidgets.QPushButton("Create")
        self.create_button.setStyleSheet("padding: 10px; font-size: 14pt;")
        layout.addWidget(self.create_label)
        layout.addWidget(self.create_input)
        layout.addWidget(self.create_button)
        self.pagesWidget.addWidget(self.createKeyPage)

        # вкладка логіну (індекс 1)
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setObjectName("loginPage")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.loginPage)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(490, 240, 341, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.loginBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.loginBox.setContentsMargins(0, 0, 0, 0)
        self.loginBox.setObjectName("loginBox")
        self.text_enterMasterKey = QtWidgets.QLabel("ENTER MASTER KEY")
        self.text_enterMasterKey.setAlignment(QtCore.Qt.AlignCenter)
        self.text_enterMasterKey.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2c3e50;")
        self.loginBox.addWidget(self.text_enterMasterKey)
        self.lineEdit_masterKey = QtWidgets.QLineEdit()
        self.lineEdit_masterKey.setStyleSheet("QLineEdit "
                                              "{ border: 2px solid #3498db; border-radius: 5px;"
                                              "padding: 5px; font-size: 12pt;"
                                              "color: #2c3e50; background-color: #ecf0f1;} "
                                              "QLineEdit:focus { border: 2px solid #2980b9;"
                                              "background-color: #ffffff; }")
        self.lineEdit_masterKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginBox.addWidget(self.lineEdit_masterKey)
        self.button_enter = QtWidgets.QPushButton("Enter")
        self.button_enter.setStyleSheet("QPushButton { background-color: #2980b9; color: white; "
                                        "font-size: 12pt; font-weight: bold; border: none; "
                                        "border-radius: 6px; padding: 8px 16px; } "
                                        "QPushButton:hover { background-color: #3498db; } "
                                        "QPushButton:pressed { background-color: #1c638d; }")
        self.loginBox.addWidget(self.button_enter)
        self.pagesWidget.addWidget(self.loginPage)

        # сторінка з паролями (індекс 2)
        self.passwordsPage = QtWidgets.QWidget()
        self.passwordsPage.setObjectName("passwordsPage")
        self.scrollArea = QtWidgets.QScrollArea(self.passwordsPage)
        self.scrollArea.setGeometry(QtCore.QRect(19, 9, 971, 701))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContent = QtWidgets.QWidget()
        self.scrollAreaContent.setObjectName("scrollAreaContent")
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaContent)
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.scrollAreaContent)

        self.add_new_btn = QtWidgets.QPushButton("Add new", self.passwordsPage)
        self.add_new_btn.setGeometry(QtCore.QRect(1140, 10, 130, 50))
        self.add_new_btn.setStyleSheet("padding: 10px; font-size: 14pt;")

        self.import_btn = QtWidgets.QPushButton("Import", self.passwordsPage)
        self.import_btn.setGeometry(QtCore.QRect(1140, 70, 130, 50))
        self.import_btn.setStyleSheet("padding: 10px; font-size: 14pt;")

        self.export_btn = QtWidgets.QPushButton("Export", self.passwordsPage)
        self.export_btn.setGeometry(QtCore.QRect(1140, 130, 130, 50))
        self.export_btn.setStyleSheet("padding: 10px; font-size: 14pt;")

        self.exit_btn = QtWidgets.QPushButton("Exit", self.passwordsPage)
        self.exit_btn.setGeometry(QtCore.QRect(1140, 190, 130, 50))
        self.exit_btn.setStyleSheet("padding: 10px; font-size: 14pt;")

        self.pagesWidget.addWidget(self.passwordsPage)

        MainWindow.setCentralWidget(self.centralwidget)