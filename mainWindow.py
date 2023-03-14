from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QLabel,
    QGridLayout, QGroupBox, QDialog, QWidget, QDial, QSlider, QLineEdit, QPushButton, 
    QHBoxLayout, QTabWidget, QComboBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QMovie
import pyqtgraph as pg
import numpy as np
import sys
from scipy.integrate import odeint, solve_ivp
import scipy as sp
import matplotlib.pyplot as plt
from slider import Slider
from doublePendulumSolver import Solver
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib import animation 
from animationWidget import animatePendulum

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.GraphBox = self.createGraphBox()
        variableComboBox = self.createVariableGroupBox()
        initialConditionsComboBox = self.createInitialConditionsGroupBox()

        runButton = QPushButton("Run")
        runButton.pressed.connect(self.runButtonPressed)
        
        #Temporary Variables to test ODE solver and grpahing functions, since the UI does not have input for gravity and time yet. Delete when it does. 
        self.g = 9.81
        self.t = 40
        #END OF CODE TO TEST GRAPHING FUNCTION

        tab1MainLayout = QGridLayout()
        tab1MainLayout.addWidget(self.GraphBox, 0, 0, 1, 6)
        tab1MainLayout.addWidget(variableComboBox, 1, 0, 1, 6)
        tab1MainLayout.addWidget(initialConditionsComboBox, 2, 0, 1, 6)
        tab1MainLayout.addWidget(runButton, 3, 2, 1, 2)
        tab1MainLayout.setRowStretch(0, 5)
        tab1MainLayout.setRowStretch(1, 1)
        tab1MainLayout.setRowStretch(2, 1)
        tab1MainLayout.setRowStretch(3, 1)
        self.setLayout(tab1MainLayout)
    
    def runButtonPressed(self):
        self.inputValuesChanged()
        g = self.g
        t = self.t
        m1 = float(self.mass1Input.text())
        m2 = float(self.mass2Input.text())
        L1 = float(self.rod1LengthInput.text())
        L2 = float(self.rod2LengthInput.text())
        theta10 = float(self.theta1InitialInput.text())
        theta20 = float(self.theta2InitialInput.text()) 

        output = Solver(g, t, m1, m2, L1, L2, theta10, theta20)
        self.graphPositions(output)
        animatePendulum(output, L1, L2)
        animationOutput = QMovie("animation.gif")
        self.animationLabel.setMovie(animationOutput)
        animationOutput.start()

        return output
    
    
    def graphPositions(self, solverOutput):
        Theta1 = solverOutput.T[0]
        Z1 = solverOutput.T[1]
        Theta2 = solverOutput.T[2]
        Z2 = solverOutput.T[3]
        t = np.linspace(0, self.t, 1001)
        m1 = float(self.mass1Input.text())
        m2 = float(self.mass2Input.text())
        L1 = float(self.rod1LengthInput.text())
        L2 = float(self.rod2LengthInput.text())

        x1 = L1 * np.sin(Theta1)
        y1 = -L1 * np.cos(Theta1)
        x2 = x1 + L2 * np.sin(Theta2)
        y2 = y1 + (-L2 * np.cos(Theta2))

        self.XYLine1.setData(x1, y1)
        self.XYLine2.setData(x2, y2)

        pass

    def createGraphBox(self, output=[]):
        tabWidget = QTabWidget()
        graphTab = QWidget()
        self.animationTab = QWidget()
        
        #Create Graph Tab
        graphLayout = QGridLayout()
        x = []
        y = []
        XYgraph = pg.plot()
        XYgraph.showGrid(x=True, y=True)
        XYgraph.setLabel('left', 'Vertical Position')
        XYgraph.setLabel('bottom', 'Horizontal Position')
        XYgraph.addLegend(offset=(-1, 1))
        self.XYLine1 = XYgraph.plot(x, y, pen='r', name="Mass 1")
        self.XYLine2 = XYgraph.plot(x, y, pen='b', name="Mass 2")
        graphLayout.addWidget(XYgraph)
        graphTab.setLayout(graphLayout)
        tabWidget.addTab(graphTab, "Graph")

        #Create Animation Tab
        self.animationLabel = QLabel()
        self.animationLayout = QGridLayout()
        self.animationLayout.addWidget(self.animationLabel)
        self.animationTab.setLayout(self.animationLayout)
        tabWidget.addTab(self.animationTab, "Animation")

        return tabWidget
    
    def createVariableGroupBox(self):
        Box = QGroupBox(title="Variables")

        rod1LengthLabel = QLabel("Rod 1 Length")
        self.rod1LengthSlider = Slider(0.01, 5.0, "horizontal")
        self.rod1LengthInput = QLineEdit()
        self.rod1LengthInput.setText("1")
        self.rod1LengthSlider.setValue(int(100 * float(self.rod1LengthInput.text())))
        self.rod1LengthSlider.valueChanged.connect(self.sliderValuesChanged)

        rod2LengthLabel = QLabel("Rod 2 Length")
        self.rod2LengthSlider = Slider(0.01, 5.0, "horizontal")
        self.rod2LengthInput = QLineEdit()
        self.rod2LengthInput.setText("1")
        self.rod2LengthSlider.setValue(int(100 * float(self.rod2LengthInput.text())))
        self.rod2LengthSlider.valueChanged.connect(self.sliderValuesChanged)

        mass1Label = QLabel("Mass 1")
        self.mass1Slider = Slider(0.01, 2.0, "horizontal")
        self.mass1Input = QLineEdit()
        self.mass1Input.setText("1")
        self.mass1Slider.setValue(int(100 * float(self.mass1Input.text())))
        self.mass1Slider.valueChanged.connect(self.sliderValuesChanged)

        mass2Label = QLabel("Mass 2")
        self.mass2Slider = Slider(0.01, 2.0, "horizontal")
        self.mass2Input = QLineEdit()
        self.mass2Input.setText("1")
        self.mass2Slider.setValue(int(100 * float(self.mass2Input.text())))
        self.mass2Slider.valueChanged.connect(self.sliderValuesChanged)

        layout = QGridLayout()
        layout.addWidget(rod1LengthLabel, 0, 0)
        layout.addWidget(self.rod1LengthSlider, 0, 1)
        layout.addWidget(self.rod1LengthInput, 0, 2)

        layout.addWidget(rod2LengthLabel, 1, 0)
        layout.addWidget(self.rod2LengthSlider, 1, 1)
        layout.addWidget(self.rod2LengthInput, 1, 2)

        layout.addWidget(mass1Label, 0, 3)
        layout.addWidget(self.mass1Slider, 0, 4)
        layout.addWidget(self.mass1Input, 0, 5)

        layout.addWidget(mass2Label, 1, 3)
        layout.addWidget(self.mass2Slider, 1, 4)
        layout.addWidget(self.mass2Input, 1, 5)

        Box.setLayout(layout)
        
        return Box
    
    def createInitialConditionsGroupBox(self):
        Box = QGroupBox(title="Initial Conditions")        

        theta1InitialLabel = QLabel("Initial Theta 1 (radians)")
        self.theta1InitialSlider = Slider(0.0, 2*np.pi, "horizontal")
        self.theta1InitialInput = QLineEdit()
        self.theta1InitialInput.setText("0")
        self.theta1InitialSlider.setValue(int(100 * float(self.theta1InitialInput.text())))
        self.theta1InitialSlider.valueChanged.connect(self.sliderValuesChanged)

        theta2InitialLabel = QLabel("Initial Theta 2 (radians)")
        self.theta2InitialSlider = Slider(0.0, 2*np.pi, "horizontal")
        self.theta2InitialInput = QLineEdit()
        self.theta2InitialInput.setText("0")
        self.theta2InitialSlider.setValue(int(100 * float(self.theta2InitialInput.text())))
        self.theta2InitialSlider.valueChanged.connect(self.sliderValuesChanged)

        layout = QHBoxLayout()
        layout.addWidget(theta1InitialLabel, 4)
        layout.addWidget(self.theta1InitialSlider, 4)
        layout.addWidget(self.theta1InitialInput, 1)
        layout.addStretch(2)
        layout.addWidget(theta2InitialLabel, 4)
        layout.addWidget(self.theta2InitialSlider, 4)
        layout.addWidget(self.theta2InitialInput, 1)
        Box.setLayout(layout)

        return Box
    
    def sliderValuesChanged(self):
        #System Variable values:
        self.rod1LengthInput.setText(str(self.rod1LengthSlider.value() / 100))
        self.rod2LengthInput.setText(str(self.rod2LengthSlider.value() / 100))
        self.mass1Input.setText(str(self.mass1Slider.value() / 100))
        self.mass2Input.setText(str(self.mass2Slider.value() / 100))

        #Initial Condition values:
        self.theta1InitialInput.setText(str(self.theta1InitialSlider.value() / 100))
        self.theta2InitialInput.setText(str(self.theta2InitialSlider.value() / 100))


    def inputValuesChanged(self):
        #System Variable values:
        self.rod1LengthSlider.setValue(int(100 * float(self.rod1LengthInput.text())))
        self.rod2LengthSlider.setValue(int(100 * float(self.rod2LengthInput.text())))
        self.mass1Slider.setValue(int(100 * float(self.mass1Input.text())))
        self.mass2Slider.setValue(int(100 * float(self.mass2Input.text())))

        #Initial Condition values:
        self.theta1InitialSlider.setValue(int(100 * float(self.theta1InitialInput.text())))
        self.theta2InitialSlider.setValue(int(100 * float(self.theta2InitialInput.text())))

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())