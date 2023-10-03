colors = ['red', 'green', 'green', 'red' , 'red']

#measurements = ['green']                                       # test 1
measurements = ['green', 'green', 'green' ,'green', 'green']   # test 2

sensor_right = {}
sensor_right['green'] = 0.6
sensor_right['red'] = 0.8

def sense(p, Z):
    """Update belief array p according to new measurement Z"""

    cells = list(set(colors))
    cells.remove(Z)

    for i in range(len(p)):
        if Z == colors[i]:
            p[i] *= sensor_right[Z]
        else:
            p[i] *= (1 - sensor_right[cells[0]])

    # return if already normalized
    if sum(p) == 1:
        return p

    # normalize
    return [round(x / sum(p), 4) for x in p]

#main
p = [0.2, 0.2, 0.2, 0.2, 0.2]

width  = len(colors)
n = width

for s in range(len(measurements)):
    p = sense(p,measurements[s])

print(p)