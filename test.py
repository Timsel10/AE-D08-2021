# Main goal: give k, c and m from data points
# 6 dimensions. x, y, z and in roll
# data input is X, Y, Z + roll, pitch, yaw of head
# The base forced vibration is also given

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from scipy.optimize import least_squares

# c is infact c/m
# k is infact k/m

# constants
c = 0.5
k = 1.5
f0 = 1.0
w_dr = (1.5 - 0.1) ** 0.5

# average head weight: m_head = 5 [kg]
# average Dutch man weight, m_man_D = 85 [kg]

# initial conditions
y0 = [1.0, 0.0]

# time 
t = np.linspace(0, 20, 201)

def mass_spring_damper(y, t, c, k): # , x_forced):
    x, x_prime = y
    x_forced = np.exp(-((t - 1) ** 2))
    v_forced = -2 * (t - 1) * np.exp(-((t - 1) ** 2))
    dydt = [x_prime, -c * x_prime - k * x + x_forced * k + v_forced * c]
    return dydt

# actual solution
sol = odeint(mass_spring_damper, y0, t, args=(c, k))
randomized_x = np.copy(sol[:, 0])

for i in range(len(randomized_x)):
    randomized_x[i] += randomized_x[i] * uniform(-0.1, 0.1) + uniform(-0.05, 0.05)

initial_guess = np.array([c - 0.2, k + 0.1, 0.9, 0.1])

# only necessary input is data and an initial guess
def residuals(guess, t, data):
    return odeint(mass_spring_damper, [guess[2], guess[3]], t, args=(guess[0], guess[1]))[:,0] - data

results = least_squares(residuals, initial_guess, args=(t, randomized_x))

guess = results.x

resulting_x = odeint(mass_spring_damper, [guess[2], guess[3]], t, args=(guess[0], guess[1]))[:,0]

# plotting
plt.plot(t, sol[:, 0], 'b', label='x(t) original')
plt.plot(t, resulting_x, 'g', label='x(t) estimation')
plt.scatter(t, randomized_x, 4, c="r", label='"data"')
# plt.plot(t, sol[:, 1], 'g', label='x_prime(t) original')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()

print("c = " + str(guess[0]))
print("k = " + str(guess[1]))
print("xi = " + str(guess[2]))
print("xi' = " + str(guess[3]))
