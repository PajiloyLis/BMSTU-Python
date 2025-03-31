from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from model import calc
from math import *


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("def2.ui", self)
        self.bindings()

    def bindings(self):
        self.calc.clicked.connect(self.push)

    def push(self):
        a, b, eps = float(eval(self.a_edit.text())), float(eval(
            self.b_edit.text())), float(eval(self.eps_edit.text()))
        ans = f"{calc(a, b, eps):.5g}"
        self.out_lbl.setText(ans)
