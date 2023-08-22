import os
import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from dao.controller_dao import ControllerDAO
from mainPage import MainPage
from loginPage import LoginPage
from dao import UserDAO

STYLESHEET_PATH = os.path.join('styles')
STYLESHEETS = {
    "MainWindow": "MainWindow.css",
}
STYLES = {}


def load_stylesheet(filename):
    with open(filename, "r") as f:
        return f.read()


try:
    for widget, stylesheet in STYLESHEETS.items():
        STYLES[widget] = load_stylesheet(os.path.join(STYLESHEET_PATH, stylesheet))
except Exception as e:
    print(f"An error occurred: {e}")
    raise

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

        self.w = MyQMainWindow()
        self.w.setStyleSheet(STYLES["MainWindow"])
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
