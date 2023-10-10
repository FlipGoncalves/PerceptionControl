import random

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

#measurements = ['green']                                        # test 1
#motions is a list of 2d lists. each 2d list represents first movement in x (columns in colors) then in y (lines in colors)
#motions = [[1,0]]                                               # test 1
measurements = ['green', 'red', 'red' ,'green', 'red','red']    # test 2
motions = [[1,0],[0,0],[0,1],[0,1],[-1,0],[0,0]]                # test 2

sensor_right = {}
sensor_right['green'] = 0.8
sensor_right['red'] = 0.7

p_move = 1.0

def show(p):
    for i in range(len(p)):
        print(p[i])

def sense(p, Z):
    """Update belief array p according to new measurement Z"""

    # weights
    w = [[sensor_right[colors[i]] if Z == sensor_right[colors[i]] else 1 - sensor_right[colors[i]] for i in j] for j in p]

    # resampling
    particles = random.choices(p, w, k=len(p))
    return sorted(particles)


def move(p, U):
    """Update p after movement U"""

    if sum(U) == 0:
        return p


    #### ERRADO BUT CBA


    # weights
    w = [[(1-p_move)+(p_move*(j.count(i-U[0])/len(j)))+(p_move*(j.count(i-U[1])/len(j))) for i in j] for j in p]

    # resampling
    particles = random.choices(p, w, k=len(p))
    return sorted(particles)

#main

height = len(colors)
width  = len(colors[0])

n = height * width

num_particles = 400
p = [[int(i//(num_particles/len(colors[0]))) for i in range(num_particles)] for i in range(len(colors))]
print(p)

for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    show(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    show(p)


