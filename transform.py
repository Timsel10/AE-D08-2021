import numpy as np
import math as m
import os

headMotions_1 = []
headMotions_2 = []

for fileName in os.listdir("filtered_data"):
    if "MC1" in fileName:
        headMotions_1.append(np.genfromtxt("filtered_data/" + filename, delimiter = ",", skip_header = 1))

    if "MC2" in fileName:
        headMotionNames_2.append(np.genfromtxt("filtered_data/" + filename, delimiter = ",", skip_header = 1))

simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)


simMotion_1[:,0] = (simData[:,0] - simData[0,0]) * 0.0001
simMotion_2[:,0] = (simData[:,0] - simData[0,0]) * 0.0001

for i, headMotion in enumerate(headMotions_1):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if (i >= 2 and i <= 9):
        headMotion[:,0] += 0.02

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if ((i >= 1 and i <= 4) or i == 8 or i == 10):
        headMotion[:,0] += 0.02




#HeadMotion:
# degrees goes from 3 to 5
# distance goes from 6 to 8

#MotionCondition:
# degress goes from 4 to 6
# distance goes from 1 to 3

#-------------------------------------------------------------------------------------
# change the raw data to actual data

step_distance = float(50 / 16383)
step_degree = float(180 / 16383)


def change_data_raw(column, factor, data): # column = int, factor = int, data = nested list
    for i in range(len(data)):
        value_raw = data[i][column]
        value_actual = value_raw * factor
        data[i][column].change(value_actual)  #dont know if this line works
    return

# call function multiple times

for i in range("data related to distance"):
    change_data_raw(i, step_distance, simMotion_1[:,15:1)
    change_data_raw(i, step_distance, simMorion_2)

for j in range("data realted to degrees"):
    change_data_raw(j, step_degree, simMotion_1)
    change_data_raw(j, step_degree, simMotion_2)




###   position of the UGP x,y,z inertial  (-> body reference frame) -> head reference frame

def position():
    # input
    cx_in = 0         #coordinate x in inertial ref          
    cy_in = 0         #coordinate y in inertial ref 
    cz_in = 0         #coordinate z in inertial ref 

    cx_dot_in = 0     #velocity x in inertial ref      
    cy_dot_in = 0     #velocity y in inertial ref
    cz_dot_in = 0     #velocity z in inertial ref

    cx_ddot_in = 0    #acceleration x in inertial ref
    cy_ddot_in = 0    #acceleration y in inertial ref
    cz_ddot_in = 0    #acceleration z in inertial ref

    x_in = roll_in   #angle about x 
    y_in = pitch_in  #angle about y
    z_in = yaw_in    #angle about z

    p = 0             #roll rate simulator body
    q = 0             #pitch rate simulator body
    r = 0             #yaw rate simulator body

    pd = 0            #roll acceleration simulator body
    qd = 0            #pitch acceleration simulator body
    rd = 0            #yaw acceleration simulator body            

    return cx_in, cy_in, cz_in, cx_dot_in, cy_dot_in, cz_dot_in, cx_ddot_in, cy_ddot_in, cz_ddot_in

    ###  entries transformation matrix 
def transform_matrix_Angles_gen_MotionCond(x_in, y_in, z_in):
    #- row 1 of transformation matrix
    m_11 = m.cos(y_in)*m.cos(z_in)
    m_12 = m.cos(y_in)*m.sin(z_in)
    m_13 = -m.sin(y_in)

    #- row 2 of transformation matrix
    m_21 = m.sin(x_in)*m.sin(y_in)*m.cos(z_in)-m.cos(x_in)*m.sin(z_in)
    m_22 =  m.sin(x_in)*m.sin(y_in)*m.sin(z_in) + m.cos(x_in)*m.cos(z_in)
    m_23 =  m.sin(x_in)*m.cos(y_in)

    #- row 3 of transformation matrix
    m_31 =  m.cos(x_in)*m.sin(y_in)*m.cos(z_in) + m.sin(x_in)*m.sin(z_in)
    m_32 =  m.cos(x_in)*m.sin(y_in)*m.sin(z_in) - m.sin(x_in)*m.cos(z_in)
    m_33 =  m.cos(x_in)*m.cos(y_in)

    # transformation matrix
    trans_matrix = np.array([[m_11,m_12,m_13],[m_21,m_22,m_23],[m_31,m_32,m_33]])
    return trans_matrix


def transforming():
    ### position
    # vector x,y,z inertial reference frame
    vec_co_in = np.array([cx_in],[cy_in],[cz_in])
    # vector x,y,z in body reference frame
    vec_co_br = np.dot(trans_matrix,vec_co_in) # transformatrix * vector_inertial
    # vector x,y,z in head reference frame ( -y_br -> x_hr, -z_b -> y_hr, x_b -> z_hr )
    vec_co_hr = np.array([-vec_co_br[1]],[-vec_co_br[2]],[vec_co_br[0]])


    ### veloctiy
    # veloctiy vector inertial frame
vec_v_in = np.array([cx_dot_in],[cy_dot_in],[cz_dot_in])

# velocity vector body frame
vec_v_br = np.dot([trans_matrix,vec_v_in])

# velocity vector head frame
omega = np.array([-q,0,0],[0,-r,0],[0,0,p])
neg_vec_co_hr = -1* np.array([-vec_co_br[1]],[-vec_co_br[2]],[vec_co_br[0]])
vec_v_hr = np.array([-vec_v_br[1]],[-vec_v_br[2]],[vec_v_br[0]])+ np.dot(omega,neg_vec_co_hr)


### acceleration
# acceleration vector inertial frame
vec_a_in = np.array([cx_ddot_in],[cy_ddot_in],[cz_ddot_in])

# acceleration vector body frame
vec_a_br = np.dot([trans_matrix,vec_a_in])

#acceleration vector head ref frame
acc = np.array([-qd,0,0],[0,-rd,0],[0,0,pd])

#acceleration vector head reference
omega_d =  np.array([q**2,0,0],[0,r**2,0],[0,0,p**2])
vec_a_hr = np.array([-vec_a_br[1]],[-vec_a_br[2]],[vec_a_br[0]])+ np.dot(acc,neg_vec_co_hr) - np.dot(omega_d,neg_vec_co_hr)


 
#_______________________________________________________________________
