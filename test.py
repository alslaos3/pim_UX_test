from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QButtonGroup

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.stackedWidget = QStackedWidget()

        # 페이지 추가
        tab1 = QPushButton("Content for Tab 1")
        tab2 = QPushButton("Content for Tab 2")
        tab3 = QPushButton("Content for Tab 3")
        self.stackedWidget.addWidget(tab1)
        self.stackedWidget.addWidget(tab2)
        self.stackedWidget.addWidget(tab3)

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(True) # 한 번에 하나의 버튼만 선택됨

        # 버튼 추가
        self.button1 = QPushButton("Tab 1")
        self.button2 = QPushButton("Tab 2")
        self.button3 = QPushButton("Tab 3")
        self.button1.setCheckable(True)
        self.button2.setCheckable(True)
        self.button3.setCheckable(True)
        self.button1.setChecked(True) # 초기 선택 버튼
        self.buttonGroup.addButton(self.button1, 0)
        self.buttonGroup.addButton(self.button2, 1)
        self.buttonGroup.addButton(self.button3, 2)

        # 버튼과 페이지 전환 연결
        self.buttonGroup.buttonClicked.connect(self.changePage)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.stackedWidget)

        self.setLayout(layout)

    def changePage(self, button):
        # 선택된 페이지로 전환
        self.stackedWidget.setCurrentIndex(self.buttonGroup.id(button))

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
