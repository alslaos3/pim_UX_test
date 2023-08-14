from PySide6.QtCore import QObject, QDate, Signal
from PySide6.QtSql import QSqlQuery, QSqlDatabase
from .hashing import Hashing
from .supervisor_dao import SupervisorDAO


class UserAlreadyExistsError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserDAO(QObject):
    logInSuccessSignal = Signal()
    logOutSuccessSignal = Signal()
    signUpSuccessSignal = Signal(str)
    _db = None
    _instance = None

    def __init__(self):
        super(UserDAO, self).__init__()

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def connectDatabase(cls):
        if cls._db is None:
            db = QSqlDatabase.addDatabase("QODBC")
            db.setDatabaseName("DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER=localhost;DATABASE=testdb;UID=root;PWD=ekqdms1")
            if db.open():
                cls._db = db
            else:
                raise AccessDeniedError("Could not open database connection")
        return cls._db

    @classmethod
    def signIn(cls, _username: str, _password: str, _rememberMe: bool):
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare("SELECT passwordHash, name, birthDate, gender, organization, email FROM users WHERE userId = :userId")
        SQL.bindValue(":userId", _username)

        if not SQL.exec():
            raise AccessDeniedError('Query Error: ' + SQL.lastError().text())

        if SQL.next():
            _hashedPassword = SQL.value(0)
            _inputPassword = Hashing.hash_password(_password)

            if _hashedPassword == _inputPassword:
                infoSupervisor = {
                    'username': _username,
                    'name': SQL.value(1),
                    'birthDate': SQL.value(2),
                    'gender': SQL.value(3),
                    'organization': SQL.value(4),
                    'email': SQL.value(5),
                    'remember': _rememberMe
                }

                dao = SupervisorDAO()
                dao.supervisorInfo = infoSupervisor

                cls.getInstance().logInSuccessSignal.emit()
                return True

        return False

    @classmethod
    def signUp(cls, _username: str, _password, _name: str, _birthDate: str, _gender: str, _organization: str, _email: str):
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare(
            "INSERT INTO users (userId, passwordHash, name, birthDate, gender, organization, email)"
            "VALUES (:userId, :passwordHash, :name, :birthDate, :gender, :organization, :email)")
        SQL.bindValue(":userId", _username)
        SQL.bindValue(":passwordHash", Hashing.hash_password(_password))
        SQL.bindValue(":name", _name)
        SQL.bindValue(":birthDate", _birthDate)
        SQL.bindValue(":gender", _gender)
        SQL.bindValue(":organization", _organization)
        SQL.bindValue(":email", _email)

        if not SQL.exec():
            raise AccessDeniedError("Query error", SQL.lastError().text())

        else:
            cls.getInstance().signUpSuccessSignal.emit(_username)
            return True

    @classmethod
    def checkUserExists(cls, _userId):
        """Raise Error if user already exists. If not, return False"""
        cls.connectDatabase()
        SQL = QSqlQuery(cls._db)
        SQL.prepare("SELECT * FROM users WHERE userId = :_userId")
        SQL.bindValue(":_userId", _userId)

        if not SQL.exec():
            raise AccessDeniedError("Query error", SQL.lastError().text())

        if SQL.next():
            raise UserAlreadyExistsError("User ID already exists")

        return False

    @classmethod
    def signOut(cls, _rememberMe):
        if _rememberMe:
            cls.getInstance().logOutSuccessSignal.emit()
            return True

        elif not _rememberMe:
            dao = SupervisorDAO()
            dao.settings.clear()
            dao.settings.sync()
            cls.getInstance().logOutSuccessSignal.emit()
            return True

        return False
