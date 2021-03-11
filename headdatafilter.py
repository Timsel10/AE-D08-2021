import numpy as np

#filename = 'S01_MC1_HeadMotion.csv'
filename = 'test.txt'

data = np.genfromtxt(filename, skip_header=1)
#print(data)
bad_data_history = [filename]
frame_lst = []

for i in range(len(data)):
   frame_lst.append(int(data[i][2]))

for i in range(len(frame_lst)):
   
   if frame_lst[i] == frame_lst[i+1] and frame_lst[i] == frame_lst[i+2] and frame_lst[i] == frame_lst[i+3] and frame_lst[i] == frame_lst[i+4] and frame_lst[i] == frame_lst[i+5]:
      i_list = [i+1,i+2,i+3,i+4,i+5]
      k = 6
      
      while frame_lst[i]== frame_lst[i+k]:
         print(k)
         i_list.append(i+k)
         k += 1
      i= i+k
      
      print('eureka')
      
      for j in i_list: 
         bad_data_history.append(frame_lst[j])
         print('j:', j)
         frame_lst[j] = 0

      if i >= len(frame_lst)-6:
         break
print(frame_lst)
print(data)
for n in range(len(frame_lst)):
    if frame_lst[n] == 0:
        data.remove[n]
print(data)
print(bad_data_history)








