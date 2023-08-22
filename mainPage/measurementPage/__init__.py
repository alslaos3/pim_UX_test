import numpy as np
from PySide6.QtCore import Slot, Qt, Signal, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QPushButton, QProgressBar, QHBoxLayout, \
    QFormLayout, QMessageBox

from dao.controller_dao import ControllerDAO
from dao.save_db_dao import SaveDAO
from .graphWidget import GraphWidget
from dao.selected_subject import SelectedSubjectData


class MeasurementPage(QWidget):
    measurementBtnClicked = Signal()

    def __init__(self):
        super(MeasurementPage, self).__init__()
        self.stageNum = -1
        self.measurementBtnClicked.connect(self.setLabels)

        hboxBack = QHBoxLayout()
        self.btnBack = QPushButton("←")
        hboxBack.addWidget(self.btnBack)
        hboxBack.addStretch(1)

        gBoxInfo = QGroupBox()
        formInfo = QFormLayout()

        self.lblChartNum = QLabel("")
        self.lblName = QLabel("")
        self.lblBirthDate = QLabel("")
        self.lblProfessor = QLabel("")

        formInfo.addRow("차트번호 : ", self.lblChartNum)
        formInfo.addRow("성명 : ", self.lblName)
        formInfo.addRow("생년월일 : ", self.lblBirthDate)
        formInfo.addRow("담당교수 : ", self.lblProfessor)
        gBoxInfo.setLayout(formInfo)

        self.btnRun = QPushButton("Run")
        self.progressBar = QProgressBar()

        hboxMeasure = QHBoxLayout()
        hboxMeasure.addWidget(self.btnRun)
        hboxMeasure.addWidget(self.progressBar)

        self.graphWidget = GraphWidget()

        self.btnPredict = QPushButton("Run Analysis")
        self.btnRun.clicked.connect(self.startMeasurement)

        vbox = QVBoxLayout()
        vbox.addLayout(hboxBack)
        vbox.addWidget(gBoxInfo)
        vbox.addLayout(hboxMeasure)
        vbox.addWidget(self.graphWidget)
        vbox.addWidget(self.btnPredict)
        self.setLayout(vbox)

    def startMeasurement(self):
        # INITS
        self.progressBar.setValue(0)
        self.stageNum = -1
        # CONNECTS
        ControllerDAO.getAPI().exam.spec.resGetSpectrum.connect(self.graphWidget.getPlotData)
        ControllerDAO.getAPI().exam.focusController.measuredSignal.connect(self.getMeasuredSignal)
        ControllerDAO.getAPI().exam.focusController.focusCompleteSignal.connect(self.getMeasurementData)
        # METHOD
        ControllerDAO.defaultFocusing()
        self.setButtonsDisabled()

    def setButtonsDisabled(self, status=True):
        self.btnRun.setDisabled(status)
        self.btnPredict.setDisabled(status)
        self.btnBack.setDisabled(status)

    def endMeasurement(self):
        # CONNECTS
        ControllerDAO.getAPI().exam.spec.resGetSpectrum.disconnect(self.graphWidget.getPlotData)
        ControllerDAO.getAPI().exam.focusController.measuredSignal.disconnect(self.getMeasuredSignal)
        ControllerDAO.getAPI().exam.focusController.focusCompleteSignal.disconnect(self.getMeasurementData)
        self.setButtonsDisabled(False)

    @Slot(int, int, int)
    def getMeasuredSignal(self, current_round, total_round, stage_num):
        if self.stageNum != stage_num:
            self.stageNum += 1
            self.progressBar.setMaximum(total_round)
            self.progressBar.setValue(0)
        else:
            self.progressBar.setValue(current_round)
        print(current_round, total_round, stage_num)

    @Slot(np.ndarray)
    def getMeasurementData(self, intensity):
        SaveDAO.saveMeasurementData(SelectedSubjectData.getChartNum(), intensity)
        print(SelectedSubjectData.getChartNum(), intensity)
        self.endMeasurement()

    @Slot()
    def setLabels(self):
        self.lblChartNum.setText(str(SelectedSubjectData.getChartNum()))
        self.lblName.setText(SelectedSubjectData.getName())
        self.lblBirthDate.setText(SelectedSubjectData.getBirthDate().toString(Qt.ISODate))
        self.lblProfessor.setText(SelectedSubjectData.getProfessor())
