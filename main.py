import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Mainwindow.ui', self)
        self.pushButton_2.clicked.connect(self.plain1)
        self.show()

    def plain1(self):
        self.close()
        self.name1 = Watchlaterlist()


class Watchlaterlist(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Watchlaterlist.ui', self)
        self.pushButton_3.clicked.connect(self.plain2)
        self.show()

    def plain2(self):
        self.close()
        self.name2 = Mainwindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainwindow()
    sys.exit(app.exec())
