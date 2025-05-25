from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1280, 720)
        MainWindow.setStyleSheet("background-color: #233444; color: #ECF0F1;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pagesWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.pagesWidget.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.pagesWidget.setObjectName("pagesWidget")

        common_input_style = (
            "QLineEdit { color: #ECF0F1; background-color: #34495E; border: 2px solid #5DADE2; "
            "border-radius: 6px; padding: 10px; font-size: 14pt; } "
            "QLineEdit:focus { border: 2px solid #3498DB; }"
        )

        common_button_style = (
            "QPushButton { background-color: #5DADE2; color: white; font-size: 14pt; font-weight: bold; "
            "border: none; border-radius: 6px; padding: 10px; } "
            "QPushButton:hover { background-color: #3498DB; } "
            "QPushButton:pressed { background-color: #2E86C1; }"
        )

        exit_button_style = (
            "QPushButton { background-color: #DE3C31; color: white; font-size: 14pt; font-weight: bold; "
            "border: none; border-radius: 6px; padding: 10px; } "
            "QPushButton:hover { background-color: #F07F78; } "
            "QPushButton:pressed { background-color: #B5605B; }"
        )

        label_style = "QLabel { color: #ECF0F1; font-size: 20pt; font-weight: bold; }"

        # Create Key Page
        self.createKeyPage = QtWidgets.QWidget()
        self.createKeyPage.setObjectName("createKeyPage")
        layout = QtWidgets.QVBoxLayout(self.createKeyPage)
        layout.setContentsMargins(100, 100, 100, 100)

        self.create_label = QtWidgets.QLabel("Create Master Key")
        self.create_label.setAlignment(QtCore.Qt.AlignCenter)
        self.create_label.setStyleSheet(label_style)
        self.create_input = QtWidgets.QLineEdit()
        self.create_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create_input.setPlaceholderText("Enter new master key")
        self.create_input.setStyleSheet(common_input_style)
        self.create_button = QtWidgets.QPushButton("Create")
        self.create_button.setStyleSheet(common_button_style)
        layout.addWidget(self.create_label)
        layout.addWidget(self.create_input)
        layout.addWidget(self.create_button)
        self.pagesWidget.addWidget(self.createKeyPage)

        # Login Page
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setObjectName("loginPage")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.loginPage)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(490, 240, 341, 180))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.loginBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.loginBox.setContentsMargins(0, 0, 0, 0)
        self.loginBox.setSpacing(15)

        self.text_enterMasterKey = QtWidgets.QLabel("ENTER MASTER KEY")
        self.text_enterMasterKey.setAlignment(QtCore.Qt.AlignCenter)
        self.text_enterMasterKey.setStyleSheet(label_style)
        self.lineEdit_masterKey = QtWidgets.QLineEdit()
        self.lineEdit_masterKey.setStyleSheet(common_input_style)
        self.lineEdit_masterKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.button_enter = QtWidgets.QPushButton("Enter")
        self.button_enter.setStyleSheet(common_button_style)
        self.loginBox.addWidget(self.text_enterMasterKey)
        self.loginBox.addWidget(self.lineEdit_masterKey)
        self.loginBox.addWidget(self.button_enter)
        self.pagesWidget.addWidget(self.loginPage)

        # Passwords Page
        self.passwordsPage = QtWidgets.QWidget()
        self.passwordsPage.setObjectName("passwordsPage")

        self.search_input = QtWidgets.QLineEdit(self.passwordsPage)
        self.search_input.setGeometry(QtCore.QRect(20, 10, 962, 44))
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                color: #ECF0F1;
                background-color: #202e3b;
                border: 2px solid #5DADE2;
                border-radius: 6px;
                padding: 10px;
                font-size: 14pt;
            }
            QLineEdit:focus {
                border: 2px solid #3498DB;
            }
        """)

        self.scrollArea = QtWidgets.QScrollArea(self.passwordsPage)
        self.scrollArea.setGeometry(QtCore.QRect(19, 60, 971, 650))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                background-color: #34495E;
                border: none;
            }
            
            QScrollBar:vertical {
                background: #2C3E50;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #5DADE2;
                min-height: 25px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #3498DB;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaContent = QtWidgets.QWidget()
        self.scrollAreaContent.setObjectName("scrollAreaContent")
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaContent)
        self.scrollAreaContent.setLayout(self.scrollLayout)
        self.scrollAreaContent.setMinimumHeight(0)
        self.scrollLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollLayout.setSpacing(10)

        self.scrollArea.setWidget(self.scrollAreaContent)

        # Buttons on the right side
        self.add_new_btn = QtWidgets.QPushButton("Add new", self.passwordsPage)
        self.add_new_btn.setGeometry(QtCore.QRect(1140, 10, 130, 45))
        self.add_new_btn.setStyleSheet(common_button_style)

        self.import_btn = QtWidgets.QPushButton("Import", self.passwordsPage)
        self.import_btn.setGeometry(QtCore.QRect(1140, 70, 130, 45))
        self.import_btn.setStyleSheet(common_button_style)

        self.export_btn = QtWidgets.QPushButton("Export", self.passwordsPage)
        self.export_btn.setGeometry(QtCore.QRect(1140, 130, 130, 45))
        self.export_btn.setStyleSheet(common_button_style)

        self.exit_btn = QtWidgets.QPushButton("Exit", self.passwordsPage)
        self.exit_btn.setGeometry(QtCore.QRect(1140, 190, 130, 45))
        self.exit_btn.setStyleSheet(exit_button_style)

        self.pagesWidget.addWidget(self.passwordsPage)

        MainWindow.setCentralWidget(self.centralwidget)
