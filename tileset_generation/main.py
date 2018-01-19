import numpy as np
import noise
# help(noise)
import minecraft

width = 250
solids = []

solidity = np.zeros([width] * 3).astype(np.int32)

for x in range(width):
    for y in range(width):
        for z in range(width):
            scale = .05
            p = noise.snoise3(x * scale,y* scale,z* scale, octaves=1, persistence=.5, lacunarity=2.0)
            if p > 0:
                solids.append((x,y,z, 1))
                solidity[x,y,z] = 1

all_patterns = set([])
for x in range(0, width - 2, 3):
    for y in range(0, width - 2, 3):
        for z in range(0, width - 2, 3):
            all_patterns.add(tuple(solidity[x:x+3, y:y+3, z:z+3].flatten()))


# print len(all_patterns), "/", (width - 2) ** 3
# print 1.0 * len(all_patterns) / (width - 2) ** 3
# minecraft.main(solid = solids)

all_patterns = list(all_patterns)

text_rows = []
for i in range(len(all_patterns)):

    # print "tile", i
    tile = np.array(all_patterns[i]).reshape([3]*3)
    for slice in range(3):
        text_line = ""
        slice = tile[:,:,slice]
        for line in range(3):
            text_line += ("".join([str(x) for x in list(slice[line])]) + " ")
        text_rows.append(text_line)
    text_rows.append(" ")

# text_rows.replace("0", ",")
# text_rows.replace("1", "#")

print "\n".join(text_rows)