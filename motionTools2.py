# -*- coding: utf-8 -*-
import numpy as np
from scipy.misc import derivative
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

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
    dydt is a list [x', x'']

    Description:
    This is the function required by the solve
    """
    # commented below is some old code which can be deleted in the final version
    #x_forced = np.exp(-((t - 1) ** 2))
    #v_forced = -2 * (t - 1) * np.exp(-((t - 1) ** 2))

    k, c, xn = k_and_c
    x_forced, v_forced = forcing_functions(t)
    x, x_prime = y
    dydt = [x_prime, -c * (x_prime - v_forced) - k * ((x - xn) - x_forced)]
    return dydt

class headMotionSystem:

    def __init__(self, simMotionArray, headMotionArray, ident_numbers):
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
        self.headMotionRaw = np.copy(headMotionArray)
        self.results = []
        print("Started transforming: Motion condition: "+ str(self.MC) + "; Person: " + str(self.Person))
        
        # self.headMotion = self.headMotionRaw
        
        # self.headMotion[:,6:9] = headMotionArray[:,3:6] * (np.pi / 16383)
        # self.headMotion[:,3:6] = headMotionArray[:,6:9] * (0.50 / 16383)
        
        # plt.scatter(self.headMotion[:,0], self.headMotion[:,3], 5, marker = "x")
        # plt.scatter(self.headMotion[:,0], headMotionArray[:,6], 5, marker = "x")
        # plt.show()
        
        self.headMotion = self.transform()
        

        print("Done transforming: Motion condition: "+ str(self.MC) + "; Person: " + str(self.Person))

    def transform(self):
        simMotion = np.copy(self.simMotion[:,:7])
        headMotion = np.copy(self.headMotionRaw)
        max_simTime = simMotion[-1,0]
        i = len(headMotion) - 1
        while headMotion[i,0] > max_simTime:
            i -= 1

        headMotion = headMotion[:i+1]
        
        headMotion[:,6:9] = np.copy(headMotion[:,6:9]) * (0.50 / 16383)
        headMotion[:,3:6] = np.copy(headMotion[:,3:6]) * (np.pi / 16383)
        
        simInterpFunction = interp1d(simMotion[:,0], simMotion[:,1:7], axis = 0, kind = "nearest")
        simInterp = simInterpFunction(headMotion[:,0])
        

        np.savetxt("real_data/MC" + str(self.MC) + "HM" +  str(self.Person).zfill(2) + ".csv", headMotion, delimiter = ",")
        
        #-------------Position transformation------------
        headPosHRF = np.empty((len(headMotion), 3))
        
        headPosHRF[:,0] = headMotion[:,8]
        headPosHRF[:,1] = -headMotion[:,6] - 0.55
        headPosHRF[:,2] = -headMotion[:,7] - 1.2075
        
        # plt.title("headPosHRF")
        # plt.scatter(headMotion[:,0], headPosHRF[:,0], 5, marker = "x")
        # plt.scatter(headMotion[:,0], headPosHRF[:,1], 5, marker = "x")
        # plt.scatter(headMotion[:,0], headPosHRF[:,2], 5, marker = "x")
        # plt.show()
        
        x_angle = simInterp[:,3]
        y_angle = simInterp[:,4]
        z_angle = simInterp[:,5]
        
        # plt.title("angles")
        # plt.scatter(headMotion[:,0], x_angle, 5, marker = "x", label = "roll")
        # plt.scatter(headMotion[:,0], y_angle, 5, marker = "x", label = "pitch")
        # plt.scatter(headMotion[:,0], z_angle, 5, marker = "x", label = "yaw")
        # plt.legend()
        # plt.show()
        

        ##- row 1 of transformation matrix
        m_11 = np.cos(y_angle)*np.cos(z_angle)
        m_12 = np.cos(y_angle)*np.sin(z_angle)
        m_13 = -np.sin(y_angle)

        ##- row 2 of transformation matrix
        m_21 =  np.sin(x_angle)*np.sin(y_angle)*np.cos(z_angle) - np.cos(x_angle)*np.sin(z_angle)
        m_22 =  np.sin(x_angle)*np.sin(y_angle)*np.sin(z_angle) + np.cos(x_angle)*np.cos(z_angle)
        m_23 =  np.sin(x_angle)*np.cos(y_angle)

        ##- row 3 of transformation matrix
        m_31 =  np.cos(x_angle)*np.sin(y_angle)*np.cos(z_angle) + np.sin(x_angle)*np.sin(z_angle)
        m_32 =  np.cos(x_angle)*np.sin(y_angle)*np.sin(z_angle) - np.sin(x_angle)*np.cos(z_angle)
        m_33 =  np.cos(x_angle)*np.cos(y_angle)

        trans_matrix = np.swapaxes(np.array([[m_11,m_12,m_13],[m_21,m_22,m_23],[m_31,m_32,m_33]]), 0, 2)

        headPosSI = np.squeeze(np.matmul(trans_matrix, np.expand_dims(headPosHRF, headPosHRF.ndim)))
        
        # plt.title("headPosSI")
        # plt.scatter(headMotion[:,0], headPosSI[:,0], 5, marker = "x")
        # plt.scatter(headMotion[:,0], headPosSI[:,1], 5, marker = "x")
        # plt.scatter(headMotion[:,0], headPosSI[:,2], 5, marker = "x")
        # plt.show()
        
        headPosSI = headPosSI + simInterp[:,0:3]
        
        #-------------Angle tranformation------------
        headAngleSI = np.empty((len(headMotion), 3))
        headAngleSI[:,0] = x_angle + headMotion[:,3]
        headAngleSI[:,1] = y_angle - headMotion[:,4]
        headAngleSI[:,2] = z_angle - headMotion[:,5]
        
        #--------Compiling all into one array--------
        headMotionSI = np.empty(headMotion.shape)
        headMotionSI[:,0:3] = headMotion[:,0:3]
        headMotionSI[:,3:6] = headPosSI
        headMotionSI[:,6:9] = headAngleSI
        
        return headMotionSI

    def solve(self):
        for i in range(6):
            print("solving: dimension", i)
            self.results.append(singleDOFsystem(self.simMotion[:,[0, i + 1, i + 7]], self.headMotion[:,[0, i + 3]]).solve())
        print(self.results)


class singleDOFsystem:
    def __init__(self, simMotion, headMotion):
        self.simMotion = simMotion
        self.initialConditions = [headMotion[0,1], 0.0]
        self.headMotion = headMotion
        self.forcing_functions = interp1d(simMotion[:,0], simMotion[:,[1,2]].T)

    def solve(self):
        max_headTime = self.headMotion[-1,0]
        i = len(self.simMotion) - 1
        while self.simMotion[i,0] > max_headTime:
            i -= 1
        simMotion = self.simMotion[3:i]
        t = (simMotion.T)[0]
        xs = (simMotion.T)[1]
        xdots = (simMotion.T)[2]
        xhfunc = interp1d(self.headMotion[:,0], self.headMotion[:,1], kind="cubic", assume_sorted = True)
        xh = xhfunc(t)
        deltaT = 1e-5
        xdoth = derivative(xhfunc, t, dx = deltaT, n = 1)
        xdotdot = derivative(xhfunc, t, dx = deltaT, n = 2)
        
        # plt.scatter(t, xh, label = "position")
        # plt.scatter(t, xdoth, label = "velocity")
        # plt.scatter(t, xdotdot, label = "acceleration")
        # plt.legend()
        # plt.show()
        
        # plt.scatter(t, xs - xh, 5, marker = "x")
        # plt.show()
        
        
        A = np.array([xs - xh, xdots - xdoth, np.ones(xs.shape)]).T
        k_and_c, residuals, rank, s = np.linalg.lstsq(A, xdotdot, rcond=None)
        
        # print(residuals)
        
        # xdotdotmodel = np.matmul(A, k_and_c)
        # plt.scatter(t, xdotdotmodel, label = "model")
        # plt.scatter(t, xdotdot, label = "real")
        # plt.legend()
        # plt.show()
        
        
        
        # return k_and_c
        
        
        
        # sol = solve_ivp(forced_mass_spring_damper, (t[0], t[-1]), [xh[0], xdoth[0]], t_eval = t, args = (k_and_c, self.forcing_functions))
        # nonInterpSol = sol.y
        # plshelp = xh - self.forcing_functions(t)[0]
        # # plt.scatter(t, xs, 5, label="sim motion pos", marker = "x")
        # plt.scatter(t, plshelp, 5, label="real", marker = "x")
        # # plt.scatter(self.headMotion[:-1,0], np.diff(self.headMotion[:,1])/np.diff(self.headMotion[:,0]) - self.forcing_functions(self.headMotion[:-1,0])[0], 5, label="real Velocity", marker = "x")
        # plt.scatter(t, xdoth, 5, label="real Velocity", marker = "x")
        # plt.scatter(sol.t, nonInterpSol[0] - self.forcing_functions(sol.t)[0], 5, label="integrated model", marker = "^")
        # plt.scatter(sol.t, nonInterpSol[1] - self.forcing_functions(sol.t)[1], 4, label="integrated model Velocity", marker = "^")      
        # plt.title(str(k_and_c))
        # plt.legend()
        # plt.show()
        # plt.clf()
        
        return k_and_c

