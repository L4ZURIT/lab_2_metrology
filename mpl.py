import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import  QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure()
        self.axes = fig.add_subplot()
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.scatter([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()





def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
    pass
if __name__ == '__main__':
    main()



