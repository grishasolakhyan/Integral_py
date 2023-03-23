import sys
import random
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Область для черчения
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # Панель управления
from matplotlib.figure import Figure # Фигура для черчения

# Импортирование виджетов
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QSlider, QWidget, QApplication, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QTextEdit, QGroupBox
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QTextOption

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUi()
        self.connectUi()
        self.update_NumSeg()

    def initUi(self):
        self.centralWidget = QWidget(self)
        self.plotWidget = PlotWidget()
        self.integral_methods = Integral_Methods(self)

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

        #self.btn_graph.setStyleSheet('font-size: 12pt; font-weight: 530;')
        #self.btn_integral.setStyleSheet('font-size: 12pt; font-weight: 530;')

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
        self.btn_integral.clicked.connect(self.integral_methods.int_borders)
        self.btn_graph.clicked.connect(self.plotWidget.Graph)
        self.num_seg.valueChanged.connect(self.update_NumSeg)

class Integral_Methods():
    def __init__(self, MainWindow, parent=None):
        super(Integral_Methods, self).__init__()
        self.mainwindow = MainWindow

    def int_borders(self): #функция границ интеграла
        self.xa = self.mainwindow.Xa
        self.xb = self.mainwindow.Xb

        self.xa = float(self.xa.toPlainText())
        self.xb = float(self.xb.toPlainText())

        if self.xa>self.xb:
            xbn=self.xb
            self.xb=self.xa
            self.xa=xbn

        print(self.xa, ' ',self.xb, sep='')
        return self.xa, self.xb

    def func(self, x):
        x = 10
        self.equa = self.mainwindow.equation.toPlainText()
        self.ev_res = eval(self.equa)
        print(self.ev_res)
        return 0

    def Integral(self):
        print("Hello, World!")

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent) # Инициализирование экземпляр
        self.initUi() # Формирование интерфейса

    def initUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

    def Graph(self):
        print("Hello, Human!")

app = QApplication([])
p = MainWindow()
p.show()

sys.exit(app.exec_())