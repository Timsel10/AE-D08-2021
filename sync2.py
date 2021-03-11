import numpy as np
import os
simData1 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)
#headData1 = np.genfromtxt("data/S02_MC1_HeadMotion.csv", delimiter = ",", skip_header = 1)

simTime  = (simData1[:,0] - simData1[0,0]).astype(int)
simXdotdot = (simData1[:,13]*10000000).astype(int)
simData = simData1[:,13]
headXdotdots = []
fileNames = []
headDatas = []
for file in os.listdir("data"):
    if "MC2" in file:
        headData = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
        headXdotdots.append([(headData[:,0] - headData[0,0]).astype(int), (headData[:,1]*10000000).astype(int)])
        headDatas.append(headData[:,1])
        fileNames.append(file)

#for i, fileName in enumerate(fileNames):
#    print(str(headXdotdots[i][0][431]), str(headXdotdots[i][1][431]))
#print()
#print(str(simTime[1724]), simXdotdot[1726])
def square_diff(array1, array2):
    max_crop = min(array1.size, array2.size)
    return np.sum(np.square(array1[:max_crop] - array2[:max_crop]))

print("-----BEFORE-----")
for i, fileName in enumerate(fileNames):
    print(square_diff(headDatas[i], simData[::4]))

print("-----AFTER-----")
for i, fileName in enumerate(fileNames):
    if i+1 in [1,6,7,8,10,12]:
        print(square_diff(headDatas[i], simData[::4]))
    else:
        print(square_diff(headDatas[i], simData[2::4]))

for i in range(len(headDatas[1])):
    if abs(headDatas[1][i] - headDatas[2][i]) > 0.0000000001:
        print(i)