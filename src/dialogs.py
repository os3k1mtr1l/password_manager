from PyQt5 import QtCore, QtWidgets

#додавання нового паролю
class AddDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New")
        self.setFixedSize(300, 200)
        layout = QtWidgets.QVBoxLayout(self)

        #поля вводу
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.login_input = QtWidgets.QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")

        layout.addWidget(self.name_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        #кнопки
        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.add_button = QtWidgets.QPushButton("Add")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)

    def get_data(self):
        return self.name_input.text(), self.login_input.text(), self.password_input.text()



#перегляд збереженого паролю
class ViewDialog(QtWidgets.QDialog):
    def __init__(self, login, password):
        super().__init__()
        self.setWindowTitle("View details")
        self.setFixedSize(300, 150)
        layout = QtWidgets.QVBoxLayout(self)

        #кнопки та поля
        login_layout = QtWidgets.QHBoxLayout()
        self.login_edit = QtWidgets.QLineEdit(login)
        self.login_edit.setReadOnly(True)
        login_layout.addWidget(self.login_edit)
        self.copy_login_btn = QtWidgets.QPushButton("📋")
        login_layout.addWidget(self.copy_login_btn)
        layout.addLayout(login_layout)

        #властивості полей
        password_layout = QtWidgets.QHBoxLayout()
        self.password_edit = QtWidgets.QLineEdit(password)
        self.password_edit.setReadOnly(True)
        password_layout.addWidget(self.password_edit)
        self.copy_password_btn = QtWidgets.QPushButton("📋")
        password_layout.addWidget(self.copy_password_btn)
        layout.addLayout(password_layout)

        self.close_btn = QtWidgets.QPushButton("Close")
        layout.addWidget(self.close_btn)

        #копіювання
        self.copy_login_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(login))
        self.copy_password_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(password))
        self.close_btn.clicked.connect(self.accept)
