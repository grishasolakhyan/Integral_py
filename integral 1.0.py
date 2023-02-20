import sys
import random # Для рандомного выбора функций
import numpy as np # Для вычислений

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # Область для черчения
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # Панель управления
from matplotlib.figure import Figure # Фигура для черчения

# Импортирование необходимых виджетов
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QWidget, QApplication, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):


app = QApplication([])
p = MainWindow()
p.show()

sys.exit(app.exec_())