import motionTools
import numpy as np
import os

print("Loading Simulator Motion Files")
simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)


simMotion_1[:,0] = (simMotion_1[:,0] - simMotion_1[0,0]) * 0.0001
simMotion_2[:,0] = (simMotion_2[:,0] - simMotion_2[0,0]) * 0.0001

#np.savetxt("real_data/MotionCondition1.csv", simMotion_1, delimiter = ",")
#np.savetxt("real_data/MotionCondition2.csv", simMotion_2, delimiter = ",")

print("Loading Head Motion Files")

headMotions_1 = []
headMotions_2 = []

for filename in os.listdir("filtered_data"):
    #if "MC1" in filename:
        #headMotions_1.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        #print(filename)

    if "MC2" in filename:
        if "01" in filename:
            headMotions_2.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
            print(filename)

headMotionSystems = []

print("Initializing all experiments")

for i, headMotion in enumerate(headMotions_1):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if (i >= 2 and i <= 9):
        headMotion[:,0] += 0.02
    headMotionSystems.append(motionTools.headMotionSystem(simMotion_1, headMotion, (i + 1, 1), [[1000,10,0.3]] * 6))

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if ((i >= 1 and i <= 4) or i in [8, 10]):
        headMotion[:,0] += 0.02
    headMotionSystems.append(motionTools.headMotionSystem(simMotion_2, headMotion, (i + 1, 2), [[1000,10,0.3]] * 6))

print("Solving all experiments")

for i, system in enumerate(headMotionSystems):
    print("solving:", i)
    system.solve()