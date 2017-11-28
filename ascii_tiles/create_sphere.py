from constants import *
from potentials import *
import numpy as np


def grid_bfs(starti, startj, width):
    queue = [(starti, startj)]
    visited = set({})
    while queue:
        i, j = queue.pop()
        yield i,j
        visited.add((i,j))
        n = set(map(tuple, neighbors(i, j, width = width)))
        n -= visited
        n = list(n)
        queue = [k for k in n if k not in queue] + queue


def test_bfs():
    grid = np.zeros((3,3))
    for i, item in enumerate(grid_bfs(1,1,3)):
        print item
        grid[item] = i
    print grid
test_bfs()




def create_spheres(tiles):
    spheres = np.zeros([len(tiles), SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    print spheres.shape
    for central_tile_index, central_tile in enumerate(tiles):
        print "CENTRAL TILE", central_tile_index
        visited = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH]) 
        visited[SPHERE_WIDTH / 2, SPHERE_WIDTH / 2] = 1
        spheres[central_tile_index, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, :] = 0
        spheres[central_tile_index, SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, central_tile_index] = 1 


        for i, j in grid_bfs(SPHERE_WIDTH / 2, SPHERE_WIDTH / 2, SPHERE_WIDTH):
            print "  bfs to", i,j
            for query_tile_index in range(len(tiles)):
                if i == SPHERE_WIDTH / 2 and j == SPHERE_WIDTH / 2:
                    continue
                visited[i,j] = 1
                for neighbor_i, neighbor_j in neighbors(i,j, width = SPHERE_WIDTH):
                    if visited[neighbor_i, neighbor_j] == 1:
                        print "    looking from", i,j, "to neighbors at", neighbor_i, neighbor_j, "as tile", query_tile_index

                        for neighbor_tile_index in range(len(tiles)):
                            pot = potential(tiles[query_tile_index], tiles[neighbor_tile_index], 
                                          neighbor_i - i, neighbor_j - j)
                            prior = spheres[central_tile_index, neighbor_i, neighbor_j, neighbor_tile_index]

                            spheres[central_tile_index, i,j, query_tile_index] += pot * prior
                            print "        neighbor", neighbor_tile_index, "has potential", pot, " and prior", prior
                        print "    p", spheres[central_tile_index, i,j, query_tile_index] 
                print np.sum(spheres[central_tile_index, i,j, :])
                if np.sum(spheres[central_tile_index, i,j, :]) != 0:
                    spheres[central_tile_index, i,j, :] = spheres[central_tile_index, i,j, :] / np.sum(spheres[central_tile_index, i,j, :])
                else:
                    spheres[central_tile_index, i,j, :] = 0
                print "  ", spheres[central_tile_index, i,j, :]


    return spheres

