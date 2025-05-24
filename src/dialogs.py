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

    def get_data(self) -> tuple[str, str, str]:
        return self.name_input.text(), self.login_input.text(), self.password_input.text()

#перегляд збереженого паролю
class ViewDialog(QtWidgets.QDialog):
    def __init__(self, login, password):
        super().__init__()
        self.setWindowTitle("View details")
        self.setFixedSize(300, 200)
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

        buttons_layout = QtWidgets.QHBoxLayout()
        self.edit_btn = QtWidgets.QPushButton("Edit")
        buttons_layout.addWidget(self.edit_btn)
        self.close_btn = QtWidgets.QPushButton("Close")
        buttons_layout.addWidget(self.close_btn)
        layout.addLayout(buttons_layout)

        #копіювання
        self.copy_login_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(login))
        self.copy_password_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(password))
        self.close_btn.clicked.connect(self.accept)


#експорт
class ExportDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export")
        self.setFixedSize(400, 200)
        layout = QtWidgets.QVBoxLayout(self)

        #назва
        self.filename_input = QtWidgets.QLineEdit()
        self.filename_input.setPlaceholderText("File name")
        layout.addWidget(self.filename_input)

        #шлях
        path_layout = QtWidgets.QHBoxLayout()
        self.path_input = QtWidgets.QLineEdit()
        self.path_input.setPlaceholderText("Select folder")
        self.browse_btn = QtWidgets.QPushButton("Browse")
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        #кнопки
        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.export_button = QtWidgets.QPushButton("Export")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.export_button)
        layout.addLayout(button_layout)

        self.browse_btn.clicked.connect(self.select_folder)
        self.cancel_button.clicked.connect(self.reject)
        self.export_button.clicked.connect(self.accept)

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)

#імпорт
class ImportDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import")
        self.setFixedSize(400, 150)
        layout = QtWidgets.QVBoxLayout(self)

        #вибір
        file_layout = QtWidgets.QHBoxLayout()
        self.file_input = QtWidgets.QLineEdit()
        self.file_input.setPlaceholderText("Select file to import")
        self.browse_btn = QtWidgets.QPushButton("Browse")
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)

        #кнопки
        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.import_button = QtWidgets.QPushButton("Import")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.import_button)
        layout.addLayout(button_layout)

        self.browse_btn.clicked.connect(self.select_file)
        self.cancel_button.clicked.connect(self.reject)
        self.import_button.clicked.connect(self.accept)

    def select_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, )
        if file:
            self.file_input.setText(file)