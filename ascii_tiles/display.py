import numpy as np

def draw_world(world, tiles):
    chars = np.array([[" "] * 3 *world.shape[1]] * 3 * world.shape[0])
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            t = tiles[world[i,j]]
            chars[i*3: i*3+3, j*3:j*3+3] = t
    chars = list(map(list, chars))
    for i in range(len(chars)):
        print " ".join(chars[i])


def show_tiles(tiles):
    for i in range(len(tiles)):
        print
        print i
        print tiles[i]
