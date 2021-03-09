import numpy as np
import matplotlib.pyplot as plt
import os

#def squares(array1, array2, shift):
#    sum = 0
#    print(shift)
#    for i in range(shift, len(array1) - 5 * (abs(shift) + 5)):
#        if i > 45000 - 5:
#            print("test " + str(len(array1) - 5 * (abs(shift) + 5)))
#            print(i)
#        sum += (array1[i + shift] - array2[i * 4]) ** 2

#    return sum / (len(array1) - 5 * (abs(shift) + 5))

#def determine_shift(steps, array1, array2):
#    min_squares = 10**100
#    min_shift = 0
#    for shift in range(-steps, steps):
#        test_squares = squares(array1, array2, shift)
#        if test_squares < min_squares:
#            min_squares = test_squares
#            min_shift = shift

#    return shift

def squares(array1, array2):
    max_crop = min(array2.size, array1.size)
    residual = array1[:max_crop] - array2[:max_crop]
    return np.sum((residual) ** 2)

def determine_shift(steps, array1, array2, scale = 4):
    max_crop = min(array1.size, array2.size // scale) - steps
    sample1 = np.copy(array1)
    sample2 = np.copy(array2)
    min_squares = 10 ** 100
    min_shift = 0
    for shift in range(-steps, steps):
        test_squares = squares(sample1[steps:max_crop], sample2[steps+shift:(max_crop - 1) * scale:scale])
        if test_squares < min_squares:
            min_squares = test_squares
            min_shift = shift

    print(min_squares)
    return shift

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
shifts = []
plt.plot(simTime, simXdotdot, "r")
for i, headXdotdot in enumerate(headXdotdots):
    shift = determine_shift(5, headXdotdot[1], simXdotdot)
    print(str(i + 1) + "takes" + str(shift) + "shifts or " + str(shift * 0.01) + "ms")
    headXdotdot[0] = headXdotdot[0] + shift * 0.01
    shifts.append(shift * 0.01)
    plt.plot(headXdotdot[0], headXdotdot[1], label=fileNames[i], linestyle = linestyles[i//10])
    #plt.plot(headTime, headXdotdot, "b")

print(shifts)

plt.legend()
plt.show()
print(len(headXdotdots))


