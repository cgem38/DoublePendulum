import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import animation
from PyQt5 import QtCore, QtWidgets
import sys
from numpy import cos, sin
from doublePendulumSolver import Solver


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


# class AnimationWidget(QtWidgets):

#     def __init__(self, *args, **kwargs):
#         super(AnimationWidget, self).__init__(*args, **kwargs)

#         # Create the maptlotlib FigureCanvas object,
#         # which defines a single set of axes as self.axes.
#         sc = MplCanvas(self, width=5, height=4, dpi=100)
#         sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
#         self.setCentralWidget(sc)

def animatePendulum(solverOutput, L1, L2):
    theta1 = solverOutput.T[0]
    theta2 = solverOutput.T[2]

    def getx1y1x2y2(theta1, theta2, L1, L2):
        return (L1 * sin(theta1), 
                -L1 * cos(theta1),
                L1 * sin(theta1) + L2 * sin(theta2),
                -L1 * cos(theta1) - L2 * cos(theta2))

    solx1, soly1, solx2, soly2 = getx1y1x2y2(theta1, theta2, L1, L2)

    # testData = [x**2 for x in range(10)]
    # testFigure = plt.figure()
    # canvas = FigureCanvasQTAgg(testFigure)
    # testAxis = testFigure.add_subplot(111)
    # testAxis.plot(testData)
    # canvas.draw()

    
    def animate(i):
        ln1.set_data([0, solx1[i], solx2[i]], [0, soly1[i], soly2[i]])
        

    fig, ax = plt.subplots(1,1, figsize = (8,8))
    # canvas = FigureCanvasQTAgg(fig)
    ax.set_facecolor('k')
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ln1, = plt.plot([], [], 'ro--', lw=3, markersize=8)
    ax.set_ylim(-4,4)
    ax.set_xlim(-4,4)
    ani = animation.FuncAnimation(fig, animate, frames=1000, interval=10)
    # plt.show()
    ani.save('animation.gif', writer='pillow', fps=25)
    

    # return canvas

if __name__ == '__main__':
    output = Solver(9.81, 50, 1, 1, 1, 1, 3, 2)
    w = animatePendulum(output, 1, 1)
    print('done')