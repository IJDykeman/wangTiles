import numpy as np
from helpers import *

delta_to_matrix = {}

def potential(a,b,di,dj):
    # return 1
    p_match = 1
    p_no_match = 0
    if di == 0 and dj == 1:
        match = (np.all(a[:,-1] == b[:,0])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    if di == 0 and dj == -1:
        match = (np.all(a[:,0] == b[:,-1])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match

    if dj == 0 and di == 1:
        match = (np.all(a[-1, :] == b[0, :])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    if dj == 0 and di == -1:
        match = (np.all(a[0, :] == b[-1, :])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    return 1

def build_transition_matrices(tiles):
    for i, j in [(0,1), (0,-1), (1,0), (-1,0)]:
        build_transition_matrix(i,j,tiles)


def build_transition_matrix(di, dj, tiles):
    p_match = 1
    p_no_match = 0
    result = np.zeros([len(tiles)] * 2)
    if di == 0 and dj == 1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                match = (np.all(a[:,-1] == b[:,0])).astype(np.int32)
                result[i,j] = match * p_match + (1-match) * p_no_match
    elif di == 0 and dj == -1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                match = (np.all(a[:,0] == b[:,-1])).astype(np.int32)
                result[i,j] = match * p_match + (1-match) * p_no_match

    elif dj == 0 and di == 1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                match = (np.all(a[-1, :] == b[0, :])).astype(np.int32)
                result[i,j] = match * p_match + (1-match) * p_no_match
    elif dj == 0 and di == -1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                match = (np.all(a[0, :] == b[-1, :])).astype(np.int32)
                result[i,j] = match * p_match + (1-match) * p_no_match
    delta_to_matrix[(di, dj)] = result

def transition_matrix(di, dj):
    return delta_to_matrix[(di, dj)]

