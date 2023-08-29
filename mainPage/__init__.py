from PySide6.QtCore import QPropertyAnimation, Property, Signal, Qt, Slot
from PySide6.QtGui import QPainter, QColor, Qt, QIcon, QAction
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, \
    QPushButton, QTabWidget, QTabBar, QButtonGroup, QToolBar, QFormLayout

from dao.controller_dao import ControllerDAO
from .alertThread import AlertThread
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


class MainPage(QWidget):
    _history = []
    signOutSignal = Signal()
    supervisorSignal = Signal(str, str, str, str, str)
    infoDict = {}

    def __init__(self):
        super(MainPage, self).__init__()

        self.supervisorDAO = SupervisorDAO()
        self.infoSupervisor = self.supervisorDAO.supervisorInfo

        self.stackedWidget = QStackedWidget()

        self.blankTestPage = BlankTestPage()
        self.subjectListPage = SubjectListPage()
        self.measurementListPage = MeasurementListPage()
        self.predictionListPage = PredictionListPage()

        self.stackedWidget.addWidget(self.blankTestPage)
        self.stackedWidget.addWidget(self.subjectListPage)
        self.stackedWidget.addWidget(self.measurementListPage)
        self.stackedWidget.addWidget(self.predictionListPage)

        # self.statusWidget = QWidget()

        hboxGraph = QHBoxLayout()
        hboxGraph.addWidget(self.measurementListPage.graphWidget, 1)
        hboxGraph.addWidget(self.predictionListPage.graphWidget, 1)

        gboxTab = QGroupBox()
        btnSubjectList = QPushButton("Subject")
        btnSubjectList.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        btnMeasurement = QPushButton("Measurement")
        btnMeasurement.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        btnPrediction = QPushButton("Prediction")
        btnPrediction.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        formStatus = QFormLayout()
        formStatus.addRow("a: ", QLabel("test"))
        formStatus.addRow("b: ", QLabel("test"))
        formStatus.addRow("c: ", QLabel("test"))
        formStatus.addRow("d: ", QLabel("test"))
        formStatus.addRow("e: ", QLabel("test"))
        formStatus.addRow("f: ", QLabel("test"))

        gboxStatus = QGroupBox()
        gboxStatus.setLayout(formStatus)

        vboxBtn = QVBoxLayout()
        vboxBtn.addWidget(btnSubjectList)
        vboxBtn.addWidget(btnMeasurement)
        vboxBtn.addWidget(btnPrediction)
        gboxTab.setLayout(vboxBtn)

        vboxTab = QVBoxLayout()
        vboxTab.addWidget(gboxTab)
        vboxTab.addWidget(gboxStatus)
        vboxTab.addStretch()

        hboxMain = QHBoxLayout()
        hboxMain.addLayout(vboxTab)
        hboxMain.addWidget(self.stackedWidget)

        vbox = QVBoxLayout()
        vbox.addLayout(hboxMain)
        vbox.addLayout(hboxGraph)
        self.setLayout(vbox)

        # self.measurementPage = MeasurementPage()
        # self.tabWidget.addWidget(self.measurementPage)
        #
        # self.predictionPage = PredictionPage()
        # self.tabWidget.addWidget(self.predictionPage)
        #
        # self.btnSignOut = SignOutWidget()

    # def show(self):
    #     self.supervisorSignal.emit(self.supervisorDAO.sv_name,
    #                                self.supervisorDAO.sv_birthDate.toString(Qt.ISODate),
    #                                self.supervisorDAO.sv_gender,
    #                                self.supervisorDAO.sv_organization,
    #                                self.supervisorDAO.sv_email)
