import numpy as np
import time

from extract_tiles import *
from potentials import *
from create_sphere import *
from display import *
from constants import *
import random

# np.random.seed(0)

spherehood_relative_array = []
for i in range(SPHERE_WIDTH):
    for j in range(SPHERE_WIDTH):
        loc = (i - SPHERE_WIDTH / 2, j - SPHERE_WIDTH / 2)
        if loc != (0, 0):
            spherehood_relative_array.append(loc)
spherehood_relative_array = np.array(spherehood_relative_array)

def spherehood(i,j):
    hood = spherehood_relative_array + np.array([i,j])
    condition = np.logical_and(
                np.logical_and(hood[:,0] >= 0,
                hood[:,1] >= 0),
                np.logical_and(
                hood[:,0] < SPHERE_WIDTH,
                hood[:,1] < SPHERE_WIDTH))
    return hood[condition]

def sphere_probability(i,j):
    p = np.ones_like(spheres[0,0,0])
    for ni, nj in spherehood(i,j):
        p *= spheres[world[ni, nj], i-ni, j-nj, :] * decided[ni,nj] 
    return (p / (np.sum(p)))
    # return np.ones_like(p) / len(tiles)


def place(i, j, tile_index):
    print "  placing", tile_index, "at", i,j
    decided[i,j] = 1
    global probmap
    print "probmap, i, j", probmap[WORLD_WIDTH / 2,WORLD_WIDTH / 2-1]
    print probmap[max(0, i - SPHERE_WIDTH / 2): min(WORLD_WIDTH, i + SPHERE_WIDTH / 2 + 1),
            max(0, j - SPHERE_WIDTH / 2): min(WORLD_WIDTH, j + SPHERE_WIDTH / 2 + 1)].shape

    print spheres[tile_index,
                   max(0, -(i-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH),
                   max(0, -(j-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH)].shape


    probmap[max(0, i - SPHERE_WIDTH / 2): min(WORLD_WIDTH, i + SPHERE_WIDTH / 2 + 1),
            max(0, j - SPHERE_WIDTH / 2): min(WORLD_WIDTH, j + SPHERE_WIDTH / 2 + 1)]\
        *= spheres[tile_index,
                   max(0, -(i-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH),
                   max(0, -(j-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH)]



    print "probmap, i, j", probmap[WORLD_WIDTH / 2,WORLD_WIDTH / 2-1]
    print "sphere is"
    print spheres[tile_index,
                   max(0, -(i-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH),
                   max(0, -(j-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH)].shape
    for k in range(len(tiles)):
        print k
        print spheres[tile_index,
                       max(0, -(i-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH),
                       max(0, -(j-SPHERE_WIDTH / 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH / 2 + 1 - WORLD_WIDTH), k]
    # print "  range", i - SPHERE_WIDTH / 2, i + SPHERE_WIDTH / 2 + 1
    # probmap[i - SPHERE_WIDTH / 2: i + SPHERE_WIDTH / 2 + 1,
    #         j - SPHERE_WIDTH / 2: j + SPHERE_WIDTH / 2 + 1]\
    #     *= spheres[tile_index, :, :]
    probmap /= np.sum(probmap, axis = -1).reshape(WORLD_WIDTH, WORLD_WIDTH, 1)
    world[i,j] = tile_index
    # quit()


def get_all_valid(i,j):
    result = []
    for t in range(len(tiles)):
        ismatch = True
        for ni, nj in neighbors(i,j):
            ismatch = ismatch and match(tiles[t], tiles[world[ni,nj]], ni - i, nj - j)
        if ismatch:
            result.append(t)
    return result


            # else:
            #     world[i,j] = random.choice(tiles)



def logp(world):
    logp = 0
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            logp += np.log(p(i,j,tiles[world[i,j]]))
    print logp





tile_file_content = get_lines("tiles.txt")
tile_file_content = np.array(tile_file_content)


print "===="
tiles = get_tiles(tile_file_content)
# random.shuffle(tiles)
tile_index_to_prior = np.ones(len(tiles)) / len(tiles)

show_tiles(tiles)
# quit()
spheres = create_spheres(tiles)

print "===SPHERES===="
print spheres.shape
print spheres[0,:,:,0]
print spheres[0,:,:,1]

print "===="
print spheres[1,:,:,0]
print spheres[1,:,:,1]

# show_tiles()
# print potential(tiles[1], tiles[1], 1,0)
# print potential(tiles[1], tiles[1], 0,1)
# print potential(tiles[0], tiles[1], 1,0)
# print potential(tiles[0], tiles[1], 0,1)
# quit()

world = np.zeros((WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)
probmap = np.ones((WORLD_WIDTH,WORLD_WIDTH, len(tiles))).astype(np.float32)
decided = np.zeros((WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)


all_coords = []

for i in range(world.shape[0]):
    for j in range(world.shape[1]):
        all_coords.append((i,j))

def report_on_probmap_location(i,j):
    print "=================================="
    print "reporting information about probmap at", i, j
    for tile, p in zip(tiles, probmap[i,j]):
        print tile
        print p
        print
    print "=================================="

def report_on_sphere(i):
    print "=================================="
    print "reporting information about tile", i
    print tiles[i]
    for t2 in range(len(tiles)):
        print "transition to", t2
        print tiles[t2]
        print spheres[i, :,:, t2]

    print "=================================="

# place(2,2, 1)
place(WORLD_WIDTH / 2,WORLD_WIDTH / 2, 4)
draw_world(world, tiles, mask = decided)
report_on_sphere(4)
# print probmap[WORLD_WIDTH / 2,WORLD_WIDTH / 2 - 1]
report_on_probmap_location(WORLD_WIDTH / 2,WORLD_WIDTH / 2 - 1)
# quit()
print "=======START GENERATION=========="

step=0
while np.prod(decided.shape) - np.sum(decided) > 0:
    print " ============= starting step", step, "==============="
    step += 1
    entropy = np.exp(-np.sum((probmap * np.exp(probmap)) * (probmap > 0) * (decided == 0).reshape(WORLD_WIDTH,WORLD_WIDTH,1), axis = -1))
    # entropy /= np.sum(entropy)
    entropy += (decided == 1) * np.max(entropy)
    # print "min", np.min(entropy)
    entropy_argmin = np.unravel_index(np.argmin(entropy), entropy.shape)
    i,j = entropy_argmin
    # i,j = WORLD_WIDTH / 2 -1, WORLD_WIDTH / 2
    report_on_probmap_location(i,j)

    # print "probs"
    # print probmap[:,:,0]
    # print ""
    # print probmap[:,:,1]
    print "entropy"
    print entropy
    print "argmin", i,j
    print "world"
    print world
    
    ts, ps = range(len(tiles)), probmap[i,j]#sphere_probability(i,j)
    print "ps", ps
    to_place = np.random.choice(ts, 1, p=np.array(ps))[0]
    print "placing", to_place, "at", i,j
    place(i,j, to_place)


    draw_world(world, tiles, mask = decided)
    time.sleep(.2)
    # quit()

draw_world(world, tiles)

show_tiles(tiles)

