from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Slot, QObject, Property, Signal, QUrl, Qt
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from datetime import datetime
from qroundprogressbar import QRoundProgressBar
import os
import random

class ResultGraphWidget(QWidget):
    predictedValue = 75
    offset = 100 - predictedValue
    timestamp = float
    goHomeSignal = Signal()

    def __init__(self):
        super(ResultGraphWidget, self).__init__()

        self.roundProgressBar = QRoundProgressBar()
        self.roundProgressBar.setObjectName("RoundProgressBar")
        self.roundProgressBar.setFixedSize(400, 400)
        self.roundProgressBar.setDecimals(0)
        self.roundProgressBar.setValue(0)

        self.roundProgressBar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # New line
        vbox = QVBoxLayout()
        hboxAlign = QHBoxLayout()
        hboxAlign.addStretch(1)
        hboxAlign.addWidget(self.roundProgressBar)
        hboxAlign.addStretch(1)
        vbox.addLayout(hboxAlign)
        self.setLayout(vbox)

    def update(self, value):
        self.roundProgressBar.setValue(value)


if __name__ == "__main__":
    app = QApplication([])

    w = ResultGraphWidget()

    w.show()
    app.exec()
