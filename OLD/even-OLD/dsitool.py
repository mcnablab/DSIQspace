import numpy as np

def create_btable(radius_max, bmax):
    bvecs = []
    for i in range(-radius_max, radius_max + 1):
        for j in range(-radius_max, radius_max + 1):
            for k in range(-radius_max, radius_max + 1):
                if (i ** 2 + j ** 2 + k ** 2) <= radius_max ** 2:
                    bvecs.append([i, j, k])
    bvecs = np.array(bvecs, dtype=np.float32)
    radius = np.sqrt(bvecs[:, 0] ** 2 + bvecs[:, 1] ** 2 + bvecs[:, 2] ** 2)
    I = np.argsort(radius)
    radius = radius[I]
    bvecs = bvecs[I, :]
    bvals = (radius ** 2) * bmax / (float(radius.max()) ** 2)
    bvecs[1:] = bvecs[1:] / radius[1:, None].astype(np.float32)
    return bvecs, bvals

def create_qtable(gtab):
    bv = gtab.bvals
    bmin = np.sort(bv)[1]
    qv = np.sqrt(bv / bmin)
    qtable = np.vstack((qv, qv, qv)).T * gtab.bvecs
    return np.floor(qtable + .5)

def create_qspace(gtab, origin):
    qtable = create_qtable(gtab)
    #qgrid = qtable * deltar + origin
    qgrid = qtable + origin
    return qgrid.astype('i8')

def hanning_filter(gtab, filter_width):
    qtable = create_qtable(gtab)
    r = np.sqrt(qtable[:, 0] ** 2 + qtable[:, 1] ** 2 + qtable[:, 2] ** 2)
    return 0.5 * (1 + np.cos(2 * np.pi * r / filter_width))
