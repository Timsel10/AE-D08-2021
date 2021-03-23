import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
from scipy.interpolate import interp1d

def forced_mass_spring_damper(t, y, k_and_c, forcing_functions):
    """
    Inputs:
    t is a float for time
    y is a list [x, x']
    c is a float which is infact c/m
    k is a float which is infact k/m
    x_forced is an interp1d function which returns a x_forced value for a given t within the domain
    v_forced is an interp1d function which returns a v_forced value for a given t within the domain

    Output:
    dydt is a list [x'', x']

    Description:
    This is the function required by the solve
    """
    # commented below is some old code which can be deleted in the final version
    #x_forced = np.exp(-((t - 1) ** 2))
    #v_forced = -2 * (t - 1) * np.exp(-((t - 1) ** 2))
    k, c = k_and_c
    x_forced, v_forced = forcing_functions(t)
    x, x_prime = y
    dydt = [x_prime, -c * x_prime - k * x + x_forced(t) * k + v_forced(t) * c]
    return dydt

class headMotionSystem:

    def __init__(self, simMotionArray, headMotionArray, ident_numbers, guesses):
        """
        Inputs:
        simMotionArray is a numpy array
        headMotionArray is a numpy array containing the head motion data
        ident_numbers is a tuple or list containing [0] is the person [1] is the condition
        guesses is a list containing the guesses [k, c] for each DOF
        """
        self.MC = ident_numbers[1]
        self.Person = ident_numbers[0]
        self.simMotion = simMotionArray
        self.headMotion = headMotionArray
        self.results = []
        self.guesses = guesses
        # simMotion.transform()
        self.headMotion.transform()

    def transform(self):
        # to be copied from transform.py or imported and run from there
        # this needs to take the coordinates in the head reference frame and put them in the inertial frame
        raise NotImplementedError

    def solve(self):
        for i in range(6):
            # initializes DOF, solves it and then appends to results
            self.results.append(singleDOFsystem(self.simMotion[:,[0, i + 1, 2 * i + 1]], self.headMotion[:,[0, i + 3]], self.guesses[i]).solve())



class singleDOFsystem:
    def __init__(self, simMotion, headMotion, guess):
        self.simMotion = simMotion
        self.initialConditions = headMotion[0,:].tolist()
        self.headMotion = headMotion
        self.forcing_functions = interp1d(simMotion[:,0], simMotion[:,[1,2]].T)
        self.startT = simMotion[0,0]
        self.endT = simMotion[-1,0]
        self.guess = guess
        # it might be interesting to do a cubic interpolation as well later
        # forcing_functions(t) will return a numpy array with the sim's forced position and velocity at time t


    def solveODE(self, k_and_c):
        return solve_ivp(forced_mass_spring_damper, (self.startT, self.endT), self.initialConditions, t_eval = self.simMotion[:,0], args = (k_and_c, self.forcing_functions))
    
    def residuals(self, k_and_c):
        solution = interp1d(self.simMotion[:,0], self.solveODE(k_and_c)[0], 'nearest')
        return solution(self.headMotion[:,0]) - self.headMotion[:,1]

    def solve(self):
        return least_squares(self.residuals, self.guess)