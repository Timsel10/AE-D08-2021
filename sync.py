import numpy as np
import matplotlib.pyplot as plt
import os

def squares(array1, array2):
    sum = 0
    for i in range(len(array1)):
        sum += (array1[i] - array2[i]) ** 2

    return sum

def determine_shift(steps = range(-0.05, 0.05, 0.01)):
    squares()


simData1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
#headData1 = np.genfromtxt("data/S02_MC1_HeadMotion.csv", delimiter = ",", skip_header = 1)

headXdotdots = []
fileNames = []
for file in os.listdir("data"):
    if "MC1" in file:
        headData = np.genfromtxt("data/" + file, delimiter = ",", skip_header = 1)
        headXdotdots.append([(headData[:,0] - headData[0,0]) * 0.0001, headData[:,1]])
        fileNames.append(file)


simTime  = (simData1[:,0] - simData1[0,0]) * 0.0001
simXdotdot = simData1[:,13]

#headTime = (headData1[:,0] - headData1[0,0]) * 0.0001
#headXdotdot = headData1[:,1]

linestyles = ["--", "-."]
plt.plot(simTime, simXdotdot, "r")
for i, headXdotdot in enumerate(headXdotdots):
    if not(i == 1 or i == 9):
        print(len(headXdotdot[1]))
        plt.plot(headXdotdot[0], headXdotdot[1], label=fileNames[i], linestyle = linestyles[i//10])
    #plt.plot(headTime, headXdotdot, "b")

plt.legend()
plt.show()
print(len(headXdotdots))


