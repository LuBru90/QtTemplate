from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
import sys
import time
import numpy as np
import os
import threading
from ui_class import Ui_MainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.updatetime = 10 # ms
        self.sampleCount = 500
        self.dt = 0

        self.values = [0]
        self.show_fft()
        self.update()

    def show_fft(self):
        try:
            fft_y = np.abs(np.fft.fft(self.values - np.array(self.values).mean())) * self.updatetime/1000
            fft_x = np.fft.fftfreq(len(self.values), self.updatetime/1000) 
            self.ui.graphicsView2.clear()
            self.ui.graphicsView2.plot(fft_x[:fft_x.size//2], fft_y[:fft_y.size//2])

        except Exception as e:
            print(e)

        finally:
            QTimer.singleShot(self.updatetime, self.show_fft)

    def update(self):
        try:
            # generate data
            f = 1
            w = 2*np.pi*f

            y = np.sin(w*time.time())
            y += 1/3*np.sin(w*time.time()*3)
            y += 1/5*np.sin(w*time.time()*5)
            y += 1/7*np.sin(w*time.time()*7)
            y += np.random.random()/2

            if len(self.values) != self.sampleCount:
                self.values.append(y)
            else:
                for i in range(len(self.values) - 1):
                    self.values[i] = self.values[i + 1]
                self.values[-1] = y

            self.ui.graphicsView.clear()
            self.ui.graphicsView.plot(self.values)

        finally:
            QTimer.singleShot(self.updatetime, self.update)

    def slot_test(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    myapp = MyWindow()
    myapp.show()
    app.exec_()

if __name__ == "__main__":
    main()
