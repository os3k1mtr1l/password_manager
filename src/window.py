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

        ui.search_input.textChanged.connect(self.refresh_entries)

    def __setup_timer(self) -> None:
        self.auto_logout_timer = QtCore.QTimer()
        self.auto_logout_timer.timeout.connect(self.logout)
        self.auto_logout_timer.start(LOGOUT_TIME)
        self.installEventFilter(self)

    def clear_entries(self) -> None:
        while self.ui.scrollLayout.count():
            widget = self.ui.scrollLayout.itemAt(0).widget()
            self.ui.scrollLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()

    def refresh_entries(self) -> None:
        self.clear_entries()

        keyword = self.ui.search_input.text().strip()
        if keyword:
            entries = self.pwddb.find_by_name(keyword)
        else:
            entries = self.pwddb.get_all_record_names()

        for entry in entries:
            self.record_entry(entry)

    def create_master_key(self):
        password = self.ui.create_input.text()
        self.ui.create_input.clear()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Password cannot be empty")
            return

        self.pwddb.start(password)
        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)

    def login(self):
        password = self.ui.lineEdit_masterKey.text()
        self.ui.lineEdit_masterKey.clear()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Password cannot be empty")
            return

        try:
            self.pwddb.start(password)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"{e}")
            return

        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)
        self.refresh_entries()

    def logout(self) -> None:
        self.auto_logout_timer.stop()
        self.ui.pagesWidget.setCurrentIndex(Pages.LOGIN_PAGE_EXISTS)
        self.pwddb.end()
        self.clear_entries()

    def view_entry(self, widget: QtWidgets.QWidget) -> None:
        login, password = self.pwddb.show_record(widget.property("record_id"))
        dialog = ViewDialog(widget.property("record_id"), login, password, self)

        dialog.exec_()
        if dialog.modified:
            self.refresh_entries()

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
        layout = QtWidgets.QHBoxLayout(entry_widget)
        entry_widget.setMinimumHeight(60)
        entry_widget.setProperty("record_id", id)
        entry_widget.setStyleSheet("background-color: transparent; border: none;")

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
                background-color: #DE3C31;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 5px 16px;
            }
            QPushButton:hover { background-color: #F07F78; }
            QPushButton:pressed { background-color: #B5605B; }
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
            returned = dialog.exec_()

            if returned == QtWidgets.QDialog.Accepted:
                name, login, password = dialog.get_data()

                if not name or not login or not password:
                    QtWidgets.QMessageBox.warning(self, "Warning", "All fields must be filled")
                    continue

                entry: dict[str, Any] = {
                    "name": name,
                    "login": login,
                    "password": password
                }

                self.record_entry(entry)
                return
            elif returned == QtWidgets.QDialog.Rejected:
                return

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent):
        if event.type() in (QtCore.QEvent.Type.MouseMove, QtCore.QEvent.Type.KeyPress):
            self.auto_logout_timer.start(LOGOUT_TIME)
        return super().eventFilter(source, event)

    def import_entry(self) -> None:
        dialog = ImportDialog()

        while True:
            returned = dialog.exec_()
            if returned == QtWidgets.QDialog.Accepted:
                count = 0
                try:
                    count = self.pwddb.import_db(dialog.file_input.text(), dialog.key_input.text())
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Warning", f"{e}")
                    continue

                QtWidgets.QMessageBox.information(self, "Done", f"Imported {count} records")
                self.refresh_entries()
                return
            elif returned == QtWidgets.QDialog.Rejected:
                return

    def export_entry(self) -> None:
        dialog = ExportDialog()

        while True:
            returned = dialog.exec_()
            if returned == QtWidgets.QDialog.Accepted:
                try:
                    self.pwddb.export_db(dialog.path_input.text(), dialog.filename_input.text())
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Warning", f"{e}")
                    continue

                QtWidgets.QMessageBox.information(self, "Done", f"File saved at {dialog.path_input.text()} as {dialog.filename_input.text()}")
                return
            elif returned == QtWidgets.QDialog.Rejected:
                return
