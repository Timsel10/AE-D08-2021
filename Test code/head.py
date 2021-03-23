import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import numpy as np
import os

headMotions = []

print("Data loading...")

for filename in os.listdir("filtered_data"):
    if "MC1" in filename:
        headMotions.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        print(filename)

for filename in os.listdir("filtered_data"):
    if "MC2" in filename:
        headMotions.append(np.genfromtxt("filtered_data/" + filename, delimiter = ","))
        print(filename)

for no, filtered in enumerate(headMotions):
    print("Number: " + str(no) + "; data length: " + str(len(filtered[:,0])))

    #headings = ["DUECA time","xdotdot","FrameSignature","Roll raw","Pitch raw","Yaw raw","X raw","Y raw","Z raw"]

    data = [filtered[:,6], filtered[:,7], filtered[:,8]] #X,Y,Z

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    ax.set_xlim3d([min(data[0]), max(data[0])])
    ax.set_xlabel('X')

    ax.set_ylim3d([min(data[1]), max(data[1])])
    ax.set_ylabel('Y')

    ax.set_zlim3d([min(data[2]), max(data[2])])
    ax.set_zlabel('Z')

    ax.set_title("3D Head Motion Plot of: " + str(no))
    plt.legend(str(no))

    ax.plot3D(data[0], data[1], data[2], 'gray')

    plt.title("3D Head Motion Plot of: " + str(no))

    plt.show()
    plt.clf()

    #def crappy_code(data) :
    #    lineData = np.empty((3, len(data[0])))
    #    for i in range(len(data[0])) :
    #        d3d = np.array([data[0][i], data[1][i], data[2][i]])
    #        lineData[:, i] = d3d

    #    return lineData

    #yeet = [crappy_code(data) for index in range(1)]

    ## NOTE: Cannot pass empty arrays into 3D version of plot()
    #lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in yeet]

    #def update_lines(num, dataLines, lines) :
    #    for line, data in zip(lines, dataLines) :
    #        # NOTE: there is no .set_data() for 3 dim data...
    #        line.set_data(data[0:2, :num])
    #        line.set_3d_properties(data[2,:num])
    #    return lines

    # Creating the Animation object
    #line_ani = animation.FuncAnimation(fig, update_lines, len(data[0]), fargs=(yeet, lines), interval=1, blit=False)

    #plt.show()
    #plt.clf()