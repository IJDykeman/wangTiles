import numpy as np
from tqdm import tqdm
from datetime import datetime

from matplotlib.cm import inferno

from pyvox.models import Vox, Color
from pyvox.writer import VoxWriter

n = 126

res = np.zeros((n,n,n), dtype='B')

# scott-gray from
# http://www.labri.fr/perso/nrougier/from-python-to-numpy/code/gray_scott.py


# Du, Dv, F, k = 0.16, 0.08, 0.035, 0.065  # Bacteria 1
# Du, Dv, F, k = 0.14, 0.06, 0.035, 0.065  # Bacteria 2
# Du, Dv, F, k = 0.16, 0.08, 0.060, 0.062  # Coral
# Du, Dv, F, k = 0.19, 0.05, 0.060, 0.062  # Fingerprint
# Du, Dv, F, k = 0.10, 0.10, 0.018, 0.050  # Spirals
# Du, Dv, F, k = 0.12, 0.08, 0.020, 0.050  # Spirals Dense
# Du, Dv, F, k = 0.10, 0.16, 0.020, 0.050  # Spirals Fast
Du, Dv, F, k = 0.16, 0.08, 0.020, 0.055  # Unstable
# Du, Dv, F, k = 0.16, 0.08, 0.050, 0.065  # Worms 1
# Du, Dv, F, k = 0.16, 0.08, 0.054, 0.063  # Worms 2
# Du, Dv, F, k = 0.16, 0.08, 0.035, 0.060  # Zebrafish

random_start = False

Z = np.zeros((n+2, n+2), [('U', np.double),
                          ('V', np.double)])
U, V = Z['U'], Z['V']
u, v = U[1:-1, 1:-1], V[1:-1, 1:-1]

if not random_start:
    r = 20
    u[...] = 1.0
    U[n//2-r:n//2+r, n//2-r:n//2+r] = 0.50
    V[n//2-r:n//2+r, n//2-r:n//2+r] = 0.25
else:
    u[...] = 1
    for x in range(500):
        v[np.random.randint(0,n,2)] = 0.5
    #v[...] = np.random.uniform(0,1,(n,n))

u += 0.05*np.random.uniform(-1, +1, (n, n))
v += 0.05*np.random.uniform(-1, +1, (n, n))


def update():
    global U, V, u, v

    for i in range(20):
        Lu = (                  U[0:-2, 1:-1] +
              U[1:-1, 0:-2] - 4*U[1:-1, 1:-1] + U[1:-1, 2:] +
                                U[2:  , 1:-1])
        Lv = (                  V[0:-2, 1:-1] +
              V[1:-1, 0:-2] - 4*V[1:-1, 1:-1] + V[1:-1, 2:] +
                                V[2:  , 1:-1])
        uvv = u*v*v
        u += (Du*Lu - uvv + F*(1-u))
        v += (Dv*Lv + uvv - (F+k)*v)

t = 0.3

for i in tqdm(range(n)):
    res[:,n-i-1][v>t] = 256*u[v>t]
    update()

mask = res == 0
res += np.arange(n,dtype='B')[:, np.newaxis]//8
res[mask] = 0

pal = [ Color(0,0,0,0) ] + [ Color( *[ int(255*x) for x in inferno(i/128)] ) for i in range(255) ]

# res[res<0.1] = 0
# res = (res*256).astype('B')

res = res[:,:-3,...]
nz = len(res.nonzero()[0])
print(nz, 'non-zero')
if nz:
    vox = Vox.from_dense(res)
    vox.palette = pal

    fn = 'test-%s.vox'%datetime.now().isoformat().replace(':', '_')
    print('wrote', fn)
    VoxWriter(fn, vox).write()
