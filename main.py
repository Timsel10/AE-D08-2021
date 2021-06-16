import motionTools
import numpy as np
import os

print("Loading Simulator Motion Files")
simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)

# Changing time to seconds instead of DUECA time
simMotion_1[:,0] = (simMotion_1[:,0] - simMotion_1[0,0]) * 0.0001
simMotion_2[:,0] = (simMotion_2[:,0] - simMotion_2[0,0]) * 0.0001

print("Loading Head Motion Files")

headMotions_1 = []
headMotions_2 = []

for filename in os.listdir("filtered_data"):
    #if "MC1" in filename:
        #headMotions_1.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        #print(filename)

    if "MC1" in filename:
        if "01" in filename:
            headMotions_1.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
            print(filename)

headMotionSystems = []

print("Initializing all experiments")

max_rotation = 0

for i, headMotion in enumerate(headMotions_1):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    # Synchronising
    # It was found the subjects 3 to 10 had to be synchronized by changing the time by 0.02s
    if (i >= 2 and i <= 9):
        headMotion[:,0] += 0.02
    # Initializes model
    headMotionSystems.append(motionTools.headMotionSystem(simMotion_1, headMotion, (i + 1, 1), [[0.75,4.0,0.0]] * 6))

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    # Synchronising
    if ((i >= 1 and i <= 4) or i in [8, 10]):
        headMotion[:,0] += 0.02
    # Initializes model
    headMotionSystems.append(motionTools.headMotionSystem(simMotion_2, headMotion, (i + 1, 2), [[1.0,3.0,-0.55]] * 6))

print("Solving all experiments")

for i, system in enumerate(headMotionSystems):
    print("solving:", i)
    system.solve()