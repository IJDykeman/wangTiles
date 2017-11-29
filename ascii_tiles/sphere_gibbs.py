import numpy as np
import time

from extract_tiles import *
from potentials import *
from create_sphere import *
from display import *
from constants import *
import random


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

def sphere_probability(i,j, world):
    p = np.ones_like(spheres[0,0,0])
    for ni, nj in spherehood(i,j):
        p += spheres[world[ni, nj], i-ni, j-nj, :] * decided[ni,nj]
    return p / np.sum(p)


def place(i, j, tile_index):
    # print spheres[tile_index].shape
    # print max(0, i - SPHERE_WIDTH / 2), min(WORLD_WIDTH, i + SPHERE_WIDTH / 2 + 1)
    # print max(0, j - SPHERE_WIDTH / 2), min(WORLD_WIDTH, j + SPHERE_WIDTH / 2 + 1)
    # print probmap[max(0, i - SPHERE_WIDTH / 2): min(WORLD_WIDTH, i + SPHERE_WIDTH / 2 + 1),
    #               max(0, j - SPHERE_WIDTH / 2): min(WORLD_WIDTH, j + SPHERE_WIDTH / 2 + 1)].shape

    probmap[max(0, i - SPHERE_WIDTH / 2): min(WORLD_WIDTH, i + SPHERE_WIDTH / 2 + 1),
            max(0, j - SPHERE_WIDTH / 2): min(WORLD_WIDTH, j + SPHERE_WIDTH / 2 + 1)]\
        *= spheres[tile_index][0]
    world[i,j] = tile_index


def p(i, j, t):
    p = 1.0
    for i2, j2 in neighbors(i,j):
        p *= potential(t, tiles[world[i2, j2]], i2-1, j2-j)
    return p

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
tile_index_to_prior = np.ones(len(tiles)) / len(tiles)

show_tiles(tiles)
spheres = create_spheres(tiles)
print spheres.shape
print spheres[0,:,:,0]
print spheres[0,:,:,1]

print "===="
print spheres[1,:,:,0]
print spheres[1,:,:,1]
# print spheres[1]

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

for step, (i,j) in enumerate(grid_bfs(WORLD_WIDTH / 2, WORLD_WIDTH / 2, WORLD_WIDTH)):
    if step % 10 == 0:
        print 
        print
        draw_world(world, tiles)
        time.sleep(.1)
        # logp(world)
    decided[i,j] = 1
    ts, ps = get_tiles_and_probs(i,j,tiles, p)
    place(i,j, np.random.choice(ts, 1, p=np.array(ps)))

# grid_bfs(starti, startj, width)


