from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from model import code, decode, EXIT_OVERFLOW, EXIT_SUCCESS, EXIT_PERMISSON, EXIT_OTHER


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("lab3.ui", self)
        self.menu_binds()
        self.bindings()

    # Бинды меню
    def menu_binds(self):
        self.info.triggered.connect(self.show_about_message)
        self.make.triggered.connect(self.set_dialog_window)

    # Информационное окно
    def show_about_message(self):
        msg_window = QMessageBox()
        msg_window.setWindowTitle("Info")
        msg_window.setText("Программа для решения \
уравнений и построения графиков\n\
Автор: Бугаков И. С. ИУ7-24Б")
        msg_window.exec()

    # Окно сообщения об ошибке
    def show_exception_message(self, text):
        msg_window = QMessageBox()
        msg_window.setWindowTitle("Произошла ошибка!")
        msg_window.setText(text)
        msg_window.exec()

    # Настройка интерфейса и привязка функций
    def bindings(self):
        self.setStyleSheet("color:white")
        self.to_code.setPlaceholderText("Введите текст")
        self.make_btn.clicked.connect(self.set_dialog_window)

    # Создание диалогового окна и вызов функции выполнения
    def set_dialog_window(self):
        # Окно декодирования
        if self.decode_rBtn.isChecked():
            file_name = QFileDialog.getOpenFileName(
                caption="Выбрать изображение", filter="Файлы изображений (*.bmp)")
            return_code, decoded_str = decode(file_name[0])
            if return_code == EXIT_SUCCESS:
                self.decoded.setText(decoded_str)
            else:
                if return_code == EXIT_PERMISSON:
                    string = "Доступ отклонен"
                elif return_code == EXIT_OVERFLOW:
                    string = "Размер строки превышен"
                elif return_code == EXIT_OTHER:
                    string = "Непредвиденная ошибка"
                self.show_exception_message(string)
        # Окно кодирования
        else:
            choosed_file = QFileDialog.getOpenFileName(
                caption="Выбрать изображение", filter="Файлы изображений (*.bmp)")
            new_file = QFileDialog.getSaveFileName(
                caption="Сохранить изображение", filter="Файлы изображений (*.bmp)")
            return_code = code(
                choosed_file[0], self.to_code.text(), new_file[0])
            if return_code[0] == EXIT_SUCCESS:
                self.preview.clear()
                self.preview.setScaledContents(True)
                self.preview.setPixmap(QPixmap(new_file[0]))
            else:
                if return_code[0] == EXIT_PERMISSON:
                    string = "Доступ отклонен"
                elif return_code[0] == EXIT_OVERFLOW:
                    string = "Размер строки превышен"
                elif return_code[0] == EXIT_OTHER:
                    string = "Непредвиденная ошибка"
                self.show_exception_message(return_code[1])
