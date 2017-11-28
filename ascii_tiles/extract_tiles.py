import numpy as np
import random
TILE_CONTENT_WIDTH = 4

WORLD_WIDTH = 10

# NORTH = 0
# SOUTH = 1
# EAST = 2
# WEST = 3

def get_lines(fname):
    with open(fname) as f:
        content = f.readlines()
    grid_height = len(content)
    grid_width = np.max(map(len, content))
    for i, l in enumerate(content):
        content[i] = content[i].replace("\n", "")
        content[i] = content[i] + " " * (grid_width - len(content[i])) 
        content[i] = np.array(list(content[i]))
        print content[i].shape
    return content

content = get_lines("tiles.txt")
# print content
content = np.array(content)
# print content
# print content.shape
# print content[:3,:3]

def get_tiles(char_grid):
    result = []
    for i in range(char_grid.shape[0] / 4 + 1):
        for j in range(char_grid.shape[0] / 4 + 1):
            data = char_grid[i*TILE_CONTENT_WIDTH:i*TILE_CONTENT_WIDTH + TILE_CONTENT_WIDTH,
                             j*TILE_CONTENT_WIDTH:j*TILE_CONTENT_WIDTH + TILE_CONTENT_WIDTH]
            print data

            if data.shape == (4,4):
                print data[1,-1]
                tile = data[:-1,:-1]
                if np.all([x != ' ' for x in list(tile.flatten())]):
                    if not data[1,-1]=="#":
                        if data[0,-1]=="*":
                            print "rotated"
                            result.append(np.rot90(tile))
                            result.append(np.rot90(np.rot90(tile)))
                            result.append(np.rot90(np.rot90(np.rot90(tile))))
                        result.append(tile)
                        print "added"
                    else:
                        print "commented"
                    print
    return result

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

def potential(a,b,di,dj):
    slop = .0001
    if di == 0 and dj == 1:
        return np.mean(a[:,-1] == b[:,0]) + slop
    if di == 0 and dj == -1:
        return np.mean(a[:,0] == b[:,-1]) + slop

    if dj == 0 and di == 1:
        return np.mean(a[-1, :] == b[0, :]) + slop
    if dj == 0 and di == -1:
        return np.mean(a[0, :] == b[-1, :]) + slop
    return slop

def p(i, j, t):
    p = 1.0
    for i2, j2 in neighbors(i,j):
        p *= potential(t, tiles[world[i2, j2]], i2-1, j2-j)
    return p

print "===="
tiles = get_tiles(content)
for t in tiles:
    print t
    print

# print match(tiles[0],tiles[1],0,1)
# print match(tiles[0],tiles[1],1,0)
print len(tiles)
world = np.zeros((WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)
world = np.random.randint(0,len(tiles),(WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)
# world = np.zeros((WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)

print world
def neighbors(i,j):
    neighbors = np.array([[-1,0], [1,0], [0,-1], [0,1]])
    result = neighbors + np.array([i,j])
    condition = np.logical_and(
                np.logical_and(result[:,0] >= 0,
                result[:,1] >= 0),
                np.logical_and(
                result[:,0] < WORLD_WIDTH,
                result[:,1] < WORLD_WIDTH))
    result = result[condition]
    return result

def get_tiles_and_probs(i,j, tiles):
    tile_list = []
    prob_list = []
    for i, t in enumerate(tiles):
        tile_list.append(i)
        prob_list.append(p(i,j,t))
    s = sum(prob_list)
    prob_list = [x/s for x in prob_list]
    return tile_list, prob_list


def get_all_valid(i,j):
    result = []
    for t in range(len(tiles)):
        ismatch = True
        for ni, nj in neighbors(i,j):
            ismatch = ismatch and match(tiles[t], tiles[world[ni,nj]], ni - i, nj - j)
        if ismatch:
            result.append(t)
    return result


            # else:
            #     world[i,j] = random.choice(tiles)

def draw_world(world):
    chars = np.array([[" "] * 3 *world.shape[1]] * 3 * world.shape[0])
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            t = tiles[world[i,j]]
            chars[i*3: i*3+3, j*3:j*3+3] = t
    chars = list(map(list, chars))
    for i in range(len(chars)):
        print " ".join(chars[i])

all_coords = []
for i in range(world.shape[0]):
    for j in range(world.shape[1]):
        all_coords.append((i,j))

# for step in range(5000):
#     i,j = random.choice(all_coords)
#     if step % 500 == 0:
#         print 
#         draw_world(world)
#     v = get_all_valid(i,j)
#     if v:
#         world[i,j] = random.choice(v)

for step in range(5000):
    i,j = random.choice(all_coords)
    if step % 500 == 0:
        print 
        print
        draw_world(world)
    ts, ps = get_tiles_and_probs(i,j,tiles)
    world[i,j] = np.random.choice(ts, 1, p=np.array(ps))

print
print
draw_world(world)

# for i in range(len(tiles)):
#     print
#     print i
#     print tiles[i]


# print match(tiles[2], tiles[0], 0, -1)