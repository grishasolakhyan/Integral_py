from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel, QWidget
import numpy as np
import matplotlib.pyplot as plt
import math

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        window_title = "Интеграл v. 0.5.1"
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1200, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowTitle(window_title)

        self.equation = QtWidgets.QTextEdit(self.centralwidget)
        self.equation.setGeometry(QtCore.QRect(770, 10, 150, 30))
        self.equation.setObjectName("equation")
        self.equation.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.bord_a = QtWidgets.QTextEdit(self.centralwidget)
        self.bord_a.setGeometry(QtCore.QRect(770, 50, 150, 30))
        self.bord_a.setObjectName("bord_a")
        self.bord_a.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.bord_b = QtWidgets.QTextEdit(self.centralwidget)
        self.bord_b.setGeometry(QtCore.QRect(770, 90, 150, 30))
        self.bord_b.setObjectName("bord_b")
        self.bord_b.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.num_seg = QtWidgets.QSlider(self.centralwidget)

        min_seg=2
        max_seg=100

        self.num_seg.setGeometry(QtCore.QRect(770, 130, 150, 22))
        self.num_seg.setOrientation(QtCore.Qt.Horizontal)
        self.num_seg.setRange(min_seg, max_seg)
        self.num_seg.setObjectName("num_seg")
        self.num_seg.setTickInterval(10)
        self.num_seg.setSingleStep(5)
        self.num_seg.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.num_seg.setValue(min_seg)

        self.text_seg = QtWidgets.QLabel(self.centralwidget)
        self.text_seg.setGeometry(QtCore.QRect(930, 130, 100, 22))
        self.text_seg.setObjectName("label_seg")

        self.text_seg_name = QtWidgets.QLabel(self.centralwidget)
        self.text_seg_name.setGeometry(QtCore.QRect(770, 160, 100, 22))
        self.text_seg_name.setObjectName("label_seg_name")

        self.btn_graph = QtWidgets.QPushButton(self.centralwidget)
        self.btn_graph.setGeometry(QtCore.QRect(770, 400, 120, 30))
        self.btn_graph.setStyleSheet("")
        self.btn_graph.setObjectName("btn_graph")

        self.btn_integral = QtWidgets.QPushButton(self.centralwidget)
        self.btn_integral.setGeometry(QtCore.QRect(770, 440, 120, 30))
        self.btn_integral.setStyleSheet("")
        self.btn_integral.setObjectName("btn_integral")

        self.result_rect = QtWidgets.QTextBrowser(self.centralwidget)
        self.result_rect.setGeometry(QtCore.QRect(770, 480, 150, 30))
        self.result_rect.setObjectName("result_rect")

        self.result_trap = QtWidgets.QTextBrowser(self.centralwidget)
        self.result_trap.setGeometry(QtCore.QRect(770, 520, 150, 30))
        self.result_trap.setObjectName("result_trap")

        self.result_Simp = QtWidgets.QTextBrowser(self.centralwidget)
        self.result_Simp.setGeometry(QtCore.QRect(770, 560, 150, 30))
        self.result_Simp.setObjectName("result_Simp")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 10, 750, 580))
        self.widget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget.setObjectName("widget")

        self.text_equa = QtWidgets.QLabel(self.centralwidget)
        self.text_equa.setGeometry(QtCore.QRect(930, 10, 100, 30))
        self.text_equa.setObjectName("label_equa")

        self.text_a = QtWidgets.QLabel(self.centralwidget)
        self.text_a.setGeometry(QtCore.QRect(930, 50, 100, 30))
        self.text_a.setObjectName("label_xa")

        self.text_b = QtWidgets.QLabel(self.centralwidget)
        self.text_b.setGeometry(QtCore.QRect(930, 90, 100, 30))
        self.text_b.setObjectName("label_xb")

        self.text_rect = QtWidgets.QLabel(self.centralwidget)
        self.text_rect.setGeometry(QtCore.QRect(930, 480, 150, 30))
        self.text_rect.setObjectName("label_rect")

        self.text_trap = QtWidgets.QLabel(self.centralwidget)
        self.text_trap.setGeometry(QtCore.QRect(930, 520, 150, 30))
        self.text_trap.setObjectName("label_trap")

        self.text_Simp = QtWidgets.QLabel(self.centralwidget)
        self.text_Simp.setGeometry(QtCore.QRect(930, 560, 150, 30))
        self.text_Simp.setObjectName("label_Simp")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_functions()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_graph.setText(_translate("MainWindow", "Построить график"))
        self.btn_integral.setText(_translate("MainWindow", "Вычислить"))
        self.text_seg.setText(_translate("MainWindow", "0"))
        self.text_seg_name.setText(_translate("MainWindow", "Число разбиений"))
        self.text_equa.setText(_translate("MainWindow", "Уравнение f(x)"))
        self.text_a.setText(_translate("MainWindow", "Левая граница"))
        self.text_b.setText(_translate("MainWindow", "Правая граница"))

        self.text_rect.setText(_translate("MainWindow", "Метод прямоугольников"))
        self.text_trap.setText(_translate("MainWindow", "Метод трапеций"))
        self.text_Simp.setText(_translate("MainWindow", "Метод Симпсона"))


    def add_functions(self):
        self.btn_graph.clicked.connect(lambda: self.draw_graph())
        self.btn_integral.clicked.connect(lambda: self.Integral())
        self.num_seg.valueChanged.connect(self.update_NumSeg)

    def check_empty_equation(self): #функция проверки на пустоту строки уравнения
        c_equa = self.equation.toPlainText()
        if not c_equa or c_equa.isspace():
            return False
        else:
            return True

    def error_empty_equation(self): #функция вывода ошибки пустой строки уравнения
        error_equa = QMessageBox()
        error_equa.setWindowTitle("Ошибка")
        error_equa.setText("Не указано уравнение функции!")
        error_equa.setIcon(QMessageBox.Warning)
        error_equa.setStandardButtons(QMessageBox.Close)
        error_equa.exec_()
        return 0

    def check_empty_borders(self): #функция проверки на пустоту строк границ интеграла
        c_A = self.bord_a.toPlainText()
        c_B = self.bord_b.toPlainText()

        if (not c_A or not c_B or c_A.isspace() or c_B.isspace()):
            return False
        else:
            return True

    def error_empty_borders(self): #функция вывода ошибки пустых строк границ интеграла
        error_bord = QMessageBox()
        error_bord.setWindowTitle("Ошибка")
        error_bord.setText("Не указаны границы интеграла!")
        error_bord.setIcon(QMessageBox.Warning)
        error_bord.setStandardButtons(QMessageBox.Close)
        error_bord.exec_()
        return 0

    def check_digital_borders(self):
        c_A = self.bord_a.toPlainText()
        c_B = self.bord_b.toPlainText()

        try:
            float (c_A)
            float (c_B)
            return True
        except ValueError:
            return False

    def error_digital_borders(self):
        error_bord = QMessageBox()
        error_bord.setWindowTitle("Ошибка")
        error_bord.setText("Неверно указаны границы интеграла!")
        error_bord.setIcon(QMessageBox.Warning)
        error_bord.setStandardButtons(QMessageBox.Close)
        error_bord.exec_()
        return 0

    def func(self, x): #функция функции уравнения
        equa = self.equation.toPlainText()
        ev=eval(equa)
        return ev

    def int_borders(self): #функция границ интеграла
        xa = float(self.bord_a.toPlainText())
        xb = float(self.bord_b.toPlainText())

        if xa>xb:
            xbn=xb
            xb=xa
            xa=xbn
        return xa, xb

    def update_NumSeg(self): #функция вывода числа разбиений интеграла
        self.text_seg.setText(str(self.num_seg.value()))
        val = self.num_seg.value()
        return val

    def rectangle(self): #функция метода прямоугольников
        xa, xb = self.int_borders()
        n = self.update_NumSeg()
        sum = 0
        h = (xb - xa) / n
        btx = xa + h/2
        while(btx < xb):
            sum += self.func(btx)
            btx += h
        return sum * h

    def trapezium(self): #функция метода трапеций
        xa, xb = self.int_borders()
        n = self.update_NumSeg()
        sum = 0
        h = (xb - xa) / n
        btx = xa+h
        sum = (self.func(xa)+self.func(xb))/2
        for i in range (1, n):
            sum += self.func(btx)
            btx += h
        return sum * h

    def Simpson(self): #функция метода Симпсона
        xa, xb = self.int_borders()
        n = self.update_NumSeg()
        sum=0
        btx = xa
        h = (xb - xa) / n
        sum = self.func(xa)+self.func(xb)
        sum1 = 0
        sum2 = 0
        for i in range (1, n, 2):
            sum1 += self.func(btx + i * h)
        for i in range (2, n, 2):
            sum2 += self.func(btx + i * h)
        sum = (h / 3) * (sum + 4 * sum1 + 2 * sum2)
        return sum

    def Integral(self): #функция расчёта интеграла
        check_e_r = self.check_empty_equation()
        check_e_b = self.check_empty_borders()
        check_d_b = self.check_digital_borders()
        if check_e_r == False:
            self.error_empty_equation()
        else:
            if check_e_b == False:
                self.error_empty_borders()
            else:
                if check_d_b == False:
                    self.error_digital_borders()
                else:
                    r_res = self.rectangle()
                    t_res = self.trapezium()
                    s_res = self.Simpson()

                    self.result_rect.setText(str(r_res))
                    self.result_trap.setText(str(t_res))
                    self.result_Simp.setText(str(s_res))
        return 0

    def draw_graph(self): #функция построения графика функции
        check_e_r = self.check_empty_equation()
        check_e_b = self.check_empty_borders()
        check_d_b = self.check_digital_borders()
        if check_e_r == False:
            self.error_empty_equation()
        else:
            if check_e_b == False:
                self.error_empty_borders()
            else:
                if check_d_b == False:
                    self.error_digital_borders()
                else:
                    xa, xb = self.int_borders()

                    fig = plt.figure()
                    fig.patch.set_facecolor('#4a5b67')
                    fig.patch.set_alpha(1)

                    ax = fig.add_subplot(111)
                    ax.patch.set_alpha(0.0)

                    t=np.linspace(xa, xb)
                    y=self.func(t)
                    plt.plot(t, y, color='#ffa1c0')
                    plt.fill_between(t, y, np.zeros_like(y), color='#bd305b')
                    plt.grid()
                    plt.show()
        return 0


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())