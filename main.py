import sys
import copy
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidgetItem
from PyQt5 import uic, QtCore


count = ['alesha', 'oleg', 'rusik', 'mongol']
colors = []


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name1 = None
        self.name3 = None

        uic.loadUi('ui/Mainwindow.ui', self)

        self.pushButton_2.clicked.connect(self.plain1)
        self.pushButton.clicked.connect(self.instructions)

        self.show()

    def plain1(self):
        self.close()
        self.name1 = Watchlaterlist()

    def instructions(self):
        self.name3 = Read()


class Watchlaterlist(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Watchlaterlist.ui', self)

        global count, colors
        self.colors = copy.deepcopy(colors)
        self.count = copy.deepcopy(count)
        self.name2 = None

        self.solve()

        self.pushButton_3.clicked.connect(self.plain2)
        self.pushButton_4.clicked.connect(self.removing)
        self.pushButton_5.clicked.connect(self.accept)
        self.pushButton_7.clicked.connect(self.color)
        self.listWidget.itemSelectionChanged.connect(self.enable)

        self.calendarWidget.hide()
        self.show()

    def solve(self):
        for i in enumerate(self.count, 1):
            item = QListWidgetItem(str(i))
            if i[1] in self.colors:
                item.setForeground(QtCore.Qt.red)
            self.listWidget.addItem(item)

    def color(self):
        a = eval(self.listWidget.currentItem().text())[0] - 1

        self.colors.append(self.count[a])
        self.listWidget.clear()
        self.solve()

    def removing(self):
        try:
            a = eval(self.listWidget.currentItem().text())[0] - 1

            self.listWidget.takeItem(a)
            if self.count[a] in colors:
                self.colors.remove(self.count[a])
            self.count.remove(self.count[a])
            self.listWidget.clear()
            self.solve()
        except Exception as e:
            print(e)

    def plain2(self):
        self.close()
        self.name2 = Mainwindow()

    def enable(self):
        if self.listWidget.selectedItems():
            flag = True
        else:
            flag = False

        self.pushButton_4.setEnabled(flag)
        self.pushButton_6.setEnabled(flag)
        self.pushButton_7.setEnabled(flag)
        self.pushButton_8.setEnabled(flag)
        self.pushButton_9.setEnabled(flag)

    def accept(self):
        global count, colors
        count = self.count
        colors = self.colors


class Read(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Read.ui', self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainwindow()
    sys.exit(app.exec())
