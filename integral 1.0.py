import sys
import random # Для рандомного выбора функций
import numpy as np # Для вычислений

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Область для черчения
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # Панель управления
from matplotlib.figure import Figure # Фигура для черчения

# Импортирование необходимых виджетов
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QWidget, QApplication, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QTextEdit

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent) # Инициализируем экземпляр
        self.initUi() # Строит интерфейс

    def initUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUi()
        #self.connectUi()

    def initUi(self):
        self.centralWidget = QWidget(self)

        #self.l = QVBoxLayout(self.centralWidget)
        #self.bl = QHBoxLayout(self.centralWidget)

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

        self.plotWidget = PlotWidget()

        self.btn_graph = QPushButton('Построить график')
        self.btn_integral = QPushButton('Вычислить')

        self.equation = QTextEdit()


        self.btn_graph.setStyleSheet('font-size: 12pt; font-weight: 530;')
        self.btn_integral.setStyleSheet('font-size: 12pt; font-weight: 530;')

        #self.bl.addWidget(self.buildButton)
        #self.bl.addWidget(self.calculateButton)

        #self.l.addLayout(self.bl)
        #self.l.addWidget(self.plotWidget)

        self.V7.addLayout(self.H6)
        self.V7.addLayout(self.H7)
        self.V7.addLayout(self.H8)

        self.V6.addWidget(self.btn_graph)
        self.V6.addWidget(self.btn_integral)

        self.V3.addLayout(self.V7)
        self.V3.addLayout(self.V6)

        self.V4.addLayout(self.H2)
        self.V4.addLayout(self.H3)
        self.V4.addLayout(self.H4)

        self.V5.addLayout(self.H5)

        self.V2.addLayout(self.V4)
        self.V2.addLayout(self.V5)

        self.V1.addLayout(self.V2)
        self.V1.addLayout(self.V3)

        self.H1.addWidget(self.plotWidget)
        self.H1.addLayout(self.V1)

        self.setCentralWidget(self.centralWidget)

app = QApplication([])
p = MainWindow()
p.show()

sys.exit(app.exec_())