import os

for i in range(2):
    for j in range(12):
        person = j + 1
        if person < 10:
            person = "0" + str(person)
        person = str(person)
        os.mkdir("results/MC" + str(i + 1) + "_S" + person)