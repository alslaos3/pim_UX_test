import datetime

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGroupBox, QComboBox, QHBoxLayout, \
    QRadioButton, QButtonGroup, \
    QMessageBox
from PySide6.QtCore import Qt, Signal, QDate, QRegularExpression

from dao import SubjectDAO
from dao.supervisor_dao import SupervisorDAO
from modules.reg_ex import RegEx
from modules.check_reg_ex import Check

VK_CAPITAL = 0x14


class EnrollWidget(QWidget):
    btnID = None

    def __init__(self):
        super().__init__()

        self.supervisorDAO = SupervisorDAO()

        self.btnBack = QPushButton("←")
        self.hboxBack = QHBoxLayout()
        self.hboxBack.addWidget(self.btnBack)
        self.hboxBack.addStretch(1)

        lblChartNum = QLabel("차트번호")
        self.editChartNum = QLineEdit()
        self.editChartNum.setPlaceholderText("차트번호를 입력해주세요.")

        lblName = QLabel("성명")
        self.editName = QLineEdit()
        self.editName.setPlaceholderText("성명을 입력해주세요.")

        lblBirthDate = QLabel("생년월일")
        self.hBoxBirthDate = QHBoxLayout()

        self.editYear = QLineEdit()
        self.editYear.setPlaceholderText("년(4자)")
        self.editYear.setMaxLength(4)

        self.editMonth = QComboBox()
        self.editMonth.setPlaceholderText("월")
        self.editMonth.addItems(str(mm) for mm in range(1, 13))

        self.editDay = QLineEdit()
        self.editDay.setPlaceholderText("일")
        self.editDay.setMaxLength(2)

        self.hBoxBirthDate.addWidget(self.editYear, 1)
        self.hBoxBirthDate.addWidget(self.editMonth, 1)
        self.hBoxBirthDate.addWidget(self.editDay, 1)

        lblGender = QLabel("성별")
        btnMale = QRadioButton("남자")
        btnFemale = QRadioButton("여자")
        btnNone = QRadioButton("선택안함")
        self.btnGenderGroup = QButtonGroup()
        self.btnGenderGroup.addButton(btnMale, 0)
        self.btnGenderGroup.addButton(btnFemale, 1)
        self.btnGenderGroup.addButton(btnNone, 2)
        self.btnGenderGroup.button(2).setChecked(True)

        self.gBoxGenderGroup = QGroupBox()
        btnHBox = QHBoxLayout()
        btnHBox.addWidget(btnMale)
        btnHBox.addWidget(btnFemale)
        btnHBox.addWidget(btnNone)
        self.gBoxGenderGroup.setLayout(btnHBox)

        lblPhoneNum = QLabel("연락처")
        self.editPhoneNum = QLineEdit()
        self.editPhoneNum.setPlaceholderText("전화번호를 입력해주세요.")

        hboxProfessor = QHBoxLayout()
        lblProfessor = QLabel("담당교수")
        self.editProfessor = QComboBox()
        self.editProfessor.setPlaceholderText("담당교수를 선택해주세요.")
        self.editProfessor.addItem("담당교수 추가...")
        self.editProfessor.insertSeparator(1)
        self.editProfessor.addItems(SubjectDAO.getExistProfessors())
        self.addButton = QPushButton("확인")
        self.addButton.clicked.connect(self.addEditProfessor)
        self.addButton.hide()
        hboxProfessor.addWidget(self.editProfessor)
        hboxProfessor.addWidget(self.addButton)

        lblSupervisor = QLabel("사용자")
        self.editSupervisor = QLineEdit()
        self.editSupervisor.setText(self.supervisorDAO.sv_name)
        self.editSupervisor.setReadOnly(True)

        self.btnEnroll = QPushButton("등록하기")
        self.btnEnroll.clicked.connect(self.checkForm)

        self.editName.textEdited.connect(lambda: Check.checkValidityName(self.editName))
        self.editYear.textEdited.connect(lambda: Check.checkValidityBirthYear(self.editYear))
        self.editPhoneNum.textEdited.connect(lambda: Check.checkValidityPhoneNum(self.editPhoneNum))
        self.editChartNum.textEdited.connect(lambda: Check.checkValidityChartNum(self.editChartNum))

        self.editProfessor.currentIndexChanged.connect(self.onEditProfessorChanged)

        vbox = QVBoxLayout()

        gBoxPrivate = QGroupBox()
        vboxPrivate = QVBoxLayout()

        vboxPrivate.addWidget(lblChartNum)
        vboxPrivate.addWidget(self.editChartNum)

        vboxPrivate.addWidget(lblName)
        vboxPrivate.addWidget(self.editName)

        vboxPrivate.addWidget(lblBirthDate)
        vboxPrivate.addLayout(self.hBoxBirthDate)

        vboxPrivate.addWidget(lblGender)
        vboxPrivate.addWidget(self.gBoxGenderGroup)
        gBoxPrivate.setLayout(vboxPrivate)

        gBoxAddition = QGroupBox()
        vBoxAddition = QVBoxLayout()
        vBoxAddition.addWidget(lblPhoneNum)
        vBoxAddition.addWidget(self.editPhoneNum)
        vBoxAddition.addWidget(lblProfessor)
        vBoxAddition.addLayout(hboxProfessor)
        vBoxAddition.addWidget(lblSupervisor)
        vBoxAddition.addWidget(self.editSupervisor)
        gBoxAddition.setLayout(vBoxAddition)

        vbox.addLayout(self.hboxBack)
        vbox.addWidget(gBoxPrivate)
        vbox.addWidget(gBoxAddition)
        vbox.addWidget(self.btnEnroll)

        self.setLayout(vbox)

    def onEditProfessorChanged(self, index):
        if self.editProfessor.currentIndex() == 0:
            self.editProfessor.setEditable(True)
            self.editProfessor.setFocus()
            self.editProfessor.clearEditText()
            self.addButton.show()
        else:
            self.editProfessor.setEditable(False)
            self.addButton.hide()

    def addEditProfessor(self):
        custom_text = self.editProfessor.currentText()
        if custom_text and custom_text != "담당교수 추가..." and \
                custom_text not in [self.editProfessor.itemText(i) for i in range(self.editProfessor.count())]:
            self.editProfessor.insertItem(self.editProfessor.count(), custom_text)
            self.editProfessor.setCurrentText(custom_text)
            self.editProfessor.setEditable(False)
            self.addButton.hide()

    def checkForm(self):

        if self._chartNum == "" or len(str(self._chartNum)) != 9:
            self.editChartNum.setFocus()
            if self._chartNum == "":
                self.editChartNum.clear()
                self.editChartNum.setPlaceholderText("차트번호를 입력해주세요.")
            elif len(str(self._chartNum)) != 9:
                self.editChartNum.clear()
                self.editChartNum.setPlaceholderText("차트번호 형식이 잘못되었습니다.")
            return False

        if self._name == "":
            self.editName.setFocus()
            self.editName.setPlaceholderText("이름을 입력해주세요.")
            return False

        if self.editMonth.currentIndex() == -1:
            self.editMonth.setFocus()
            return False

        if self._gender is None:
            self.gBoxGenderGroup.setStyleSheet("QGroupBox { border : 1px solid red;}")
            return False

        if self._phone_num == "":
            self.editPhoneNum.setFocus()
            self.editPhoneNum.setPlaceholderText("연락처를 입력해주세요.")
            return False

        if self.editProfessor.currentIndex() == -1:
            self.editProfessor.setFocus()
            return False

        if not Check.checkValidityBirthDate(self._birth_date, self.editYear, self.editMonth, self.editDay):
            self.editYear.setStyleSheet("QLineEdit {border : 1px solid red;}")
            self.editMonth.setStyleSheet("QComboBox {border : 1px solid red;}")
            self.editDay.setStyleSheet("QLineEdit {border : 1px solid red;}")
            return False

        return self.tryEnroll()

    def tryEnroll(self):
        if not SubjectDAO.checkChartNumExists(self._chartNum):
            if SubjectDAO.enroll(self._chartNum, self._name, self._birth_date, self._gender, self._phone_num,
                                 self._professor, self._supervisor, self._enroll_date):
                reply = QMessageBox.information(self, 'Success', 'Enrolled successfully', QMessageBox.Ok)
                if reply == QMessageBox.Ok:
                    self.clearForm()
                    return True

    def clearForm(self):
        self.editName.setText("")
        self.btnGenderGroup.button(2).setChecked(True)
        self.editPhoneNum.setText("")
        self.editProfessor.setCurrentIndex(-1)
        self.editYear.setText("")
        self.editMonth.setCurrentIndex(-1)
        self.editDay.setText("")
        self.editYear.setStyleSheet("")
        self.editMonth.setStyleSheet("")
        self.editDay.setStyleSheet("")

    @property
    def _chartNum(self):
        return self.editChartNum.text()

    @property
    def _name(self):
        return self.editName.text()

    @property
    def _year(self):
        return self.editYear.text()

    @property
    def _month(self):
        return self.editMonth.currentText()

    @property
    def _day(self):
        return self.editDay.text()

    @property
    def _birth_date(self):
        return QDate(int(self._year), int(self._month), int(self._day))

    @property
    def _gender(self):
        _id = self.btnGenderGroup.checkedId()
        if _id == 0:
            return "M"
        elif _id == 1:
            return "F"
        elif _id == 2:
            return "N"

    @property
    def _phone_num(self):
        return self.editPhoneNum.text()

    @property
    def _professor(self):
        return self.editProfessor.currentText()

    @property
    def _supervisor(self):
        return self.editSupervisor.text()

    @property
    def _enroll_date(self):
        return QDate.currentDate()
