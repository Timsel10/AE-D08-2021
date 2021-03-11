#import numpy as np
#import math
import os

folder = os.listdir("data")
Motioncond_1 = folder[0]
Motioncond_2 = folder[1]

file_1 = open(Motioncond_1)
    file_1.readlines(400)
   
file_1.close()

file_2 = open(motioncond_2)


# degrees goes from 3 to 5
# distance goes from 6 to 8

#-------------------------------------------------------------------------------------
# change the raw data to actual data

step_distance = 50 / 16383
step_degree = 180 / 16383
data = np.genfromtxt(filename, skip_header=1)

def change_data_raw(column, factor, data): # column = int, factor = int, data = nested list
    for i in range(len(data)):
        value_raw = data[i][column]
        value_actual = value_raw * factor
        data[i][column].change(value_actual)  #dont know if this line works
return

# call function multiple times
....

#-----------------------------------------------------------------------------------------
# position of the UGP x,y,z inertial -> head reference frame

x_ugp_hf = 

y_ugp_hf = 

z_ugp_hf = 

# np.matrix(" ; ; ; ")
# np.array([], [], [])

# Transform head_reference to body_reference



# Transform body_reference to inertial_reference