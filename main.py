import sys
import copy
from datetime import datetime, date
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidgetItem, QMessageBox
from PyQt5 import uic, QtCore


count = ['alesha', 'oleg', 'rusik', 'mongol']
colors = []
d = {'2022-11-08': ['csdf', 'dffdg'], '2022-10-08': ['csdf', 'dffdg']}


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global d

        self.name1 = None
        self.name3 = None

        uic.loadUi('ui/Mainwindow.ui', self)

        self.pushButton_2.clicked.connect(self.plain1)
        self.pushButton.clicked.connect(self.instructions)

        a = date.today()
        line = []
        for i, j in d.items():
            if datetime.strptime(i, '%Y-%m-%d').date() < a:
                line.append(i)
        [d.pop(i, None) for i in line]
        if str(a) in d.keys():
            self.error = QMessageBox()
            self.error.setWindowTitle("notification")
            self.error.setText(f'your set films for today: {d[str(a)]}')
            self.error.setIcon(QMessageBox.Warning)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.show()

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

        self.error = QMessageBox()
        self.error.setWindowTitle("success")
        self.error.setText('date successfully set')
        self.error.setIcon(QMessageBox.Warning)
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.hide()

        self.solve()

        self.pushButton_3.clicked.connect(self.plain2)
        self.pushButton_4.clicked.connect(self.removing)
        self.pushButton_5.clicked.connect(self.accept)
        self.pushButton_7.clicked.connect(self.color)
        self.pushButton_8.clicked.connect(self.up)
        self.pushButton_9.clicked.connect(self.down)
        self.pushButton_6.clicked.connect(self.data)
        self.listWidget.itemSelectionChanged.connect(self.enable)
        try:
            self.calendarWidget.clicked['QDate'].connect(self.date_track)
        except Exception as e:
            print(e)

        self.calendarWidget.hide()
        self.show()

    def date_track(self):
        global d
        a = eval(self.listWidget.currentItem().text())[0] - 1
        b = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        if b in d.keys():
            if self.count[a] not in d[b]:
                d[b].append(self.count[a])
        else:
            d[b] = []
        self.error.show()

    def data(self):
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.hide()
        self.pushButton_8.setEnabled(False)
        self.pushButton_8.hide()
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.hide()
        self.calendarWidget.setEnabled(True)
        self.pushButton_4.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.calendarWidget.show()

    def up(self):
        a = eval(self.listWidget.currentItem().text())[0] - 1

        try:
            if a - 1 >= 0:
                self.count[a], self.count[a - 1] = self.count[a - 1], self.count[a]
            else:
                raise IndexError
        except IndexError:
            print('Film is already first in list')

        self.listWidget.clear()
        self.solve()

    def down(self):
        a = eval(self.listWidget.currentItem().text())[0] - 1

        try:
            self.count[a], self.count[a + 1] = self.count[a + 1], self.count[a]
        except IndexError:
            print('Film is already last in list')

        self.listWidget.clear()
        self.solve()

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
        a = eval(self.listWidget.currentItem().text())[0] - 1

        self.listWidget.takeItem(a)
        if self.count[a] in colors:
            self.colors.remove(self.count[a])
        self.count.remove(self.count[a])
        self.listWidget.clear()
        self.solve()

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
