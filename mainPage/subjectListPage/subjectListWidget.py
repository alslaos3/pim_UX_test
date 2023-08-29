from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from ..search_engine import SearchEngineWidget
from ..subjectRecordTable import SubjectRecordTable
from dao.selected_subject import SelectedSubjectData


class SubjectListWidget(QWidget):
    searchEngineWidget = QWidget
    subjectRecordTable = QWidget

    def __init__(self):
        super(SubjectListWidget, self).__init__()

        self.btnNewEnroll = QPushButton("신규 등록")
        self.btnMeasurement = QPushButton("Measurement")

        # self.searchEngineWidget = SearchEngineWidget(1)
        self.subjectRecordTable = SubjectRecordTable()
        # self.searchEngineWidget.btnSearch.clicked.connect(self.searchEngineWidget.emitSearchSignal)
        # self.searchEngineWidget.searchSignal.connect(self.subjectRecordTable.searchClicked)

        # self.btnMeasurement.clicked.connect(self.measurementClicked)

        vbox = QVBoxLayout()
        # vbox.addWidget(self.searchEngineWidget)
        vbox.addWidget(self.btnNewEnroll)
        vbox.addWidget(self.subjectRecordTable)
        vbox.addWidget(self.btnMeasurement)
        self.setLayout(vbox)

    def enrollComplete(self, arg__1):
        pass
    #     self.searchEngineWidget.editChartNum.setText(str(arg__1))
    #     self.searchEngineWidget.btnSearch.click()


    # 잘 작동함
    # def measurementClicked(self):
    #     print("this is clicked")
    #     print(SelectedSubjectData.getData())
    #     print(SelectedSubjectData.getChartNum())
    #     print(SelectedSubjectData.getName())
    #     print(SelectedSubjectData.getBirthDate())
