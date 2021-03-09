import numpy as np
import matplotlib.pyplotas plt

simData1 = np.genfromtxt("csvFiles/MotionCondition_1.csv", delimiter = ",", skip_header = 1)

simData1[:,0]  = (simData1[:,0] - simData[0,0]) * 0.0001


