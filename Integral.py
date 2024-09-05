import sys
import numpy as np
import re

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QSlider, QWidget, QApplication, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption

class MainError(Exception): pass

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUi()
        self.connectUi()
        self.update_NumSeg()
        # self.setFixedSize(1000, 700)

    def initUi(self):
        self.centralWidget = QWidget(self)
        self.integral_methods = Integral_Methods(self)
        self.plotWidget = PlotWidget(self.integral_methods)

        self.H1 = QHBoxLayout(self.centralWidget)
        self.H2 = QHBoxLayout(self.centralWidget)
        self.H3 = QHBoxLayout(self.centralWidget)
        self.H4 = QHBoxLayout(self.centralWidget)
        self.H5 = QHBoxLayout(self.centralWidget)
        self.H6 = QHBoxLayout(self.centralWidget)
        self.H7 = QHBoxLayout(self.centralWidget)
        self.H8 = QHBoxLayout(self.centralWidget)

        self.V1 = QVBoxLayout(self.centralWidget)
        self.V2 = QVBoxLayout(self.centralWidget)
        self.V3 = QVBoxLayout(self.centralWidget)
        self.V4 = QVBoxLayout(self.centralWidget)
        self.V5 = QVBoxLayout(self.centralWidget)
        self.V6 = QVBoxLayout(self.centralWidget)
        self.V7 = QVBoxLayout(self.centralWidget)

        self.btn_graph = QPushButton('Построить график')
        self.btn_graph.setFixedWidth(150)

        self.btn_integral = QPushButton('Вычислить')
        self.btn_integral.setFixedWidth(150)

        self.equation = QTextEdit(self)
        self.equation.setFixedSize(150, 24)
        self.equation.setWordWrapMode(QTextOption.NoWrap)

        self.tit_equation = QLabel('Уравнение f(x)')

        self.Xa = QTextEdit()
        self.Xa.setFixedSize(150, 24)
        self.tit_Xa = QLabel('Левая граница')

        self.Xb = QTextEdit()
        self.Xb.setFixedSize(150, 24)
        self.tit_Xb = QLabel('Правая граница')

        min_seg = 2
        max_seg = 100
        self.num_seg = QSlider()
        self.num_seg.setOrientation(Qt.Horizontal)
        self.num_seg.setFixedWidth(150)
        self.num_seg.setRange(min_seg, max_seg)
        self.num_seg.setObjectName("num_seg")
        self.num_seg.setTickInterval(10)
        self.num_seg.setSingleStep(5)
        self.num_seg.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.num_seg.setValue(min_seg)
        self.tit_num_seg = QLabel('Число разбиений')
        self.text_num_seg = QLabel('1')

        self.res_rect = QTextEdit()
        self.res_rect.setFixedSize(150, 24)
        self.tit_res_rect = QLabel('Метод прямоугольников')

        self.res_trap = QTextEdit()
        self.res_trap.setFixedSize(150, 24)
        self.tit_res_trap = QLabel('Метод трапеций')

        self.res_Simp = QTextEdit()
        self.res_Simp.setFixedSize(150, 24)
        self.tit_res_Simp = QLabel('Метод Симпсона')

        self.H6.addWidget(self.res_rect)
        self.H6.addWidget(self.tit_res_rect)

        self.H7.addWidget(self.res_trap)
        self.H7.addWidget(self.tit_res_trap)

        self.H8.addWidget(self.res_Simp)
        self.H8.addWidget(self.tit_res_Simp)

        self.V7.addLayout(self.H6)
        self.V7.addLayout(self.H7)
        self.V7.addLayout(self.H8)

        self.V6.addWidget(self.btn_graph)
        self.V6.addWidget(self.btn_integral)

        self.V3.addLayout(self.V6)
        self.V3.addLayout(self.V7)

        self.H2.addWidget(self.equation)
        self.H2.addWidget(self.tit_equation)

        self.H3.addWidget(self.Xa)
        self.H3.addWidget(self.tit_Xa)

        self.H4.addWidget(self.Xb)
        self.H4.addWidget(self.tit_Xb)

        self.V4.addLayout(self.H2)
        self.V4.addLayout(self.H3)
        self.V4.addLayout(self.H4)

        self.H5.addWidget(self.num_seg)
        self.H5.addWidget(self.text_num_seg)

        self.V5.addLayout(self.H5)
        self.V5.addWidget(self.tit_num_seg)
        self.V5.setAlignment(Qt.AlignTop)

        self.V2.addLayout(self.V4)
        self.V2.addLayout(self.V5)

        self.V1.addLayout(self.V2)
        self.V1.addLayout(self.V3)

        self.H1.addWidget(self.plotWidget)
        self.H1.addLayout(self.V1)

        self.setCentralWidget(self.centralWidget)

    def update_NumSeg(self):
        self.text_num_seg.setText(str(self.num_seg.value()))
        val = self.num_seg.value()
        return val

    def connectUi(self):
        self.btn_integral.clicked.connect(self.integral_methods.Integral)
        self.btn_graph.clicked.connect(self.plotWidget.plot)
        self.num_seg.valueChanged.connect(self.update_NumSeg)

class Integral_Methods():
    def __init__(self, MainWindow, parent=None):
        #super(Integral_Methods, self).__init__()
        self.mainwindow = MainWindow

    def borders(self): #функция границ интеграла
        self.xa = self.mainwindow.Xa
        self.xb = self.mainwindow.Xb

        self.xa = float(self.xa.toPlainText())
        self.xb = float(self.xb.toPlainText())

        if self.xa>self.xb:
            xbn=self.xb
            self.xb=self.xa
            self.xa=xbn

        return self.xa, self.xb

    def func(self, x):
        self.equa = self.mainwindow.equation.toPlainText()
        try:
            self.ev_res = eval(self.equa)
        except ZeroDivisionError:
            self.ev_res = 0
        return self.ev_res

    def rectangle(self):
        xa, xb = self.borders()
        n = self.mainwindow.update_NumSeg()
        sum = 0
        h = (xb - xa) / n
        btx = xa + h/2
        while (btx < xb):
            sum += self.func(btx)
            btx += h

        return sum * h

    def trapezium(self):
        xa, xb = self.borders()
        n = self.mainwindow.update_NumSeg()
        sum = 0
        h = (xb - xa) / n
        btx = xa + h
        sum = (self.func(xa) + self.func(xb)) / 2
        for i in range(1, n):
            sum += self.func(btx)
            btx += h

        return sum * h

    def Simpson(self):
        xa, xb = self.borders()
        n = self.mainwindow.update_NumSeg()
        sum = 0
        btx = xa
        h = (xb - xa) / n
        sum = self.func(xa) + self.func(xb)
        sum1 = 0
        sum2 = 0
        for i in range(1, n, 2):
            sum1 += self.func(btx + i * h)
        for i in range(2, n, 2):
            sum2 += self.func(btx + i * h)
        sum = (h / 3) * (sum + 4 * sum1 + 2 * sum2)

        return sum

    def check_empty_equation(self):
        self.c_equa = self.mainwindow.equation.toPlainText()
        if not self.c_equa or self.c_equa.isspace():
            return False
        else:
            return True

    def check_x_equation(self):
        x_equa = self.mainwindow.equation.toPlainText()
        print(x_equa)
        reg = "^[0-9^.x*()/+-]+$"
        pattern = re.compile(reg)
        print(pattern.search(x_equa) is not None)
        if pattern.search(x_equa) is not None:
            return True
        else:
            return False

    def check_empty_borders(self):
        c_A = self.mainwindow.Xa.toPlainText()
        c_B = self.mainwindow.Xb.toPlainText()

        if (not c_A or not c_B or c_A.isspace() or c_B.isspace()):
            return False
        else:
            return True

    def check_digital_borders(self):
        c_A = self.mainwindow.Xa.toPlainText()
        c_B = self.mainwindow.Xb.toPlainText()

        try:
            float(c_A)
            float(c_B)
            return True
        except ValueError:
            return False

    def error_messageBox(self, error_description):
        error_equa = QMessageBox()
        error_equa.setWindowTitle("Ошибка")
        error_equa.setText(error_description)
        error_equa.setIcon(QMessageBox.Warning)
        error_equa.setStandardButtons(QMessageBox.Close)
        error_equa.exec_()
        return 0

    def Integral(self):
        check_e_e = self.check_empty_equation()
        check_x_e = self.check_x_equation()
        check_e_b = self.check_empty_borders()
        check_d_b = self.check_digital_borders()

        self.res_rect = self.mainwindow.res_rect
        self.res_trap = self.mainwindow.res_trap
        self.res_Simp = self.mainwindow.res_Simp

        if check_e_e == False:
            self.error_messageBox('Не указано уравнение функции!')
        else:
            if check_x_e == False:
                self.error_messageBox('Неверный формат уравнения!')
            else:
                if check_e_b == False:
                    self.error_messageBox('Не указаны границы интеграла!')
                else:
                    if check_d_b == False:
                        self.error_messageBox('Неверно указаны границы интеграла!')
                    else:
                        r_res = self.rectangle()
                        t_res = self.trapezium()
                        s_res = self.Simpson()

                        self.res_rect.setText(str(r_res))
                        self.res_trap.setText(str(t_res))
                        self.res_Simp.setText(str(s_res))
        return 0

class PlotWidget(QWidget):
    def __init__(self, Integral_Methods, parent=None):
        super(PlotWidget, self).__init__(parent) # Инициализирование экземпляр
        self.initUi() # Формирование интерфейса
        self.integral_methods = Integral_Methods

    def initUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

    def plot(self):
        check_e_e = self.integral_methods.check_empty_equation()
        check_x_e = self.integral_methods.check_x_equation()
        check_e_b = self.integral_methods.check_empty_borders()
        check_d_b = self.integral_methods.check_digital_borders()

        if check_e_e == False:
            self.integral_methods.error_messageBox('Не указано уравнение функции!')
        else:
            if check_x_e == False:
                self.integral_methods.error_messageBox('Неверный формат уравнения!')
            else:
                if check_e_b == False:
                    self.integral_methods_methods.error_messageBox('Не указаны границы интеграла!')
                else:
                    if check_d_b == False:
                        self.integral_methods.error_messageBox('Неверно указаны границы интеграла!')
                    else:
                        font = FontProperties()
                        font.set_family('serif')
                        font.set_name('Arial')
                        font.set_size('large')

                        xa, xb = self.integral_methods.borders()

                        x = np.linspace(xa, xb, 100)
                        y = self.integral_methods.func(x)

                        self.figure.clear()

                        ax = self.figure.add_subplot(111)
                        ax.set_facecolor('#4a5b67')
                        ax.grid()
                        ax.plot(x, y, linestyle = '-', color='#ffa1c0', label='f(x)')
                        ax.legend(loc='upper right')
                        ax.set_xlabel('X', fontproperties=font)
                        ax.set_ylabel('Y', fontproperties=font)
                        ax.fill_between(x, y, np.zeros_like(y), color='#bd305b')

                        self.canvas.draw()

app = QApplication([])
p = MainWindow()
p.show()

sys.exit(app.exec_())
