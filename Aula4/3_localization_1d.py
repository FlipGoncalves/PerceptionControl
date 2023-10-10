import random

colors = ['red', 'green', 'green', 'red' , 'red']

#measurements = ['green']                                            # test 1
#motions = [[1]]                                                     # test 1
measurements = ['green', 'green', 'green' ,'green', 'green','red']  # test 2
motions = [[1],[0],[-1],[1],[1],[0]]                                # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8

p_move = 0.8

def sense(p, Z):
    """Update belief array p according to new measurement Z"""

    # weights
    w = [sensor_right[colors[i]] if Z == sensor_right[colors[i]] else 1 - sensor_right[colors[i]] for i in p]

    # resampling
    particles = random.choices(p, w, k=len(p))
    return sorted(particles)


def move(p, U):
    """Update p after movement U"""

    if U[0] == 0:
        return p

    # weights
    w = [(1-p_move)+(p_move*(p.count(i-U[0])/len(p))) for i in p]

    # resampling
    particles = random.choices(p, w, k=len(p))
    return sorted(particles)

#main
num_particles = 100
p = [int(i//(num_particles/len(colors))) for i in range(num_particles)]

width  = len(colors)
n = width

for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    print(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    print(p)


