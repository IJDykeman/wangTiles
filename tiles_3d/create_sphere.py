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

def get_sphere_slice(central_tile_index, tiles):
    sphere = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    # print "CENTRAL TILE", central_tile_index
    visited = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH]) 
    visited[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2] = 1
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, :] = 0
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, central_tile_index] = 1 


    for query_i, query_j, query_l in grid_bfs(SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH):
        # if central_tile_index == 2:    
        #     print query_i, query_j
        # if query_i == SPHERE_WIDTH / 2 and query_j == SPHERE_WIDTH / 2:
        #     continue
        # print "  bfs to", i,j
        for neighbor_i, neighbor_j, neighbor_l in neighbors(query_i,query_j, query_l, width = SPHERE_WIDTH):
            if visited[neighbor_i, neighbor_j, neighbor_l] == 1:
                prob_from = sphere[neighbor_i, neighbor_j, neighbor_l, :]
                # print "=="
                # print transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_l - query_l).shape
                # print prob_from.shape
                prob_to = transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_l - query_l).dot(prob_from)
                sphere[query_i,query_j, query_l, :] += prob_to

        if np.sum(sphere[query_i,query_j, query_l, :]) != 0:
            sphere[query_i,query_j, query_l, :] = sphere[query_i,query_j, query_l, :] / np.sum(sphere[query_i,query_j, query_l, :])
        else:
            sphere[query_i,query_j, query_l, :] = 0
        visited[query_i,query_j, query_l] = 1

    return sphere

def f(a):
    central_tile_index, tiles = a
    return get_sphere_slice(central_tile_index, tiles)

# def create_spheres(tiles):
#     p = Pool(7)
#     spheres = p.map(f, zip(range(len(tiles)), [tiles] * len(tiles)))
#     spheres = np.array(spheres)
#     return spheres

def create_spheres(tiles):
    spheres = []
    for i in range(len(tiles)):
        spheres.append(get_sphere_slice(i, tiles))
        # print "made sphere", i
    return np.array(spheres)


