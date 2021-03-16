import numpy as np
import os

def filter(filename):
    #filename = 'S01_MC2_HeadMotion.csv'
    #filename = 'test.txt'

    data = np.genfromtxt("filtered_data/" + filename, delimiter=",", skip_header=1)
    #delimiter=","
    #print(data)
    bad_data_history = [filename]
    frame_lst = []

    for l in range(len(data)):
       frame_lst.append(int(data[l][2]))

    i=0
    while i < len(frame_lst)-6:
       #print('i:', i)
       if frame_lst[i] == frame_lst[i+1] and frame_lst[i] == frame_lst[i+2] and frame_lst[i] == frame_lst[i+3] and frame_lst[i] == frame_lst[i+4] and frame_lst[i] == frame_lst[i+5]:
          i_list = [i+1,i+2,i+3,i+4,i+5]
          k = 6
      
          while frame_lst[i]== frame_lst[i+k]:
             #print('k: ',k)
             i_list.append(i+k)
             k += 1
          i= i+k-1
      
          #print('eureka') #lol
      
          for j in i_list: 
             bad_data_history.append(frame_lst[j])
             #print('j:', j)
             frame_lst[j] = 0

       i += 1
      


    #print(frame_lst)
    #print(data)
    n_lst = []
    for n in range(len(frame_lst)):
       if frame_lst[n] == 0:
          n_lst.append(n)

    data_new = np.delete(data, n_lst,0)

    np.savetxt("refiltered_data/" + filename, data_new, delimiter=",")

    #print(data_new)
    print(bad_data_history)

for filename in os.listdir("filtered_data"):
    if "MC" in filename:
        print(filename)
        filter(filename)








