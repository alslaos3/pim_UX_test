import random

from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QPushButton, QProgressBar, QHBoxLayout, \
    QFormLayout
from .graphWidget import ResultGraphWidget
from dao.selected_subject import SelectedSubjectData


class PredictionPage(QWidget):
    predictionBtnClicked = Signal()

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

