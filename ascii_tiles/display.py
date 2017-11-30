import numpy as np
from constants import *


def draw_world(world, tiles, mask = None):
    print "=" * WORLD_WIDTH * 3
    if mask == None:
        mask = np.ones_like(world)
    chars = np.array([[" "] * 3 *world.shape[1]] * 3 * world.shape[0])
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            if mask[i,j] == 1:
                t = tiles[world[i,j]]
                chars[i*3: i*3+3, j*3:j*3+3] = t
            else:
                chars[i*3: i*3+3, j*3:j*3+3] = np.array([list("   ")]*3)
    chars = list(map(list, chars))
    for i in range(len(chars)):
        print " ".join(chars[i])
    print "=" * WORLD_WIDTH * 3


def show_tiles(tiles):
    for i in range(len(tiles)):
        print
        print i
        print tiles[i]
