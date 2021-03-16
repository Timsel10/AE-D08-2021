import numpy as np
import math as m
import os

#-------------------------------------------------------------------
#Shift index of array

def shift(shiftArray, shiftTime):
    for i in range(len(shiftArray)):
        shiftArray[i] += shiftTime
    return shiftArray

#------------------------------------------------------------------
# Return [names, data[]] first data is MotionCondition_#.csv with [0-18]; the rest is [0-8]
# This function will first open up MotionCondition_#, based on Condition1 = True/False
# Use False for condition 2
# It will then open head motion models for that condition
# Following up it will append the MotionCondition data to the returnData, this will be in the form of ["MotionCondition_#", [List[0-18]]]
# After this the synchronization will happen for the head motion models
# Once synchronized by 0.02 seconds for the corresponding files it will append the data to the returnData in the form of ["FileName", [List[0-8]]]
# NOTE: The first list index [0] is the time, this will start at 0.0 seconds; the data in the motion files use DUECA time, which starts at some random integer, so this has been altered to 0.0

def getSyncedLists(Condition1 = True): 
    headData = []

    fileNames = []

    if Condition1:
        simData = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
        fileNames.append("MotionCondition_1")
    else:
        simData = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)
        fileNames.append("MotionCondition_2")

    for file in os.listdir("data"):
        if (Condition1 and ("MC1" in file)) or (not Condition1 and ("MC2" in file)):
            headDat = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
            headData.append([(headDat[:,0] - headDat[0,0]) * 0.0001, headDat[:,1], headDat[:,2], headDat[:,3], headDat[:,4], headDat[:,5], headDat[:,6], headDat[:,7], headDat[:,8]])
            fileNames.append(file)

    simTime  = (simData[:,0] - simData[0,0]) * 0.0001

    simData[:,0] = simTime

    returnData = [] #Time, Data points, name

    returnData.append([fileNames[0], [simData[:,0], simData[:,1], simData[:,2], simData[:,3], simData[:,4], simData[:,5], simData[:,6], simData[:,7], simData[:,8], simData[:,9], simData[:,10], simData[:,11], simData[:,12], simData[:,13], simData[:,14], simData[:,15], simData[:,16], simData[:,17], simData[:,18]]])

    for i, data in enumerate(headData):
        returnDat = data

        if (Condition1 and (i >= 2 and i <= 9)) or (not Condition1 and ((i >= 1 and i <= 4) or i == 8 or i == 10)):
            shift(returnDat[0], 0.02)

        returnData.append([fileNames[i+1], returnDat])

    return returnData

#HeadMotion:
# degrees goes from 3 to 5
# distance goes from 6 to 8

#MotionCondition:
# degress goes from 4 to 6
# distance goes from 1 to 3

#-------------------------------------------------------------------------------------
# change the raw data to actual data

step_distance = 50 / 16383
step_degree = 180 / 16383
data = np.genfromtxt(filename, skip_header=1)

def change_data_raw(column, factor, data): # column = int, factor = int, data = nested list
    for i in range(len(data)):
        value_raw = data[i][column]
        value_actual = value_raw * factor
        data[i][column].change(value_actual)  #dont know if this line works
return

# call function multiple times
....


###   position of the UGP x,y,z inertial  (-> body reference frame) -> head reference frame

# input
cx_in =          #coordinate x in inertial ref          
cy_in =          #coordinate y in inertial ref 
cz_in =          #coordinate z in inertial ref 

x_in =   roll_in         #angle about x 
y_in =   pitch_in        #angle about y
z_in =   yaw_in          #angle about z



#  entries transformation matrix 

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



# vector x,y,z inertial reference frame
vec_co_in = np.array([cx_in],[cy_in],[cz_in])

# vector x,y,z in body reference frame
vec_co_br = np.dot(trans_matrix,vec_co_in) # transformatrix * vector_inertial

# vector x,y,z in head reference frame ( -y_br -> x_hr, -z_b -> y_hr, x_b -> z_hr )
vec_co_hr = np.array([-vec_co_br[1],[-vec_co_br[2]],[vec_co_br[0]])




