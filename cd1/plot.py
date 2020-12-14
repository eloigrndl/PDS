import numpy as np
import matplotlib.pyplot as plt
from mpc_robot import MPC_Robot_model
import cicruit


#staight line
goal = (30,15)
if goal[0] != 0.0:
    m = goal[1]/goal[0]
else:
    m = 10000.0
"""
x = np.linspace(0.0, goal[0], num=40)
y = m * x
points = list(zip(x, y))
bounds = [-1, 35, -1, 20]
start_position = [0, 0, 0]
"""
"""
#line with sharp turn
x = np.arange(0,30, 1)
y = np.sin(x/3) * 3
points = list(zip(x,y))
start_position = [0, 0, 0]
bounds = [-1, 35, -4, 4]
"""
"""
#long turn line
x = np.arange(0,30, 1)
y = np.exp(x/10)
points = list(zip(x,y))
start_position = [0, 0, 0]
bounds = [-1, 35, -1, 25]
"""

#robot start in a different poition than the path
points = cicruit.CIRCUIT
bounds = [-2, 35, -8, 20]
start_position = [7, -5.69, 0]

def display_figure(points, position, bounds):

    plt.clf()
    plt.axis(bounds)
    plt.scatter(position[0], position[1], c=10, s=20, zorder=3)

    for i in range(len(points)):
        plt.scatter(points[i][0], points[i][1], zorder=1)
        if(i != 0):
            plt.plot([points[i-1][0], points[i][0]], [points[i-1][1], points[i][1]], 'ro-', zorder=1)
            #plt.pause(0.0005)


    plt.pause(0.001)


def plot_MPC(x0, points, bounds):

    mpc_module = MPC_Robot_model()
    final_pos = (points[len(points) - 1][0], points[len(points) - 1][1])
    current_pos = (x0[0], x0[1])

    #initialize path on MPC module 
    mpc_module.acquire_path(points.copy())

    #initialze records if wanted to be printed at the end of the algo.
    current_state = x0
    states = list(x0)
    u_vectors = [[0, 0]]
    dU_vectors = [[0, 0]]
    distance = mpc_module.calc_distance(final_pos, current_pos)
    mpc_module.set_state(current_state)


    #running it final goal is reached
    while(distance > 0.1):
        new_u = mpc_module.run_MPC()
        head = u_vectors[len(u_vectors) - 1]
        new_dU = (new_u[0] - head[0], new_u[1] - head[1])

        u_vectors.append(new_u)
        dU_vectors.append(new_dU)
        new_state = mpc_module.f_next_state(current_state, new_u)

        current_pos = (new_state[0], new_state[1])
        states.append(new_state)
        current_state = new_state
        mpc_module.set_state(current_state)
        mpc_module.shift_path()


        distance = mpc_module.calc_distance(final_pos, current_pos)
        display_figure(points, current_pos, bounds)


        #De-comment to see the updates
        print("\n NEW ITERATION : \n")
        print("Distance until final destination :", distance)
        print("New U vector : ", new_u)
        print("New DU vector : ", new_dU)
        print("New state :", new_state)



    #De-comment to see the records
    #print("States : ",states)
    #print("U_vectors : ", u_vectors)
    #print("dU_vectors : ", dU_vectors)

    return 0

plt.show()
display_figure(points, start_position, bounds)

plot_MPC(start_position, points, bounds)
while(1==1):
    x = 1