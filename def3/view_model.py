from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic
from model import binarize


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("def3.ui", self)
        self.bindings()

    # Настройка интерфейса и привязка функций
    def bindings(self):
        self.setStyleSheet("color:white")
        self.limit_edit.setPlaceholderText("Введите пороговое значение")
        self.choose_btn.clicked.connect(self.set_choose_dialog_window)
        self.bin_btn.clicked.connect(self.set_save_dialog_window)

    def set_choose_dialog_window(self):
        file_name = QFileDialog.getOpenFileName(
            caption="Выбрать изображение", filter="Файлы изображений (*.bmp)")
        self.file_name_label.clear()
        self.file_name_label.setText(file_name[0])

    def set_save_dialog_window(self):
        bound = self.limit_edit.text()
        if bound == "":
            self.limit_edit.setStyleSheet("color:red")
        else:
            try:
                bound = int(bound)
            except ValueError:
                self.limit_edit.setStyleSheet("color:red")
            else:
                self.limit_edit.setStyleSheet("color:white")
                file_name = QFileDialog.getSaveFileName(
                    caption="Выбрать изображение", filter="Файлы изображений (*.bmp)")
                binarize(self.file_name_label.text(), bound, file_name[0])
