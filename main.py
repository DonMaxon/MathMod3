import sys
sys.path.append('C:\\Users\Max\AppData\Local\Programs\Python\Python310\Lib\site-packages')

import numpy as np
import pandas as pd

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from pyqtgraph import PlotWidget

def get_values():
    modelling_time = int(form.lineEdit.text())
    num_of_lines = int(form.lineEdit_2.text())
    time_coeff = float(form.lineEdit_3.text())
    max_num_of_lines = int(form.lineEdit_4.text())
    duration_time = float(form.lineEdit_5.text())
    capacity = int(form.lineEdit_6.text())
    print(modelling_time)
    print(num_of_lines)
    print(time_coeff)
    print(max_num_of_lines)
    print(duration_time)
    print(capacity)
    return modelling_time, num_of_lines, time_coeff, max_num_of_lines, duration_time, capacity


def solve():
    modelling_time, num_of_lines, time_coeff, max_num_of_lines, duration_time, capacity = get_values()


Form, Window = uic.loadUiType('interface.ui')
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(solve)
window.show()
app.exec_()
