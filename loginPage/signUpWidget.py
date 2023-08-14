from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGroupBox, QComboBox, QHBoxLayout, \
    QRadioButton, QButtonGroup, QMessageBox
from PySide6.QtCore import Signal, QDate, QRegularExpression, QTimer
import ctypes
from dao.hashing import Hashing
from dao import UserDAO, AccessDeniedError, UserAlreadyExistsError, InvalidPasswordError
from modules.check_reg_ex import Check

VK_CAPITAL = 0x14


class SignUpWidget(QWidget):
    _username_checked = False
    _filled_form = {}

    def __init__(self):
        super().__init__()

        lblUsername = QLabel("아이디")
        self.editUsername = QLineEdit()
        self.editUsername.setPlaceholderText("아이디를 입력해주세요.")

        lblPassword = QLabel("비밀번호")
        self.lblPasswordCapsLock = QLabel("")
        hBoxPassword = QHBoxLayout()
        hBoxPassword.addWidget(lblPassword)
        hBoxPassword.addWidget(self.lblPasswordCapsLock)
        self.editPassword = QLineEdit()
        self.editPassword.setPlaceholderText("비밀번호를 입력해주세요.")
        self.editPassword.setEchoMode(QLineEdit.Password)

        lblPasswordRepeat = QLabel("비밀번호 재확인")
        self.editPasswordRepeat = QLineEdit()
        self.editPasswordRepeat.setPlaceholderText("비밀번호를 다시 입력해주세요.")
        self.editPasswordRepeat.setEchoMode(QLineEdit.Password)

        lblName = QLabel("이름")
        self.editName = QLineEdit()
        self.editName.setPlaceholderText("성명을 입력해주세요.")

        lblBirthDate = QLabel("생년월일")
        self.hBoxBirthDate = QHBoxLayout()

        self.editYear = QLineEdit()
        self.editYear.setPlaceholderText("년(4자)")
        self.editYear.setMaxLength(4)

        self.editMonth = QComboBox()
        self.editMonth.addItem("월")
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

        self.gBoxGenderGroup = QGroupBox()
        btnHBox = QHBoxLayout()
        btnHBox.addWidget(btnMale)
        btnHBox.addWidget(btnFemale)
        btnHBox.addWidget(btnNone)
        self.gBoxGenderGroup.setLayout(btnHBox)

        lblOrgan = QLabel("소속")
        self.editOrgan = QComboBox()
        self.editOrgan.addItem("양산부산대학교병원")

        lblEmail = QLabel("이메일 주소(선택)")
        self.editEmail = QLineEdit()
        self.editEmail.setPlaceholderText("이메일을 입력해주세요.(선택)")

        self.btnSignUp = QPushButton("가입하기")
        self.btnSignUp.clicked.connect(self.checkForm)

        self.hboxBack = QHBoxLayout()
        self.btnHome = QPushButton("←")
        self.hboxBack.addWidget(self.btnHome)
        self.hboxBack.addStretch(1)

        self.editUsername.textEdited.connect(lambda: Check.checkValidityUsername(self.editUsername))
        self.editPassword.editingFinished.connect(lambda: Check.checkValidityPassword(self.editPassword))
        self.editName.textEdited.connect(lambda: Check.checkValidityName(self.editName))
        self.editYear.textEdited.connect(lambda: Check.checkValidityBirthYear(self.editYear))
        self.editEmail.editingFinished.connect(lambda: Check.checkValidityEmail(self.editEmail))

        vbox = QVBoxLayout()

        vbox.addLayout(self.hboxBack)

        vbox.addWidget(lblUsername)
        vbox.addWidget(self.editUsername)

        vbox.addLayout(hBoxPassword)
        vbox.addWidget(self.editPassword)

        vbox.addWidget(lblPasswordRepeat)
        vbox.addWidget(self.editPasswordRepeat)

        vbox.addWidget(lblName)
        vbox.addWidget(self.editName)

        vbox.addWidget(lblBirthDate)
        vbox.addLayout(self.hBoxBirthDate)

        vbox.addWidget(lblGender)
        vbox.addWidget(self.gBoxGenderGroup)

        vbox.addWidget(lblOrgan)
        vbox.addWidget(self.editOrgan)

        vbox.addWidget(lblEmail)
        vbox.addWidget(self.editEmail)

        vbox.addWidget(self.btnSignUp)

        self.setLayout(vbox)

        self.timerCapsLock = QTimer()
        self.timerCapsLock.timeout.connect(self.checkCapsLock)
        self.timerCapsLock.start(500)

    def checkCapsLock(self):
        dll = ctypes.WinDLL("User32.dll")
        state = dll.GetKeyState(VK_CAPITAL)
        is_toggled = bool(state & 0x01)

        if is_toggled:
            self.editPassword.clear()
            self.lblPasswordCapsLock.setText("CapsLock이 켜져있습니다.")
        else:
            self.lblPasswordCapsLock.setText("")

    def checkForm(self):
        if not self.checkUsernameForm():
            return False
        if not self.checkPasswordForm():
            return False
        if not Check.checkValidityPassword(self.editPassword):
            return False
        if not self.checkNameForm():
            return False
        if not self.checkOrganForm():
            return False
        if not self.checkUsernameChecked():
            return False

        return self.trySignUp()

    def trySignUp(self):
        if UserDAO.signUp(self._username, self._password, self._name, self._birth_date,
                          self._gender, self._organization, self._email):
            reply = QMessageBox.information(self, 'Success', 'User signed up successfully', QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.clearForm()
                return True

    def checkUsernameChecked(self):
        username = self._username
        if UserDAO.checkUserExists(username):
            self.editUsername.setFocus()
            self.editUsername.clear()
            self.editUsername.setPlaceholderText("중복된 아이디입니다.")
            return False
        else:
            return True

    def checkUsernameForm(self):
        if self.editUsername.text() == "":
            self.editUsername.setFocus()
            self.editUsername.setPlaceholderText("아이디를 입력해주세요.")
            return False
        else:
            return True

    def checkPasswordForm(self):
        if not self.editPasswordRepeat.text() == self.editPassword.text():
            self.editPasswordRepeat.setFocus()
            self.editPasswordRepeat.clear()
            self.editPasswordRepeat.setPlaceholderText("비밀번호가 일치하지 않습니다.")
            return False
        else:
            return True

    def checkNameForm(self):
        if self.editName.text() == "":
            self.editName.setFocus()
            self.editName.setPlaceholderText("이름을 입력해주세요.")
            return False
        else:
            return True

    def checkOrganForm(self):
        if self.editOrgan.currentText() == "":
            self.editOrgan.setFocus()
            self.editOrgan.setPlaceholderText("소속을 선택해주세요.")
            return False
        else:
            return True

    def clearForm(self):
        self.editUsername.clear()
        self.editPassword.clear()
        self.editPasswordRepeat.clear()
        self.editName.clear()
        self.editYear.setText("")
        self.editMonth.setCurrentIndex(0)
        self.editDay.setText("")
        self.btnGenderGroup.button(2).setChecked(True)
        self.editOrgan.setCurrentIndex(0)
        self.editEmail.clear()

    @property
    def _username(self):
        return self.editUsername.text()

    @property
    def _password(self):
        return self.editPassword.text()

    @property
    def _password_repeat(self):
        return self.editPasswordRepeat.text()

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
    def _organization(self):
        return self.editOrgan.currentText()

    @property
    def _email(self):
        return self.editEmail.text()
