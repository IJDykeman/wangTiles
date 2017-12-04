import numpy as np
from helpers import *
from constants import *


# NORTH = 0
# SOUTH = 1
# EAST = 2
# WEST = 3

def get_lines(fname, v = False):
    with open(fname) as f:
        tile_file_content = f.readlines()
    # grid_height = len(tile_file_content)
    grid_width = np.max(map(len, tile_file_content))
    for i, l in enumerate(tile_file_content):
        tile_file_content[i] = tile_file_content[i].replace("\n", "")
        tile_file_content[i] = tile_file_content[i] + " " * (grid_width - len(tile_file_content[i])) 
        tile_file_content[i] = np.array(list(tile_file_content[i]))
        if v: print tile_file_content[i].shape
    return tile_file_content


def get_tiles(char_grid, v = False):
    result = []
    for i in range(char_grid.shape[0] / 4 + 1):
        for j in range(char_grid.shape[0] / 4 + 1):
            data = char_grid[i*TILE_CONTENT_WIDTH:i*TILE_CONTENT_WIDTH + TILE_CONTENT_WIDTH,
                             j*TILE_CONTENT_WIDTH:j*TILE_CONTENT_WIDTH + TILE_CONTENT_WIDTH]
            # print data

            if data.shape == (4,4):
                if v: print data[1,-1]
                tile = data[:-1,:-1]
                if np.all([x != ' ' for x in list(tile.flatten())]):
                    if not data[1,-1]=="#":
                        if data[0,-1]=="*":
                            if v: print "rotated"
                            result.append(np.rot90(tile))
                            result.append(np.rot90(np.rot90(tile)))
                            result.append(np.rot90(np.rot90(np.rot90(tile))))
                        result.append(tile)
                        if v: print "added"
                    else:
                        if v: print "commented"
                    if v: print
    return result
