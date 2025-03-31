from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic
import re
from model import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("sum.ui", self)
        self.bindings()

    def check_correct(self):
        if len(self.input.text()) > 8 or re.fullmatch('^[01]*$', self.input.text()) is None:
            cur_pos = self.input.cursorPosition()
            self.input.setText(
                self.input.text()[:cur_pos-1]+self.input.text()[cur_pos:])

    def show_result(self):
        self.reverse.setText(gen_reverse(self.input.text()))
        self.additional.setText(gen_add(self.reverse.text()))

    def bindings(self):
        self.input.textEdited.connect(self.check_correct)
        self.push.clicked.connect(self.show_result)
