import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit


class Example(QWidget):
    def __init__(self):
        app = QApplication(sys.argv)
        super().__init__()
        self.num = 1
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('перекидыватель слов')

        self.btn = QPushButton('->', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(150, 150)
        self.btn.clicked.connect(self.hello)

        self.name_input1 = QLineEdit(self)
        self.name_input1.move(150, 250)
        self.name_input1.setText('ЕГГОГ')

        self.name_input2 = QLineEdit(self)
        self.name_input2.move(150, 90)
        self.show()

        sys.exit(app.exec())

    def hello(self):
        self.num += 1
        if self.num % 2 == 0:
            self.name_input2.setText('ЕГГОГ')
            self.name_input1.setText('')
        else:
            self.name_input1.setText('ЕГГОГ')
            self.name_input2.setText('')


if __name__ == '__main__':
    ex = Example()
