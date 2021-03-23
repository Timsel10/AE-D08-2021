import matplotlib.pyplot as plt
import numpy as np
import os

headMotionsOriginal = []
headMotionsFiltered = []

print("Original data loading...")
for filename in os.listdir("data"):
    if "MC1" in filename:
        headMotionsOriginal.append(np.genfromtxt("data/" + filename, delimiter = ",", skip_header = 1))
        print(filename)

for filename in os.listdir("data"):
    if "MC2" in filename:
        headMotionsOriginal.append(np.genfromtxt("data/" + filename, delimiter = ",", skip_header = 1))
        print(filename)

print("Filtered data loading...")
for filename in os.listdir("filtered_data"):
    if "MC1" in filename:
        headMotionsFiltered.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        print(filename)

for filename in os.listdir("filtered_data"):
    if "MC2" in filename:
        headMotionsFiltered.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        print(filename)


for no, filtered in enumerate(headMotions):
    #filename = "S02_MC1_HeadMotion.csv"

    #original = np.genfromtxt("data/" + filename, delimiter=",", skip_header=1)
    #filtered = np.genfromtxt("filtered_data/" + filename, delimiter=",")

    original = headMotionsOriginal[no]
    filtered = headMotionsFiltered[no]

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