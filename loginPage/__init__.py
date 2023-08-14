import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QWidget, QPushButton, QStackedWidget, QVBoxLayout, QApplication
# from PySide6.QtGui import
# from PySide6.QtCore import
from dao import UserDAO
from .signInWidget import SignInWidget
from .signUpWidget import SignUpWidget


class LoginPage(QWidget):
    signInSignal = Signal(dict)

    def __init__(self):
        super(LoginPage, self).__init__()

        self.stackedWidget = QStackedWidget()
        self.signInWidget = SignInWidget()
        self.signUpWidget = SignUpWidget()

        self.stackedWidget.addWidget(self.signInWidget)
        self.stackedWidget.addWidget(self.signUpWidget)

        vbox = QVBoxLayout()
        vbox.addWidget(self.stackedWidget)
        self.setLayout(vbox)

        self.signInWidget.btnSignUp.clicked.connect(self.setSignUpWidget)
        self.signUpWidget.btnHome.clicked.connect(self.setSignInWidget)
        self.signUpWidget.btnHome.clicked.connect(self.signUpWidget.clearForm)
        UserDAO.getInstance().signUpSuccessSignal.connect(self.afterSignUp)

    def setSignInWidget(self):
        self.stackedWidget.setCurrentIndex(0)

    def setSignUpWidget(self):
        self.stackedWidget.setCurrentIndex(1)

    @Slot(str)
    def afterSignUp(self, _username):
        self.stackedWidget.setCurrentIndex(0)
        self.signInWidget.editUsername.setText(_username)
