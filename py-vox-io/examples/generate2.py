import numpy as np

from pyvox.models import Vox
from pyvox.writer import VoxWriter

size=15j

a=np.mgrid[1:255:size, 1:255:size, 1:255:size].T.astype('B')

size=int(size.imag)

# clear alternate rows/cols
# in the least numpy way possible
for x in range(1,size,2):
    a[x] = 0
    a[:,x] = 0
    a[:,:,x] = 0

vox = Vox.from_dense(a)

VoxWriter('test.vox', vox).write()
