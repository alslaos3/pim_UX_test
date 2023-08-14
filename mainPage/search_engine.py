from PySide6.QtCore import Qt, QRegularExpression, Signal, QDate, Slot
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QDateEdit
from PySide6.QtGui import QRegularExpressionValidator

import dao
from dao import SubjectDAO, TableDAO, SupervisorDAO  # TableDAO
from modules.check_reg_ex import Check

searchFeatures = ["차트번호", "성명", "담당교수", "측정기간"]


class SearchEngineWidget(QWidget):
    filterCreated = Signal(str, int)
    searchAtIndex = 0
    _newSubjectInfo = dict
    searchSignal = Signal(int, str, str, str, str, str)

    def __init__(self, At):
        super(SearchEngineWidget, self).__init__()

        SubjectDAO.getInstance().EnrollSuccessSignal.connect(self.afterEnrollSearch)
        self.searchAtIndex = At
        self.lineEdits = {}

        lblVBox = QVBoxLayout()
        editVBox = QVBoxLayout()

        lblChartNum = QLabel(searchFeatures[0])
        self.editChartNum = QLineEdit()

        lblName = QLabel(searchFeatures[1])
        self.editName = QLineEdit()

        lblProfessor = QLabel(searchFeatures[2])
        self.editProfessor = QLineEdit()

        lblPeriod = QLabel(searchFeatures[3])
        lblPeriodTilde = QLabel("~")
        lblPeriod.setAlignment(Qt.AlignCenter)

        self.editPeriodFrom = QDateEdit()
        self.editPeriodFrom.setCalendarPopup(True)
        self.editPeriodFrom.setSpecialValueText("")
        self.editPeriodFrom.setDate(QDate.currentDate())

        self.editPeriodTo = QDateEdit()
        self.editPeriodTo.setCalendarPopup(True)
        self.editPeriodTo.setSpecialValueText("")
        self.editPeriodTo.setDate(QDate.currentDate())

        periodHBox = QHBoxLayout()
        periodHBox.addWidget(self.editPeriodFrom)
        periodHBox.addWidget(lblPeriodTilde)
        periodHBox.addWidget(self.editPeriodTo)

        self.btnSearch = QPushButton("조회")
        self.btnEdit = QPushButton("수정")
        hboxBtn = QHBoxLayout()
        hboxBtn.addWidget(self.btnSearch)
        hboxBtn.addWidget(self.btnEdit)

        lblVBox.addWidget(lblChartNum)
        lblVBox.addWidget(lblName)
        lblVBox.addWidget(lblProfessor)
        lblVBox.addWidget(lblPeriod)

        editVBox.addWidget(self.editChartNum)
        editVBox.addWidget(self.editName)
        editVBox.addWidget(self.editProfessor)
        editVBox.addLayout(periodHBox)

        hbox = QHBoxLayout()
        hbox.addLayout(lblVBox)
        hbox.addLayout(editVBox)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hboxBtn)

        self.setLayout(vbox)

        self.initConnect()

    def initConnect(self):
        self.editName.textChanged.connect(Check.checkValidityName(self.editName))
        self.editChartNum.textChanged.connect(Check.checkValidityChartNum(self.editChartNum))
        self.editProfessor.textChanged.connect(Check.checkValidityName(self.editProfessor))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            focused_widget = QApplication.focusWidget().parentWidget()
            if isinstance(focused_widget, QWidget):
                self.btnSearch.click()

    def setTextAsSearchEngine(self):
        dao = SupervisorDAO()
        print(dao.je_chartNum, dao.je_name, dao.je_professor)
        self.editChartNum.setText(str(dao.je_chartNum))
        self.editName.setText(dao.je_name)
        self.editProfessor.setText(dao.je_professor)
        self.editPeriodFrom.setDate(dao.je_searchFrom)
        self.editPeriodTo.setDate(dao.je_searchTo)

    def afterEnrollSearch(self):
        self.setTextAsSearchEngine()
        self.btnSearch.click()

    @property
    def _chartNum(self):
        return self.editChartNum.text()

    @property
    def _name(self):
        return self.editName.text()

    @property
    def _professor(self):
        return self.editProfessor.text()

    @property
    def _searchFrom(self):
        return self.editPeriodFrom.text()

    @property
    def _searchTo(self):
        return self.editPeriodTo.text()

    def emitSearchSignal(self):
        self.searchSignal.emit(self.searchAtIndex, self._chartNum, self._name, self._professor, self._searchFrom, self._searchTo)

