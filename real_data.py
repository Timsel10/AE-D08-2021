import os
import numpy as np

step_distance = float(10**-3 * 50 / 16383)
step_degree = float(180 / 16383)

def change_data_raw(column, factor, data): # column = int, factor = int, data = nested list
    data[:,column] = data[:,column] * factor
    

# Changing from Raw to Real Values
def real_data_Motion_condition(step_distance, simMotion_1, simMotion_2):
    for i in range(1, 19):
        if i in [1,2,3,7,8,9,13,14,15]:
            change_data_raw(i, step_distance, simMotion_1)
            change_data_raw(i, step_distance, simMotion_2)

        if i in [4,5,6,10,11,12,16,17,18]:
            change_data_raw(i, step_degree, simMotion_1)
            change_data_raw(i, step_degree, simMotion_2)

def real_data_Head_Motion(data):
    for i in [6, 7, 8]:
        change_data_raw(i, step_distance, data)
    for i in [3, 4, 5]:
        change_data_raw(i, step_degree, data)


for filename in os.listdir("filtered_data"):
    # folder = list.(os.listdir("filtered_data"))
    data = np.genfromtxt("filtered_data/" + filename, delimiter = ",")

    real_data_Head_Motion(data)

    np.savetxt("real_data/" + filename, data, delimiter = ",")