from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox, QApplication
from dao import UserDAO, SupervisorDAO


class SignInWidget(QWidget):
    _rememberMe = False
    _username = str
    _password = str

    def __init__(self):
        super(SignInWidget, self).__init__()

        self.supervisorDAO = SupervisorDAO()
        self.editUsername = QLineEdit()
        self.btnRememberMe = QCheckBox("Remember me")
        self.btnRememberMe.clicked.connect(self.updateCheckBox)
        self.editPassword = QLineEdit()

        self.btnSignIn = QPushButton("Sign In")
        self.btnSignUp = QPushButton("Sign Up")
        self.btnSignIn.clicked.connect(self.checkSignIn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.editUsername)
        vbox.addWidget(self.btnRememberMe)
        vbox.addWidget(self.editPassword)
        vbox.addWidget(self.btnSignIn)
        vbox.addWidget(self.btnSignUp)
        self.setLayout(vbox)

        self.checkBtnRememberMe()

    def checkBtnRememberMe(self):
        state = self.supervisorDAO.sv_rememberMe
        if state:
            self.updateCheckBox(state)
            self.btnRememberMe.setChecked(state)
            if self.supervisorDAO.supervisorInfo:
                self.editUsername.setText(self.supervisorDAO.sv_username)

    def checkSignIn(self):
        check = UserDAO.signIn(self.username, self.password, self.rememberMe)
        if check:
            return True
        else:
            return False

    def updateCheckBox(self, state):
        if state:
            self._rememberMe = True
        else:
            self._rememberMe = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            focused_widget = QApplication.focusWidget().parentWidget()
            if isinstance(focused_widget, QWidget):
                self.btnSignIn.click()

    @property
    def username(self):
        self._username = self.editUsername.text()
        return self._username

    @property
    def password(self):
        self._password = self.editPassword.text()
        return self._password

    @property
    def rememberMe(self):
        return self._rememberMe
