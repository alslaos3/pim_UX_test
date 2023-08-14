import sys

# from PySide6.QtCore import
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
# from PySide6.QtGui import
import pyqtgraph as pg
import numpy as np


class GraphWidget(QWidget):

    def __init__(self):
        super(GraphWidget, self).__init__()

        self.plotWidget = pg.PlotWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.plotWidget)
        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphWidget()
    w.show()
    sys.exit(app.exec())