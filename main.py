import sys
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from model import SMO
from PyQt5 import QtCore

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
    global form
    modelling_time, num_of_lines, time_coeff, max_num_of_lines, duration_time, capacity = get_values()
    system = SMO(mod_time=modelling_time, start_lines=num_of_lines, max_lines=max_num_of_lines, time_coeff=time_coeff,
                 dur_coeff=duration_time, cap=capacity)
    print('SMO_created')
    res = np.zeros((max_num_of_lines, modelling_time + 1), dtype=int)
    queue = np.zeros(modelling_time + 1, dtype=int)
    for i in range(modelling_time):
        lines, q, tasks_num, accepted, rejected = system.step()
        for k in range(max_num_of_lines):
            res[k, i] = form_val(lines[k])
        queue[i] = q.len
    lines, q, tasks_num, accepted, rejected = system.step()
    for k in range(max_num_of_lines):
        res[k, -1] = form_val(lines[k])
    queue[-1] = q.len
    form.lineEdit_7.setText(str(tasks_num))
    form.lineEdit_8.setText(str(accepted))
    form.lineEdit_9.setText(str(rejected))
    form.lineEdit_10.setText("{:.6f}".format(accepted/tasks_num) if tasks_num != 0 else 0)
    form.lineEdit_11.setText("{:.6f}".format(rejected/tasks_num) if tasks_num != 0 else 0)
    plot_scatter(res, queue)


def form_val(line):
    if not line.status:
        return -1
    if line.free:
        return 0
    return 1


def plot_scatter(lines, queue):
    t = np.array(range(queue.shape[0]))
    total = np.zeros(queue.shape[0], dtype=int)
    for i in range(total.shape[0]):
        total[i] = lines[lines[:, i] == 1, i].shape[0]
    fig1, axs1 = plt.subplots(nrows=1, ncols=2)
    axs1[0].scatter(t, total, s=5)
    axs1[0].grid()
    axs1[0].set_title('Число занятых линий')
    axs1[1].scatter(t, queue, s=5)
    axs1[1].grid()
    axs1[1].set_title('Загруженность очереди')
    fig2, axs2 = plt.subplots(nrows=lines.shape[0], ncols=1)
    for i in range(lines.shape[0]):
        axs2[i].grid()
        axs2[i].set_title(f'Линия {i}')
        for j in range(lines.shape[1]):
            if lines[i, j] == -1:
                axs2[i].scatter(t[j], np.zeros(1), c='r', s=5)
            else:
                axs2[i].scatter(t[j], lines[i, j], c='g', s=5)
    fig1.show()
    fig2.show()


Form, Window = uic.loadUiType('interface.ui')
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(solve)
window.show()
app.exec_()
