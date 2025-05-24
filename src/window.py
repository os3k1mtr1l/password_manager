from PyQt5 import QtWidgets, QtCore
from typing import Any

from src.ui.main import Ui_MainWindow
from src.dialogs import AddDialog, ViewDialog, ExportDialog, ImportDialog
from src.db.passworddatabase import PasswordDatabase
from src.constants import LOGOUT_TIME, Pages


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setup_logic()
        self.__setup_timer()
        self.pwddb: PasswordDatabase = PasswordDatabase()

        if self.pwddb.is_initialized():
            self.ui.pagesWidget.setCurrentIndex(Pages.LOGIN_PAGE_EXISTS)
        else:
            self.ui.pagesWidget.setCurrentIndex(Pages.LOGIN_PAGE_CREATE)

    def __setup_logic(self) -> None:
        ui = self.ui

        ui.create_button.clicked.connect(self.create_master_key)
        self.ui.create_input.returnPressed.connect(self.ui.create_button.click)

        ui.button_enter.clicked.connect(self.login)
        self.ui.lineEdit_masterKey.returnPressed.connect(self.ui.button_enter.click)

        ui.add_new_btn.clicked.connect(self.add_new_entry)
        ui.exit_btn.clicked.connect(self.logout)

        ui.import_btn.clicked.connect(self.import_entry)
        ui.export_btn.clicked.connect(self.export_entry)

    def __setup_timer(self) -> None:
        self.auto_logout_timer = QtCore.QTimer()
        self.auto_logout_timer.timeout.connect(self.logout)
        self.auto_logout_timer.start(LOGOUT_TIME)
        self.installEventFilter(self)

    def show_warning(self, title: str, message: str) -> None:
        box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, message, QtWidgets.QMessageBox.Ok, self)
        box.setStyleSheet("""
            QMessageBox {
                background-color: #1B2631;
                color: #ECF0F1;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 14pt;
                border: 2px solid #5DADE2;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 14pt;
                background-color: transparent;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 12pt;
                font-weight: normal;
                border: 1px solid #2980B9;
                border-radius: 4px;
                padding: 6px 16px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #2980B9;
                border: 1px solid #1ABC9C;
            }
            QPushButton:pressed {
                background-color: #2E86C1;
            }
        """)
        box.exec_()

    def create_master_key(self):
        password = self.ui.create_input.text()
        self.ui.create_input.clear()
        if not password:
            self.show_warning("Error", "Password cannot be empty")
            return

        self.pwddb.start(password)
        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)

    def login(self):
        password = self.ui.lineEdit_masterKey.text()
        self.ui.lineEdit_masterKey.clear()
        if not password:
            self.show_warning("Error", "Password cannot be empty")
            return

        try:
            self.pwddb.start(password)
        except Exception as e:
            self.show_warning("Error", f"{e}")
            return

        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)
        entries = self.pwddb.get_all_record_names()
        for entry in entries:
            self.record_entry(entry)

    def logout(self) -> None:
        self.auto_logout_timer.stop()
        self.ui.pagesWidget.setCurrentIndex(Pages.LOGIN_PAGE_EXISTS)
        self.pwddb.end()

        while self.ui.scrollLayout.count():
            widget = self.ui.scrollLayout.itemAt(0).widget()
            self.ui.scrollLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

    def view_entry(self, widget: QtWidgets.QWidget) -> None:
        login, password = self.pwddb.show_record(widget.property("record_id"))
        ViewDialog(login, password).exec_()

    def remove_entry(self, widget: QtWidgets.QWidget) -> None:
        self.pwddb.delete_password(widget.property("record_id"))
        self.ui.scrollLayout.removeWidget(widget)
        widget.deleteLater()

    def record_entry(self, entry: dict[str, Any]) -> None:
        id = entry.get("id")
        name = entry.get("name")
        login = entry.get("login")
        password = entry.get("password")

        if not id:
            id = self.pwddb.add_password(name, login, password)

        entry_widget = QtWidgets.QWidget()
        entry_widget.setProperty("record_id", id)

        entry_widget.setStyleSheet("background-color: transparent; border: none;")

        layout = QtWidgets.QHBoxLayout(entry_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        name_label = QtWidgets.QLabel(name)
        name_label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 14pt;
                background-color: transparent;
            }
        """)

        view_btn = QtWidgets.QPushButton("View")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #5DADE2;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 5px 16px;
            }
            QPushButton:hover { background-color: #3498DB; }
            QPushButton:pressed { background-color: #2E86C1; }
        """)

        delete_btn = QtWidgets.QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #5DADE2;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 5px 16px;
            }
            QPushButton:hover { background-color: #3498DB; }
            QPushButton:pressed { background-color: #2E86C1; }
        """)

        view_btn.clicked.connect(lambda: self.view_entry(entry_widget))
        delete_btn.clicked.connect(lambda: self.remove_entry(entry_widget))

        layout.addWidget(name_label)
        layout.addWidget(view_btn)
        layout.addWidget(delete_btn)

        self.ui.scrollLayout.addWidget(entry_widget)

    def add_new_entry(self) -> None:
        dialog = AddDialog()

        while True:
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                name, login, password = dialog.get_data()

                if not name or not login or not password:
                    self.show_warning("Warning", "All fields must be filled")
                    continue

                entry: dict[str, Any] = {
                    "name": name,
                    "login": login,
                    "password": password
                }

                self.record_entry(entry)
                break

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent):
        if event.type() in (QtCore.QEvent.Type.MouseMove, QtCore.QEvent.Type.KeyPress):
            self.auto_logout_timer.start(LOGOUT_TIME)
        return super().eventFilter(source, event)

    def import_entry(self) -> None:
        dialog = ImportDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ...

    def export_entry(self) -> None:
        dialog = ExportDialog()
        dialog.exec_()
