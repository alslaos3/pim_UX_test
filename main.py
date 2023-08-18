import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from mainPage import MainPage
from loginPage import LoginPage
from dao import UserDAO


class PimBody(QApplication):
    def __init__(self):
        super(PimBody, self).__init__()

        self.w = QMainWindow()
        UserDAO.getInstance().logInSuccessSignal.connect(self.showMainPage)
        UserDAO.getInstance().logOutSuccessSignal.connect(self.showLoginPage)

        self.loginPage = LoginPage()
        # self.loginPage.signInSignal.connect(self.showMainPage)

        self.mainPage = QWidget()

        self.w.setCentralWidget(self.loginPage)

        self.setUpScreens()
        # self.w.showFullScreen()
        self.w.show()
    @Slot()
    def showMainPage(self):
        self.mainPage = MainPage()
        self.w.setCentralWidget(self.mainPage)
        self.mainPage.signOutSignal.connect(self.showLoginPage)

    @Slot()
    def showLoginPage(self):
        self.loginPage = LoginPage()
        self.w.setCentralWidget(self.loginPage)
        self.loginPage.signInSignal.connect(self.showMainPage)

    def setUpScreens(self):
        screens = QGuiApplication.screens()
        for screen in screens:
            rect = screen.geometry()
            if screen.isPortrait(screen.orientation()):
                self.w.move(rect.left(), rect.top())



if __name__ == "__main__":
    app = PimBody()
    sys.exit(app.exec())
