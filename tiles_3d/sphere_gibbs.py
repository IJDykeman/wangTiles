import numpy as np
import time
from pyvox.models import Vox
from pyvox.writer import VoxWriter
# from qubicle import Qb, QbMatrix

from extract_tiles_vox import *
from potentials import *
from create_sphere import *
from display import *
from constants import *

import random


# np.random.seed(0)
fixup_budget = 100

def get_slice_around(i, j, l, width):
    a = slice(max(0, i - width // 2), min(WORLD_WIDTH, i + width // 2 + 1))
    b = slice(max(0, j - width // 2), min(WORLD_WIDTH, j + width // 2 + 1))
    c = slice(max(0, l - width // 2), min(WORLD_WIDTH, l + width // 2 + 1))
    return (a, b, c)


# @profile
def get_entropy(probmap, decided):
    decided_deep = decided.reshape(decided.shape[0], decided.shape[1], -1, 1)
    entropy = np.sum((probmap > 0).astype(np.int32) * (decided_deep == 0)\
            .reshape(decided.shape[0],decided.shape[1],decided.shape[2],1), axis = -1)

    entropy += (decided == 1) * 200000#np.max(entropy)
    return entropy


# @profile
def update_entropy_around(i, j, l):
    global probmap
    global entropy
    sphere_slice = get_slice_around(i,j,l,SPHERE_WIDTH)
    entropy[sphere_slice] = get_entropy(probmap[sphere_slice], decided[sphere_slice])


def normalize_probmap_around(i, j, l):
    global probmap
    sphere_slice = get_slice_around(i,j,l,SPHERE_WIDTH)
    p = probmap[sphere_slice]
    s = np.sum(p, axis = -1)
    p[s==0,:]=1
    probmap[sphere_slice] = p


def is_valid_around(i, j, l):
    global probmap
    p = probmap[sphere_slice(i,j,l,SPHERE_WIDTH)]
    s = np.sum(p, axis = -1)
    return len(np.where(s==0)[0]) == 0

# @profile
def place(i, j, l, tile_index):
    sphere_slice = get_slice_around(i,j,l,SPHERE_WIDTH)
    global probmap
    sphere = spheres[tile_index]
    old_p = probmap[sphere_slice].copy()
    probmap[sphere_slice] *= sphere[
                   max(0, -(i-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH),
                   max(0, -(j-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH),
                   max(0, -(l-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, l + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH)]
    
    normalize_probmap_around(i, j, l)
    update_entropy_around(i, j, l)

    decided[i,j,l] = 1
    world[i,j, l] = tile_index


def forget(i, j, l):
    global probmap
    s = spheres[world[i,j, l],
                   max(0, -(i-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, i + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH),
                   max(0, -(j-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, j + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH),
                   max(0, -(l-SPHERE_WIDTH // 2)) : SPHERE_WIDTH - max(0, l + SPHERE_WIDTH // 2 + 1 - WORLD_WIDTH)]
    probmap[get_slice_around(i, j, l, SPHERE_WIDTH)] /= s + np.ones_like(s) * (s==0)
    normalize_probmap_around(i,j,l)
    update_entropy_around(i, j,l)


def is_valid(i,j,l):
    for ni, nj, nl in neighbors(i,j,l):
        if decided[ni, nj, nl] == 1:
            ismatch = match(tiles[world[i,j,l]], tiles[world[ni,nj,nl]], ni - i, nj - j, nl - l)
            if not ismatch:
                return False
    return True



def report_on_probmap_location(i,j):
    print ( "==================================")
    print ( "reporting information about probmap at", i, j)
    for tile, p in zip(tiles, probmap[i,j]):
        print ( tile)
        print ( p)
        print ()
    print ( "==================================")


tiles, tile_properties, tile_priors = get_tiles()
print (tile_priors)


tile_index_to_prior = np.ones(len(tiles)) / len(tiles)
build_transition_matrices(tiles)

t1 = time.time()
spheres = create_spheres(tiles)
print (time.time() - t1, "to build tiles")



def get_air_index():
    for i, props in enumerate(tile_properties):
        if props.name[:3] =="air":
            return i
    assert False, "you must have a tile namex air*.vox"

def get_dirt_index():
    for i, props in enumerate(tile_properties):
        if props.name[:4] == "dirt":
            return i
    assert False, "you must have a tile namex dirt*.vox"


# @profile
def place_a_tile():
    # if RANDOM_TIE_BREAKING:
    entropy_argmin = np.unravel_index(np.argmin(entropy  + np.random.normal(size=entropy.shape, scale = .00001)), entropy.shape)
    # else:
        # entropy_argmin = np.unravel_index(np.argmin(entropy), entropy.shape)

    i,j,l= entropy_argmin
    # print i
    ts, ps = range(len(tiles)), probmap[i,j,l]
    probs = np.array(tile_priors) * np.array(ps)
    to_place = np.random.choice(ts, 1, p=np.array(probs) / np.sum(probs))[0]
    place(i,j,l, to_place)

# @profile
def generate_world():

    if SURROUND_BY_AIR:
        air_index = get_air_index()
        for i in range(WORLD_WIDTH):
            for j in range(WORLD_WIDTH):
                for l in range(WORLD_WIDTH):
                    if (i == 0 or i == WORLD_WIDTH-1
                        or j == 0 or j == WORLD_WIDTH-1
                        or l == 0 or l == WORLD_WIDTH-1):
                            place(i, j, l, air_index)

    if AIR_ON_TOP:
        air_index = get_air_index()
        for i in range(WORLD_WIDTH):
            for j in range(WORLD_WIDTH):
                for l in range(WORLD_WIDTH-1,WORLD_WIDTH):
                    if (i == 0 or i == WORLD_WIDTH-1
                        or j == 0 or j == WORLD_WIDTH-1
                        or l == 0 or l == WORLD_WIDTH-1):
                            place(i, j, l, air_index)
    if DIRT_ON_BOTTOM:
        dirt_index = get_dirt_index()
        for i in range(WORLD_WIDTH):
            for l in range(WORLD_WIDTH):
                for j in range(0,1):
                    if (i == 0 or i == WORLD_WIDTH-1
                        or j == 0 or j == WORLD_WIDTH-1
                        or l == 0 or l == WORLD_WIDTH-1):
                            place(i, j, l, dirt_index)

    step=0
    while np.prod(decided.shape) - np.sum(decided) > 0:
        step += 1
        place_a_tile()

N_TRIALS = 1
invalid_locations_record = []
for i in range(N_TRIALS):
    
    world = np.zeros((WORLD_WIDTH,WORLD_WIDTH, WORLD_WIDTH)).astype(np.int32)
    probmap = np.ones((WORLD_WIDTH,WORLD_WIDTH, WORLD_WIDTH, len(tiles))).astype(np.float32)
    decided = np.zeros((WORLD_WIDTH,WORLD_WIDTH, WORLD_WIDTH)).astype(np.int32)
    entropy = np.ones((WORLD_WIDTH,WORLD_WIDTH, WORLD_WIDTH)) * 1000000
    t1 = time.time()
    generate_world()
    t2 = time.time()
    print (t2-t1, "seconds")
    invalid_locations = 0

    for i in range(0, WORLD_WIDTH):
        for j in range(0, WORLD_WIDTH):
            for l in range(0, WORLD_WIDTH):
                if not is_valid(i,j,l):
                    invalid_locations += 1

    print( invalid_locations, "locations invalid")
    invalid_locations_record.append(invalid_locations)


print( "mean locations invalid", np.mean(invalid_locations_record))



worldchars = np.zeros([WORLD_WIDTH*TILE_WIDTH]*3).astype(np.int32)
stride = TILE_WIDTH-1
REMOVE_EDGE_WIDTH = 0
for i in range(REMOVE_EDGE_WIDTH, WORLD_WIDTH-REMOVE_EDGE_WIDTH):
    for j in range(REMOVE_EDGE_WIDTH, WORLD_WIDTH-REMOVE_EDGE_WIDTH):
        for l in range(REMOVE_EDGE_WIDTH, WORLD_WIDTH-REMOVE_EDGE_WIDTH):
            if COLOR_INVALID_TILES:
                if not is_valid(i,WORLD_WIDTH-j-1,l):
                    worldchars[i*stride:i*stride+TILE_WIDTH,j*stride:j*stride+TILE_WIDTH,l*stride:l*stride+TILE_WIDTH]\
                         = (tiles[world[i,WORLD_WIDTH-j-1,l]][:,::-1,:]>0) * (tiles[world[i,WORLD_WIDTH-j-1,l]][:,::-1,:] + 50)%255

            if not tile_properties[world[i,WORLD_WIDTH-j-1,l]].is_air:
                worldchars[i*stride:i*stride+TILE_WIDTH,j*stride:j*stride+TILE_WIDTH,l*stride:l*stride+TILE_WIDTH] \
                     = tiles[world[i,WORLD_WIDTH-j-1,l]][:,::-1,:]
            else:
                worldchars[i*stride:i*stride+TILE_WIDTH,j*stride:j*stride+TILE_WIDTH,l*stride:l*stride+TILE_WIDTH] = 0

# with open('/Users/idykeman/Documents/comp460/example.qb', 'wb') as file:
#     qb = Qb()
#     layer = QbMatrix("main", worldchars + 0xFFFFFF, (0, 0, 0)) # Matrix name, data as 3-dimensional array, position of matrix
#     qb.matrixList.append(layer)
#     qb.save(file)

a = (worldchars).astype(np.int32)
# print( np.mean(a))
vox = Vox.from_dense(a)
VoxWriter('test.vox', vox).write()
print (a.shape)
print( ".vox output written")

