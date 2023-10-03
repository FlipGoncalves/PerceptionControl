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

    cells = list(set(sensor_right.keys()))
    cells.remove(Z)

    for i in range(height):
        for j in range(width):
            if Z == colors[i][j]:
                p[i][j] *= sensor_right[Z]
            else:
                p[i][j] *= (1 - sensor_right[cells[0]])

    # return if already normalized
    if sum([sum(x) for x in p]) == 1:
        return p

    # normalize
    return [[round(y / sum([sum(z) for z in p]), 4) for y in x] for x in p]

def move(p, U):
    """Update p after movement U"""

    if sum(U) == 0:
        return p
    
    temp = []
    for i in range(height):
        temp_2 = []
        for j in range(width):
            
            t = p[i][j] * (1-p_move)
            if U[0] == 0:
                t += p[(i-U[0])%len(p)][j] * p_move
            else:
                t += p[i][(j-U[0])%len(p[0])] * p_move
                
            temp_2.append(round(t, 4))

        temp.append(temp_2)
    
    return [[round(y / sum([sum(z) for z in temp]), 4) for y in x] for x in temp]

#main

height = len(colors)
width  = len(colors[0])

n = height * width

p = []
for l in range(height):
    q=[]
    for c in range(width):
        q.append(1./n)
    p.append(q)

for s in range(len(measurements)):
    print("sense ",measurements[s])
    p = sense(p,measurements[s])
    show(p)
    print("move ", motions[s])
    p = move(p,motions[s])
    show(p)


