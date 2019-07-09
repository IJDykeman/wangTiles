import numpy as np
from helpers import *
from constants import *
from vox_import import *
from os import listdir
from os.path import isfile, join
from tile_properties import TileProperties
import re

def get_tile(path, v=False, ignore_rotations=False):
    solids, material_ids = import_vox(path)
    tile = np.array([[[0]*TILE_WIDTH]*TILE_WIDTH]*TILE_WIDTH)
    for i, b in enumerate(solids):
        tile[b] = material_ids[i]

    prior = 1.0
    path = path.replace(":","")
    p = re.compile("prior:?\d*\.?\d*")
    # if v: print (path)
    if len(p.findall(path)) > 0:
        prior = float(p.findall(path)[0].split("prior")[1])
        if v: print ("  ", prior)
    result = [tile]
    tile_properties = [TileProperties(is_air = 'air' in path.lower(), name = path.split("/")[-1].split(".vox")[0])]
    priors = [prior]
    if not "norotation" in path and not ignore_rotations:
        axes = (0,2)            
        result.append(np.rot90(tile, axes=axes))
        result.append(np.rot90(np.rot90(tile, axes=axes), axes=axes))
        result.append(np.rot90(np.rot90(np.rot90(tile, axes=axes), axes=axes), axes=axes))
        tile_properties = tile_properties * 4
        priors = priors * 4
    return result, tile_properties, priors


def get_tiles(v = False, ignore_rotations=False):
    onlyfiles = sorted([join(VOX_PATH, f) for f in listdir(VOX_PATH) if isfile(join(VOX_PATH, f))])
    result = []
    tile_properties = []
    priors = []
    for f in onlyfiles:
        try:
            new_tiles, new_tile_properties, new_priors = get_tile(f, v = v, ignore_rotations=ignore_rotations)
            result.extend(new_tiles)
            tile_properties.extend(new_tile_properties)
            priors.extend(new_priors)
        except:
            print ("  error processing", f)
            pass

    return result, tile_properties, priors
