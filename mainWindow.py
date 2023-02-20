from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QLabel,
    QGridLayout, QGroupBox, QDialog, QWidget, QDial, QSlider, QLineEdit, QPushButton, 
    QHBoxLayout, QTabWidget, QComboBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys
from scipy.integrate import odeint, solve_ivp
import scipy as sp
import matplotlib.pyplot as plt

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        tab1MainLayout = QGridLayout()
        label = QLabel("hello")
        tab1MainLayout.addWidget(label)
        self.setLayout(tab1MainLayout)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())