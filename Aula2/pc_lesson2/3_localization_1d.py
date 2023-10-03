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


def move(p, U):
    """Update p after movement U"""

    if U[0] == 0:
        return p

    temp = []
    for i in range(len(p)):    
        t = p[i]*(1-p_move) + p[(i-U[0])%len(p)] * p_move
        temp.append(round(t, 4))
    
    return temp if temp != [] else p

#main
p = []

width  = len(colors)
n = width

for c in range(width):
    p.append(1./n)


for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    print(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    print(p)


