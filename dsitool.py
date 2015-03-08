import numpy as np
import nibabel as nib
import dsiadapt as dsi
import dipy.core.gradients as grad

def loaddata(filename):
    # Load data
    data = nib.load('data/' + filename + '.nii.gz').get_data();
    return data

def loadgtab(filename):
    # Load bvals and bvecs
    filename = filename[0:12]; # Use key letters to differentiate data
    gtab = grad.gradient_table('data/' + filename + '_bvals.txt', 'data/' + filename + '_bvecs.txt');
    return gtab

def loadtime(filename):
    # Load diffusion time and gradient pulse duration time
    filename = filename[6:12]; # Use key letters to differentiate data
    if filename == 'exvivo':
        bigdelta = 29.4 * 10**-3; # Unit: second
	smalldelta = 16.7 * 10**-3;
    elif filename == 'invivo':
	bigdelta = 20.9 * 10**-3;
	smalldelta = 12.9 * 10**-3;
    else:
	print('Error: no such option!!')
    return bigdelta, smalldelta

def loadroi(filename, qgridsz):
    filename1 = filename[6:15];
    if filename1 == 'exvivo_cc':
	pdfroi = np.array([0, 0, 0]);
    elif filename == 'DSI11_exvivo_xfib':
	pdfroi = np.array([0, 1, 0]);
    elif filename == 'DSI11_invivo_cc':
	pdfroi = np.array([0, 0, 1]);
    elif filename == 'DSI11_invivo_xfib':
	pdfroi = np.array([1, 0, 0]);
    else:
	pdfroi = [];
    
    filename2 = filename[6:12]; 
    if filename2 == 'exvivo':
        camerapos = np.array([1, 0, 0]);
	pdfslicestart = np.array([qgridsz//2, 0, 0]);
	pdfsliceend = np.array([qgridsz//2 + 1, qgridsz, qgridsz]);
    elif filename2 == 'invivo':
	camerapos = np.array([0, 1, 0]);
	pdfslicestart = np.array([0, qgridsz//2, 0]);
	pdfsliceend = np.array([qgridsz, qgridsz//2 + 1, qgridsz]);
    else:
	print('error: no such option!!')

    return pdfroi, pdfslicestart, pdfsliceend, camerapos

def loadfigconfig(filename):
    filename = filename[0:12];
    if filename == 'DSI11_exvivo':
	fov = 28.0 #um
	mdd = 5. #um
    elif filename == 'DSI15_exvivo':
	fov = 39.2 #um
	mdd = 5. #um
    elif filename == 'DSI17_exvivo':
	fov = 44.8 #um
	mdd = 5. #um
    elif filename == 'DSI11_invivo':
	fov = 39.2 #um
	mdd = 13.4 #um
    else:
	print('error: no such option!!')
    return fov, mdd

def weightpdfslice(pdfslice):
    qgridsz = pdfslice.shape[0]
    center = qgridsz//2
    tmp = np.arange(qgridsz) - center
    x, y = np.meshgrid(tmp, tmp)
    r2 = x ** 2 + y ** 2
    weightedpdfslice = pdfslice * r2
    return weightedpdfslice

def downsample(data, gtab, downratio):
    qtable = dsi.create_qtable(gtab);

    idx1 = (np.mod(np.abs(qtable[:, 0]), downratio)==0) * (np.mod(np.abs(qtable[:, 1]), downratio)==0) * (np.mod(np.abs(qtable[:, 2]), downratio)==0)
    
    idx2 = np.logical_or(np.logical_or(np.abs(qtable[:, 0]) == qtable.max(), np.abs(qtable[:, 1]) == qtable.max()), np.abs(qtable[:, 2]) == qtable.max());
    
    idxremain = np.logical_or(idx1, idx2)  
    idxremove = np.logical_not(idxremain);

    subdata = data
    subdata[..., idxremove] = 0; # Subsample the data by inserting 0 so the FOV is unchanged

    return subdata

def uniquebvals(data, bvals):
    uniqbvals = np.unique(bvals)
    uniqdata = np.zeros((uniqbvals.shape[0], 1))
    for i in range(uniqbvals.shape[0]):
        idx = bvals == uniqbvals[i]
        tmp = data[idx,...]
        uniqdata[i] = tmp.mean()
    return uniqdata, uniqbvals

def downsample_qball(data, gtab, downratio):
    qtable = dsi.create_qtable(gtab);
    
    idxremain = np.logical_or(np.logical_or(np.abs(qtable[:, 0]) == downratio, np.abs(qtable[:, 1]) == downratio), np.abs(qtable[:, 2]) == downratio);
    
    idxremove = np.logical_not(idxremain);

    subdata = data
    subdata[..., idxremove] = 0; # Subsample the data by inserting 0 so the FOV is unchanged

    return subdata


