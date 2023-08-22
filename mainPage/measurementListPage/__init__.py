from PySide6.QtCore import Slot, QItemSelection
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

from .graphWidget import GraphWidget
from ..search_engine import SearchEngineWidget
from ..subjectRecordTable import SubjectRecordTable


class MeasurementListPage(QWidget):
    infoDict = {}

    def __init__(self):
        super(MeasurementListPage, self).__init__()

        self.searchEngineWidget = SearchEngineWidget(2)
        self.subjectRecordTable = SubjectRecordTable()
        self.graphWidget = GraphWidget()
        self.searchEngineWidget.btnSearch.clicked.connect(self.searchEngineWidget.emitSearchSignal)
        self.searchEngineWidget.searchSignal.connect(self.subjectRecordTable.searchClicked)
        self.btnPredict = QPushButton("Run Predict")

        vbox = QVBoxLayout()
        vbox.addWidget(self.searchEngineWidget)
        vbox.addWidget(self.subjectRecordTable)
        vbox.addWidget(self.graphWidget)
        vbox.addWidget(self.btnPredict)
        self.setLayout(vbox)
        self.graphWidget.hide()

        self.subjectRecordTable.measurementListSignal.connect(self.getRowSelectedSignal)

    @Slot()
    def getRowSelectedSignal(self):
        self.graphWidget.show()
        self.graphWidget.getPlotData()

    def mousePressEvent(self, event):
        if not self.subjectRecordTable.table.geometry().contains(event.pos()):
            self.subjectRecordTable.table.clearSelection()
        super(MeasurementListPage, self).mousePressEvent(event)
