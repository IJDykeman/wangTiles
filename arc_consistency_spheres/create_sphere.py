from constants import *
from potentials import *
from helpers import *
from display import *
import numpy as np
from multiprocessing import Pool
# from numba import jit




def test_bfs():
    grid = np.zeros((3,3))
    for i, item in enumerate(grid_bfs(1,1,3)):
        print item
        grid[item] = i
    print grid

def get_bfs_counting_slice(central_tile_index, tiles):
    sphere = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])

    # print "CENTRAL TILE", central_tile_index
    visited = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH]) 
    visited[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2] = 1
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, :] = 0
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, central_tile_index] = 1 


    for query_i, query_j in grid_bfs(SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH):
        # if central_tile_index == 2:    
        #     print query_i, query_j
        # if query_i == SPHERE_WIDTH / 2 and query_j == SPHERE_WIDTH / 2:
        #     continue
        # print "  bfs to", i,j
        for neighbor_i, neighbor_j in neighbors(query_i,query_j, width = SPHERE_WIDTH):
            if visited[neighbor_i, neighbor_j] == 1:
                prob_from = sphere[neighbor_i, neighbor_j, :]
                prob_to = transition_matrix(neighbor_i - query_i, neighbor_j - query_j).dot(prob_from)
                sphere[query_i,query_j, :] += prob_to

        if np.sum(sphere[query_i,query_j, :]) != 0:
            sphere[query_i,query_j, :] = sphere[query_i,query_j, :] / np.sum(sphere[query_i,query_j, :])
        else:
            sphere[query_i,query_j, :] = 0
        visited[query_i,query_j] = 1

    return sphere


def get_arc_consistency_slice(central_tile_index, tiles):
    sphere = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, :] = 0
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, central_tile_index] = 1

    while True:
        old_sphere = sphere.copy()
        for query_i in range(SPHERE_WIDTH):
            for query_j in range(SPHERE_WIDTH):
                for neighbor_i, neighbor_j in neighbors(query_i,query_j, width = SPHERE_WIDTH):
                        prob_from = sphere[neighbor_i, neighbor_j, :]
                        trans = transition_matrix(neighbor_i - query_i, neighbor_j - query_j)
                        assert np.max(trans) <= 1
                        prob_to = trans.dot(prob_from)
                        prob_to = (prob_to > 0).astype(np.int32)
                        assert np.max(prob_to) <= 1

                        sphere[query_i,query_j, :] *= prob_to
        if np.all(sphere == old_sphere):
            break
    # print "created sphere", central_tile_index
    return sphere

def get_sphere_slice(central_tile_index, tiles):
    # return get_arc_consistency_slice(central_tile_index, tiles) * get_bfs_counting_slice(central_tile_index, tiles)
    return get_arc_consistency_slice(central_tile_index, tiles)
    # return get_bfs_counting_slice(central_tile_index, tiles)

def f(a):
    central_tile_index, tiles = a
    return get_sphere_slice(central_tile_index, tiles)

def create_spheres(tiles):
    p = Pool(7)
    spheres = p.map(f, zip(range(len(tiles)), [tiles] * len(tiles)))
    spheres = np.array(spheres)
    return spheres


