import csv
from datetime import datetime
import numpy as np
from modules.spectrometerFocusController.deviceAPIs import Laser, Spectrometer, Stage
from modules.spectrometerFocusController.focusController import FocusController
from PySide6.QtCore import QObject, Signal, Slot

TAG = "실제 기기 테스트 : "
TIME = datetime.now


def use_mm(value):
    return value / 1000


def use_um(value):
    return value / 1000000


def m_to_Mm(value):
    return int(value * 1000000)


stageSettings = {
    "bottom": use_mm(3),
    "top": use_mm(17),
    "maxVelocity": use_mm(1),
    "acceleration": use_mm(1)
}


class Status:
    DEFAULT = 0
    IDLE = 1
    CLOSING = 2
    CLOSED = 3

    @classmethod
    def get_status(cls, code):
        status_dict = {
            cls.DEFAULT: "DEFAULT",
            cls.IDLE: "IDLE",
            cls.CLOSING: "CLOSING",
            cls.CLOSED: "CLOSED",
        }
        return status_dict.get(code, "UNKNOWN")


class FocusControllerExam(QObject):
    focusController = FocusController(testing=True)
    focusController.setStartPosition(stageSettings["top"])

    laserConnected = False
    specConnected = False
    stageConnected = False

    laser = Laser()
    spec = Spectrometer()
    stage = Stage(1)

    status = Status.DEFAULT

    statusMessage = Signal(str)
    logMessage = Signal(str)

    ''' 모듈 통신 '''
    reqMoveStage = Signal(int, float)
    reqStopStage = Signal(int)

    ''' 포커스 컨트롤러 통신 '''
    initFocusingSignal = Signal()
    resumeFocusingSignal = Signal()
    pauseFocusingSignal = Signal()
    restartFocusingSignal = Signal()
    resSetIntegrationTime = Signal()

    resDeviceConnected = Signal(bool)
    resMoveStage = Signal(float)
    resStopStage = Signal()
    resGetSpectrum = Signal(np.ndarray)
    exePositionOver = Signal(float, float)

    closeAbleSignal = Signal()

    def __init__(self):
        super().__init__()

    def initConnect(self):
        # 포커스 컨트롤러 -> 테스트 모듈 요청
        self.focusController.reqSetIntegrationTime.connect(self.onReqSetIntegrationTime)
        self.focusController.reqDeviceConnected.connect(self.onReqDeviceConnected)
        self.focusController.reqConnectDevice.connect(self.onReqConnectDevice)
        self.focusController.reqMoveStage.connect(self.onReqMoveStage)
        self.focusController.reqStopStage.connect(self.onReqStopStage)

        # 포커스 컨트롤러 -> 일반 시그널
        self.focusController.normalLogSignal.connect(self.log_print)
        self.focusController.alreadyRunningSignal.connect(self.onAlreadyRunningSignal)
        self.focusController.alreadyStoppedSignal.connect(self.onAlreadyStoppedSignal)
        self.focusController.collectingCompleteSignal.connect(self.onCollectingCompleteSignal)
        self.focusController.focusCompleteSignal.connect(self.onFocusCompleteSignal)
        self.focusController.focusDisabledErr.connect(self.onfocusDisabledErr)

        # 테스트 모듈 -> 포커스 컨트롤러 응답
        self.resDeviceConnected.connect(self.focusController.onResDeviceConnected)
        self.resSetIntegrationTime.connect(self.focusController.onResSetIntegrationTime)
        self.resMoveStage.connect(self.focusController.onResMoveStage)
        self.resStopStage.connect(self.focusController.onResStopStage)
        self.resGetSpectrum.connect(self.focusController.onResGetSpectrum)
        self.exePositionOver.connect(self.focusController.onExePositionOver)

        # 테스트 모듈 -> 포커스 컨트롤러 요청
        self.initFocusingSignal.connect(self.focusController.initFocusing)
        self.resumeFocusingSignal.connect(self.focusController.resumeFocusing)
        self.pauseFocusingSignal.connect(self.focusController.pauseFocusing)
        self.restartFocusingSignal.connect(self.focusController.restartFocusing)

        # 테스트 모듈 -> 기기 요청
        self.reqMoveStage.connect(self.stage.move)
        self.reqStopStage.connect(self.stage.stopMove)

        # 기기 -> 일반 시그널
        self.stage.normalLogSignal.connect(self.onNormalLogSignal)
        self.stage.stageMovedSignal.connect(self.onResMoveStage)
        self.stage.stoppedSignal.connect(self.onResStopStage)
        self.stage.errCannotDetect.connect(self.onErrorSignal)
        self.stage.errPositionLimit.connect(self.onErrorSignal)
        self.spec.resGetSpectrum.connect(self.onResGetSpectrum)
        self.spec.integrationTimeSettedSignal.connect(self.onResSetIntegrationTime)

        # 기기 -> 테스트 모듈 응답
        self.laser.connectedSignal.connect(self.onLaserConnected)
        self.spec.connectedSignal.connect(self.onSpectrometerConnected)
        self.stage.connectedSignal.connect(self.onStageConnected)

        self.laser.checkConnected()
        self.spec.checkConnected()
        self.stage.checkConnected()

        self.initDevice()

    def initDevice(self):
        self.log_print(f"{TIME()} {TAG} init")

        if self.laserConnected:
            self.laser.turnOn()
        else:
            self.log_print(f"{TIME()} {TAG} 레이저 초기화 실패")
        if self.stageConnected:
            self.stage.setLimit(0, stageSettings["bottom"], stageSettings["top"])
            self.stage.setUpVelocity(
                0,
                stageSettings["maxVelocity"],
                stageSettings["acceleration"]
            )
        else:
            self.log_print(f"{TIME()} {TAG} 스테이지 초기화 실패")
        if self.specConnected:
            self.spec.setIntegrationTime(500000)
        else:
            self.log_print(f"{TIME()} {TAG} 스펙트로 미터 초기화 실패")

        self.setStatus(Status.IDLE)
        self.initFocusing()

    def close(self):
        print("exam close")
        if self.spec.isProcessing:
            print("processing")
            self.setStatus(Status.CLOSING)
            self.spec.stopGetSpectrum()
            return

        if self.status != Status.CLOSED:
            print("set status")
            self.spec.stopGetSpectrum()
            self.spec.close()
            self.laser.close()
            self.stage.close()
            self.setStatus(Status.CLOSED)

        self.closeAbleFlag = True
        self.closeAbleSignal.emit()

    def setStatus(self, status):
        self.status = status

    @Slot(str, bool)
    def log_print(self, message, log=True):
        self.statusMessage.emit(message)
        if log:
            self.logMessage.emit(message)

    @Slot(str)
    def onNormalLogSignal(self, msg):
        self.log_print(msg)

    @Slot(int)
    def onReqSetIntegrationTime(self, value):
        self.spec.setIntegrationTime(value)

    ''' 모듈 '''

    def initFocusing(self):
        self.log_print(f"\n{TIME()} {TAG} initFocusing 버튼")
        self.initFocusingSignal.emit()

    @Slot(bool)
    def onLaserConnected(self, isConnected):
        if isConnected:
            self.log_print(f"{TIME()} {TAG} 레이저 연결됨")
            self.laserConnected = True
        else:
            self.log_print(f"{TIME()} {TAG} 레이저 연결 실패")
            self.laserConnected = False

    @Slot(bool)
    def onSpectrometerConnected(self, isConnected):
        if isConnected:
            self.log_print(f"{TIME()} {TAG} 스펙트로미터 연결됨")
            self.specConnected = True
        else:
            self.log_print(f"{TIME()} {TAG} 스펙트로미터 연결 실패")
            self.specConnected = False

    @Slot(list)
    def onStageConnected(self, stageConnected):
        if stageConnected[0]:
            self.log_print(f"{TIME()} {TAG} 스테이지 연결됨")
            self.stageConnected = True
        else:
            self.log_print(f"{TIME()} {TAG} 스테이지 연결 실패")
            self.stageConnected = False

    @Slot(str)
    def onErrorSignal(self, msg):
        self.log_print(f"{TIME()} {TAG} {msg}")

    ''' 콜렉팅 '''

    @Slot(dict)
    def onCollectingCompleteSignal(self, collectingDatas):
        time = f"{TIME().strftime('%y%m%d_%H%M%S')}"
        with open(f"collecting_{time}.csv", "w", newline="") as f:
            w = csv.writer(f)
            headers = ["integration time"] + list(collectingDatas.keys())
            w.writerow(headers)

            length = len(list(collectingDatas.values())[0])
            rows = [[i] for i in range(length)]
            for data in collectingDatas.values():
                for idx, value in enumerate(data):
                    rows[idx].append(value)
            print("완료\n", rows)
            w.writerows(rows)

        # print("완료\n", collectingDatas)

    ''' 포커싱 '''

    # 베이직 시그널
    def resumeFocusing(self):
        self.log_print(f"\n{TIME()} {TAG} resumeFocusing 버튼")
        self.resumeFocusingSignal.emit()

    def pauseFocusing(self):
        self.log_print(f"\n{TIME()} {TAG} pauseFocusing 버튼")
        self.pauseFocusingSignal.emit()

    def restartFocusing(self):
        self.log_print(f"\n{TIME()} {TAG} restartFocusing 버튼")
        self.restartFocusingSignal.emit()

    # 베이직 시그널 응답
    @Slot()
    def onAlreadyRunningSignal(self):
        self.log_print(f"\n{TIME()} {TAG} alreadyRunningSignal 발생\n")

    @Slot()
    def onAlreadyStoppedSignal(self):
        self.log_print(f"\n{TIME()} {TAG} alreadyStoppedSignal 발생\n")

    @Slot(np.ndarray)
    def onFocusCompleteSignal(self, intensities):
        self.log_print("=" * 80)
        self.log_print(f"{TIME()} {TAG} 포커싱 완료")

    # 기기 응답에 따라 포커싱알고리즘에 응답
    @Slot()
    def onReqDeviceConnected(self):
        self.log_print(
            f"{TIME()} {TAG} 기기 연결 확인 요청 감지 laser: {self.laserConnected}, spec: {self.specConnected}, stage: {self.stageConnected}\n")
        if self.laserConnected and self.specConnected and self.stageConnected:
            self.resDeviceConnected.emit(True)
        else:
            self.resDeviceConnected.emit(False)

    @Slot()
    def onReqConnectDevice(self):
        self.log_print(f"{TIME()} {TAG} 기기 연결 요청 감지\n")
        ''' 
        Todo: 연결안된 기기 파악하여 연결
        '''

    @Slot(float)
    def onReqMoveStage(self, position):
        self.log_print(f"{TIME()} {TAG} 스테이지 이동 요청 감지: {round(position * 1000, 6)}", False)
        self.reqMoveStage.emit(0, position)

    def onReqStopStage(self):
        self.log_print(f"\n{TIME()} {TAG} 기기 중지 요청 감지\n")
        if self.stage.isMoving(0):
            self.reqStopStage.emit(0)
            return

    @Slot(np.ndarray)
    def onResGetSpectrum(self, spectrumInfo):
        if self.status == Status.IDLE:
            self.resGetSpectrum.emit(spectrumInfo)
            return

        if self.status == Status.CLOSING:
            self.close()

    def onResSetIntegrationTime(self):
        self.resSetIntegrationTime.emit()

    # 포커싱알고리즘 응답에 따라 기기에 응답
    @Slot(int, float)
    def onResMoveStage(self, idx, position):
        self.log_print(f"{TIME()} {TAG} 스테이지 #{idx} 이동 완료", False)
        self.resMoveStage.emit(position)

    @Slot(int, float)
    def onResStopStage(self, idx, position):
        # self.log_print(f"{TIME()} {TAG} 스테이지 #{idx} 정지")
        self.resStopStage.emit()

    @Slot(str)
    def onfocusDisabledErr(self, errMsg):
        self.log_print(f"{TIME()} {TAG} 에러 발생 : {errMsg}")

    @Slot(bool)
    def isSpecimenExists(self, exist):
        if exist:
            return True
        else:
            return False


class ControllerAPI(QObject):
    exam = FocusControllerExam()  # 실제 사용

    def __init__(self, parent=None):
        super().__init__(parent)
        self.exam.initConnect()

        print("ControllerAPI OPENED!!!")

    def closeEvent(self, event):
        if hasattr(self.exam, "closeAbleFlag") and self.exam.closeAbleFlag:
            self.exam.close()
            event.accept()
        else:
            self.exam.close()
            event.ignore()

    # Focusing
    def initFocusing(self):
        self.exam.initFocusing()

    def resumeFocusing(self):
        self.exam.resumeFocusing()

    def pauseFocusing(self):
        self.exam.pauseFocusing()

    def restartFocusing(self):
        self.exam.restartFocusing()

    # blank test
    # -> 시료가 있니없니 (기본) + focusing -> 결과나옴
    # measure
    # -> 시료가 있니없니 (기본) + focusing + "그래프 실시간 그림 (spectrum)" -> 결과나옴
