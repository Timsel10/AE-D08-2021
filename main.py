import motionTools
import numpy as np
import os


headMotionNames_1 = []
headMotionNames_2 = []

# could change to filteredData folder
for fileName in os.listdir("filteredData"):
    if "MC1" in fileName:
        headMotionNames_1.append(fileName)

    if "MC2" in fileName:
        headMotionNames_2.append(fileName)

simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)

headMotionSystems = []

for headMotionName in headMotionNames_1:
    headMotionSystems.append(motionTools.headMotion(simMotion_1, headMotionName))

for headMotionName in headMotionNames_2:
    headMotionSystems.append(motionTools.headMotion(simMotion_2, headMotionName))

for system in headMotionSystems:
    system.solve()