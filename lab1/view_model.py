from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic
from model import ten_to_base, base_to_ten
import re


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("Calc.ui", self)
        self.clear_all()
        self.bindings()

    # Отображение результата перевода
    def show_result(self):
        if (self.lineEdit.text() != ""):
            tmp = base_to_ten(self.lineEdit.text(), int(
                self.comboBox.currentText()))
            self.label.setText(ten_to_base(
                tmp, int(self.comboBox_2.currentText())))
        else:
            self.label.setText("")

    # Обработчик нажатия точки или цифры
    def symbol_clicked(self, symb):
        self.lineEdit.setText(self.lineEdit.text() + symb)
        self.check_correct(self.lineEdit.text())
        self.show_result()

    # Обработчик нажатия backspace
    def backspace(self):
        self.lineEdit.setText(self.lineEdit.text()[:-1])
        self.show_result()

    # Проверка корректности ввода
    def check_correct(self, cur_text):
        if self.lineEdit.text() != "":
            if re.fullmatch(f"^[+-]?[0-{int(self.comboBox.currentText())-1:d}]*\.?\
[0-{int(self.comboBox.currentText())-1:d}]*$", cur_text) is None:
                cur_pos = self.lineEdit.cursorPosition()
                self.lineEdit.setText(cur_text[:cur_pos-1]+cur_text[cur_pos:])
        self.show_result()

    # Очистка окон ввода при изменении системы счисления
    def clear_all(self):
        self.lineEdit.clear()
        self.label.clear()

    # Обработчик нажатия минуса
    def minus_clicked(self):
        cur_str = self.lineEdit.text()
        if cur_str != "":
            if cur_str[0] != '-':
                self.lineEdit.setText("-"+cur_str)
            else:
                self.lineEdit.setText(cur_str[1:])
        self.check_correct(self.lineEdit.text())

    # Привязка обработчиков событий к кнопкам
    def bindings(self):
        self.pushButton_14.clicked.connect(self.clear_all)
        self.pushButton.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton.text()))
        self.pushButton_2.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_4.text()))
        self.pushButton_5.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_5.text()))
        self.pushButton_6.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_6.text()))
        self.pushButton_7.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_7.text()))
        self.pushButton_8.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_8.text()))
        self.pushButton_9.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_9.text()))
        self.pushButton_10.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_10.text()))
        self.pushButton_11.clicked.connect(
            lambda: self.symbol_clicked(self.pushButton_11.text()))
        self.pushButton_12.clicked.connect(self.backspace)
        self.lineEdit.textEdited.connect(
            lambda: self.check_correct(self.lineEdit.text()))
        self.comboBox.currentIndexChanged.connect(self.clear_all)
        self.comboBox_2.currentIndexChanged.connect(self.show_result)
        self.btn_minus.clicked.connect(self.minus_clicked)
        self.menu_binds()

    # Бинды меню
    def menu_binds(self):
        self.action_reset.triggered.connect(self.clear_all)
        self.action_clear.triggered.connect(self.backspace)
        self.action_exit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.show_about_message)

    # Создание информационного окна
    def show_about_message(self):
        msg_window = QMessageBox()
        msg_window.setWindowTitle("About")
        msg_window.setText("Калькулятор систем счисления\n\
Автор: Бугаков И. С. ИУ7-24Б")
        msg_window.exec()
