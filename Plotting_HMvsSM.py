## Plotting HeadMotion vs SimMotions ##

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

for filename in os.listdir("real_data"):
    if "MC1" in filename:
        headMotions_1.append(np.genfromtxt("real_data/" + filename, delimiter = ","))
        print(filename)

    if "MC2" in filename:
        headMotions_2.append(np.genfromtxt("real_data/" + filename, delimiter = ","))
        print(filename)

headMotionSystems = []

print("Initializing all experiments")

for i, headMotion in enumerate(headMotions_1):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if (i >= 2 and i <= 9):
        headMotion[:,0] += 0.02
    #headMotionSystems.append(motionTools.headMotionSystem(simMotion_1, headMotion, (i + 1, 1), [[1000,10],[1000,10],[1000,10],[1000,10],[1000,10],[1000,10]]))

for i, headMotion in enumerate(headMotions_2):
    headMotion[:,0] = (headMotion[:,0] - headMotion[0,0]) * 0.0001
    if ((i >= 1 and i <= 4) or i in [8, 10]):
        headMotion[:,0] += 0.02
    #headMotionSystems.append(motionTools.headMotionSystem(simMotion_2, headMotion, (i + 1, 2), [[1000,10],[1000,10],[1000,10],[1000,10],[1000,10],[1000,10]]))


#np.savetxt("test" , headMotions_1[0], delimiter=",")
print(headMotions_1)
print(simMotion_1[-1,0])

## TAKE VALUES ##
hm_x = headMotions_1[0][:,6]
hm_y = headMotions_1[0][:,7]
hm_z = headMotions_1[0][:,8]

sm_x = simMotion_1[:,1]
sm_y = simMotion_1[:,2]
sm_z = simMotion_1[:,3]

## PRINT AVERAGE LOCATIONS ## 
hm_x_avg= (sum(hm_x)/len(hm_x))
hm_y_avg= (sum(hm_y)/len(hm_y))
hm_z_avg= (sum(hm_z)/len(hm_z))

sm_x_avg= (sum(sm_x)/len(sm_x))
sm_y_avg= (sum(sm_y)/len(sm_y))
sm_z_avg= (sum(sm_z)/len(sm_z))
print("hm_x_avg= ",hm_x_avg)
print("hm_y_avg= ",hm_y_avg)
print("hm_z_avg= ",hm_z_avg)

print("sm_x_avg= ",sm_x_avg)
print("sm_y_avg= ",sm_y_avg)
print("sm_z_avg= ",sm_z_avg)


## Set average to 0 ##
hm_x = hm_x - (sum(hm_x)/len(hm_x))
hm_y = hm_y - (sum(hm_y)/len(hm_y))
hm_z = hm_z - (sum(hm_z)/len(hm_z))

sm_x = sm_x - (sum(sm_x)/len(sm_x))
sm_y = sm_y - (sum(sm_y)/len(sm_y))
sm_x = sm_z - (sum(sm_z)/len(sm_z))

## Normalize Data (with maximal displacement being 1) ##

if max(hm_x) > abs(min(hm_x)):
    hm_x = hm_x / max(hm_x)
else:
    hm_x = hm_x / abs(min(hm_x))

if max(hm_y) > abs(min(hm_y)):
    hm_y = hm_y / max(hm_y)
else:
    hm_y = hm_y / abs(min(hm_y))


if max(hm_z) > abs(min(hm_z)):
    hm_z = hm_z / max(hm_z)
else:
    hm_z = hm_z / abs(min(hm_z))



if max(sm_x) > abs(min(sm_x)):
    sm_x = sm_x/ max(sm_x)
else:
    sm_x = sm_x / abs(min(sm_x))

if max(sm_y) > abs(min(sm_y )):
    sm_y = sm_y  / max(sm_y)
else:
    sm_y = sm_y  / abs(min(sm_y ))

if max(sm_z) > abs(min(sm_z)):
    sm_z = sm_z / max(sm_z)
else:
    sm_z = sm_z / abs(min(sm_z))



## PLOT X-DIR ##
    
plt.plot(simMotion_1[:,0],sm_x,label="Simulator")
plt.plot(headMotions_1[0][:,0],hm_x, label="Head")
plt.title("X-Direction")
plt.xlabel("Time (s)")
plt.ylabel("Displacement Normalized to Max Value")
plt.legend()
plt.show()

## PLOT Y-DIR ##

plt.plot(simMotion_1[:,0],sm_y,label="Simulator")
plt.plot(headMotions_1[0][:,0],hm_y,label="Head")
plt.title("Y-Direction")
plt.xlabel("Time (s)")
plt.ylabel("Displacement Normalized to Max Value")
plt.legend()
plt.show()

## PLOT Z-DIR ##

plt.plot(simMotion_1[:,0],sm_z,label="Simulator")
plt.plot(headMotions_1[0][:,0],hm_z,label="Head")
plt.title("Z-Direction")
plt.xlabel("Time (s)")
plt.ylabel("Displacement Normalized to Max Value")
plt.legend()
plt.show()



