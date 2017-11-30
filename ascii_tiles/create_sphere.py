from constants import *
from potentials import *
from helpers import *
from display import *
import numpy as np




def test_bfs():
    grid = np.zeros((3,3))
    for i, item in enumerate(grid_bfs(1,1,3)):
        print item
        grid[item] = i
    print grid
test_bfs()


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
        for query_tile_index in range(len(tiles)):
            for neighbor_i, neighbor_j in neighbors(query_i,query_j, width = SPHERE_WIDTH):
                if visited[neighbor_i, neighbor_j] == 1:
                    # if central_tile_index == 2:
                    #     print "  looking from", query_i,query_j, "to neighbors at", neighbor_i, neighbor_j, "as tile", query_tile_index
                    for neighbor_tile_index in range(len(tiles)):
                        # if central_tile_index == 2:
                        #     print  "    neighbor =", neighbor_tile_index
                        pot = potential(tiles[query_tile_index], tiles[neighbor_tile_index], 
                                        neighbor_i - query_i, neighbor_j - query_j)
                        prior = sphere[neighbor_i, neighbor_j, neighbor_tile_index]
                        # if central_tile_index == 2:
                        #     print  "    pot =",pot
                        sphere[query_i,query_j, query_tile_index] += pot * prior
        # print "  setting sphere at q=", query_i, query_j
        if np.sum(sphere[query_i,query_j, :]) != 0:
            sphere[query_i,query_j, :] = sphere[query_i,query_j, :] / np.sum(sphere[query_i,query_j, :])
        else:
            sphere[query_i,query_j, :] = 0
        visited[query_i,query_j] = 1

    return sphere



def create_spheres(tiles):
    spheres = np.zeros([len(tiles), SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    # print spheres.shape
    for central_tile_index, central_tile in enumerate(tiles):
        spheres[central_tile_index] = get_sphere_slice(central_tile_index, tiles)

    # report_on_sphere(4, spheres, tiles)
    return spheres

