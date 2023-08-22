import random

import numpy as np
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QPushButton, QProgressBar, QHBoxLayout, \
    QFormLayout

from dao.save_db_dao import SaveDAO
from .graphWidget import ResultGraphWidget
from dao.selected_subject import SelectedSubjectData


class PredictionPage(QWidget):
    predictionBtnClicked = Signal()
    temp_signal = Signal(np.ndarray)

    def __init__(self):
        super(PredictionPage, self).__init__()
        self.predictionBtnClicked.connect(self.setLabels)
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
        self.lblMeasureDate = QLabel("")
        self.lblSupervisor = QLabel("")

        formInfo.addRow("차트번호 : ", self.lblChartNum)
        formInfo.addRow("성명 : ", self.lblName)
        formInfo.addRow("생년월일 : ", self.lblBirthDate)
        formInfo.addRow("담당교수 : ", self.lblProfessor)
        formInfo.addRow("측정 시기 : ", self.lblMeasureDate)
        formInfo.addRow("측정 담당자 : ", self.lblSupervisor)
        gBoxInfo.setLayout(formInfo)

        self.btnRun = QPushButton("Run")
        self.btnRun.clicked.connect(self.startPrediction)

        self.progressBar = QProgressBar()

        hboxMeasure = QHBoxLayout()
        hboxMeasure.addWidget(self.btnRun)
        hboxMeasure.addWidget(self.progressBar)

        self.graphWidget = ResultGraphWidget()

        self.btnAnalysis = QPushButton("End")

        vbox = QVBoxLayout()
        vbox.addLayout(hboxBack)
        vbox.addWidget(gBoxInfo)
        vbox.addLayout(hboxMeasure)
        vbox.addWidget(self.graphWidget)
        vbox.addWidget(self.btnAnalysis)
        self.setLayout(vbox)
        self.btnRun.clicked.connect(self.graphWidget.update)

    @Slot()
    def setLabels(self):
        self.lblChartNum.setText(str(SelectedSubjectData.getChartNum()))
        self.lblName.setText(SelectedSubjectData.getName())
        self.lblBirthDate.setText(SelectedSubjectData.getBirthDate().toString(Qt.ISODate))
        self.lblProfessor.setText(SelectedSubjectData.getProfessor())
        self.lblMeasureDate.setText(SelectedSubjectData.getMeasurementDate().toString(Qt.ISODate))
        self.lblSupervisor.setText(SelectedSubjectData.getSupervisor())

    @Slot(str)
    def getPredictionData(self, UUID):
        rand = random.randint(50,100)
        SaveDAO.savePredictionData(SelectedSubjectData.getChartNum(), UUID, rand)
        print(SelectedSubjectData.getChartNum(), UUID)
        self.progressBar.setValue(100)
        self.graphWidget.update(rand)
        self.endPrediction()

    def startPrediction(self):
        # INITS
        self.progressBar.setValue(0)
        # self.stageNum = -1
        # CONNECTS
        UUID = SelectedSubjectData.getUUID()
        print(UUID)
        # intensity = np.load(file_name)[1]
        self.temp_signal.connect(self.getPredictionData)
        # METHOD
        self.temp_signal.emit(UUID)

    def endPrediction(self):
        # CONNECTS
        self.temp_signal.disconnect(self.getPredictionData)
