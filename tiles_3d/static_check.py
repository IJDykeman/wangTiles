import numpy as np
import time

from extract_tiles_vox import *
from potentials import *
from create_sphere import *
from display import *
from constants import *
import random


tiles, tile_properties, tile_priors = get_tiles()
# random.shuffle(tiles)


tile_index_to_prior = np.ones(len(tiles)) / len(tiles)
build_transition_matrices(tiles)
import time
t1 = time.time()

spheres = create_spheres(tiles)
print (time.time() - t1, "to build tiles")

for sphere, props in zip(spheres, tile_properties):
	if np.sum(np.sum(sphere, axis=-1)==0) != 0:
		print (props.name, "has a zero entry in its sphere")

assert np.sum(np.sum(spheres, axis=-1)==0) == 0, "untileable tile set."


print ("All static checks passed.")