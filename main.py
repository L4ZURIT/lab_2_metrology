from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys
from mpl import MplCanvas
from numpy import arange, polyfit, poly1d, interp
from scipy import interpolate




class ExtraWindow(MplCanvas):
    def __init__(self, title, start_data) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.start_data = start_data
        self.axes.grid()
        self.axes.plot(self.start_data[0], self.start_data[1], color = "red")
        self.axes.scatter(self.start_data[0], self.start_data[1], s = [10 for i in range(len(self.start_data[0]))])



class MainWindow(QMainWindow):

    def GraphInit(self):
        self.graph.axes.grid()
        self.graph.axes.set_title("Начальный набор точек")
        self.graph.axes.set_xlabel('t')
        self.graph.axes.set_ylabel('y(t)')
        self.graph.axes.plot(self.start_data[0], self.start_data[1], color = "red")
        self.graph.axes.scatter(self.start_data[0], self.start_data[1], s = [10 for i in range(self.sd_size)])
        

    def IInit(self):
        self.gb_graphic: QGroupBox = self.gb_graphic
        self.gb_graphic.setLayout(QVBoxLayout())
        self.gb_graphic.layout().addWidget(self.graph)

    def StartDotsInit(self):
        
        y:list = []
        x:list = []

        t = arange(-0.9, 1, 0.1)
        x = t.tolist()

        for x_value in x:
            y.append(float(1/(1-x_value)))

        return x, y

    def TableInit(self, data):
        self.tw_table:QTableWidget = self.tw_table
        self.tw_table.setColumnCount(len(data[0]))
        self.tw_table.setRowCount(2)
        for col in range(self.tw_table.columnCount()):
            self.tw_table.setItem(0,col, QTableWidgetItem('{:.1f}'.format(data[0][col]))) 
            self.tw_table.setItem(1,col, QTableWidgetItem('{:.3f}'.format(data[1][col]))) 
            self.tw_table.setColumnWidth(col, 15)
        self.tw_table.setVerticalHeaderLabels(["t", "y(t)"])
        
    def NewTableInit(self, x, y):
        self.tw_table_new:QTableWidget = self.tw_table_new
        self.tw_table_new.setColumnCount(len(x))
        self.tw_table_new.setRowCount(2)
        for col in range(self.tw_table_new.columnCount()):
            self.tw_table_new.setItem(0,col, QTableWidgetItem('{:.1f}'.format(x[col]))) 
            self.tw_table_new.setItem(1,col, QTableWidgetItem('{:.3f}'.format(y[col]))) 
            self.tw_table_new.setColumnWidth(col, 15)
        self.tw_table_new.setVerticalHeaderLabels(["t", "f(t)"])

    


    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('Imain.ui',self)


        #region переменные
        self.graph = MplCanvas()
        self.start_data = self.StartDotsInit()
        self.extra_wgt = ExtraWindow("", self.start_data)
        self.sd_size = len(self.start_data[0])
        #region переменные


        self.GraphInit()
        self.IInit()
        self.TableInit(self.start_data)

        #region связка сигналов
        self.pb_spline.clicked.connect(self.Spline)
        self.pb_lagrange.clicked.connect(self.Lagrange)
        self.pb_linear.clicked.connect(self.LinearInterp)
        self.pb_mnk.clicked.connect(self.MNK)
        self.pb_clear.clicked.connect(self.Clear)
        #region связка сигналов

    def Clear(self):
        self.tw_table_new.clear()
        self.graph.axes.cla()
        self.GraphInit()
        self.graph.draw()


    def ShowApproximation(self):
        self.cb_new_window:QCheckBox = self.cb_new_window
        self.extra_wgt.close()

        if self.cb_new_window.isChecked():
            self.extra_wgt = ExtraWindow("МНК", self.start_data)
            cur_axes = self.extra_wgt
            cur_axes.show()
            
        else:
            cur_axes = self.graph

        return cur_axes

    def Mean(self, f):
        summ = 0
        for i, y  in enumerate(self.start_data[1]):
            summ += abs(y-f[i])
        return "{:.12f}".format(summ/self.sd_size)

    # разработка методов аппроксимирующих функций где 
        # start_data - кортеж массивов t, y(t)
        # cur_axes - график
    def MNK(self):
        cur_axes = self.ShowApproximation()
        # полиномиальная апроксимация методом наименьших квадратов с указанием порядка полинома 18
        # вычисление коэффициентов полинома
        t = polyfit(self.start_data[0], self.start_data[1], 18)
        # получение функции
        f = poly1d(t)
        # построение функции по найденным коэффициентам
        cur_axes.axes.plot(self.start_data[0],f(self.start_data[0]), color = "green")
        cur_axes.draw()
        self.NewTableInit(self.start_data[0], f(self.start_data[0]))

        self.lbl_pogr.setText(str(self.Mean(f(self.start_data[0]))))

    def LinearInterp(self):
        cur_axes = self.ShowApproximation()
        # линейная интерполяция
        cur_axes.axes.plot(self.start_data[0], interp(self.start_data[0], self.start_data[0], self.start_data[1]), color = "green")
        cur_axes.draw()
        self.NewTableInit(self.start_data[0], interp(self.start_data[0], self.start_data[0], self.start_data[1]))
        
        self.lbl_pogr.setText(str(self.Mean(interp(self.start_data[0], self.start_data[0], self.start_data[1]))))

    def Lagrange(self):
        cur_axes = self.ShowApproximation()
        # получение аппроксимирующей функции
        f = interpolate.lagrange(self.start_data[0], self.start_data[1])
        # построение функции по найденным коэффициентам
        cur_axes.axes.plot(self.start_data[0],f(self.start_data[0]), color = "green")
        cur_axes.draw()
        self.NewTableInit(self.start_data[0], f(self.start_data[0]))

        self.lbl_pogr.setText(str(self.Mean(f(self.start_data[0]))))
        

    def Spline(self):
        cur_axes = self.ShowApproximation()
        # получение аппроксимирующей функции
        f = interpolate.interp1d(self.start_data[0], self.start_data[1], "cubic")
        # построение функции по найденным коэффициентам
        cur_axes.axes.plot(self.start_data[0],f(self.start_data[0]), color = "green")
        cur_axes.draw()
        self.NewTableInit(self.start_data[0], f(self.start_data[0]))

        self.lbl_pogr.setText(str(self.Mean(f(self.start_data[0]))))


    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())