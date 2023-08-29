import os
import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QGuiApplication, QIcon, QAction, Qt
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar, QLabel, QToolBar

from dao.controller_dao import ControllerDAO
from mainPage import MainPage
from loginPage import LoginPage
from dao import UserDAO


# STYLESHEET_PATH = os.path.join('styles')
# STYLESHEETS = {
#     "MainWindow": "MainWindow.css",
# }
# STYLES = {}
#
#
# def load_stylesheet(filename):
#     with open(filename, "r") as f:
#         return f.read()
#
#
# try:
#     for widget, stylesheet in STYLESHEETS.items():
#         STYLES[widget] = load_stylesheet(os.path.join(STYLESHEET_PATH, stylesheet))
# except Exception as e:
#     print(f"An error occurred: {e}")
#     raise

class MyQMainWindow(QMainWindow):
    def __init__(self):
        super(MyQMainWindow, self).__init__()

    def closeEvent(self, event):
        self.setWindowTitle("종료중...")
        ControllerDAO.getAPI().exam.closeAbleSignal.connect(self.closing)
        ControllerDAO.getAPI().closeEvent(event)

    @Slot()
    def closing(self):
        self.close()


class PimBody(QApplication):


    def __init__(self):
        super(PimBody, self).__init__()

        self._statusBar = QStatusBar()
        self._lblSupervisorName = QLabel("")
        self._lblSupervisorBirthDate = QLabel("")
        self._lblSupervisorGender = QLabel("")
        self._lblSupervisorOrg = QLabel("")
        self._lblSupervisorEmail = QLabel("")
        self._mainPage = QWidget()

        self.w = MyQMainWindow()
        # self.w.setStyleSheet(STYLES["MainWindow"])
        UserDAO.getInstance().logInSuccessSignal.connect(self.showMainPage)
        UserDAO.getInstance().logOutSuccessSignal.connect(self.showLoginPage)
        self.loginPage = LoginPage()
        # self.loginPage.signInSignal.connect(self.showMainPage)

        self.w.setCentralWidget(self.loginPage)
        self._statusBar.addWidget(self._lblSupervisorName)
        self._statusBar.addWidget(self._lblSupervisorBirthDate)
        self._statusBar.addWidget(self._lblSupervisorGender)
        self._statusBar.addWidget(self._lblSupervisorOrg)
        self._statusBar.addWidget(self._lblSupervisorEmail)
        self.w.setStatusBar(self._statusBar)

        # self.setUpScreens()
        # self.w.showFullScreen()
        self.w.show()

    def addTopToolBar(self):
        self._topToolBar = QToolBar()

        _iconLogo = QIcon("images/icon_example.png")
        self._actLogo = QAction(_iconLogo, "logo", self)
        self._topToolBar.addAction(self._actLogo)

        _iconMeasure = QIcon("images/icon_example.png")
        self._actMeasure = QAction(_iconMeasure, "measure", self)
        self._topToolBar.addAction(self._actMeasure)

        _iconPrediction = QIcon("images/icon_example.png")
        self._actPrediction = QAction(_iconPrediction, "prediction", self)
        self._topToolBar.addAction(self._actPrediction)

        _iconSearch = QIcon("images/icon_example.png")
        self._actSearch = QAction(_iconSearch, "search", self)
        self._topToolBar.addAction(self._actSearch)

        _iconModifyUser = QIcon("images/icon_example.png")
        self._actModifyUser = QAction(_iconModifyUser, "modify_user", self)
        self._topToolBar.addAction(self._actModifyUser)
        self._actSearch.connect(self._mainPage)

        self.w.addToolBar(Qt.TopToolBarArea, self._topToolBar)

    @Slot()
    def showMainPage(self):
        self._mainPage = MainPage()
        self.w.setCentralWidget(self._mainPage)
        self.addTopToolBar()
        self._mainPage.supervisorSignal.connect(self.getStatusBarArgs)
        self._mainPage.signOutSignal.connect(self.showLoginPage)

    @Slot(str, str, str, str, str)
    def getStatusBarArgs(self, _name, _birthDate, _gender, _org, _email):
        self._lblSupervisorName.setText(_name)
        self._lblSupervisorBirthDate.setText(_birthDate)
        self._lblSupervisorGender.setText(_gender)
        self._lblSupervisorOrg.setText(_org)
        self._lblSupervisorEmail.setText(_email)

    @Slot()
    def showLoginPage(self):
        self.loginPage = LoginPage()
        self.w.setCentralWidget(self.loginPage)
        self.loginPage.signInSignal.connect(self.showMainPage)

    # def setUpScreens(self):
    #     screens = QGuiApplication.screens()
    #     for screen in screens:
    #         rect = screen.geometry()
    #         if screen.isPortrait(screen.orientation()):
    #             self.w.move(rect.left(), rect.top())


if __name__ == "__main__":
    app = PimBody()
    sys.exit(app.exec())
