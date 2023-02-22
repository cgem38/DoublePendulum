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
import time
import sympy as smp

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.positionGraph = self.createPositionGraph()
        variableComboBox = self.createVariableComboBox()


        runButton = QPushButton("Run")
        runButton.pressed.connect(self.runButtonPressed)
        #BEGINNING OF CODE TO TEST GRAPHING FUNCTION -- DELETE WHEN ODE SOLVER IS COMPLETED
        self.x = np.linspace(0, 10, 1000)
        self.y = self.x**2
        #END OF CODE TO TEST GRAPHING FUNCTION

        tab1MainLayout = QGridLayout()
        tab1MainLayout.addWidget(self.positionGraph, 0, 0, 1, 6)
        tab1MainLayout.addWidget(variableComboBox, 1, 0, 1, 6)
        tab1MainLayout.addWidget(runButton, 2, 2, 1, 2)
        tab1MainLayout.setRowStretch(0, 5)
        tab1MainLayout.setRowStretch(1, 1)
        tab1MainLayout.setRowStretch(2, 1)
        self.setLayout(tab1MainLayout)

        
    
    def runButtonPressed(self):
        self.graphPositions()
    
    def graphPositions(self):
        # startTime = time.time()
        # timeInterval = 1/60
        # for i in range(int(len(self.x)/2)):
        #     currentSpot = 2 * i
        #     xPoints = [self.x[currentSpot], self.x[currentSpot + 1]]
        #     yPoints = [self.y[currentSpot], self.y[currentSpot + 1]]
        #     self.positionGraph.plot(xPoints, yPoints)
        #     time.sleep(timeInterval) 
        pass



    def createPositionGraph(self):
        graph = pg.plot()
        graph.showGrid(x=True, y=True)
        graph.setLabel('left', 'Vertical Position')
        graph.setLabel('bottom', 'Horizontal Position')

        return graph
    
    def createVariableComboBox(self):
        Box = QGroupBox(title="Variables")

        rod1LengthLabel = QLabel("Rod 1 Length")
        rod1LengthSlider = Slider(0.01, 5.0, "horizontal")
        rod1LengthInput = QLineEdit()

        rod2LengthLabel = QLabel("Rod 2 Length")
        rod2LengthSlider = Slider(0.01, 5.0, "horizontal")
        rod2LengthInput = QLineEdit()

        mass1LengthLabel = QLabel("Mass 1 Length")
        mass1LengthSlider = Slider(0.01, 2.0, "horizontal")
        mass1LengthInput = QLineEdit()

        mass2LengthLabel = QLabel("Mass 2 Length")
        mass2LengthSlider = Slider(0.01, 2.0, "horizontal")
        mass2LengthInput = QLineEdit()

        layout = QGridLayout()
        layout.addWidget(rod1LengthLabel, 0, 0)
        layout.addWidget(rod1LengthSlider, 0, 1)
        layout.addWidget(rod1LengthInput, 0, 2)

        layout.addWidget(rod2LengthLabel, 1, 0)
        layout.addWidget(rod2LengthSlider, 1, 1)
        layout.addWidget(rod2LengthInput, 1, 2)

        layout.addWidget(mass1LengthLabel, 0, 3)
        layout.addWidget(mass1LengthSlider, 0, 4)
        layout.addWidget(mass1LengthInput, 0, 5)

        layout.addWidget(mass2LengthLabel, 1, 3)
        layout.addWidget(mass2LengthSlider, 1, 4)
        layout.addWidget(mass2LengthInput, 1, 5)

        Box.setLayout(layout)

        return Box
    

    

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())