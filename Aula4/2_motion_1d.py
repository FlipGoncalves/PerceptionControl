import random

colors = ['red', 'green', 'green', 'red' , 'red']

#motions = [[1]]                      # test 1
motions = [[1],[0],[-1],[1],[0]]     # test 2

p_move = 0.8

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

for s in range(len(motions)):
    p = move(p,motions[s])

print(p)

