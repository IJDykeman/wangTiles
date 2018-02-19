import numpy as np
import time
import kernprof

from extract_tiles import *
from potentials import *
from create_sphere import *
from display import *
from constants import *
from helpers import *
import random

import ortools




from ortools.constraint_solver import pywrapcp

solver = pywrapcp.Solver("wangTiles")
# print "\n".join(dir(solver))
# quit()

tile_file_content = get_lines("simpleRoads.txt")
tile_file_content = np.array(tile_file_content)
tiles = get_tiles(tile_file_content)

world = {} #(int,int) => int

def constraint_with_value_pairs(a, b, di, dj):
    result = a == 0
    for i in range(len(tiles)):
        for j in range(len(tiles)):
            if match(tiles[i], tiles[j],di,dj):
                result = solver.Max(result, solver.Min(a==i, b==j))
    # print result
    # quit()
    return result == 1



for i in range(WORLD_WIDTH):
    for j in range(WORLD_WIDTH):
        world[(i,j)] = solver.IntVar(0, len(tiles)-1, str(i) + "," + str(j))
        # solver.Min() # and
        # solver.Max() # or

for i in range(WORLD_WIDTH):
    for j in range(WORLD_WIDTH):
        # solver.Add(solver.Max(x != y, y != z) == 1)
        for n in neighbors(i,j):
            # solver.Add(world[(i,j)] != world[tuple(n)])
            solver.Add(constraint_with_value_pairs(world[(i,j)], world[tuple(n)], n[0]-i, n[1]-j))

print "solving..."
# print world.values()
# db = solver.Phase(world.values(), solver.CHOOSE_MIN_SLACK_RANK_FORWARD, solver.ASSIGN_RANDOM_VALUE)
db = solver.Phase(world.values(), solver.CHOOSE_MIN_SIZE, solver.ASSIGN_RANDOM_VALUE)
# CHOOSE_MIN_SIZE
# CHOOSE_MIN_SIZE_HIGHEST_MAX
# CHOOSE_MIN_SIZE_HIGHEST_MIN
# CHOOSE_MIN_SIZE_LOWEST_MAX
# CHOOSE_MIN_SIZE_LOWEST_MIN
# CHOOSE_MIN_SLACK_RANK_FORWARD

solver.Solve(db)

while solver.NextSolution():
    print ""
    print world[(0,0)].Value()
    print world[(0,1)].Value()
    print world[(1,1)].Value()
    world_ar = np.zeros([WORLD_WIDTH, WORLD_WIDTH]).astype(np.int32)
    for i in range(WORLD_WIDTH):
        for j in range(WORLD_WIDTH):
            world_ar[i,j] = world[(i, j)].Value()
    print world_ar
    print len(tiles)
    draw_world(world_ar, tiles)

# import numpy as np
# import time
# import kernprof

# from extract_tiles import *
# from potentials import *
# from create_sphere import *
# from display import *
# from constants import *
# from helpers import *
# import random

# import ortools




# from ortools.constraint_solver import pywrapcp

# solver = pywrapcp.Solver("wangTiles")
# # print "\n".join(dir(solver))
# # quit()

# tile_file_content = get_lines("tiles3.txt")
# tile_file_content = np.array(tile_file_content)
# tiles = get_tiles(tile_file_content)

# world = {} #(int,int) => int

# def constraint_with_value_pairs(a, b, di, dj):
#     result = a > -1
#     for i in range(len(tiles)):
#         for j in range(len(tiles)):
#             if match(tiles[i], tiles[j],di,dj):
#                 result = solver.Max(result, solver.Min(a==i, b==j))
#     return result == 1



# for i in range(WORLD_WIDTH):
#     for j in range(WORLD_WIDTH):
#         world[(i,j)] = solver.IntVar(0, len(tiles), str(i) + "," + str(j))
#         # solver.Min() # and
#         # solver.Max() # or

# for i in range(WORLD_WIDTH):
#     for j in range(WORLD_WIDTH):
#         # solver.Add(solver.Max(x != y, y != z) == 1)
#         for n in neighbors(i,j):
#             # solver.Add(world[(i,j)] != world[tuple(n)])
#             solver.Add(constraint_with_value_pairs(world[(i,j)], world[tuple(n)], n[0]-i, n[1]-j))

# print "solving..."
# # print world.values()
# db = solver.Phase(world.values(), solver.CHOOSE_MIN_SLACK_RANK_FORWARD, solver.ASSIGN_RANDOM_VALUE)
# solver.Solve(db)

# while solver.NextSolution():
#     world[(0, 0)].Value()
    # world_ar = np.zeros([WORLD_WIDTH, WORLD_WIDTH])
    # for i in range(WORLD_WIDTH):
    #     for j in range(WORLD_WIDTH):
    #         world_arr[i,j] = world[(i, j)].Value()
    # draw_world(world_arr, tiles)
