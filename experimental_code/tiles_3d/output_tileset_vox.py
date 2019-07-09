import numpy as np

from constants import *
from extract_tiles_vox import *
from pyvox.models import Vox

from pyvox.writer import VoxWriter


tiles, tile_properties, tile_priors = get_tiles(v=True, ignore_rotations=True)

# for t in tile_properties:
#   print t.is_air
print len(tiles), "tiles"

padding = 7

tile_footprint_width= TILE_WIDTH + padding
world_width = int(100.0 / tile_footprint_width)
# assert (len(tiles) < world_width

i = 0
world = np.zeros((world_width,world_width, world_width)).astype(np.int32)

# output = 
for x in range(world_width):
    for y in range(world_width):
        for z in range(world_width):
            if i >= len(tiles):
                    break
            if x%2==0 and y%2==0 and  z%2==0:
                print x,y,z
                world[y,x,z] = i
                i+=1

assert i == len(tiles)
print "done placing"


worldchars = np.zeros([world_width*TILE_WIDTH]*3).astype(np.int32)
stride = TILE_WIDTH
for i in range(0, world_width-0):
    for j in range(0, world_width-0):
        for l in range(0, world_width-0):
            if not tile_properties[world[i,j,l]].is_air:
            # if not world[i,j,l] != 0:
                worldchars[i*stride:i*stride+TILE_WIDTH,j*stride:j*stride+TILE_WIDTH,l*stride:l*stride+TILE_WIDTH] \
                     = tiles[world[i,j,l]]
            else:
                worldchars[i*stride:i*stride+TILE_WIDTH,j*stride:j*stride+TILE_WIDTH,l*stride:l*stride+TILE_WIDTH] = 0
                # print "air"


print "writing .vox output"
from pyvox.models import Vox
from pyvox.writer import VoxWriter
a = (worldchars).astype(np.int32)
vox = Vox.from_dense(a)
VoxWriter('tileset.vox', vox).write()
