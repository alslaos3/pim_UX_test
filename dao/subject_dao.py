from PySide6.QtCore import QObject, QDate, Signal
from PySide6.QtSql import QSqlQuery, QSqlDatabase

from .user_dao import UserDAO
from .supervisor_dao import SupervisorDAO

class ChartNumAlreadyExistsError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class SubjectDAO(QObject):
    EnrollSuccessSignal = Signal()
    DeleteSuccessSignal = Signal()
    _db = None
    _instance = None

    def __init__(self):
        super(SubjectDAO, self).__init__()

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def connectDatabase(cls):
        if cls._db is None:
            db = UserDAO.connectDatabase()
            if db.open():
                cls._db = db
            else:
                raise AccessDeniedError("Could not open database connection")
        return cls._db

    @classmethod
    def enroll(cls, _name: str, _birthDate: str, _gender: str, _phoneNum: str, _professor: str, _supervisor: str, _enrollDate: QDate):
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare(
            "INSERT INTO subject_test (name, birthDate, gender, phoneNum, professor, supervisor, enrollDate)"
            "VALUES (:name, :birthDate, :gender, :phoneNum, :professor, :supervisor, :enrollDate)")
        SQL.bindValue(":name", _name)
        SQL.bindValue(":birthDate", _birthDate)
        SQL.bindValue(":gender", _gender)
        SQL.bindValue(":phoneNum", _phoneNum)
        SQL.bindValue(":professor", _professor)
        SQL.bindValue(":supervisor", _supervisor)
        SQL.bindValue(":enrollDate", _enrollDate)

        if not SQL.exec():
            raise AccessDeniedError("Query error", SQL.lastError().text())

        else:
            SQL.exec_("SELECT name, professor, enrollDate FROM subject_test WHERE chartNum = LAST_INSERT_ID()")
            if SQL.next():
                newSubjectInfo = {
                    'chartNum': SQL.lastInsertId(),
                    'name': SQL.value(0),
                    'professor': SQL.value(1),
                    'searchFrom': SQL.value(2),
                    'searchTo': SQL.value(2)
                }
                dao = SupervisorDAO()
                dao.justEnroll = newSubjectInfo
                print("dao start")
                print(newSubjectInfo)
                print(dao.je_chartNum, dao.je_name, dao.je_professor)
                print("dao ends")

                cls.getInstance().EnrollSuccessSignal.emit()
                return True

        return False

    @classmethod
    def delete(cls, _chartNum):
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare("DELETE FROM subject_test WHERE chartNum = :chartNum")
        SQL.bindValue(":chartNum", _chartNum)

        if not SQL.exec():
            raise AccessDeniedError("Query error", SQL.lastError().text())

        else:
            return True

    @classmethod
    def checkChartNumExists(cls, _chartNum):
        '''Raise Error if chartNum already exists. If not, return False'''
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare("SELECT * FROM subject_test WHERE chartNum = :_chartNum")
        SQL.bindValue(":_chartNum", _chartNum)

        if not SQL.exec():
            raise AccessDeniedError("Query error", SQL.lastError().text())

        if SQL.next():
            raise ChartNumAlreadyExistsError("User ID already exists")

        return False
