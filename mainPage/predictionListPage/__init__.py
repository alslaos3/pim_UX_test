from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from .graphWidget import ResultGraphWidget
from ..search_engine import SearchEngineWidget
from ..subjectRecordTable import SubjectRecordTable


class PredictionListPage(QWidget):

    infoDict = {}

    def __init__(self):
        super(PredictionListPage, self).__init__()

        self.searchEngineWidget = SearchEngineWidget(3)
        self.subjectRecordTable = SubjectRecordTable()
        self.graphWidget = ResultGraphWidget()
        self.searchEngineWidget.btnSearch.clicked.connect(self.searchEngineWidget.emitSearchSignal)
        self.searchEngineWidget.searchSignal.connect(self.subjectRecordTable.searchClicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.searchEngineWidget)
        vbox.addWidget(self.subjectRecordTable)
        self.setLayout(vbox)