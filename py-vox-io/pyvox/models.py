from collections import namedtuple

from .defaultpalette import default_palette
from .utils import chunks
def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]
Size = namedtuple('Size', 'x y z')
Color = namedtuple('Color', 'r g b a')
Voxel = namedtuple('Voxel', 'x y z c')
Model = namedtuple('Model', 'size voxels')
Material = namedtuple('Material', 'id type weight props')

def get_default_palette():
    return [ Color( *tuple(to_bytes(i,4,'little')) ) for i in default_palette ]


class Vox(object):

    def __init__(self, models, palette=None, materials=None):
        self.models = models
        self.default_palette = not palette
        self._palette = palette or get_default_palette()
        self.materials = materials or []

    @property
    def palette(self):
        return self._palette

    @palette.setter
    def palette(self, val):
        self._palette = val
        self.default_palette = False

    def to_dense_rgba(self, model_idx=0):

        import numpy as np
        m = self.models[model_idx]
        res = np.zeros(( m.size.y, m.size.z, m.size.x, 4 ), dtype='B')

        for v in m.voxels:
            res[v.y, m.size.z-v.z-1, v.x] = self.palette[v.c]

        return res

    def to_dense(self, model_idx=0):

        import numpy as np
        m = self.models[model_idx]
        res = np.zeros(( m.size.y, m.size.z, m.size.x ), dtype='B')

        for v in m.voxels:
            res[v.y, m.size.z-v.z-1, v.x] = v.c

        return res

    def __str__(self):
        return 'Vox(%s)'%(self.models)

    @staticmethod
    def from_dense(a, black=[0,0,0]):

        palette = None

        if len(a.shape) == 4:
            from PIL import Image
            import numpy as np

            mask = np.all(a == np.array([[black]]), axis=3)

            x,y,z,_ = a.shape

            # color index 0 is reserved for empty, so we get 255 colors
            img = Image.fromarray(a.reshape(x,y*z,3)).quantize(255)
            palette = img.getpalette()
            palette = [ Color(0,0,0,0) ] + [ Color(c[0], c[1], c[2], 255) for c in chunks(palette, 3) ]
            a = np.asarray(img, dtype='B').reshape(x,y,z).copy() + 1
            a[mask] = 0


        if len(a.shape) != 3: raise Exception("I expect a 4 or 3 dimensional matrix")

        y,z,x = a.shape

        nz = a.nonzero()

        voxels = [ Voxel( nz[2][i], nz[0][i], z-nz[1][i]-1, a[nz[0][i], nz[1][i], nz[2][i]] ) for i in range(nz[0].shape[0]) ]

        return Vox([ Model(Size(x,y,z), voxels)], palette)
