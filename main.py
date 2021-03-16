import motionTools
import numpy as np
import os


headMotionNames_1 = []
headMotionNames_2 = []

for fileName in os.listdir("filtered_data"):
    if "MC1" in fileName:
        headMotionNames_1.append(fileName)

    if "MC2" in fileName:
        headMotionNames_2.append(fileName)

simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)


simMotion_1[:,0] = (simData[:,0] - simData[0,0]) * 0.0001
simMotion_2[:,0] = (simData[:,0] - simData[0,0]) * 0.0001

headMotionSystems = []

for headMotionName in headMotionNames_1:
    headMotionSystems.append(motionTools.headMotion(simMotion_1, headMotionName))

for headMotionName in headMotionNames_2:
    headMotionSystems.append(motionTools.headMotion(simMotion_2, headMotionName))

for system in headMotionSystems:
    system.solve()


#------------------------------------------------------------------
# Return [names, data[]] first data is MotionCondition_#.csv with [0-18] for 1 & 2; the rest is [0-8]
# This function will first open up MotionCondition_#, based on Condition1 = True/False
# It will then open head motion models for that condition
# Following up it will append the MotionCondition data to the returnData, this will be in the form of ["MotionCondition_#", [List[0-18]]]
# After this the synchronization will happen for the head motion models
# Once synchronized by 0.02 seconds for the corresponding files it will append the data to the returnData in the form of ["FileName", [List[0-8]]]
# NOTE: The first list index [0] is the time, this will start at 0.0 seconds; the data in the motion files use DUECA time, which starts at some random integer, so this has been altered to 0.0
def getSyncedLists(): 
    headData = []
    fileNames = []

    for file in os.listdir("filtered_data"):
        if ("MC1" in file):
            headDat = np.genfromtxt("filtered_data/" + file, delimiter = ",", skip_header = 1)
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