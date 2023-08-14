from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class BlankTestPage(QWidget):
    def __init__(self):
        super(BlankTestPage, self).__init__()

        self.test = QLabel("test")

        vbox = QVBoxLayout()
        vbox.addWidget(self.test)

        self.setLayout(vbox)
