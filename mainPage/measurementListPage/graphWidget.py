import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from dao import SelectedSubjectData
from dao.controller_dao import ControllerDAO


class GraphWidget(QWidget):
    # display_size = 10000
    all_data = np.zeros(1044)
    new_data = np.zeros(1044) # 가정: 1초마다 1044개의 데이터가 들어옴

    def __init__(self):
        super(GraphWidget, self).__init__()

        self.plotWidget = pg.PlotWidget()
        self.curve = self.plotWidget.plot(self.all_data)

        vbox = QVBoxLayout()
        vbox.addWidget(self.plotWidget)
        self.setLayout(vbox)
        #
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(1) # 10밀리초 간격으로 업데이트

    def getPlotData(self):
        file_name = SelectedSubjectData.getUUID()
        intensity = np.load(file_name)
        self.new_data = intensity
        self.curve.setData(self.new_data[0],self.new_data[1])



    # def update(self):
    #     print("Size of all_data:", len(self.all_data))  # 디버깅 출력
    #     print("Size of new_data:", len(self.new_data))  # 디버깅 출력
    #     # 데이터를 오른쪽으로 슬라이드
    #     if len(self.new_data) > 0:
    #
    #         self.all_data[:-1] = self.all_data[1:]
    #
    #         # 새로운 데이터의 첫 번째 값 추가 (나머지는 다음 업데이트에 사용됨)
    #         self.all_data[-1] = self.new_data[0]
    #
    #         # 새로운 데이터에서 사용한 값 제거
    #         self.new_data = self.new_data[1:]
    #
    #         # 그래프 업데이트
    #         self.curve.setData(self.all_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphWidget()
    w.show()
    sys.exit(app.exec())
