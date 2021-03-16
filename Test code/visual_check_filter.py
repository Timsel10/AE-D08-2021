import matplotlib.pyplot as plt
import numpy as np

filename = "S02_MC1_HeadMotion.csv"

original = np.genfromtxt("data/" + filename, delimiter=",", skip_header=1)
filtered = np.genfromtxt("filtered_data/" + filename, delimiter=",")

print(len(original[:,0]))
print(len(filtered[:,0]))

headings = ["DUECA time","xdotdot","FrameSignature","Roll raw","Pitch raw","Yaw raw","X raw","Y raw","Z raw"]

plt.grid()
for i in range(2,7):
    print("showing: " + headings[i+1])
    plt.scatter(original[:,0]+100,original[:,i+1], 2, label="original")
    plt.scatter(filtered[:,0],filtered[:,i+1], 2, label="filtered")
    plt.legend(loc='best')
    plt.show()
    input("enter for next plot")
    plt.clf()





