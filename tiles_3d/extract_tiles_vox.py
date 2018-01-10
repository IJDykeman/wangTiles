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
    return tile

def get_tiles(v = False):
    mypath = "/home/isaac/Desktop/comp460/tiles/"
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    result = []
    for f in onlyfiles:
        result.append(get_tile(f))

    for i in range(10):
        result.append(get_tile("/home/isaac/Desktop/comp460/tiles/boxWithHall_stairBottom.vox"))

    return result
