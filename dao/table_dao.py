from PySide6.QtSql import QSqlQueryModel
from PySide6.QtCore import Qt, QObject, QDate, Signal
from PySide6.QtSql import QSqlQuery, QSqlDatabase
from PySide6.QtWidgets import QTableView, QAbstractItemView
from .user_dao import UserDAO
from .selected_subject import SelectedSubjectData


class AccessDeniedError(Exception):
    pass


class SqlQueryModelAlignCenter(QSqlQueryModel):

    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            # Set the alignment for the second column (index 1) to center
            if index.column():
                return Qt.AlignCenter

        return super().data(index, role)


class TableDAO(QObject):
    rowSelectedSignal = Signal(str)

    def __init__(self):
        super(TableDAO, self).__init__()

        self._db = UserDAO.connectDatabase()  # This will use UserDAO's connectDatabase method
        self._table = QTableView()
        self._model = SqlQueryModelAlignCenter()
        self._query = None
        self._chartNum = ""
        self._name = ""
        self._professor = ""
        self._searchFrom = ""
        self._searchTo = ""

    def connectDatabase(self):
        return self._db

    def makeTable(self):
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        return self._table

    def handleRowSelected(self, current, previous):
        row = current.row()
        model = self._table.model()

        selected_data = {}

        for column in range(model.columnCount()):
            index = model.index(row, column)
            value = model.data(index, Qt.DisplayRole)
            header = model.headerData(column, Qt.Horizontal)
            selected_data[header] = value

        SelectedSubjectData.setData(selected_data)

    def makeModel(self):
        return self._model

    def querySubject(self, chartNum, name, professor, fromDate, toDate):
        where_conditions = []

        if chartNum:
            where_conditions.append(f"s.chartNum = {chartNum}")
        if name:
            where_conditions.append(f"s.name = '{name}'")
        if professor:
            where_conditions.append(f"s.professor = '{professor}'")
        # if fromDate and toDate:
        #     where_conditions.append(f"MAX(m.measurementDate) BETWEEN '{fromDate}' AND '{toDate}'")
        #     where_conditions.append(f"MAX(m.diagnosisDate) BETWEEN '{fromDate}' AND '{toDate}'")

        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)

        SQL = f"""
            SELECT s.chartNum, s.name, s.birthDate, s.gender, s.professor, s.supervisor, s.enrollDate, s.phoneNum,
            MAX(m.measurementDate) AS 최근측정일, MAX(m.diagnosisDate) AS 최근진단일
            FROM subject_test s
            LEFT JOIN measurement_test m
            ON s.chartNum = m.chartNum
            {where_clause}
            GROUP BY s.chartNum, s.name, s.birthDate, s.gender, s.professor, s.supervisor, s.enrollDate, s.phoneNum
            """
        self._model.setQuery(SQL)
        self._table.setModel(self._model)
        self._table.selectionModel().currentRowChanged.connect(self.handleRowSelected)

        return True

    def queryMeasureList(self, chartNum, name, professor, fromDate, toDate):
        where_conditions = []

        if chartNum:
            where_conditions.append(f"s.chartNum = {chartNum}")
        if name:
            where_conditions.append(f"s.name = '{name}'")
        if professor:
            where_conditions.append(f"s.professor = '{professor}'")
        # if fromDate and toDate:
        #     where_conditions.append(f"m.measurementDate BETWEEN '{fromDate}' AND '{toDate}'")

        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        SQL = f"""
            SELECT s.chartNum, s.name, s.birthDate, s.professor, s.supervisor, m.measurementDate
            FROM subject_test s
            JOIN measurement_test m
            ON s.chartNum = m.chartNum
            {where_clause}
            """
        self._model.setQuery(SQL)
        self._table.setModel(self._model)
        self._table.selectionModel().currentRowChanged.connect(self.handleRowSelected)

        return

    def queryAnalysisList(self, chartNum, name, professor, fromDate, toDate):
        where_conditions = []

        if chartNum:
            where_conditions.append(f"s.chartNum = {chartNum}")
        if name:
            where_conditions.append(f"s.name = '{name}'")
        if professor:
            where_conditions.append(f"s.professor = '{professor}'")
        # if fromDate and toDate:
        #     where_conditions.append(f"m.diagnosisDate BETWEEN '{fromDate}' AND '{toDate}'")

        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        SQL = f"""
            SELECT s.chartNum, s.name, s.birthDate, s.professor, s.supervisor, m.measurementDate, m.diagnosisDate, m.diagnosisResult
            FROM subject_test s
            JOIN measurement_test m
            ON s.chartNum = m.chartNum
            {where_clause}
            """
        self._model.setQuery(SQL)
        self._table.setModel(self._model)
        self._table.selectionModel().currentRowChanged.connect(self.handleRowSelected)

        return
