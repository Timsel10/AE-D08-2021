import numpy as np
from scipy.integrate import odeint
from scipy.optimize import least_squares

def forced_mass_spring_damper(y, t, c, k, x_forced, v_forced):
    x, x_prime = y
    #x_forced = np.exp(-((t - 1) ** 2))
    #v_forced = -2 * (t - 1) * np.exp(-((t - 1) ** 2))
    #dydt = [x_prime, -c * x_prime - k * x + x_forced * k + v_forced * c]
    raise NotImplementedError
    return dydt


class headMotion:
    def __init__(self, simMotionFile, headMotionFile):
        simulatorMotion = np.genfromtxt(simMotionFile)
        headMotion = np.genfromtxt(headMotionFile)


class singleDOFsystem:
    def __init__(self, simMotion, headMotion):
        #initialConditions = 

    def solveODE():
        raise NotImplementedError
        return odeint(forced_mass_spring_damper, self.initialConditions, )


