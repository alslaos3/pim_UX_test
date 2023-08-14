from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from dao import SubjectDAO
from .enrollWidget import EnrollWidget
from .subjectListWidget import SubjectListWidget


class SubjectListPage(QWidget):

    def __init__(self):
        super(SubjectListPage, self).__init__()

        SubjectDAO.getInstance().EnrollSuccessSignal.connect(self.setSubjectListWidget)

        self.subjectListWidget = SubjectListWidget()
        self.enrollWidget = EnrollWidget()
        self.stackedWidget = QStackedWidget()

        self.stackedWidget.addWidget(self.subjectListWidget)
        self.stackedWidget.addWidget(self.enrollWidget)
        self.subjectListWidget.btnNewEnroll.clicked.connect(self.setEnrollWidget)
        self.enrollWidget.btnBack.clicked.connect(self.btnBackClicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.stackedWidget)
        self.setLayout(vbox)

    def btnBackClicked(self):
        self.setSubjectListWidget()
        self.enrollWidget.clearForm()

    def setWidgetIndex(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def setSubjectListWidget(self):
        self.setWidgetIndex(0)

    def setEnrollWidget(self):
        self.setWidgetIndex(1)
