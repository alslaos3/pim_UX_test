import uuid

import numpy as np
from PySide6.QtCore import QObject, QDate, Signal, Qt
from PySide6.QtSql import QSqlQuery, QSqlDatabase

from . import SelectedSubjectData
from .user_dao import UserDAO
from .supervisor_dao import SupervisorDAO


class ChartNumAlreadyExistsError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class SaveDAO(QObject):
    EnrollSuccessSignal = Signal()
    DeleteSuccessSignal = Signal()
    _db = None
    _instance = None

    def __init__(self):
        super(SaveDAO, self).__init__()

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
    def saveMeasurementData(cls, _chartNum: str, intensity: np.ndarray):
        # UUID 생성하고 파일 이름으로 사용
        file_uuid = uuid.uuid4()
        file_name = f"{file_uuid}.npy"
        # NumPy 배열을 파일로 저장
        np.save(file_name, intensity)

        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare("INSERT INTO measurement_test (chartNum, measurementDate, uuid) VALUES (:chartNum, NOW(), :uuid)")
        SQL.bindValue(":chartNum", _chartNum)
        SQL.bindValue(":uuid", file_name)

        SelectedSubjectData.setMeasurementDate(QDate.currentDate())
        SelectedSubjectData.setUUID(file_name)

        # 쿼리 실행
        if not SQL.exec():
            raise Exception('Query Error: ' + SQL.lastError().text())

        print(f"Data for chart number {_chartNum} has been saved successfully.")

    @classmethod
    def savePredictionData(cls, _chartNum: str, _uuid: str, diagnosisResult: int):
        print("This is savePredictionData")
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)

        # 오늘 날짜를 문자열 형태로 가져오기
        diagnosisDate = QDate.currentDate().toString(Qt.ISODate)

        # 업데이트 쿼리를 준비
        SQL.prepare(
            "UPDATE measurement_test SET diagnosisDate = :diagnosisDate, diagnosisResult = :diagnosisResult "
            "WHERE chartNum = :chartNum AND uuid = :uuid")

        SQL.bindValue(":chartNum", _chartNum)
        SQL.bindValue(":uuid", _uuid)
        SQL.bindValue(":diagnosisDate", diagnosisDate)
        SQL.bindValue(":diagnosisResult", diagnosisResult)
        if not SQL.exec_():
            print(SQL.lastError().text())  # 오류 메시지 출력


