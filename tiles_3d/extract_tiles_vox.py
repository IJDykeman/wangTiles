import numpy as np
from helpers import *
from constants import *
from vox_import import *
from os import listdir
from os.path import isfile, join


def get_tile(path):
    solids = import_vox(path)
    tile = np.array([[[' ']*TILE_WIDTH]*TILE_WIDTH]*TILE_WIDTH)
    for b in solids:
        tile[b] = "#"


    result = [tile]
    for i in range(4):
        axes = (0,2)
        result.append(np.rot90(tile, axes=axes))
        result.append(np.rot90(np.rot90(tile, axes=axes), axes=axes))
        result.append(np.rot90(np.rot90(np.rot90(tile, axes=axes), axes=axes), axes=axes))
    return result

def get_tiles(v = False):
    mypath = "/home/isaac/Desktop/comp460/tiles_biased_towers_3/"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    result = []
    for f in onlyfiles:
        result.extend(get_tile(f))

    # for i in range(1):
    #     result.extend(get_tile("/home/isaac/Desktop/comp460/tiles/boxWithHall_stairBottom.vox"))
    #     result.extend(get_tile("/home/isaac/Desktop/comp460/tiles/boxWithHall_stairTop.vox"))
        # result.append(get_tile("/home/isaac/Desktop/comp460/tiles/boxWithHall_4way.vox"))
        # result.append(get_tile("/home/isaac/Desktop/comp460/tiles/boxWithHall_solid.vox"))
        

    return result
