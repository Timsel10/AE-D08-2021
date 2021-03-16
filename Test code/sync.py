import numpy as np
import os

def shift(shiftArray, shiftTime):
    for i in range(len(shiftArray)):
        shiftArray[i] += shiftTime
    return shiftArray

def getSyncedLists(Condition1 = True): # return [timeList, dataList, filenames]
    if Condition1:
        simData = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
    else:
        simData = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)

    headData = []
    fileNames = []

    for file in os.listdir("data"):
        if (Condition1 and ("MC1" in file)) or (not Condition1 and ("MC2" in file)):
            headDat = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
            headData.append([(headDat[:,0] - headDat[0,0]) * 0.0001, headDat[:,1]])
            fileNames.append(file)

    simTime  = (simData[:,0] - simData[0,0]) * 0.0001
    simXdotdot = simData[:,13]

    returnData = [] #Time, Data points, name

    returnData.append([simTime, simXdotdot, "Simulator Data"])

    for i, data in enumerate(headData):
        time = data[0]
        xDotdot = data[1]
        if (Condition1 and (i >= 2 and i <= 9)):
            shift(time, 0.02)
        if (not Condition1 and ((i >= 1 and i <= 4) or i == 8 or i == 10)):
            shift(time, 0.02)

        returnData.append([time, xDotdot, fileNames[i]])

    return returnData


