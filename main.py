import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class Aloitus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Ok", self)
        self.button.move(200, 200)
        self.button.clicked.connect(self.continue2)
        self.setGeometry(600, 200, 500, 300)

    def continue2(self):
        self.close()
        _ = Second()


class Second(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Alkutiedot"
        self.top = 600
        self.left = 200
        self.width = 500
        self.height = 500

        self.button = QPushButton("Ok", self)
        self.button.move(100, 400)
        self.button.clicked.connect(self.ok)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def ok(self):
        print('close clicked')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Aloitus()
    ex.show()
    sys.exit(app.exec())
