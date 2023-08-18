from PySide6.QtCore import QPropertyAnimation, Property, Signal, Qt, Slot
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, QPushButton

from dao.controller_dao import ControllerDAO
from .blankTestPage import BlankTestPage
from .subjectListPage import SubjectListPage
from .measurementListPage import MeasurementListPage
from .measurementPage import MeasurementPage
from .predictionListPage import PredictionListPage
from .predictionPage import PredictionPage
from .search_engine import SearchEngineWidget
from .subjectRecordTable import SubjectRecordTable
from .signOutWidget import SignOutWidget
from dao.supervisor_dao import SupervisorDAO


class StackedWidget(QStackedWidget):
    def __init__(self):
        super(StackedWidget, self).__init__()
        self._animationValue = 0.0
        self.animation = QPropertyAnimation(self, b"animationValue")
        self.animation.valueChanged.connect(self.animationValueChanged)

    def setCurrentIndex(self, index):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        super().setCurrentIndex(index)

    def animationValueChanged(self, value):
        self.repaint()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.animation.state() == QPropertyAnimation.Running:
            painter = QPainter(self)
            alpha = int(self.animationValue * 255)
            painter.fillRect(self.rect(), QColor(0, 0, 0, alpha))

    def getAnimationValue(self):
        return self._animationValue

    def setAnimationValue(self, value):
        self._animationValue = value

    animationValue = Property(float, getAnimationValue, setAnimationValue)


class ClickableLabel(QLabel):
    clicked = Signal()
    state = bool

    def __init__(self, text=None, parent=None):
        super(ClickableLabel, self).__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if self.state:
            self.clicked.emit()
        else:
            pass

    def setEnabled(self, arg__1: bool):
        if arg__1:
            self.state = True
        else:
            self.state = False

    def setDisabled(self, arg__1: bool):
        if arg__1:
            self.state = False
        else:
            self.state = True


class MainPage(QWidget):
    _history = []
    signOutSignal = Signal()
    infoDict = {}

    def __init__(self):
        super(MainPage, self).__init__()

        self.supervisorDAO = SupervisorDAO()
        self.infoSupervisor = self.supervisorDAO.supervisorInfo
        self.stackedWidget = StackedWidget()

        self.blankTestPage = BlankTestPage()
        self.stackedWidget.addWidget(self.blankTestPage)

        self.subjectListPage = SubjectListPage()
        self.stackedWidget.addWidget(self.subjectListPage)

        self.measurementListPage = MeasurementListPage()
        self.stackedWidget.addWidget(self.measurementListPage)

        self.predictionListPage = PredictionListPage()
        self.stackedWidget.addWidget(self.predictionListPage)

        self.measurementPage = MeasurementPage()
        self.stackedWidget.addWidget(self.measurementPage)

        self.predictionPage = PredictionPage()
        self.stackedWidget.addWidget(self.predictionPage)

        self.btnBlankTest = ClickableLabel("Blank Test")
        self.btnBlankTest.clicked.connect(self.setBlankTest)

        self.btnSubjectList = ClickableLabel("Subject List")
        self.btnSubjectList.clicked.connect(self.setSubjectList)

        self.btnMeasurementList = ClickableLabel("Measurement List")
        self.btnMeasurementList.clicked.connect(self.setMeasurementList)

        self.btnPredictionList = ClickableLabel("Prediction List")
        self.btnPredictionList.clicked.connect(self.setPredictionList)

        lblSupervisorName = QLabel(self.supervisorDAO.sv_name)
        lblSupervisorBirthDate = QLabel(self.supervisorDAO.sv_birthDate.toString(Qt.ISODate))
        lblSupervisorGender = QLabel(self.supervisorDAO.sv_gender)
        lblSupervisorOrg = QLabel(self.supervisorDAO.sv_organization)
        lblSupervisorEmail = QLabel(self.supervisorDAO.sv_email)
        self.btnSignOut = SignOutWidget()

        vbox = QVBoxLayout()

        hbox = QHBoxLayout()
        gBoxSupervisor = QGroupBox()
        hboxSupervisor = QHBoxLayout()
        hboxSupervisor.addWidget(lblSupervisorName)
        hboxSupervisor.addWidget(lblSupervisorBirthDate)
        hboxSupervisor.addWidget(lblSupervisorGender)
        hboxSupervisor.addWidget(lblSupervisorOrg)
        hboxSupervisor.addWidget(lblSupervisorEmail)
        hboxSupervisor.addWidget(self.btnSignOut)
        gBoxSupervisor.setLayout(hboxSupervisor)

        hbox.addWidget(self.btnBlankTest)
        hbox.addWidget(self.btnSubjectList)
        hbox.addWidget(self.btnMeasurementList)
        hbox.addWidget(self.btnPredictionList)

        vbox.addLayout(hbox)
        vbox.addWidget(self.stackedWidget)
        vbox.addWidget(gBoxSupervisor)

        self.setBlankTest()

        self.setLayout(vbox)

        self.subjectListPage.subjectListWidget.btnMeasurement.clicked.connect(self.setMeasurement)
        self.measurementPage.btnPredict.clicked.connect(self.setPrediction)
        self.measurementListPage.btnPredict.clicked.connect(self.setPrediction)
        self.measurementPage.btnBack.clicked.connect(self.setBackClicked)
        self.predictionPage.btnBack.clicked.connect(self.setBackClicked)
        # ControllerDAO.getInstance().getAPI().exam.focusController.statusSignal.connect(self.getStatus)
        # ControllerDAO.getInstance().getAPI().exam.focusController.emitStatusSignal()

    @Slot(str)
    def getStatus(self, status):
        print(status)

    def setWidgetIndex(self, index, btnCurrent, btnOthers):
        self.stackedWidget.setCurrentIndex(index)
        self._history.append(index)
        font = btnCurrent.font()
        font.setPointSize(20)  # 원하는 크기로 설정
        btnCurrent.setFont(font)
        btnCurrent.setDisabled(True)
        for btn in btnOthers:
            font = btn.font()
            font.setPointSize(10)  # 원래의 크기로 설정
            btn.setFont(font)
            btn.setEnabled(True)

    def setBlankTest(self):
        self.setWidgetIndex(0, self.btnBlankTest, [self.btnSubjectList, self.btnMeasurementList, self.btnPredictionList])

    def setSubjectList(self):
        self.setWidgetIndex(1, self.btnSubjectList, [self.btnBlankTest, self.btnMeasurementList, self.btnPredictionList])

    def setMeasurementList(self):
        self.setWidgetIndex(2, self.btnMeasurementList, [self.btnBlankTest, self.btnSubjectList, self.btnPredictionList])

    def setPredictionList(self):
        self.setWidgetIndex(3, self.btnPredictionList, [self.btnBlankTest, self.btnSubjectList, self.btnMeasurementList])

    def setMeasurement(self):
        self.stackedWidget.setCurrentIndex(4)
        self.measurementPage.measurementBtnClicked.emit()

    def setPrediction(self):
        self.stackedWidget.setCurrentIndex(5)
        self.predictionPage.predictionBtnClicked.emit()

    def setBackClicked(self):
        prev = self._history[-1]
        if prev == 0:
            self.setBlankTest()
        elif prev == 1:
            self.setSubjectList()
        elif prev == 2:
            self.setMeasurementList()
        elif prev == 3:
            self.setPredictionList()
