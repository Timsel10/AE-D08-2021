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
    dydt = [x_prime, -c * x_prime - k * x + x_forced * k + v_forced * c]
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
        self.simMotion = simMotionArray[:400]
        self.headMotionRaw = headMotionArray[:100]
        self.results = []
        self.guesses = guesses
        # simMotion.transform()
        print("Started transforming: Motion condition: "+ str(self.MC) + "; Person: " + str(self.Person))
         
        self.headMotion = self.transform()

        print("Done transforming:  Motion condition: "+ str(self.MC) + "; Person: " + str(self.Person))

    def transform(self):
        simMotion = self.simMotion[:,:7]
        headMotion = self.headMotionRaw
        max_simTime = simMotion[-1,0]
        i = len(headMotion) - 1
        while headMotion[i,0] > max_simTime:
            i -= 1

        headMotion = headMotion[:i+1]


        simInterpFunction = interp1d(simMotion[:,0], simMotion[:,1:7], axis = 0, kind = "nearest")
        simInterp = simInterpFunction(headMotion[:,0])

        headMotion[:,3:6] = headMotion[:,3:6] * (np.pi / 16383)
        headMotion[:,6:9] = headMotion[:,6:9] * (0.50 / 16383)

        np.savetxt("real_data/MC" + str(self.MC) + "HM" +  str(self.Person).zfill(2) + ".csv", headMotion, delimiter = ",")

        headPosHRF = np.empty((len(headMotion), 3))
        
        headPosHRF[:,0] = headMotion[:,0]
        headPosHRF[:,1] = -headMotion[:,1] - 0.55
        headPosHRF[:,2] = -headMotion[:,2] - 1.2075

        x_angle = simInterp[:,3]
        y_angle = simInterp[:,4]
        z_angle = simInterp[:,5]

        ##- row 1 of transformation matrix
        m_11 = np.cos(y_angle)*np.cos(z_angle)
        m_12 = np.cos(y_angle)*np.sin(z_angle)
        m_13 = -np.sin(y_angle)

        ##- row 2 of transformation matrix
        m_21 =  np.sin(x_angle)*np.sin(y_angle)*np.cos(z_angle)-np.cos(x_angle)*np.sin(z_angle)
        m_22 =  np.sin(x_angle)*np.sin(y_angle)*np.sin(z_angle) + np.cos(x_angle)*np.cos(z_angle)
        m_23 =  np.sin(x_angle)*np.cos(y_angle)

        ##- row 3 of transformation matrix
        m_31 =  np.cos(x_angle)*np.sin(y_angle)*np.cos(z_angle) + np.sin(x_angle)*np.sin(z_angle)
        m_32 =  np.cos(x_angle)*np.sin(y_angle)*np.sin(z_angle) - np.sin(x_angle)*np.cos(z_angle)
        m_33 =  np.cos(x_angle)*np.cos(y_angle)

        trans_matrix = np.swapaxes(np.array([[m_11,m_12,m_13],[m_21,m_22,m_23],[m_31,m_32,m_33]]), 0, 2)

        headPosSI = np.squeeze(np.matmul(trans_matrix, np.expand_dims(headPosHRF, headPosHRF.ndim))) + simInterp[:,0:3]
        
        return headPosSI

    def solve(self):
        for i in range(2):
            # initializes DOF, solves it and then appends to results
            print("solving: dimension", i)
            self.results.append(singleDOFsystem(self.simMotion[:,[0, i + 1, 2 * i + 1]], self.headMotionRaw[:,[0, i + 3]], self.guesses[i]).solve())
        print(self.results)


class singleDOFsystem:
    

    def __init__(self, simMotion, headMotion, guess):
        self.simMotion = simMotion
        self.initialConditions = headMotion[0,:].tolist()
        self.headMotion = headMotion
        self.forcing_functions = interp1d(simMotion[:,0], simMotion[:,[1,2]].T)
        self.startT = simMotion[0,0]
        self.endT = simMotion[-1,0]
        self.guess = guess
        print("initialized")
        # it might be interesting to do a cubic interpolation as well later
        # forcing_functions(t) will return a numpy array with the sim's forced position and velocity at time t
    def solveODE(self, k_and_c):
        print(k_and_c)
        yeet = solve_ivp(forced_mass_spring_damper, (self.startT, self.endT), self.initialConditions, t_eval = self.simMotion[:,0], args = (k_and_c, self.forcing_functions), vectorized = True)
        if not yeet.y.shape == (2, 400):
            u = 1
        return yeet
    
    def residuals(self, k_and_c):
        nonInterpSol = self.solveODE(k_and_c).y
        print(nonInterpSol.shape)
        solution = interp1d(self.simMotion[:,0], nonInterpSol[0], 'nearest')
        return solution(self.headMotion[:,0]) - self.headMotion[:,1]

    def solve(self):
        return least_squares(self.residuals, self.guess, verbose = 2)