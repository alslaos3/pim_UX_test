from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from dao import UserDAO, SupervisorDAO


class SignOutWidget(QPushButton):

    def __init__(self):
        super(SignOutWidget, self).__init__()
        self.supervisorDAO = SupervisorDAO()
        self.setText("Sign Out")

        self.clicked.connect(self.checkSignOut)

    def checkSignOut(self):
        check = UserDAO.signOut(self.rememberMe)
        if check:
            return True
        else:
            return False

    @property
    def rememberMe(self):
        return self.supervisorDAO.sv_rememberMe

    def closeEvent(self, e):
        self.checkSignOut()

