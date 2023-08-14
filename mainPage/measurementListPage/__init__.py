from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from ..search_engine import SearchEngineWidget
from ..subjectRecordTable import SubjectRecordTable


class MeasurementListPage(QWidget):
    infoDict = {}

    def __init__(self):
        super(MeasurementListPage, self).__init__()

        self.searchEngineWidget = SearchEngineWidget(2)
        self.subjectRecordTable = SubjectRecordTable()
        self.searchEngineWidget.btnSearch.clicked.connect(self.searchEngineWidget.emitSearchSignal)
        self.searchEngineWidget.searchSignal.connect(self.subjectRecordTable.searchClicked)
        self.btnPredict = QPushButton("Run Predict")

        vbox = QVBoxLayout()
        vbox.addWidget(self.searchEngineWidget)
        vbox.addWidget(self.subjectRecordTable)
        vbox.addWidget(self.btnPredict)
        self.setLayout(vbox)