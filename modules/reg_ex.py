from PySide6.QtCore import QRegularExpression


class RegEx:
    _only_korean = QRegularExpression("[가-힣]*")
    _only_numbers = QRegularExpression("[0-9]*")
    _except_numbers = QRegularExpression("^[^\d]+$")
    _except_korean = QRegularExpression("[^가-힣]*")
    _only_alphabets = QRegularExpression("[a-zA-Z]*")
    _except_alphabets = QRegularExpression("^[^a-zA-Z]+$")
    _only_alphanumeric = QRegularExpression("[a-zA-Z0-9]*")
    _except_alphanumeric = QRegularExpression("^[^a-zA-Z0-9]+$")
    _except_passwords = QRegularExpression("^(?=.*[A-Z])(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?=.{8,})")
    _email_format = QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @staticmethod
    def email_format():
        #이메일 형식 허용
        return RegEx._email_format

    @staticmethod
    def only_korean():
        # 한글만 허용
        return RegEx._only_korean

    @staticmethod
    def only_numbers():
        # 숫자만 허용
        return RegEx._only_numbers

    @staticmethod
    def except_numbers():
        # 숫자를 제외한 모든 문자 허용
        return RegEx._except_numbers

    @staticmethod
    def except_korean():
        # 한글을 제외한 모든 문자 허용
        return RegEx._except_korean

    @staticmethod
    def only_alphabets():
        # 알파벳만 허용
        return RegEx._only_alphabets

    @staticmethod
    def except_alphabets():
        # 알파벳을 제외한 모든 문자 허용
        return RegEx._except_alphabets

    @staticmethod
    def only_alphanumeric():
        # 알파벳과 숫자만 허용
        return RegEx._only_alphanumeric

    @staticmethod
    def except_alphanumeric():
        # 알파벳과 숫자를 제외한 모든 문자 허용
        return RegEx._except_alphanumeric

    @staticmethod
    def except_passwords():
        return RegEx._except_passwords
