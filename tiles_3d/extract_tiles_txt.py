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


def get_tiles(v = False):
    tile_file_content = get_lines("tiles7.txt")
    char_grid = np.array(tile_file_content)
    result = []
    for i in range(char_grid.shape[0] / 4 + 1):
        for j in range(char_grid.shape[1] / 12 + 1):
            data = char_grid[i*TILE_CONTENT_HEIGHT:i*TILE_CONTENT_HEIGHT + TILE_CONTENT_HEIGHT,
                             j*TILE_CONTENT_WIDTH:j*TILE_CONTENT_WIDTH + TILE_CONTENT_WIDTH]
            print data.shape

            if data.shape == (4,12):
                if v: print data[1,-1]
                tiles = [np.array([data[:-1,:3], data[:-1,4:7], data[:-1,8:11]]).transpose(2,0,1)]
                if np.all([x != ' ' for x in list(tiles[0].flatten())]):
                    if not data[1,-1]=="#":
                        if data[2,-1]=="f" or data[2,-1]=="F" or data[2,-1]=="m" or data[2,-1]=="M":
                            tile_flipped = tiles[0][:,::-1,:]
                            tiles.append(tile_flipped)
                        if data[0,-1]=="*":
                            if v: print "rotated"
                            tiles_old = tiles[:]
                            for tile in tiles_old:
                                axes = (0,2)
                                tiles.append(np.rot90(tile, axes=axes))
                                tiles.append(np.rot90(np.rot90(tile, axes=axes), axes=axes))
                                tiles.append(np.rot90(np.rot90(np.rot90(tile, axes=axes), axes=axes), axes=axes))
                        try:
                            for i in range(int(data[3,0])):
                                result.extend(tiles)
                        except:
                            result.extend(tiles)
                    else:
                        if v: print "commented"
                    if v: print
    return result

