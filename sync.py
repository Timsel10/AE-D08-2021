import numpy as np
import matplotlib.pyplot as plt

simData1 = np.genfromtxt("data/MotionCondition_1.csv", delimiter = ",", skip_header = 1)
headData1 = np.genfromtxt("data/S01_MC1_HeadMotion.csv", delimiter = ",", skip_header = 1)

simTime  = (simData1[:,0] - simData1[0,0]) * 0.0001
simXdotdot = simData1[:,13]

headTime = (headData1[:,0] - headData1[0,0]) * 0.0001
headXdotdot = simData1[:,1]

plt.plot(simTime, simXdotdot)
plt.plot(headTime, headXdotdot)

plt.show()






