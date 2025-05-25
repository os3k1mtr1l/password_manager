from PyQt5 import QtCore, QtWidgets

DIALOG_STYLES = """
QDialog {
    background-color: #1B2631;
    color: #ECF0F1;
    font-family: Segoe UI, Arial, sans-serif;
}

QLabel {
    color: #ECF0F1;
    font-size: 14pt;
}

QLineEdit {
    background-color: #273746;
    color: #ECF0F1;
    border: 2px solid #5DADE2;
    border-radius: 6px;
    padding: 8px;
    font-size: 14pt;
}

QLineEdit:focus {
    border: 2px solid #3498DB;
}

QPushButton {
    background-color: #5DADE2;
    color: white;
    font-size: 12pt;
    font-weight: bold;
    border: 2px solid #3498DB;
    border-radius: 6px;
    padding: 10px 20px;
    min-height: 22px;
}

QPushButton:hover {
    background-color: #2980B9;
    border: 2px solid #1ABC9C;
}

QPushButton:pressed {
    background-color: #2E86C1;
}

QPushButton#cancel_button {
    background-color: #34495E;
}

QPushButton#cancel_button:hover {
    background-color: #566573;
}

QPushButton#cancel_button:pressed {
    background-color: #1C2833;
}

QPushButton#icon_button {
    background-color: transparent;
    border: none;
    color: #5DADE2;
    font-size: 16pt;
}
"""

# Додавання нового паролю
class AddDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New")
        self.setFixedSize(320, 240)
        self.setStyleSheet(DIALOG_STYLES)
        layout = QtWidgets.QVBoxLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.login_input = QtWidgets.QLineEdit()
        self.login_input.setPlaceholderText("Login")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")

        layout.addWidget(self.name_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")
        self.add_button = QtWidgets.QPushButton("Add")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)
        layout.addLayout(button_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)
        self.name_input.returnPressed.connect(self.accept)
        self.login_input.returnPressed.connect(self.accept)
        self.password_input.returnPressed.connect(self.accept)

    def get_data(self) -> tuple[str, str, str]:
        return self.name_input.text(), self.login_input.text(), self.password_input.text()

# Перегляд збереженого паролю
class ViewDialog(QtWidgets.QDialog):
    def __init__(self, record_id, login, password, parent=None):
        super().__init__()
        self.setWindowTitle("View Details")
        self.setFixedSize(320, 220)
        self.setStyleSheet(DIALOG_STYLES)
        layout = QtWidgets.QVBoxLayout(self)

        self.modified = False
        self.edit_mode = False
        self.record_id = record_id
        self.parent = parent

        login_layout = QtWidgets.QHBoxLayout()
        self.login_edit = QtWidgets.QLineEdit(login)
        self.login_edit.setReadOnly(True)
        login_layout.addWidget(self.login_edit)
        self.copy_login_btn = QtWidgets.QPushButton("📋")
        login_layout.addWidget(self.copy_login_btn)
        layout.addLayout(login_layout)

        password_layout = QtWidgets.QHBoxLayout()
        self.password_edit = QtWidgets.QLineEdit(password)
        self.password_edit.setReadOnly(True)
        password_layout.addWidget(self.password_edit)
        self.copy_password_btn = QtWidgets.QPushButton("📋")
        password_layout.addWidget(self.copy_password_btn)
        layout.addLayout(password_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.close_btn = QtWidgets.QPushButton("Close")
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.close_btn)
        layout.addLayout(buttons_layout)

        self.copy_login_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(self.login_edit.text()))
        self.copy_password_btn.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(self.password_edit.text()))
        self.close_btn.clicked.connect(self.accept)

    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.login_edit.setReadOnly(False)
            self.password_edit.setReadOnly(False)
            self.edit_btn.setText("Save")
            self.edit_mode = True
        else:
            new_login = self.login_edit.text().strip()
            new_password = self.password_edit.text().strip()

            if not new_login or not new_password:
                QtWidgets.QMessageBox.warning(self, "Error", "Fields can not be empty")
                return

            self.parent.pwddb.update_password(self.record_id, new_login, new_password)
            self.modified = True
            self.accept()

# Діалог експорту
class ExportDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export")
        self.setFixedSize(420, 220)
        self.setStyleSheet(DIALOG_STYLES)
        layout = QtWidgets.QVBoxLayout(self)

        self.filename_input = QtWidgets.QLineEdit()
        self.filename_input.setPlaceholderText("File name")
        layout.addWidget(self.filename_input)

        path_layout = QtWidgets.QHBoxLayout()
        self.path_input = QtWidgets.QLineEdit()
        self.path_input.setPlaceholderText("Select folder")
        self.browse_btn = QtWidgets.QPushButton("Browse")
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")
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

# Діалог імпорту
class ImportDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import")
        self.setFixedSize(420, 200)
        self.setStyleSheet(DIALOG_STYLES)
        layout = QtWidgets.QVBoxLayout(self)

        file_layout = QtWidgets.QHBoxLayout()
        self.file_input = QtWidgets.QLineEdit()
        self.file_input.setPlaceholderText("Select file to import")
        self.browse_btn = QtWidgets.QPushButton("Browse")
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)

        self.key_input = QtWidgets.QLineEdit()
        self.key_input.setPlaceholderText("Master Key for imported file")
        self.key_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.key_input)

        button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")
        self.import_button = QtWidgets.QPushButton("Import")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.import_button)
        layout.addLayout(button_layout)

        self.browse_btn.clicked.connect(self.select_file)
        self.cancel_button.clicked.connect(self.reject)
        self.import_button.clicked.connect(self.accept)
        self.key_input.returnPressed.connect(self.accept)

    def select_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Export File (*.pwddb)")
        if file:
            self.file_input.setText(file)
