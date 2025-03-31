from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QTableWidgetItem
from PyQt6.QtGui import QPainter, QPen, QPicture, QColor
from PyQt6.QtCore import QPoint, QLine, QRect
from PyQt6 import QtGui, uic

POINT_CELLS_NUMBER = 2
LINE_CELLS_NUMBER = 4
WHITE = QColor(255, 255, 255)
BLACK = QColor(0, 0, 0)
WIDTH = 600
HEIGHT = 600


class MainWindow(QMainWindow):

    point_cnt, line_cnt = 0, 0
    points = []
    lines = []

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("lab4.ui", self)
        self.canvas.setScaledContents(True)
        self.canvas.setPicture(QPicture())
        self.draw_point([WIDTH, HEIGHT], WHITE)
        self.bindings()

    def bindings(self):
        self.point_table.setColumnCount(POINT_CELLS_NUMBER)
        self.line_table.setColumnCount(LINE_CELLS_NUMBER)
        self.add_point.clicked.connect(self.add_row)
        self.add_line.clicked.connect(self.add_row)
        self.del_point.clicked.connect(self.del_row)
        self.del_line.clicked.connect(self.del_row)
        self.line_table.cellChanged.connect(self.data_changed)
        self.point_table.cellChanged.connect(self.data_changed)

    def data_changed(self, x, y):
        cur = self.sender()
        if cur == self.point_table:
            for i in range(POINT_CELLS_NUMBER):
                if self.points[x][i] == None or self.points[x][i] > 600 or self.points[x][i] < 0:
                    self.point_table.cell(x, i).setBackground(QColor(255, 0, 0))
                    break
            else:
                self.draw_point(self.points[x], WHITE)
            self.points[x][y] = int(cur.item(x, y).text())
            for i in range(POINT_CELLS_NUMBER):
                if self.points[x][i] == None or self.points[x][i] > 600 or self.points[x][i] < 0:
                    self.point_table.item(x, i).setBackground(QColor(255, 0, 0))
                    break
            else:
                for i in range(POINT_CELLS_NUMBER):
                    self.point_table.item(x, i).setBackground(QColor(17,18,18, 255))
                self.draw_point(self.points[x], BLACK)
        else:
            for i in range(LINE_CELLS_NUMBER):
                if self.lines[x][i] == None or self.lines[x][i] > 600 or self.lines[x][i] < 0:
                    self.line_table.item(x, i).setBackground(QColor(255, 0, 0))
                    break
            else:
                self.draw_line(self.lines[x], WHITE)
            self.lines[x][y] = int(cur.item(x, y).text())
            for i in range(LINE_CELLS_NUMBER):
                if self.lines[x][i] == None or self.lines[x][i] > 600 or self.lines[x][i] < 0:
                    self.line_table.item(x, i).setBackground(QColor(255, 0, 0))
                    break
            else:
                for i in range(LINE_CELLS_NUMBER):
                    self.line_table.item(x, i).setBackground(QColor(17,18,18, 255))
                self.draw_line(self.lines[x], BLACK)

    def add_row(self):
        sender = self.sender()
        if sender == self.add_point:
            self.point_table.insertRow(self.point_cnt)
            for i in range(POINT_CELLS_NUMBER):
                self.point_table.setItem(self.point_cnt, i, QTableWidgetItem())
            self.points.append([None, None])
            self.point_cnt += 1
        else:
            self.line_table.insertRow(self.line_cnt)
            self.lines.append([None, None, None, None])
            self.line_cnt += 1

    def del_row(self):
        sender = self.sender()
        if sender == self.del_point:
            line_number = self.point_table.currentRow()
            if line_number != -1:
                self.point_table.removeRow(line_number)
                self.point_cnt -= 1
                self.draw_point(self.points[line_number], WHITE)
                self.points.pop(line_number)
        else:
            line_number = self.line_table.currentRow()
            if line_number != -1:
                self.line_table.removeRow(line_number)
                self.line_cnt -= 1
                self.draw_line(self.lines[line_number], WHITE)
                self.lines.pop(line_number)

    def draw_point(self, cord, color=BLACK):
        pic = self.canvas.picture()
        qp = QPainter()
        new_pic = QPicture()
        qp.begin(new_pic)
        qp.setPen(QPen(color, 3))
        qp.drawPicture(0, 0, pic)
        qp.drawPoint(cord[0], cord[1])
        qp.end()
        self.canvas.setPicture(new_pic)

    def draw_line(self, cord, color=BLACK):
        qp = QPainter()
        pic = self.canvas.picture()
        new_pic = QPicture()
        qp.begin(new_pic)
        qp.setPen(QPen(color, 3))
        qp.drawPicture(0, 0, pic)
        qp.drawLine(cord[0], cord[1], cord[2], cord[3])
        qp.end()
        self.canvas.setPicture(new_pic)
    # def paintEvent(self):
    #     painter = QPainter(self.canvas)
    #     painter.setPen(QPen((0, 0, 0), 5))
    #     for point in range(len(self.points)):
    #         painter.drawPoint(point)

    # Бинды меню
#     def menu_binds(self):
#         self.info.triggered.connect(self.show_about_message)
#         self.make.triggered.connect(self.set_dialog_window)

#     # Информационное окно
#     def show_about_message(self):
#         msg_window = QMessageBox()
#         msg_window.setWindowTitle("Info")
#         msg_window.setText("Программа для решения \
# уравнений и построения графиков\n\
# Автор: Бугаков И. С. ИУ7-24Б")
#         msg_window.exec()
