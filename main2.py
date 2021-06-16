# -*- coding: utf-8 -*-
import motionTools2
import numpy as np
import os

print("Loading Simulator Motion Files")
# simMotion_1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
simMotion_2 = np.genfromtxt("data/MotionCondition_2.csv", delimiter = ",", skip_header = 1)


# simMotion_1[:,0] = (simMotion_1[:,0] - simMotion_1[0,0]) * 0.0001
simMotion_2[:,0] = (simMotion_2[:,0] - simMotion_2[0,0]) * 0.0001

print("Loading Head Motion Files")

# headMotions_1 = []
headMotions_2 = []

for filename in os.listdir("filtered_data"):
    # if "MC1" in filename: # and "S03" in filename:
    #     headMotions_1.append(np.genfromtxt("data/" + filename, delimiter = ",", skip_header = 1))
    #     print(filename)

    if "MC2" in filename: # and "S03" in filename:
        headMotions_2.append(np.genfromtxt("data/" + filename, delimiter = ",", skip_header = 1))
        print(filename)

headMotionSystems = []

print("Initializing all experiments")


# for i, headMotion in enumerate(headMotions_1):
#     headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
#     if (i >= 2 and i <= 9):
#         headMotion[:,0] += 0.02
#     headMotionSystems.append(motionTools2.headMotionSystem(simMotion_1, headMotion, (i + 1, 1)))

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if ((i >= 1 and i <= 4) or i in [8, 10]):
        headMotion[:,0] += 0.02
    if i + 1 == 2:
        headMotionSystems.append(motionTools2.headMotionSystem(simMotion_2, headMotion, (i + 1, 2)))

print("Solving all experiments")

for i, system in enumerate(headMotionSystems):
    print("solving:", i)
    system.solve()


# results = np.zeros((6, 24, 6))

# for i, system in enumerate(headMotionSystems):
#     for j, axis in enumerate(system.results):
#         results[j, i, :2] = [system.MC, system.Person]
#         results[j, i, 2:] = axis
        
# np.save("results", results)