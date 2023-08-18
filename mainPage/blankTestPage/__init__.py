from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from dao.controller_dao import ControllerDAO


class BlankTestPage(QWidget):
    startCalculation = Signal()

    def __init__(self):
        super(BlankTestPage, self).__init__()

        self.test = QLabel("test")

        self.btnStart = QPushButton("Start Blank Test")

        vbox = QVBoxLayout()
        vbox.addWidget(self.test)
        vbox.addWidget(self.btnStart)
        self.setLayout(vbox)


    def StartBlankTest(self):
        ControllerDAO.initFocusing()

