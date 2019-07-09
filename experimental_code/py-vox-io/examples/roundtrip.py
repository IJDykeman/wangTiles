import sys
import coloredlogs
from pyvox.parser import VoxParser
from pyvox.writer import VoxWriter

coloredlogs.install(level='DEBUG')

m1 = VoxParser(sys.argv[1]).parse()

print(m1)

VoxWriter('test.vox', m1).write()

m2 = VoxParser('test.vox').parse()

print(m2)

assert m1.models == m2.models
