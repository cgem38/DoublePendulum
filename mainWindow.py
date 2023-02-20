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
from slider import Slider

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        positionGraph = self.createPositionGraph()
        variableComboBox = self.createVariableComboBox()
        label = QLabel("hello")

        tab1MainLayout = QGridLayout()
        tab1MainLayout.addWidget(positionGraph, 0, 0, 1, 6)
        tab1MainLayout.addWidget(label, 1, 0)
        tab1MainLayout.addWidget(variableComboBox, 1, 1, 1, 3)
        self.setLayout(tab1MainLayout)

    def createPositionGraph(self):
        graph = pg.plot()
        graph.showGrid(x=True, y=True)
        graph.setLabel('left', 'Vertical Position')
        graph.setLabel('bottom', 'Horizontal Position')

        return graph
    
    def createVariableComboBox(self):
        testSlider = Slider(0.0, 5.0, "horizontal")
        return testSlider


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())