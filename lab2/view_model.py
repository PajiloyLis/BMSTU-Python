from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from model import *
from time import sleep
from drawer import make_plot, append_roots


class MainWindow(QMainWindow):
    ending = 1  # 1 - по значению, 0 - по разности

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("lab2.ui", self)
        self.make_table()
        self.bindings()
        self.menu_binds()

    # Бинды меню
    def menu_binds(self):
        self.info.triggered.connect(self.show_about_message)
        self.mistakes.triggered.connect(self.show_mistakes_message)
        self.calc_m.triggered.connect(self.push)

    def show_about_message(self):
        msg_window = QMessageBox()
        msg_window.setWindowTitle("Info")
        msg_window.setText("Программа для решения \
уравнений и построения графиков\n\
Автор: Бугаков И. С. ИУ7-24Б")
        msg_window.exec()

    def show_mistakes_message(self):
        msg_window = QMessageBox()
        msg_window.setWindowTitle("Mistakes")
        msg_window.setText("0 - корень успешно вычислен\n\
1 - превышено максимальное число итераций\n\
2 - ошибка связанная с областью определения\n\
3 - найденный корень лежит за пределами рассматриваемого отрезка")
        msg_window.exec()

    def make_table(self):
        for i in range(6):
            self.table.insertColumn(i)
        self.table.insertRow(0)
        self.table.setCellWidget(0, 0, QLabel("№ корня"))
        self.table.setCellWidget(0, 1, QLabel("[left; right]"))
        self.table.setCellWidget(0, 2, QLabel("x* - корень"))
        self.table.setCellWidget(0, 3, QLabel("f(x*)"))
        self.table.setCellWidget(0, 4, QLabel("Количество итераций"))
        self.table.setCellWidget(0, 5, QLabel("Код ошибки"))

    def bindings(self):
        self.setStyleSheet("color:white")
        self.func_enter.setPlaceholderText("Введите функцию")
        self.left_enter.setPlaceholderText("Введите левую границу поиска")
        self.left_enter.textEdited.connect(self.check_numeric)
        self.right_enter.setPlaceholderText("Введите правую границу поиска")
        self.right_enter.textEdited.connect(self.check_numeric)
        self.step.setPlaceholderText("Введите шаг отрезка")
        self.step.textEdited.connect(self.check_numeric)
        self.Nmax.setPlaceholderText("Введите максимальное число итераций")
        self.Nmax.textEdited.connect(self.check_numeric)
        self.eps.setPlaceholderText("Введите точность")
        self.eps.textEdited.connect(self.check_numeric)
        self.calc.clicked.connect(self.push)
        self.val_end.toggled.connect(self.ending_changed)
        self.sub_end.toggled.connect(self.ending_changed)

    def ending_changed(self):
        sender = self.sender()
        if sender == self.val_end:
            self.ending = 1
        else:
            self.ending = 0

    def push(self):
        expression = self.func_enter.text()
        left = self.make_numbers(self.left_enter.text())
        right = self.make_numbers(self.right_enter.text())
        eps = self.make_numbers(self.eps.text())
        step = self.make_numbers(self.step.text())
        Nmax = int(self.make_numbers(self.Nmax.text()))
        _, handles = make_plot(expression, left, right, eps)
        if _:
            roots = solve(left, right, step, Nmax,
                          expression, eps, self.ending)
            append_roots(roots, expression, handles)
            roots = self.format_roots(roots)
            self.table.setRowCount(1)
            for i in range(len(roots)):
                self.table.insertRow(i+1)
                for j in range(6):
                    self.table.setCellWidget(i+1, j, QLabel(str(roots[i][j])))
            self.func_enter.setStyleSheet("color:white")
            self.picture.clear()
            self.picture.setScaledContents(True)
            self.picture.setPixmap(QPixmap("plt.jpg"))
        else:
            self.func_enter.setStyleSheet("color:red")

    def format_roots(self, roots):
        for i in range(len(roots)):
            if roots[i][5] == 0:
                roots[i] = [roots[i][0], f"[{roots[i][1][0]:.5g}; {roots[i][1][1]:.5g}]", f"{roots[i][2]:.5g}",
                                f"{roots[i][3]:.5g}", roots[i][4], roots[i][5]]
            elif roots[i][5] == 3:
                roots[i] = [roots[i][0], f"[{roots[i][1][0]:.5g}; {roots[i][1][1]:.5g}]", "",
                                  "", "", roots[i][5]]
            else:
                roots[i] = [roots[i][0], f"[{roots[i][1][0]:.5g}; {roots[i][1][1]:.5g}]", "", "", roots[i][4], roots[i][5]]
        return roots

    def check_numeric(self):
        sender = self.sender()
        if sender.text() != "":
            try:
                left = float(sender.text())
            except ValueError:
                sender.setStyleSheet("color:red")
                self.calc.setEnabled(False)
            except OverflowError:
                sender.setStyleSheet("color:red")
                sender.setText("Переполнение типа в функции check_numeric")
                self.calc.setEnabled(False)
            except Exception:
                sender.setText("Unknown exception")
                sender.setStyleSheet("color:red")
                self.calc.setEnabled(False)
            else:
                sender.setStyleSheet("color:white")
                self.calc.setEnabled(True)
        else:
            sender.setStyleSheet("color:white")
            self.calc.setEnabled(True)

    def make_numbers(self, str):
        return float(str)
