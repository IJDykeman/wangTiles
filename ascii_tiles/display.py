import numpy as np
from constants import *

def prRed(prt): return ("\033[91m\033[01m{}\033[00m" .format(prt))
def prGreen(prt): return ("\033[92m\033[01m{}\033[00m" .format(prt))
def prYellow(prt): return ("\033[93m\033[01m{}\033[00m" .format(prt))
def prLightPurple(prt): return ("\033[94m\033[01m{}\033[00m" .format(prt))
def prPurple(prt): return ("\033[95m\033[01m{}\033[00m" .format(prt))
def prCyan(prt): return ("\033[96m\033[01m{}\033[00m" .format(prt))
def prLightGray(prt): return ("\033[97m\033[01m{}\033[00m" .format(prt))
def prBlack(prt): return ("\033[98m\033[01m{}\033[00m" .format(prt))
def bgBlue(prt): return ("\033[44m\033[01m{}\033[00m" .format(prt))
def bgPink(prt): return ("\033[45m\033[01m{}\033[00m" .format(prt))
def bgCyan(prt): return ("\033[46m\033[01m{}\033[00m" .format(prt))
def bgTan(prt): return ("\033[47m\033[01m{}\033[00m" .format(prt))
def bgYellow(prt): return ("\033[43m\033[01m{}\033[00m" .format(prt))
def bgGreen(prt): return ("\033[42m\033[01m{}\033[00m" .format(prt))
def bgRed(prt): return ("\033[41m\033[01m{}\033[00m" .format(prt))
def bgLightGray(prt): return ("\033[40m\033[01m{}\033[00m" .format(prt))



def prDarkgrey(prt): return ("\033[90m\033[01m{}\033[00m" .format(prt))

replacements = {
    '# ': prLightGray('# '),
    '= ': bgGreen('= '),
    '_ ': bgGreen('_ '),
    'w ': bgBlue('  '),
    '| ': bgLightGray('| '),
    'L ': bgRed('  '),
    '0 ': prCyan('  '),


    
}


def draw_world(world, tiles, mask = None):
    # print "=" * WORLD_WIDTH * 3
    if mask is None:
        mask = np.ones_like(world)
    chars = np.array([[" "] * 3 *world.shape[1]] * 3 * world.shape[0])
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            if mask[i,j] == 1:
                t = tiles[world[i,j]]
                chars[i*3: i*3+3, j*3:j*3+3] = t
            else:
                chars[i*3: i*3+3, j*3:j*3+3] = np.array([list("   ")]*3)
    chars = list(map(list, chars))
    toprint = []
    for i in range(len(chars)):
        toprint.append(" ".join(chars[i]))
    toprint = "\n".join(toprint)
    for k in replacements:
        toprint = toprint.replace(k, replacements[k])
    print toprint
    print "=" * WORLD_WIDTH * 3


def show_tiles(tiles):
    for i in range(len(tiles)):
        print
        print i
        print tiles[i]

def report_on_sphere(i, spheres, tiles):
    print "=================================="
    print "reporting information about tile", i
    print tiles[i]
    for t2 in range(len(tiles)):
        print "transition to", t2
        print tiles[t2]
        print spheres[i, :,:, t2]

    print "=================================="
