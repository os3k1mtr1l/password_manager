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


    #логіка для змінни вкладок
    def __setup_logic(self) -> None:
        ui = self.ui
        ui.create_button.clicked.connect(self.create_master_key)
        ui.button_enter.clicked.connect(self.login)
        ui.add_new_btn.clicked.connect(self.add_new_entry)
        ui.exit_btn.clicked.connect(self.close)

        ui.import_btn.clicked.connect(self.import_entry)
        ui.export_btn.clicked.connect(self.export_entry)

    def __setup_timer(self) -> None:
        self.auto_logout_timer = QtCore.QTimer()
        self.auto_logout_timer.timeout.connect(self.logout)
        self.auto_logout_timer.start(LOGOUT_TIME)
        self.installEventFilter(self)

    def create_master_key(self):
        password = self.ui.create_input.text()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
        
        self.pwddb.start(password)
        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)

    def login(self):
        password = self.ui.lineEdit_masterKey.text()
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
        
        try:
            self.pwddb.start(password)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"{e}")
            return

        self.ui.pagesWidget.setCurrentIndex(Pages.MAIN_PAGE)
        entries = self.pwddb.get_all_record_names()
        for entry in entries:
            widget = self.record_entry(entry)
            self.ui.scrollLayout.addWidget(widget)
        

    def logout(self) -> None:
        raise NotImplementedError

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
        layout = QtWidgets.QHBoxLayout(entry_widget)
        
        entry_widget.setProperty("record_id", id)
        name_label = QtWidgets.QLabel(name)
        view_btn = QtWidgets.QPushButton("View")
        delete_btn = QtWidgets.QPushButton("Delete")

        view_btn.clicked.connect(lambda: self.view_entry(entry_widget))
        delete_btn.clicked.connect(lambda: self.remove_entry(entry_widget))

        layout.addWidget(name_label)
        layout.addWidget(view_btn)
        layout.addWidget(delete_btn)
        
        self.ui.scrollLayout.addWidget(entry_widget)

    def add_new_entry(self) -> None:
        dialog = AddDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            name, login, password = dialog.get_data()
            entry: dict[str, Any] = {
                "name": name,
                "login": login,
                "password": password
            }

            self.record_entry(entry)

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent):
        if event.type() in (QtCore.QEvent.Type.MouseMove, QtCore.QEvent.Type.KeyPress):
            self.auto_logout_timer.start(LOGOUT_TIME)
        return super().eventFilter(source, event)


    def import_entry(self) -> None:
        dialog = ImportDialog()
        dialog.exec_()


    def export_entry(self) -> None:
        dialog = ExportDialog()
        dialog.exec_()
