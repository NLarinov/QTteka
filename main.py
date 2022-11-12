import sys
from random import shuffle
from datetime import datetime, date
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import uic, QtCore
import sqlite3


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.error = None
        self.name = None

        self.con = sqlite3.connect('static/Films.db')
        self.cur = self.con.cursor()

        uic.loadUi('ui/Mainwindow.ui', self)

        self.pushButton_2.clicked.connect(self.plain)
        self.pushButton.clicked.connect(self.instructions)
        self.pushButton_4.clicked.connect(self.podborka)
        self.pushButton_5.clicked.connect(self.podborka)
        self.pushButton_6.clicked.connect(self.podborka)
        self.pushButton_7.clicked.connect(self.podborka)
        self.pushButton_8.clicked.connect(self.podborka)
        self.pushButton_9.clicked.connect(self.podborka)
        self.pushButton_11.clicked.connect(self.podborka)
        self.pushButton_12.clicked.connect(self.podborka)
        self.pushButton_13.clicked.connect(self.podborka)
        self.pushButton_10.clicked.connect(self.podborka)

        a = date.today()
        try:
            self.cur.execute("""UPDATE Watchlater SET date=NULL WHERE date<?""", (a,))
            line = self.cur.execute("""SELECT name FROM Watchlater WHERE date=?""", (a,)).fetchall()
            if line:
                self.notif = QMessageBox()
                self.notif.setWindowTitle("notification")
                self.notif.setText(f'your set films for today: {line[0]}')
                self.notif.setIcon(QMessageBox.Warning)
                self.notif.setStandardButtons(QMessageBox.Ok)
                self.notif.show()
            self.con.commit()
            self.con.close()
        except Exception as e:
            print(e)

        self.show()

    def podborka(self):
        self.close()
        self.name = Podborka(QApplication.instance().sender().text())

    def some_error(self, error):
        self.error = QMessageBox()
        self.error.setWindowTitle("Error")
        self.error.setText(error)
        self.error.setIcon(QMessageBox.Warning)
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.show()

    def plain(self):
        self.close()
        self.name = Watchlaterlist()

    def instructions(self):
        self.name = Read()


class Watchlaterlist(QMainWindow):
    def __init__(self):
        super().__init__()
        self.error = None
        self.con = sqlite3.connect('static/Films.db')
        self.cur = self.con.cursor()
        self.name = None
        uic.loadUi('ui/Watchlaterlist.ui', self)

        try:
            self.solve()

            self.pushButton_3.clicked.connect(self.plain)
            self.pushButton_4.clicked.connect(self.removing)
            self.pushButton_5.clicked.connect(self.accept)
            self.pushButton_7.clicked.connect(self.color)
            self.pushButton_6.clicked.connect(self.data)
            self.pushButton_8.clicked.connect(self.uncolor)
            self.listWidget.itemSelectionChanged.connect(self.enable)
            self.calendarWidget.clicked['QDate'].connect(self.date_track)
        except Exception as e:
            print(e)

        self.calendarWidget.hide()
        self.show()

    def some_error(self, error):
        self.error = QMessageBox()
        self.error.setWindowTitle("Error")
        self.error.setText(error)
        self.error.setIcon(QMessageBox.Warning)
        self.error.setStandardButtons(QMessageBox.Ok)
        self.error.show()

    def uncolor(self):
        a = eval(self.listWidget.currentItem().text())[0]
        self.cur.execute("""UPDATE Watchlater SET color=NULL WHERE name=?""", (a,))

        self.listWidget.clear()
        self.solve()

    def date_track(self):
        a = eval(self.listWidget.currentItem().text())[0]
        b = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        self.cur.execute("""UPDATE Watchlater SET date=? WHERE name=?""", (b, a))

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

        self.cur.execute("""UPDATE Watchlater SET color='True' WHERE name=?""", (a,))

        self.listWidget.clear()
        self.solve()

    def removing(self):
        a = eval(self.listWidget.currentItem().text())[0]

        self.cur.execute("""DELETE FROM Watchlater WHERE name=?""", (a,))

        self.listWidget.clear()
        self.solve()

    def plain(self):
        self.close()
        self.con.rollback()
        self.con.close()
        self.name = Mainwindow()

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
    def __init__(self, name):
        super().__init__()
        self.name = None
        self.n = 0

        uic.loadUi('ui/Podborka.ui', self)
        self.con = sqlite3.connect('static/Films.db')
        self.cur = self.con.cursor()

        self.label_3.setText(name)
        if name == 'TOP SERIES':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE type='сериал'""").fetchall()
        elif name == 'TOP FILMS':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE type='фильм'""").fetchall()
        elif name == 'TOP NOSTALGIC':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE year<'2000'""").fetchall()
        elif name == 'TOP NEW':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE year>='2000'""").fetchall()
        elif name == 'RANDOM':
            self.count = self.cur.execute("""SELECT * FROM Main""").fetchall()
            shuffle(self.count)
        elif name == 'EPIC':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE genre IN
             ('криминальный', 'фантастика', 'военный', 'триллер')""").fetchall()
            shuffle(self.count)
        elif name == 'Rainy day':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE genre IN
             ('криминальный', 'фантастика', 'драма')""").fetchall()
            shuffle(self.count)
        elif name == 'Happy':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE genre IN
             ('комедия', 'фантастика', 'анимация')""").fetchall()
            shuffle(self.count)
        elif name == 'Sad':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE genre IN
             ('драма', 'мелодрама')""").fetchall()
            shuffle(self.count)
        elif name == 'Relaxed':
            self.count = self.cur.execute("""SELECT * FROM Main WHERE genre IN
             ('комедия', 'фантастика', 'анимация', 'кинофантазия', 'спортивный', 'приключенческий')""").fetchall()
            shuffle(self.count)
        self.display()

        self.pushButton_5.clicked.connect(self.plain1)
        self.pushButton_6.clicked.connect(self.plain2)
        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.change)
        self.pushButton_3.clicked.connect(self.like)
        self.pushButton_4.clicked.connect(self.dislike)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            self.pushButton.click()
        if event.key() == QtCore.Qt.Key_D:
            self.pushButton_2.click()
        if event.key() == QtCore.Qt.Key_W:
            self.pushButton_4.click()
        if event.key() == QtCore.Qt.Key_S:
            self.pushButton_3.click()

    def dislike(self):
        a = self.count[self.n]
        try:
            self.count.remove(a)
            self.n -= 1
            self.change()
            self.display()
        except Exception:
            self.close()
            self.plain1()

    def like(self):
        a = self.count[self.n]

        self.cur.execute(f"""INSERT OR REPLACE INTO Watchlater (position, name) VALUES {(a[0], a[1])}""")
        self.con.commit()

        self.change()
        self.display()

    def display(self):
        a = self.count[self.n]
        self.label_2.setText(f'Название: {a[1]}\nГод: {a[2]}\nТип:'
                             f' {a[3]}\nСтрана: {a[4]}\nЖанр: {a[5]}\nОписание:'
                             f' {a[6]}\nНезависимая оценка: {a[7]}\n')
        self.label_2.setWordWrap(True)
        self.label.setPixmap(QPixmap(f'static/images/{a[0]}.jpg'))

    def change(self):
        if QApplication.instance().sender().text() == '<':
            if self.n - 1 >= 0:
                self.n -= 1
        else:
            if self.n + 1 < len(self.count):
                self.n += 1

        self.display()

    def plain1(self):
        self.close()
        self.con.close()
        self.name = Mainwindow()

    def plain2(self):
        self.close()
        self.con.close()
        self.name = Watchlaterlist()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainwindow()
    sys.exit(app.exec())
