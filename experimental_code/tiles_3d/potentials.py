import numpy as np
from helpers import *

delta_to_matrix = {}

def potential(a,b,di,dj,dl):
    # return 1
    p_match = 1
    p_no_match = 0
    if di == 0 and dj == 1 and dl == 0:
        return (np.all(a[:,-1,:] == b[:,0,:])).astype(np.int32)
    if di == 0 and dj == -1 and dl == 0:
        return (np.all(a[:,0,:] == b[:,-1,:])).astype(np.int32)

    if dj == 0 and di == 1 and dl == 0:
        return (np.all(a[-1, :,:] == b[0, :,:])).astype(np.int32)
    if dj == 0 and di == -1 and dl == 0:
        return (np.all(a[0, :,:] == b[-1, :,:])).astype(np.int32)

    if dj == 0 and di == 0 and dl == 1:
        return (np.all(a[:, :,-1] == b[:, :,0])).astype(np.int32)
    if dj == 0 and di == 0 and dl == -1:
        return (np.all(a[:, :,0] == b[:, :,-1])).astype(np.int32)
    return 1


def build_transition_matrices(tiles):
    for i, j, l in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
        build_transition_matrix(i,j,l,tiles)


def build_transition_matrix(di, dj, dl, tiles):
    p_match = 1
    p_no_match = 0
    result = np.zeros([len(tiles)] * 2)
    if di == 0 and dj == 1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)
    elif di == 0 and dj == -1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)

    elif dj == 0 and di == 1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)
    elif dj == 0 and di == -1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)

    elif dj == 0 and di == 0 and dl == 1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)
    elif dj == 0 and di == 0 and dl == -1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                result[i,j] = potential(a,b,di,dj,dl)

    delta_to_matrix[(di, dj, dl)] = result

def transition_matrix(di, dj, dl):
    return delta_to_matrix[(di, dj, dl)]
