import sys

from PyQt5.QtCore import Qt

import password_checker
import random

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QLabel, QLineEdit, QDialog, QStyledItemDelegate, QAbstractItemView
from PyQt5.QtCore import QSize


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.new_window = None
        uic.loadUi('Dialog.ui', self)
        self.buttonwelcome.clicked.connect(self.open_new_window)
        self.buttonwelcome.setIcon(QIcon('welcome.png'))
        self.buttonwelcome.setIconSize(QSize(400, 80))

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.dup = []
        uic.loadUi('d2.ui', self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Login', 'Website Name', 'Password'])

        self.random_password_button.clicked.connect(self.password_generator)
        self.savebutton.clicked.connect(self.save_data)

    def save_data(self):
        address = self.addressinput.text()
        website = self.websiteinput.text()
        password = self.passwordinput.text()
        if address != '' and website != '':
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
                if len(password) == 0 and (address, website) in self.dup:
                    delete_index = self.dup.index((address, website))
                    self.table.removeRow(delete_index)
                    self.dup.remove((address, website))
                else:
                    self.ErrorLabel.setText('Пароль слишком короткий')
            except password_checker.DigitError:
                self.ErrorLabel.setText('В пароле отсутствуют цифры')
        else:
            self.ErrorLabel.setText('Поля Логина и пароля должны быть непустыми')

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
    POPULAR_PASSWORDS = ['12345', '123456', '123456789', 'test1', 'password', '12345678', 'zinch', 'g_czechout', 'asdf',
                         'qwerty',
                         '1234567890', '1234567', 'aa123456.', 'iloveyou', '1234', 'abc123', '111111', '123123',
                         'dubsmash', 'test',
                         'princess', 'qwertyuiop', 'sunshine', 'bvttest123', '11111', 'ashley', '00000', '000000',
                         'password1',
                         'monkey', 'livetest', '55555', 'soccer', 'charlie', 'asdfghjkl', '654321', 'family', 'michael',
                         '123321',
                         'football', 'baseball', 'q1w2e3r4t5y6', 'nicole', 'jessica', 'purple', 'shadow', 'hannah',
                         'chocolate',
                         'michelle', 'daniel', 'maggie', 'qwerty123', 'hello', '112233', 'jordan', 'tigger', '666666',
                         '987654321',
                         'superman', '12345678910', 'summer', '1q2w3e4r5t', 'fitness', 'bailey', 'zxcvbnm', 'fuckyou',
                         '121212',
                         'buster', 'butterfly', 'dragon', 'jennifer', 'amanda', 'justin', 'cookie', 'basketball',
                         'shopping', 'pepper',
                         'joshua', 'hunter', 'ginger', 'matthew', 'abcd1234', 'taylor', 'samantha', 'whatever',
                         'andrew',
                         '1qaz2wsx3edc', 'thomas', 'jasmine', 'animoto', 'madison', '0987654321', '54321', 'flower',
                         'password',
                         'maria', 'babygirl', 'lovely', 'sophie', 'chegg123']
    SYMBOLS = ['!', 'E', 'm', '@', 'R', 'i', '7', 'q', 'W', '3', 'I', 'o', 'J', 'Z', 'B', '*', '+', 'r', 'F', 'd', 'g',
               '5', 'Q', 't', 'C', 'A', '%', '=', '1', '#', '4', 'Y', 'j', 'y', 'G', 'f', 'V', 'M', 'w', 'z', 'b', 'K',
               '$', '^', 'T', '&', 'p', 'v', 'n', 'P', '-', 'k', '8', 'L', '9', '_', 's', 'c', 'X', 'u', 'D', 'O', 'N',
               'h', '0', 'e', 'x', 'l', 'S', 'H', '6', 'U', '2', 'a']

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())