import numpy as np
from helpers import *

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
    print "oops"

