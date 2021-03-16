import motionTools
import numpy as np
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

headMotionSystems = []

for i, headMotion in enumerate(headMotions_1):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if (i >= 2 and i <= 9):
        headMotion[:,0] += 0.02
    headMotionSystems.append(motionTools.headMotion(simMotion_1, headMotion, [i + 1, 1]))

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if ((i >= 1 and i <= 4) or i == 8 or i == 10):
        headMotion[:,0] += 0.02
    headMotionSystems.append(motionTools.headMotion(simMotion_2, headMotion, [i + 1, 2]))

for system in headMotionSystems:
    system.solve()