import numpy as np
import sympy as smp
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter
import time

startTime = time.time()
t, g = smp.symbols('t g')
m1, m2 = smp.symbols('m1 m2')
L1, L2 = smp.symbols('L1, L2')

#Since theta1 and theta2 are strictly functions of time, here they are defined symbolically as 
#such
theta1, theta2 = smp.symbols(r'\theta1, \theta2', cls=smp.Function)
theta1 = theta1(t)
theta2 = theta2(t)

#This defines the first and second derivatives of theta1 and theta2
theta1_d = smp.diff(theta1, t)
theta2_d = smp.diff(theta2, t)
theta1_2d = smp.diff(theta1_d, t)
theta2_2d = smp.diff(theta2_d, t)

#Cartesian coordinates of m1 and m2
x1 = L1 * smp.sin(theta1)
y1 = -L1 * smp.cos(theta1)
x2 = x1 + (L2 * smp.sin(theta2))
y2 = y1 + (-L2 * smp.cos(theta2))

#Kinetic energy
T1 = 1/2 * m1 * (smp.diff(x1, t)**2 + smp.diff(y1, t)**2)
T2 = 1/2 * m2 * (smp.diff(x2, t)**2 + smp.diff(y2, t)**2)
T = T1 + T2

#Potential Energy
V1 = m1 * g * y1
V2 = m2 * g * y2
V = V1 + V2

#LaGrangian
L = T - V

#Define LaGrange's Equations
LE1 = smp.diff(L, theta1) - smp.diff(smp.diff(L, theta1_d), t).simplify()
LE2 = smp.diff(L, theta2) - smp.diff(smp.diff(L, theta2_d), t).simplify()

solutions = smp.solve([LE1, LE2], (theta1_2d, theta2_2d), simplify=False, rational=False)

#Converts the symbolic functions into numerical functions that can be solved to return numeric answers 
dz1dt_f = smp.lambdify((t,g,m1,m2,L1,L2,theta1,theta2,theta1_d,theta2_d), solutions[theta1_2d])
dz2dt_f = smp.lambdify((t,g,m1,m2,L1,L2,theta1,theta2,theta1_d,theta2_d), solutions[theta2_2d])
dtheta1dt_f = smp.lambdify(theta1_d, theta1_d)
dtheta2dt_f = smp.lambdify(theta2_d, theta2_d)

def dSdt(S, t, g, m1, m2, L1, L2):
    theta1, z1, theta2, z2 = S
    return [dtheta1dt_f(z1),
            dz1dt_f(t, g, m1, m2, L1, L2, theta1, theta2, z1, z2),
            dtheta2dt_f(z2), 
            dz2dt_f(t, g, m1, m2, L1, L2, theta1, theta2, z1, z2)]

t = np.linspace(0, 40, 1001)
g = 9.81
m1 = 2
m2 = 1
L1 = 2
L2 = 1

#IMPORTANT Regarding y0: y0 represents the intitial conditions. Here, the terms in the order
#called in ans are: [theta1, d(theta1)/d(t)=angular velocity of theta1, theta2, d(theta2)/d(t)]
#Also of note: all of these units are in radians/ radians/sec.
#Finally, args is necessary here because these arguments need to be passed to the solver. Obviously. 
ans = odeint(dSdt, y0=[1, -3, -1, 5], t=t, args=(g, m1, m2, L1, L2))
endTime = time.time()
theta1 = ans.T[0]
z1 = ans.T[1]
theta2 = ans.T[2]
z2 = ans.T[3]
plot = plt.plot(t, theta2)
plt.show()
executionTime = endTime - startTime
print("execution time: ", executionTime)