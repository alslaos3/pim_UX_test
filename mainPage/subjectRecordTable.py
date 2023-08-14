import gc

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel
from PySide6.QtWidgets import QMessageBox, QTableView, QVBoxLayout, QWidget, QRadioButton, QButtonGroup

from dao import TableDAO


class SubjectRecordTable(QWidget):
    dictSubjectSignal = Signal(dict)

    dictSubject = {}

    def __init__(self):
        super(SubjectRecordTable, self).__init__()

        self.dao = TableDAO()
        self.db = self.dao.connectDatabase()
        self.table = self.dao.makeTable()

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    @Slot(int, str, str, str, str, str)
    def searchClicked(self, page, chartNum, name, professor, searchFrom, searchTo):
        print(chartNum, name, professor, searchFrom, searchTo)
        if page == 1:
            print("this is subject")
            self.dao.querySubject(chartNum, name, professor, searchFrom, searchTo)
        elif page == 2:
            print("this is measure")
            self.dao.queryMeasureList(chartNum, name, professor, searchFrom, searchTo)
        elif page == 3:
            print("this is analysis")
            self.dao.queryAnalysisList(chartNum, name, professor, searchFrom, searchTo)

