import numpy as np
import dipy.reconst.dsi as dsi
import dipy.core.gradients as grad

def weightpdf(pdfslice):
    gridsize = pdfslice.shape[0]
    center = gridsize//2
    tmp = np.arange(gridsize) - center
    x, y = np.meshgrid(tmp, tmp)
    r2 = x ** 2 + y ** 2
    weightedpdfslice = pdfslice * r2 / float((gridsize ** 2))
    return weightedpdfslice

def subsample(data, gtab, ratio, direction, fovreduce):
    # Subsample the data by inserting 0
    qtable = dsi.create_qtable(gtab);
    if direction == 'X':
        idx1 = np.mod(np.abs(qtable[:, 0]), ratio)==0
        idx1 = np.mod(np.abs(qtable[:, 1]), ratio)==0
    elif direction == 'Z':
        idx1 = np.mod(np.abs(qtable[:, 2]), ratio)==0
    else:
        idx1 = (np.mod(np.abs(qtable[:, 0]), ratio)==0)*(np.mod(np.abs(qtable[:, 1]), ratio)==0)*(np.mod(np.abs(qtable[:, 2]), ratio)==0)
    
    idx2 = np.logical_or(np.logical_or(np.abs(qtable[:, 0]) == qtable.max(), np.abs(qtable[:, 1]) == qtable.max()), np.abs(qtable[:, 2]) == qtable.max());
    idxremain = np.logical_or(idx1, idx2)  
    idxremove = np.logical_not(idxremain);
    
    subdata = data;
    subgtab = gtab;
    if fovreduce == True:
        subdata = data[..., idxremain]
        subbvals = gtab.bvals[idxremain]
        subbvecs = gtab.bvecs[idxremain, ...]
	subgtab = grad.gradient_table(subbvals, subbvecs)
    else:
	subdata = data
        subdata[..., idxremove] = 0;
	subgtab = gtab
    return subdata, subgtab
