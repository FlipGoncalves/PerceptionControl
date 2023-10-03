colors = ['red', 'green', 'green', 'red' , 'red']

#motions = [[1]]                      # test 1
motions = [[1],[0],[-1],[1],[0]]     # test 2

p_move = 0.8

def move(p, U):
    """Update p after movement U"""

    temp = []
    for i in range(len(p)):
        if U[0] == 0:
            break
        
        t = p[i]*(1-p_move) + p[(i-U[0])%len(p)] * p_move
            
        temp.append(round(t, 4))
    
    return temp if temp != [] else p

#main
p = [0.5, 0.5, 0, 0, 0]

width  = len(colors)
n = width

for s in range(len(motions)):
    p = move(p,motions[s])

print(p)

