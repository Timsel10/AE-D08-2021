import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
from scipy.interpolate import interp1d

def forced_mass_spring_damper(y, t, c, k, x_forced, v_forced):
    x, x_prime = y
    #x_forced = np.exp(-((t - 1) ** 2))
    #v_forced = -2 * (t - 1) * np.exp(-((t - 1) ** 2))
    #dydt = [x_prime, -c * x_prime - k * x + x_forced * k + v_forced * c]
    raise NotImplementedError
    return dydt


class headMotion:
    def __init__(self, simMotionFile, headMotionFile):
        simulatorMotion = np.genfromtxt(simMotionFile, skip_header = 1)
        headMotion = np.genfromtxt(headMotionFile, skip_header = 1)


class singleDOFsystem:
    def __init__(self, simMotion, headMotion):
        #initialConditions = 
        raise NotImplementedError    

    def interpolate(self):
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )
        raise NotImplementedError
        return interp1d(...)

    def solveODE(self):
        raise NotImplementedError
        return solve_ivp(forced_mass_spring_damper, self.initialConditions, )


