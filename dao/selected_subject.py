class NoDataFoundedError(Exception):
    pass


class SelectedSubjectData:
    _data = {}

    @classmethod
    def setData(cls, row_data):
        cls._data = row_data

    @classmethod
    def getData(cls):
        if not cls._data:
            raise NoDataFoundedError
        else:
            return cls._data

    @classmethod
    def getChartNum(cls):
        if not cls._data.get('chartNum'):
            raise NoDataFoundedError
        else:
            return cls._data.get('chartNum')

    @classmethod
    def getName(cls):
        if not cls._data.get('name'):
            raise NoDataFoundedError
        else:
            return cls._data.get('name')

    @classmethod
    def getBirthDate(cls):
        if not cls._data.get('birthDate'):
            raise NoDataFoundedError
        else:
            return cls._data.get('birthDate')

    @classmethod
    def getGender(cls):
        if not cls._data.get('gender'):
            raise NoDataFoundedError
        else:
            return cls._data.get('gender')

    @classmethod
    def getProfessor(cls):
        if not cls._data.get('professor'):
            raise NoDataFoundedError
        else:
            return cls._data.get('professor')

    @classmethod
    def getSupervisor(cls):
        if not cls._data.get('supervisor'):
            raise NoDataFoundedError
        else:
            return cls._data.get('supervisor')

    @classmethod
    def getMeasurementDate(cls):
        if not cls._data.get('measurementDate'):
            raise NoDataFoundedError
        else:
            return cls._data.get('measurementDate')

    @classmethod
    def getUUID(cls):
        if not cls._data.get('uuid'):
            raise NoDataFoundedError
        else:
            return cls._data.get('uuid')
