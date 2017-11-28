import numpy as np
import random
WORLD_WIDTH = 64

world = np.zeros((WORLD_WIDTH, WORLD_WIDTH)) - 1
permanent = np.zeros_like(world)


UNDEFINED = -1
WATER = 1
GRASS = 2
HILL = 3
SAND = 4
WALL = 5
FLOOR = 6
ROAD = 7
TREE = 8
BRIDGE = 9

TYPES = [WATER, GRASS, HILL, SAND, WALL, FLOOR, ROAD, TREE, BRIDGE]

UNSAMPLABLE = [BRIDGE, ROAD, WALL]

NUM_TYPES = len(TYPES)


def prRed(prt): return ("\033[91m\033[01m{}\033[00m" .format(prt))
def prGreen(prt): return ("\033[92m\033[01m{}\033[00m" .format(prt))
def prYellow(prt): return ("\033[93m\033[01m{}\033[00m" .format(prt))
def prLightPurple(prt): return ("\033[94m\033[01m{}\033[00m" .format(prt))
def prPurple(prt): return ("\033[95m\033[01m{}\033[00m" .format(prt))
def prCyan(prt): return ("\033[96m\033[01m{}\033[00m" .format(prt))
def prLightGray(prt): return ("\033[97m\033[01m{}\033[00m" .format(prt))
def prBlack(prt): return ("\033[98m\033[01m{}\033[00m" .format(prt))
def bgBlue(prt): return ("\033[44m\033[01m{}\033[00m" .format(prt))
def prDarkgrey(prt): return ("\033[90m\033[01m{}\033[00m" .format(prt))




strings = [' '] * (NUM_TYPES + 1)
strings[WATER] =   bgBlue(prLightPurple(' ~'))
strings[GRASS] =   prGreen(' "')
strings[HILL] =   prLightGray(' ^')
strings[SAND] =   prYellow(' `')
strings[WALL] =   prLightGray(' #')
strings[FLOOR] =   prLightGray(' ,')
strings[ROAD] =   prLightGray(' =')
strings[TREE] =   prGreen(' T')
strings[BRIDGE] =   prLightGray(' +')




pair_to_prob = {}

pair_to_prob[tuple(sorted([GRASS, GRASS]))] = 1.2
pair_to_prob[tuple(sorted([WATER, WATER]))] = 1.6
pair_to_prob[tuple(sorted([HILL, HILL]))] = 1

pair_to_prob[tuple(sorted([GRASS, HILL]))] = .7
pair_to_prob[tuple(sorted([GRASS, WATER]))] = .1
pair_to_prob[tuple(sorted([GRASS, WALL]))] = .2
pair_to_prob[tuple(sorted([WATER, WALL]))] = .001
pair_to_prob[tuple(sorted([GRASS, TREE]))] = .3

pair_to_prob[tuple(sorted([SAND, SAND]))] = .4
pair_to_prob[tuple(sorted([SAND, GRASS]))] = 0.5
pair_to_prob[tuple(sorted([SAND, WATER]))] = 0.7

pair_to_prob[tuple(sorted([WATER, HILL]))] = .05
pair_to_prob[tuple(sorted([WALL, HILL]))] = .05
pair_to_prob[tuple(sorted([SAND, HILL]))] = .05

# road surroundings
pair_to_prob[tuple(sorted([BRIDGE, WATER]))] = 3
pair_to_prob[tuple(sorted([ROAD, WATER]))] = 0
pair_to_prob[tuple(sorted([ROAD, SAND]))] = .005


neighbors = []
# for i in range(3):
#     for j in range(3):
#         neighbors.append([i-1, j-1])
# neighbors = np.array(neighbors)

neighbors = np.array([[-1,0], [1,0], [0,-1], [0,1]])

def get_parents(i, j):

    result = neighbors + np.array([i,j])
    condition = np.logical_and(
                np.logical_and(result[:,0] >= 0,
                result[:,1] >= 0),
                np.logical_and(
                result[:,0] < WORLD_WIDTH,
                result[:,1] < WORLD_WIDTH))
    result = result[condition]
    return result



def p(di, dj, x1, x2):
    '''
    p(x1 at i1, j1 | x2 at i2, j2)
    '''
    if x1 in UNSAMPLABLE:
        return 0.0

    if x2 == UNDEFINED:
        return 1. / NUM_TYPES
    pair = tuple(sorted([x1, x2]))

    if pair in pair_to_prob:
        return pair_to_prob[pair]
    return .01


def display(world):
    for i in range(WORLD_WIDTH):
        print "".join(map(lambda x: strings[int(x)], list(world[i])))


# all_coords = np.array(np.meshgrid(range(WORLD_WIDTH), range(WORLD_WIDTH))).T.reshape([-1, 2])
# block1_condition = np.logical_or(np.logical_and(all_coords[:, 0] % 2 == 0, all_coords[:, 1] % 2 == 0),
#                                  np.logical_and(all_coords[:, 0] % 2 == 1, all_coords[:, 1] % 2 == 1))
# block1 = all_coords[block1_condition]

# block2 = all_coords[np.logical_not(block1_condition)]



import time
def sample(i, j):
    probs = []
    for t in TYPES:
        prob = 1.0
        for i2,j2 in get_parents(i,j):
            prob *= p(i2 - i, j2 - j,t,world[i2,j2])
        probs.append(prob)
    s = sum(probs)
    for i in range(len(probs)):
        probs[i] /= s
    return np.random.choice(TYPES, 1, p = probs)


def set_permanent(i, j, t):
    permanent[i, j] = 1
    world[i, j] = t


def room(i,j,w):
    w = w + 1

    for k1 in range(w + 1):
        for k2 in range(w + 1):
            set_permanent(i + k1, j + k2, FLOOR)
    for k in range(w + 1):
        set_permanent(i + k, j,     WALL)
        set_permanent(i + k, j + w, WALL)
        set_permanent(i,     j + k, WALL)
        set_permanent(i + w, j + k, WALL)


room(7,7,4)
room(7,12,3)
room(19,31,5)

for i in range(8):
    set_permanent(9, 7 - i, ROAD)


for i in range(23):
    set_permanent(20, 9 + i, ROAD)
for i in range(9):
    set_permanent(12 + i, 9, ROAD)
for i in range(7):
    set_permanent(20, 14 + i, BRIDGE)


for i in range(500000):
    l = (random.choice(range(WORLD_WIDTH)), random.choice(range(WORLD_WIDTH)))
    if permanent[l] == 0:
        world[tuple(l)] = sample(*l)

    # for l in block1:
    #     world[tuple(l)] = sample(*l)
    # for l in block2:
    #     world[tuple(l)] = sample(*l)
    if i % WORLD_WIDTH ** 2 == 0:
        print "\n" * 5
        display(world)
print 
display(world)

