
import numpy as np
from constants import *


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


def match(a,b,di,dj):
    if di == 0 and dj == 1:
        return np.all(a[:,-1] == b[:,0])
    if di == 0 and dj == -1:
        return np.all(a[:,0] == b[:,-1])

    if dj == 0 and di == 1:
        return np.all(a[-1, :] == b[0, :])
    if dj == 0 and di == -1:
        return np.all(a[0, :] == b[-1, :])
    return True




def neighbors(i,j, width = WORLD_WIDTH):
    neighbors = np.array([[-1,0], [1,0], [0,-1], [0,1]])
    result = neighbors + np.array([i,j])
    condition = np.logical_and(
                np.logical_and(result[:,0] >= 0,
                result[:,1] >= 0),
                np.logical_and(
                result[:,0] < width,
                result[:,1] < width))
    result = result[condition]
    return result



def get_tiles_and_probs(i,j, tiles, p):
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