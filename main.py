import sys
from datetime import datetime, date
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidgetItem, QMessageBox
from PyQt5 import uic, QtCore
import sqlite3


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name4 = None
        self.con = sqlite3.connect('static/Films.db')
        self.cur = self.con.cursor()

        self.name1 = None
        self.name3 = None

        uic.loadUi('ui/Mainwindow.ui', self)

        self.pushButton_2.clicked.connect(self.plain1)
        self.pushButton.clicked.connect(self.instructions)

        a = date.today()
        self.cur.execute("""UPDATE Watchlater SET date=NULL WHERE date<?""", (a,)).fetchall()
        line = self.cur.execute("""SELECT name FROM Watchlater WHERE date=?""", (a,)).fetchall()
        if line:
            self.error = QMessageBox()
            self.error.setWindowTitle("notification")
            self.error.setText(f'your set films for today: {line[0]}')
            self.error.setIcon(QMessageBox.Warning)
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.show()
        self.con.commit()
        self.con.close()

        self.show()

    def plain1(self):
        self.close()
        self.name1 = Watchlaterlist()

    def plain4(self):
        self.close()
        self.name4 = Podborka()

    def instructions(self):
        self.name3 = Read()


class Watchlaterlist(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('static/Films.db')
        self.cur = self.con.cursor()

        self.name2 = None
        uic.loadUi('ui/Watchlaterlist.ui', self)

        self.solve()

        self.pushButton_3.clicked.connect(self.plain2)
        self.pushButton_4.clicked.connect(self.removing)
        self.pushButton_5.clicked.connect(self.accept)
        self.pushButton_7.clicked.connect(self.color)
        self.pushButton_6.clicked.connect(self.data)
        self.pushButton_8.clicked.connect(self.uncolor)
        self.listWidget.itemSelectionChanged.connect(self.enable)
        self.calendarWidget.clicked['QDate'].connect(self.date_track)

        self.calendarWidget.hide()
        self.show()

    def uncolor(self):
        a = eval(self.listWidget.currentItem().text())[0]

        self.cur.execute("""UPDATE Watchlater SET color=NULL WHERE name=?""", (a,)).fetchall()

        self.listWidget.clear()
        self.solve()

    def date_track(self):
        a = eval(self.listWidget.currentItem().text())[0]
        b = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        self.cur.execute("""UPDATE Watchlater SET date=? WHERE name=?""", (b, a)).fetchall()

        self.pushButton_7.setEnabled(True)
        self.pushButton_7.show()
        self.pushButton_8.setEnabled(True)
        self.pushButton_8.show()
        self.calendarWidget.setEnabled(False)
        self.calendarWidget.hide()

        self.listWidget.clear()
        self.solve()

    def data(self):
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.hide()
        self.pushButton_8.setEnabled(False)
        self.pushButton_8.hide()
        self.calendarWidget.setEnabled(True)
        self.pushButton_4.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.calendarWidget.show()

    def solve(self):
        for i in self.cur.execute("""SELECT name, date FROM Watchlater ORDER BY position""").fetchall():
            item = QListWidgetItem(str(i))
            if self.cur.execute("""SELECT * FROM Watchlater WHERE name=? AND color IS NOT NULL""",
                                (i[0],)).fetchall():
                item.setForeground(QtCore.Qt.red)
            else:
                item.setForeground(QtCore.Qt.black)
            self.listWidget.addItem(item)

    def color(self):
        a = eval(self.listWidget.currentItem().text())[0]

        self.cur.execute("""UPDATE Watchlater SET color='True' WHERE name=?""", (a,)).fetchall()

        self.listWidget.clear()
        self.solve()

    def removing(self):
        a = eval(self.listWidget.currentItem().text())[0]

        self.cur.execute("""DELETE FROM Watchlater WHERE name=?""", (a,)).fetchall()

        self.listWidget.clear()
        self.solve()

    def plain2(self):
        self.close()
        self.con.rollback()
        self.con.close()
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
        self.pushButton_7.show()
        self.pushButton_8.show()
        self.calendarWidget.setEnabled(False)
        self.calendarWidget.hide()

    def accept(self):
        self.con.commit()
        self.listWidget.clear()
        self.solve()


class Read(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Read.ui', self)
        self.show()


class Podborka(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Read.ui', self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainwindow()
    sys.exit(app.exec())
