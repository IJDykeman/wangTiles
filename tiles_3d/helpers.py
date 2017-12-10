
import numpy as np
from constants import *


def grid_bfs(starti, startj, startl, width):
    queue = [(starti, startj, startl)]
    visited = set({})
    while queue:
        i, j, l = queue.pop()
        yield i,j, l
        visited.add((i,j,l))
        n = set(map(tuple, neighbors(i, j, l, width = width)))
        n -= visited
        n = list(n)
        queue = [k for k in n if k not in queue] + queue


def match(a, b, di, dj, dl):
    if di == 0 and dj == 1 and dl == 0:
        return np.all(a[:,-1] == b[:,0, :])
    if di == 0 and dj == -1 and dl == 0:
        return np.all(a[:,0, :] == b[:,-1, :])

    if dj == 0 and di == 1 and dl == 0:
        return np.all(a[-1, :, :] == b[0, :, :])
    if dj == 0 and di == -1 and dl == 0:
        return np.all(a[0, :, :] == b[-1, :, :])

    if dj == 0 and di == 0 and dl == 1:
        return np.all(a[:, :, -1] == b[:, :, 0])
    if dj == 0 and di == 0 and dl == -1:
        return np.all(a[:, :, 0] == b[:, :, -1])

    return True


def logical_and_3(a,b,c):
    return np.logical_and(a, np.logical_and(b, c))

def neighbors(i, j, l, width = WORLD_WIDTH):
    neighbors = np.array([[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]])
    result = neighbors + np.array([i,j,l])
    condition = np.logical_and(
                    logical_and_3(
                        result[:,0] >= 0,
                        result[:,1] >= 0,
                        result[:,2] >= 0),
                    logical_and_3(
                        result[:,0] < width,
                        result[:,1] < width,
                        result[:,2] < width))
    result = result[condition]
    return result



def get_tiles_and_probs(i, j, l, tiles, p):
    assert 1 ==0 
    tile_list = []
    prob_list = []
    for i, t in enumerate(tiles):
        tile_list.append(i)
        prob_list.append(p(i,j,t))
    # print prob_list
    s = sum(prob_list)
    prob_list = [x/s for x in prob_list]
    # print prob_list
    return tile_list, prob_list

def in_world(i, j, l):
    return i >= 0 and i < WORLD_WIDTH and j >= 0 and j < WORLD_WIDTH and l >= 0 and l < WORLD_WIDTH 


