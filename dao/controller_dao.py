import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, QTimer, Slot
from modules.controllerAPI import ControllerAPI
import threading


class ControllerDAO(QObject):
    _controller_api = None
    _last_measurement = None
    _specimen_is_exist = None
    _instance = None
    _status = "NORMAL"
    _focused_intensity = None
    _init_complete = False

    @classmethod
    def getAPI(cls):
        if cls._controller_api is None:
            cls._controller_api = ControllerAPI()
        return cls._controller_api

    @classmethod
    def initFocusing(cls):
        cls._init_complete = False
        api = cls.getAPI()
        return api.initFocusing()

    @classmethod
    def startFocusing(cls):
        cls._init_complete = False
        api = cls.getAPI()
        return api.resumeFocusing()

    @classmethod
    def pauseFocusing(cls):
        api = cls.getAPI()
        return api.pauseFocusing()

    @classmethod
    def defaultFocusing(cls):
        cls._init_complete = False
        api = cls.getAPI()
        return api.restartFocusing()

    @classmethod
    def getStatus(cls):
        api = cls.getAPI()
        cls._status = api.exam.status
        return cls._status


