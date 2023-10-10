import random

colors = ['red', 'green', 'green', 'red' , 'red']

#measurements = ['green']                                       # test 1
measurements = ['green', 'green', 'green' ,'green', 'green']   # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8

def sense(p, Z):
    """Update belief array p according to new measurement Z"""

    # weights
    w = [sensor_right[colors[i]] if Z == sensor_right[colors[i]] else 1 - sensor_right[colors[i]] for i in p]

    # resampling
    particles = random.choices(p, w, k=len(p))
    return sorted(particles)

#main
num_particles = 100
p = [int(i//(num_particles/len(colors))) for i in range(num_particles)]

width  = len(colors)
n = width

for s in range(len(measurements)):
    p = sense(p,measurements[s])

print(p)