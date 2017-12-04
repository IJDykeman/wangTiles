from constants import *
from potentials import *
from helpers import *
from display import *
import numpy as np
from multiprocessing import Pool
from numba import jit




def test_bfs():
    grid = np.zeros((3,3))
    for i, item in enumerate(grid_bfs(1,1,3)):
        print item
        grid[item] = i
    print grid
test_bfs()

@jit
def get_sphere_slice(central_tile_index, tiles):
    sphere = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])

    # print "CENTRAL TILE", central_tile_index
    visited = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH]) 
    visited[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2] = 1
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, :] = 0
    sphere[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, central_tile_index] = 1 


    for query_i, query_j in grid_bfs(SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH):
        # if central_tile_index == 2:    
        #     print query_i, query_j
        if query_i == SPHERE_WIDTH / 2 and query_j == SPHERE_WIDTH / 2:
            continue
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

transition_matrix

# @jit
def f(a):
    central_tile_index, tiles = a
    return get_sphere_slice(central_tile_index, tiles)

def create_spheres(tiles):

    p = Pool(7)
    
    # print spheres.shape

    spheres = p.map(f, zip(range(len(tiles)), [tiles] * len(tiles)))
    # print spheres
    spheres = np.array(spheres)
    # print spheres.shape
    # quit()
    # report_on_sphere(4, spheres, tiles)
    return spheres


