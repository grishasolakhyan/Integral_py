import sys
import numpy as np
import re

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QSlider, QWidget, QApplication, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QTextEdit, QSplitter, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption

class ParametersError(Exception): pass
class EquationError(Exception): pass

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUi()
        self.connectUi()
        self.update_NumSeg()
        self.setFixedSize(1280, 720)

    def initUi(self):
        self.main_layout = QVBoxLayout()
        self.splitter_1 = QSplitter(Qt.Horizontal)
        self.setWindowTitle('Integral')

        self.integral_methods = Integral_Methods(self)
        self.plotWidget = PlotWidget(self.integral_methods)

        self.btn_graph = QPushButton('Построить график')
        self.btn_graph.setFixedHeight(24)

        self.btn_integral = QPushButton('Вычислить')
        self.btn_integral.setFixedHeight(24)

        self.equation = QTextEdit(self)
        self.equation.setFixedHeight(24)
        self.equation.setWordWrapMode(QTextOption.NoWrap)
        self.equation_layout = QHBoxLayout()
        self.equation_layout.addWidget(QLabel('Уравнение f(x)'))
        self.equation_layout.addWidget(self.equation)

        self.Xa = QTextEdit()
        self.Xa.setFixedHeight(24)
        self.Xa_layout = QHBoxLayout()
        self.Xa_layout.addWidget(QLabel('Левая граница'))
        self.Xa_layout.addWidget(self.Xa)

        self.Xb = QTextEdit()
        self.Xb.setFixedHeight(24)
        self.Xb_layout = QHBoxLayout()
        self.Xb_layout.addWidget(QLabel('Правая граница'))
        self.Xb_layout.addWidget(self.Xb)

        min_seg = 2
        max_seg = 100
        self.num_seg = QSlider()
        self.num_seg.setOrientation(Qt.Horizontal)
        # self.num_seg.setMaximumWidth(150)
        self.num_seg.setRange(min_seg, max_seg)
        self.num_seg.setObjectName("num_seg")
        self.num_seg.setTickInterval(10)
        self.num_seg.setSingleStep(5)
        self.num_seg.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.num_seg.setValue(min_seg)
        self.text_num_seg = QLabel('1')
        self.text_num_seg.setFixedHeight(24)
        self.num_seg_layout = QHBoxLayout()
        self.num_seg_layout.addWidget(QLabel('Число разбиений'))
        self.num_seg_layout.addWidget(self.num_seg)
        self.num_seg_layout.addWidget(self.text_num_seg)

        self.res_rect = QTextEdit()
        self.res_rect.setFixedHeight(24)
        self.res_rect_layout = QHBoxLayout()
        self.res_rect_layout.addWidget(QLabel('Метод прямоугольников'))
        self.res_rect_layout.addWidget(self.res_rect)


        self.res_trap = QTextEdit()
        self.res_trap.setFixedHeight(24)
        self.res_trap_layout = QHBoxLayout()
        self.res_trap_layout.addWidget(QLabel('Метод трапеций'))
        self.res_trap_layout.addWidget(self.res_trap)

        self.res_Simp = QTextEdit()
        self.res_Simp.setFixedHeight(24)
        self.res_Simp_layout = QHBoxLayout()
        self.res_Simp_layout.addWidget(QLabel('Метод Симпсона'))
        self.res_Simp_layout.addWidget(self.res_Simp)

        self.input_layout = QVBoxLayout()
        self.button_layout = QVBoxLayout()
        self.output_layout = QVBoxLayout()

        self.input_layout.addLayout(self.equation_layout)
        self.input_layout.addLayout(self.Xa_layout)
        self.input_layout.addLayout(self.Xb_layout)
        self.input_layout.addLayout(self.num_seg_layout)

        self.button_layout.addWidget(self.btn_integral)
        self.button_layout.addWidget(self.btn_graph)

        self.output_layout.addLayout(self.res_rect_layout)
        self.output_layout.addLayout(self.res_trap_layout)
        self.output_layout.addLayout(self.res_Simp_layout)

        # Group 1
        self.parameters_group = QFrame()
        self.parameters_group_layout = QVBoxLayout()
        # self.parameters_group_layout.addLayout(self.equation_layout)
        # self.parameters_group_layout.addLayout(self.Xa_layout)
        # self.parameters_group_layout.addLayout(self.Xb_layout)
        # self.parameters_group_layout.addLayout(self.num_seg_layout)
        # self.parameters_group_layout.addWidget(self.btn_integral)
        # self.parameters_group_layout.addWidget(self.btn_graph)
        # self.parameters_group_layout.addLayout(self.res_rect_layout)
        # self.parameters_group_layout.addLayout(self.res_trap_layout)
        # self.parameters_group_layout.addLayout(self.res_Simp_layout)
        self.parameters_group_layout.addLayout(self.input_layout)
        self.parameters_group_layout.addLayout(self.button_layout)
        self.parameters_group_layout.addLayout(self.output_layout)
        self.parameters_group.setLayout(self.parameters_group_layout)

        # Group 2
        self.plot_widget_group = QFrame()
        self.plot_widget_group_layout = QVBoxLayout()
        self.plot_widget_group_layout.addWidget(self.plotWidget)
        self.plot_widget_group.setLayout(self.plot_widget_group_layout)

        self.splitter_1.addWidget(self.plot_widget_group)
        self.splitter_1.addWidget(self.parameters_group)

        self.main_layout.addWidget(self.splitter_1)
        self.setLayout(self.main_layout)

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

    def checking_parameters(self):
        c_equa = self.mainwindow.equation.toPlainText()
        reg = "^[0-9^.x*()/+-]+$"
        pattern = re.compile(reg)
        c_A = self.mainwindow.Xa.toPlainText()
        c_B = self.mainwindow.Xb.toPlainText()

        if not c_equa or c_equa.isspace(): # если не указано уравнение функции
            raise EquationError()
        elif pattern.search(c_equa) is None: # если неверно указано уравнение функции
            raise EquationError()
        elif not c_A or not c_B or c_A.isspace() or c_B.isspace(): # если не указаны границы интеграла
            raise ParametersError()
        elif float(c_A) == False or float(c_B) == False: # если неверно указаны границы интеграла
            raise ParametersError()

    def error_messageBox(self, error_description):
        error_equa = QMessageBox()
        error_equa.setWindowTitle("Ошибка")
        error_equa.setText(error_description)
        error_equa.setIcon(QMessageBox.Warning)
        error_equa.setStandardButtons(QMessageBox.Close)
        error_equa.exec_()

        return 0

    def Integral(self):
        try:
            self.checking_parameters()

            self.res_rect = self.mainwindow.res_rect
            self.res_trap = self.mainwindow.res_trap
            self.res_Simp = self.mainwindow.res_Simp

            r_res = self.rectangle()
            t_res = self.trapezium()
            s_res = self.Simpson()

            self.res_rect.setText(str(r_res))
            self.res_trap.setText(str(t_res))
            self.res_Simp.setText(str(s_res))

        except EquationError:
            self.error_messageBox('Неверно указано уравнение функции!')
        except ParametersError:
            self.error_messageBox('Неверно указаны параметры интеграла!')

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
        try:
            self.integral_methods.checking_parameters()

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
            ax.plot(x, y, linestyle='-', color='#ffa1c0', label='f(x)')
            ax.legend(loc='upper right')
            ax.set_xlabel('X', fontproperties=font)
            ax.set_ylabel('Y', fontproperties=font)
            ax.fill_between(x, y, np.zeros_like(y), color='#bd305b')

            self.canvas.draw()

        except EquationError:
            self.integral_methods.error_messageBox('Неверно указано уравнение функции!')
        except ParametersError:
            self.integral_methods.error_messageBox('Неверно указаны параметры интеграла!')

app = QApplication([])
p = MainWindow()
p.show()

sys.exit(app.exec_())
