import numpy as np
from helpers import *

delta_to_matrix = {}

def potential(a,b,di,dj,dl):
    # return 1
    p_match = 1
    p_no_match = 0
    if di == 0 and dj == 1 and dl == 0:
        match = (np.all(a[:,-1,:] == b[:,0,:])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    if di == 0 and dj == -1 and dl == 0:
        match = (np.all(a[:,0,:] == b[:,-1,:])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match

    if dj == 0 and di == 1 and dl == 0:
        match = (np.all(a[-1, :,:] == b[0, :,:])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    if dj == 0 and di == -1 and dl == 0:
        match = (np.all(a[0, :,:] == b[-1, :,:])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match

    if dj == 0 and di == 0 and dl == 1:
        match = (np.all(a[:, :,-1] == b[:, :,0])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    if dj == 0 and di == 0 and dl == -1:
        match = (np.all(a[:, :,0] == b[:, :,-1])).astype(np.int32)
        return match * p_match + (1-match) * p_no_match
    return 1

# def potential(a,b,di,dj,dl):
#     # return 1
#     p_match = 1
#     p_no_match = 0
#     if di == 0 and dj == 1 and dl == 0:
#         match = (np.all(a[ 0:TILE_WIDTH,-1, TILE_WIDTH / 2] == b[ 0:TILE_WIDTH,0, TILE_WIDTH / 2])).astype(np.int32)
#         match *= (np.all(a[ TILE_WIDTH / 2,-1, 0:TILE_WIDTH] == b[ TILE_WIDTH / 2,0, 0:TILE_WIDTH])).astype(np.int32)
        
#         return match * p_match + (1-match) * p_no_match
#     if di == 0 and dj == -1 and dl == 0:
#         match = (np.all(a[ 0:TILE_WIDTH,0, TILE_WIDTH / 2] == b[0:TILE_WIDTH,-1, TILE_WIDTH / 2])).astype(np.int32)
#         match *= (np.all(a[ TILE_WIDTH / 2,0, 0:TILE_WIDTH] == b[ TILE_WIDTH / 2,-1, 0:TILE_WIDTH])).astype(np.int32)
        
#         return match * p_match + (1-match) * p_no_match

#     if dj == 0 and di == 1 and dl == 0:
#         match = (np.all(a[-1,  0:TILE_WIDTH, TILE_WIDTH / 2] == b[0,  0:TILE_WIDTH, TILE_WIDTH / 2])).astype(np.int32)
#         match *= (np.all(a[-1,  TILE_WIDTH / 2, 0:TILE_WIDTH] == b[0,  TILE_WIDTH / 2, 0:TILE_WIDTH])).astype(np.int32)
        
#         return match * p_match + (1-match) * p_no_match
#     if dj == 0 and di == -1 and dl == 0:
#         match = (np.all(a[0,  0:TILE_WIDTH, TILE_WIDTH / 2] == b[-1,  0:TILE_WIDTH, TILE_WIDTH / 2])).astype(np.int32)
#         match *= (np.all(a[0,  TILE_WIDTH / 2, 0:TILE_WIDTH] == b[-1,  TILE_WIDTH / 2, 0:TILE_WIDTH])).astype(np.int32)
        
#         return match * p_match + (1-match) * p_no_match

#     if dj == 0 and di == 0 and dl == 1:
#         match = (np.all(a[ 0:TILE_WIDTH,  TILE_WIDTH / 2,-1] == b[0:TILE_WIDTH,  TILE_WIDTH / 2,0])).astype(np.int32)
#         match *= (np.all(a[ TILE_WIDTH / 2,  0:TILE_WIDTH,-1] == b[ TILE_WIDTH / 2,  0:TILE_WIDTH,0])).astype(np.int32)

#         return match * p_match + (1-match) * p_no_match
#     if dj == 0 and di == 0 and dl == -1:
#         match = (np.all(a[ 0:TILE_WIDTH,  TILE_WIDTH / 2,0] == b[ 0:TILE_WIDTH,  TILE_WIDTH / 2,-1])).astype(np.int32)
#         match *= (np.all(a[ TILE_WIDTH / 2,  0:TILE_WIDTH,0] == b[ TILE_WIDTH / 2,  0:TILE_WIDTH,-1])).astype(np.int32)

#         return match * p_match + (1-match) * p_no_match
#     return 1


# def potential(a,b,di,dj,dl):
#     # return 1
#     p_match = 1
#     p_no_match = 0
#     if di == 0 and dj == 1 and dl == 0:
#         match = (np.all(a[ TILE_WIDTH / 2,-1, TILE_WIDTH / 2] == b[ TILE_WIDTH / 2,0, TILE_WIDTH / 2])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match
#     if di == 0 and dj == -1 and dl == 0:
#         match = (np.all(a[ TILE_WIDTH / 2,0, TILE_WIDTH / 2] == b[ TILE_WIDTH / 2,-1, TILE_WIDTH / 2])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match

#     if dj == 0 and di == 1 and dl == 0:
#         match = (np.all(a[-1,  TILE_WIDTH / 2, TILE_WIDTH / 2] == b[0,  TILE_WIDTH / 2, TILE_WIDTH / 2])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match
#     if dj == 0 and di == -1 and dl == 0:
#         match = (np.all(a[0,  TILE_WIDTH / 2, TILE_WIDTH / 2] == b[-1,  TILE_WIDTH / 2, TILE_WIDTH / 2])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match

#     if dj == 0 and di == 0 and dl == 1:
#         match = (np.all(a[ TILE_WIDTH / 2,  TILE_WIDTH / 2,-1] == b[ TILE_WIDTH / 2,  TILE_WIDTH / 2,0])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match
#     if dj == 0 and di == 0 and dl == -1:
#         match = (np.all(a[ TILE_WIDTH / 2,  TILE_WIDTH / 2,0] == b[ TILE_WIDTH / 2,  TILE_WIDTH / 2,-1])).astype(np.int32)
#         return match * p_match + (1-match) * p_no_match
#     return 1

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
                # match = (np.all(a[:,-1] == b[:,0, :])).astype(np.int32)
                # match = potential(a,b,di,dj,dl)
                result[i,j] = potential(a,b,di,dj,dl)
    elif di == 0 and dj == -1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                # match = (np.all(a[:,0] == b[:,-1, :])).astype(np.int32)
                match = potential(a,b,di,dj,dl)
                result[i,j] = match * p_match + (1-match) * p_no_match

    elif dj == 0 and di == 1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                # match = (np.all(a[-1, :] == b[0, :, :])).astype(np.int32)
                # match = potential(a,b,di,dj,dl)
                result[i,j] = potential(a,b,di,dj,dl)
    elif dj == 0 and di == -1 and dl == 0:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                # match = (np.all(a[0, :] == b[-1, :, :])).astype(np.int32)
                # match = potential(a,b,di,dj,dl)
                result[i,j] = potential(a,b,di,dj,dl)

    elif dj == 0 and di == 0 and dl == 1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                # match = (np.all(a[-1, :] == b[:, :, 0])).astype(np.int32)
                # match = potential(a,b,di,dj,dl)
                result[i,j] = potential(a,b,di,dj,dl)
    elif dj == 0 and di == 0 and dl == -1:
        for i, a in enumerate(tiles):
            for j, b in enumerate(tiles):
                # match = (np.all(a[0, :] == b[:, :, -1])).astype(np.int32)
                match = potential(a,b,di,dj,dl)
                result[i,j] = match * p_match + (1-match) * p_no_match

    delta_to_matrix[(di, dj, dl)] = result

def transition_matrix(di, dj, dl):
    return delta_to_matrix[(di, dj, dl)]
