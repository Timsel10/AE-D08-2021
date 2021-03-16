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

##def squares(array1, array2, shift):
##    sum = 0
##    print(shift)
##    for i in range(shift, len(array1) - 5 * (abs(shift) + 5)):
##        if i > 45000 - 5:
##            print("test " + str(len(array1) - 5 * (abs(shift) + 5)))
##            print(i)
##        sum += (array1[i + shift] - array2[i * 4]) ** 2

##    return sum / (len(array1) - 5 * (abs(shift) + 5))

##def determine_shift(steps, array1, array2):
##    min_squares = 10**100
##    min_shift = 0
##    for shift in range(-steps, steps):
##        test_squares = squares(array1, array2, shift)
##        if test_squares < min_squares:
##            min_squares = test_squares
##            min_shift = shift

##    return shift

#def squares(array1, array2):
#    max_crop = min(array2.size, array1.size)
#    residual = array1[:max_crop] - array2[:max_crop]
#    sum = np.sum((residual) ** 2)
#    print(sum)
#    print(str(array1.size) + " size")
#    return sum

#def determine_shift(steps, array1, array2, scale = 4):
#    max_crop = min(array1.size, array2.size // scale) - steps
#    sample1 = np.copy(array1)
#    sample2 = np.copy(array2)
#    min_squares = 10 ** 100
#    min_shift = 0
#    for shift in range(-steps, steps):
#        test_squares = squares(sample1[steps:max_crop], sample2[steps+shift:(max_crop+shift) * scale:scale])
#        if test_squares < min_squares:
#            min_squares = test_squares
#            min_shift = shift

#    print(min_squares)
#    return shift

#simData1 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)
##headData1 = np.genfromtxt("data/S02_MC1_HeadMotion.csv", delimiter = ",", skip_header = 1)

#headXdotdots = []
#fileNames = []
#for file in os.listdir("data"):
#    if "MC2" in file:
#        headData = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
#        headXdotdots.append([(headData[:,0] - headData[0,0]) * 0.0001, headData[:,1]])
#        fileNames.append(file)


#simTime  = (simData1[:,0] - simData1[0,0]) * 0.0001
#simXdotdot = simData1[:,13]

##headTime = (headData1[:,0] - headData1[0,0]) * 0.0001
##headXdotdot = headData1[:,1]

#linestyles = ["--", "-."]
#shifts = []
#plt.plot(simTime, simXdotdot, "r")
#for i, headXdotdot in enumerate(headXdotdots):
#    #shift = determine_shift(10, headXdotdot[1], simXdotdot)
#    #print(str(i + 1) + "takes" + str(shift) + "shifts or " + str(shift * 0.01) + "ms")
#    #headXdotdot[0] = headXdotdot[0] + shift * 0.01
#    #shifts.append(shift * 0.01)
#    plt.plot(headXdotdot[0]+ (- len(headXdotdots) // 2 + i) * 0.0005, headXdotdot[1], label=fileNames[i], linestyle = linestyles[i//10])
#    #plt.plot(headTime, headXdotdot, "b")

#print(shifts)

#plt.legend()
#plt.show()
#print(len(headXdotdots))




#def shift(shiftArray, shiftTime):
#    for i in range(len(shiftArray)):
#        shiftArray[i] += shiftTime
#    return shiftArray

#def getSyncedLists(Condition1 = True): # return [timeList, dataList, filenames]
#    if Condition1:
#        simData = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
#    else:
#        simData = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)

#    headData = []
#    fileNames = []

#    for file in os.listdir("data"):
#        if (Condition1 and ("MC1" in file)) or (not Condition1 and ("MC2" in file)):
#            headDat = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
#            headData.append([(headDat[:,0] - headDat[0,0]) * 0.0001, headDat[:,1]])
#            fileNames.append(file)

#    simTime  = (simData[:,0] - simData[0,0]) * 0.0001
#    simXdotdot = simData[:,13]

#    returnData = [] #Time, Data points, name

#    returnData.append([simTime, simXdotdot, "Simulator Data"])

#    for i, data in enumerate(headData):
#        time = data[0]
#        xDotdot = data[1]
#        if (Condition1 and (i >= 2 and i <= 9)):
#            shift(time, 0.02)
#        if (not Condition1 and ((i >= 1 and i <= 4) or i == 8 or i == 10)):
#            shift(time, 0.02)

#        returnData.append([time, xDotdot, fileNames[i]])

#    return returnData


#MainData = getSyncedLists(False)

#linestyles = ["--", "-.", ":"]


#for i, data in enumerate(MainData):
#    time = data[0]
#    xDotdot = data[1]

#    if i == 0:
#       plt.plot(time, xDotdot, label=data[2], color='r')
#    else:
#        plt.plot(time, xDotdot, label=data[2], linestyle = linestyles[i%2])


#plt.legend()
#plt.show()