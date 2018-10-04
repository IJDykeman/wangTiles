from constants import *
from potentials import *
from helpers import *
from display import *
import numpy as np
from multiprocessing import Pool


def get_ac3_arc_consistency_slice(central_tile_index, tiles):
    worklist = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH]).astype(np.int32)
    sphere = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)]).astype(np.int32)
    # print ("SPHERE_WIDTH", SPHERE_WIDTH / 2, sphere.shape)
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, :] = 0
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, central_tile_index] = 1

    while True:
        old_sphere = sphere.copy()
        work_indices = zip(*np.where(worklist==1))
        for indices in work_indices:
            query_i, query_j, query_k = indices
            for neighbor_i, neighbor_j, neighbor_k in neighbors(query_i, query_j, query_k, width = SPHERE_WIDTH):
                    prob_from = sphere[neighbor_i, neighbor_j, neighbor_k, :]
                    trans = transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_k - query_k)
                    prob_to = trans.dot(prob_from).astype(np.int32)
                    prob_to = (prob_to > 0)
                    sphere[query_i,query_j, query_k, :] *= prob_to
            worklist = np.any(old_sphere != sphere, axis=-1)
        if np.any(worklist > 0):
            break
    return sphere


def f(a):
    central_tile_index, tiles = a
    return get_ac3_arc_consistency_slice(central_tile_index, tiles)

def create_spheres(tiles):
    p = Pool(7)
    spheres = p.map(f, zip(range(len(tiles)), [tiles] * len(tiles)))
    spheres = np.array(spheres)
    return spheres

# def create_spheres(tiles):
#     spheres = []
#     for i in range(len(tiles)):
#         spheres.append(get_ac3_arc_consistency_slice(i, tiles))

#     return np.array(spheres)


