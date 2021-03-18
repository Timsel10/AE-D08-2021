import numpy as np
import os

print("transform.py running now..")

#headMotions_1 = []
#headMotions_2 = []

#for filename in os.listdir("filtered_data"):
#    if "MC1" in filename:
#        headMotions_1.append(np.genfromtxt("filtered_data/" + filename, delimiter = ",", skip_header = 1))

#    if "MC2" in filename:
#        headMotions_2.append(np.genfromtxt("filtered_data/" + filename, delimiter = ",", skip_header = 1))

simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)

print("yes")
simMotion_1[:,0] = (simMotion_1[:,0] - simMotion_1[0,0]) * 0.0001
simMotion_2[:,0] = (simMotion_2[:,0] - simMotion_2[0,0]) * 0.0001

#for i, headMotion in enumerate(headMotions_1):
#    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
#    if (i >= 2 and i <= 9):
#        headMotion[:,0] += 0.02

#for i, headMotion in enumerate(headMotions_2):
#    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
#    if ((i >= 1 and i <= 4) or i == 8 or i == 10):
#        headMotion[:,0] += 0.02

#1 , 5 ,5 
#2, 10, 15

#[[1, 5m, 5ms][2s, 10, 15]]
#data[:,1]

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
    data[:,column] = data[:,column] * factor
    

# call function multiple times

for i in range(1, 19):
    if i in [1,2,3,7,8,9,13,14,15]:
        change_data_raw(i, step_distance, simMotion_1)
        change_data_raw(i, step_distance, simMotion_2)

    if i in [4,5,6,10,11,12,16,17,18]:
        change_data_raw(i, step_degree, simMotion_1)
        change_data_raw(i, step_degree, simMotion_2)



print("yes")



# def transformation(data): # data = sim_motion_1 or sim_motion_2
#     return

###   position of the UGP x,y,z inertial  (-> body reference frame) -> head reference frame


def transformation_data(data):
    # input
    cx_in = data[:,1]        #coordinate x in inertial ref          
    cy_in = data[:,2]        #coordinate y in inertial ref 
    cz_in = data[:,3]        #coordinate z in inertial ref 

    cx_dot_in = data[:,7]     #velocity x in inertial ref      
    cy_dot_in = data[:,8]     #velocity y in inertial ref
    cz_dot_in = data[:,9]    #velocity z in inertial ref

    cx_ddot_in = data[:,13]    #acceleration x in inertial ref
    cy_ddot_in = data[:,14]    #acceleration y in inertial ref
    cz_ddot_in = data[:,15]    #acceleration z in inertial ref

    x_in = data[:,4]    #angle about x 
    y_in = data[:,5]    #angle about y
    z_in = data[:,6]    #angle about z

    p = data[:,10]      #roll rate simulator body
    q = data[:,11]      #pitch rate simulator body
    r = data[:,12]      #yaw rate simulator body

    pd = data[:,16]     #roll acceleration simulator body
    qd = data[:,17]     #pitch acceleration simulator body
    rd = data[:,18]     #yaw acceleration simulator body            

    return x_in, y_in, z_in, cx_in, cy_in, cz_in, cx_dot_in, cy_dot_in, cz_dot_in, cx_ddot_in, cy_ddot_in, cz_ddot_in, p, q, r, pd, qd, rd

    ###  entries transformation matrix 
def transform_matrix_Angles_gen_MotionCond(x_in, y_in, z_in):
    
    
    #- row 1 of transformation matrix
    m_11 = np.cos(y_in)*np.cos(z_in)
    m_12 = np.cos(y_in)*np.sin(z_in)
    m_13 = -np.sin(y_in)

    #- row 2 of transformation matrix
    m_21 =  np.sin(x_in)*np.sin(y_in)*np.cos(z_in)-np.cos(x_in)*np.sin(z_in)
    m_22 =  np.sin(x_in)*np.sin(y_in)*np.sin(z_in) + np.cos(x_in)*np.cos(z_in)
    m_23 =  np.sin(x_in)*np.cos(y_in)

    #- row 3 of transformation matrix
    m_31 =  np.cos(x_in)*np.sin(y_in)*np.cos(z_in) + np.sin(x_in)*np.sin(z_in)
    m_32 =  np.cos(x_in)*np.sin(y_in)*np.sin(z_in) - np.sin(x_in)*np.cos(z_in)
    m_33 =  np.cos(x_in)*np.cos(y_in)

    # transformation matrix
    trans_matrix = np.array([[m_11,m_12,m_13],[m_21,m_22,m_23],[m_31,m_32,m_33]])
    return trans_matrix



   ### tranforming the inertial reference frame -> head reference frame
def transforming(cx_in, cy_in, cz_in, cx_dot_in, cy_dot_in, cz_dot_in, cx_ddot_in, cy_ddot_in, cz_ddot_in, p, q, r, pd, qd, rd, trans_matrix):

    ### position
    # vector x,y,z inertial reference frame
    vec_co_in = np.array([[cx_in],[cy_in],[cz_in]])
    # vector x,y,z in body reference frame

    vec_co_br = np.dot(trans_matrix, vec_co_in) # transformatrix * vector_inertial
    # vector x,y,z in head reference frame ( -y_br -> x_hr, -z_b -> y_hr, x_b -> z_hr )
    vec_co_hr = np.array([-vec_co_br[1],-vec_co_br[2],vec_co_br[0]])


    ### veloctiy
    # veloctiy vector inertial frame
    vec_v_in = np.array([[cx_dot_in],[cy_dot_in],[cz_dot_in]])

    # velocity vector body frame
    vec_v_br = np.dot(trans_matrix,vec_v_in)

    # velocity vector head frame
    omega = np.array([[-q,0,0],[0,-r,0],[0,0,p]])
    neg_vec_co_hr = -1 * np.array([-vec_co_br[1],-vec_co_br[2],vec_co_br[0]])
    test = np.dot(omega,neg_vec_co_hr)
    test2 = np.array([-vec_v_br[1],-vec_v_br[2],vec_v_br[0]])
    vec_v_hr = test2 + test


    ### acceleration
    # acceleration vector inertial frame
    vec_a_in = np.array([[cx_ddot_in],[cy_ddot_in],[cz_ddot_in]])

    # acceleration vector body frame
    vec_a_br = np.dot(trans_matrix,vec_a_in)

    #acceleration vector head ref frame
    acc = np.array([[-qd,0,0],[0,-rd,0],[0,0,pd]])

    #acceleration vector head reference
    omega_d =  np.array([[q**2,0,0],[0,r**2,0],[0,0,p**2]])
    vec_a_hr = np.array([-vec_a_br[1],-vec_a_br[2],vec_a_br[0]]) + np.dot(acc,neg_vec_co_hr) - np.dot(omega_d,neg_vec_co_hr)
    
    return vec_co_hr, vec_v_hr, vec_a_hr



x_in, y_in, z_in, cx_in, cy_in, cz_in, cx_dot_in, cy_dot_in, cz_dot_in, cx_ddot_in, cy_ddot_in, cz_ddot_in, p, q, r, pd, qd, rd = transformation_data(simMotion_1)

trans_matrix = transform_matrix_Angles_gen_MotionCond(x_in, y_in, z_in)

vec_co_hr = []
vec_v_hr = []
vec_a_hr = []

for i in [x_in, y_in, z_in, cx_in, cy_in, cz_in, cx_dot_in, cy_dot_in, cz_dot_in, cx_ddot_in, cy_ddot_in, cz_ddot_in, p, q, r, pd, qd, rd]:
    print(i.shape)


for i in range(len(cx_in)):
    vec_co_hri, vec_v_hri, vec_a_hri = transforming(cx_in[i], cy_in[i], cz_in[i], cx_dot_in[i], cy_dot_in[i], cz_dot_in[i], cx_ddot_in[i], cy_ddot_in[i], cz_ddot_in[i], p[i], q[i], r[i], pd[i], qd[i], rd[i], trans_matrix[:,:,i])
    vec_co_hr.append(vec_co_hri)
    vec_v_hr.append(vec_v_hri)
    vec_a_hr.append(vec_a_hri)
    if i % 10000 == 0:
        print(i)

vec_co_hr = np.array(vec_co_hr)
vec_v_hr = np.array(vec_v_hr)
vec_a_hr = np.array(vec_a_hr)

print(vec_co_hr.shape)
print(vec_v_hr.shape)
print(vec_a_hr.shape)
# np.moveaxis(vec_co_hr,)
# final = np.array()

# np.savetxt("simMotion_1_transformed.csv")
