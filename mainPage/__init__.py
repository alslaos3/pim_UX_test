from PySide6.QtCore import QPropertyAnimation, Property, Signal, Qt, Slot
from PySide6.QtGui import QPainter, QColor, Qt, QIcon, QAction
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, \
    QPushButton, QTabWidget, QTabBar, QButtonGroup, QToolBar

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

        self.tabWidget = QTabWidget()

        self.blankTestPage = BlankTestPage()
        self.tabWidget.addTab(self.blankTestPage, QIcon("../images/icon_example.png"), "Blank Test")

        self.subjectListPage = SubjectListPage()
        self.tabWidget.addTab(self.subjectListPage, QIcon("../images/icon_example.png"), "asdfsa")

        self.measurementListPage = MeasurementListPage()
        self.tabWidget.addTab(self.measurementListPage, QIcon("../images/icon_example.png"), "dfds")

        self.predictionListPage = PredictionListPage()
        self.tabWidget.addTab(self.predictionListPage, QIcon("../images/icon_example.png"), "dsfsd")

        # self.statusWidget = QWidget()

        hboxGraph = QHBoxLayout()
        hboxGraph.addWidget(self.measurementListPage.graphWidget)
        hboxGraph.addWidget(self.predictionListPage.graphWidget)

        vboxTab = QVBoxLayout()
        vboxTab.addWidget(self.tabWidget)
        gboxTab = QGroupBox()
        gboxTab.setLayout(vboxTab)

        vbox = QVBoxLayout()
        vbox.addWidget(gboxTab)
        vbox.addLayout(hboxGraph)
        self.setLayout(vbox)

        # self.measurementPage = MeasurementPage()
        # self.tabWidget.addWidget(self.measurementPage)
        #
        # self.predictionPage = PredictionPage()
        # self.tabWidget.addWidget(self.predictionPage)
        #
        # self.btnSignOut = SignOutWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabWidget)

        self.setLayout(vbox)

    # def show(self):
    #     self.supervisorSignal.emit(self.supervisorDAO.sv_name,
    #                                self.supervisorDAO.sv_birthDate.toString(Qt.ISODate),
    #                                self.supervisorDAO.sv_gender,
    #                                self.supervisorDAO.sv_organization,
    #                                self.supervisorDAO.sv_email)
