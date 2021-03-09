import numpy as np
import math 

#body to inertial

#---- angles
phi_x
phi_y
phi_z


#---- transformation matrices
T_x = np.array([1,0,0],[0,math.cos(phi_x),sin(phi_x)],[0,-sin(phi_x),cos(phi_x)])
T_y = np.array([cos(phi_y),0,-sin(phi_y)],[0,1,0],[sin(phi_y),0,cos(phi_y)])
T_z = np.array([cos(phi_z),sin(phi_z),0],[-sin(phi_z),cos(phi_z),0],[0,0,1])

T = np.dot(T_x, T_y, T_z)



#inertial to body