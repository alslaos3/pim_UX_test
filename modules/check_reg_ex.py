from PySide6.QtCore import QRegularExpression, QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit
from .reg_ex import RegEx


class Check:

    @staticmethod
    def checkValidity(instance: QLineEdit, exclude: QRegularExpression, include: QRegularExpression,
                      lang_1: str = "", lang_2: str = "", lang_3: str = ""):
        if instance.text():
            match = exclude.match(instance.text()[-1])
            if match.capturedLength() == 1:
                instance.setValidator(QRegularExpressionValidator(include, instance))
                instance.clear()
                langs = [lang for lang in [lang_1, lang_2, lang_3] if lang]
                instance.setPlaceholderText(",".join(langs) + "로 입력해 주세요.")

    @staticmethod
    def checkValidityName(instance: QLineEdit):
        Check.checkValidity(instance, RegEx.except_korean(), RegEx.only_korean(), "한글")

    @staticmethod
    def checkValidityChartNum(instance: QLineEdit):
        Check.checkValidity(instance, RegEx.except_alphanumeric(), RegEx.only_alphanumeric(), "영문", "숫자")

    @staticmethod
    def checkValidityUsername(instance: QLineEdit):
        Check.checkValidity(instance, RegEx.except_alphanumeric(), RegEx.only_alphanumeric(), "영문", "숫자")

    @staticmethod
    def checkValidityPhoneNum(instance: QLineEdit):
        Check.checkValidity(instance, RegEx.except_numbers(), RegEx.only_numbers(), "숫자")

    @staticmethod
    def checkValidityBirthYear(instance: QLineEdit):
        year = instance.text()
        if year:
            match = RegEx.except_numbers().match(instance.text()[-1])
            if match.capturedLength() == 1:
                instance.setValidator(QRegularExpressionValidator(RegEx.only_numbers(), instance))
                instance.clear()
                instance.setPlaceholderText("숫자만 입력해 주세요.")

    @staticmethod
    def checkValidityPassword(instance: QLineEdit):
        if instance.text():
            match = RegEx.except_passwords().match(instance.text())
            if match.hasMatch():
                return True
            else:
                instance.clear()
                instance.setPlaceholderText("대문자, 특수문자를 포함한 8자 이상의 비밀번호를 입력해 주세요.")
                return False
        else:
            instance.setFocus()
            instance.setPlaceholderText("비밀번호를 입력해 주세요.")
        return False

    @staticmethod
    def checkValidityBirthDate(date: QDate, instance_year, instance_month, instance_day):
        if not date.isValid():
            instance_year.clear()
            instance_month.setCurrentIndex(0)
            instance_day.clear()

            return False

        return True

    @staticmethod
    def checkValidityEmail(instance: QLineEdit):
        if instance.text():
            match = RegEx.email_format().match(instance.text())
            if match.hasMatch():
                return True
            else:
                instance.clear()
                instance.setPlaceholderText("존재하는 이메일 주소를 입력해주세요.")
                return False
        return False
