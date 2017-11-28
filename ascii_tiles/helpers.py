
import numpy as np
from constants import *


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
