import numpy as np

a = (np.linalg.norm(np.mgrid[-5:5:10j, -5:5:10j, -5:5:10j], axis=0) < 4).astype(np.int32)
from pyvox.models import Vox
from pyvox.writer import VoxWriter

vox = Vox.from_dense(a)

VoxWriter('test.vox', vox).write()