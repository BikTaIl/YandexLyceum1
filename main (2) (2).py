import sys
import sqlite3

from PyQt5.QtCore import Qt

import password_checker
import random

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QLabel, QLineEdit, QDialog, QStyledItemDelegate, QAbstractItemView


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.new_window = None
        uic.loadUi('Dialog.ui', self)
        self.buttonwelcome.clicked.connect(self.open_new_window)
        self.buttonwelcome.setStyleSheet("border-image : url(welcome.png);")

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.dup = []
        uic.loadUi('d2.ui', self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Address', 'Website Name', 'Password'])

        self.random_password_button.clicked.connect(self.password_generator)
        self.savebutton.clicked.connect(self.save_data)

    def save_data(self):
        address = self.addressinput.text()
        website = self.websiteinput.text()
        password = self.passwordinput.text()
        if address != '' and website != '' and password != '':
            try:
                password_checker.check_password(password)
                if password not in POPULAR_PASSWORDS:
                    if (address, website) in self.dup:
                        a = self.dup.index((address, website))
                        self.table.setItem(a, 2, QTableWidgetItem(password))
                    else:
                        self.dup.append((address, website))
                        rowcount = self.table.rowCount()
                        self.table.insertRow(rowcount)
                        self.table.setItem(rowcount, 0, QTableWidgetItem(address))
                        self.table.setItem(rowcount, 1, QTableWidgetItem(website))
                        self.table.setItem(rowcount, 2, QTableWidgetItem(password))
                    self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    self.addressinput.clear()
                    self.websiteinput.clear()
                    self.passwordinput.clear()
                    self.ErrorLabel.setText('')
            except password_checker.SequenceError:
                self.ErrorLabel.setText('Пароль слишком простой')
            except password_checker.LetterError:
                self.ErrorLabel.setText('В пароле все символы одного регистра')
            except password_checker.LengthError:
                self.ErrorLabel.setText('Пароль слишком короткий')
            except password_checker.DigitError:
                self.ErrorLabel.setText('В пароле отсутствуют цифры')
        else:
            self.ErrorLabel.setText('Пароль слишком простой')

    def password_generator(self):
        length = random.randint(13, 19)
        password_is_bad = True
        while password_is_bad:
            new_password = ''
            for i in range(length):
                new_password += random.choice(SYMBOLS)
            try:
                password_checker.check_password(new_password)
                password_is_bad = False
            except password_checker.PasswordError:
                pass
        self.passwordinput.setText(new_password)


if __name__ == "__main__":

    con = sqlite3.connect("proj.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT passwords FROM popularpasswords
                WHERE 1 <= ID <= 10000""").fetchall()
    POPULAR_PASSWORDS = []
    for elem in result:
        POPULAR_PASSWORDS.append(elem)
    con.close()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
