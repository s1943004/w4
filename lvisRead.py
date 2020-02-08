import h5py
import numpy as np
import lvisClass

if __name__=="__main__":

    filename = "/geos/netdata/avtrain/data/3d/oosa/week4/lvis_antarctica/ILVIS1B_AQ2015_1014_R1605_070717.h5"
    f = h5py.File(filename,'r')

    print(list(f))

    nbins = f['RXWAVE'].shape[0]
    print(nbins)

    lon0 = np.array(f['LON0'])
    lonN = np.array(f['LON527'])
    latN = np.array(f['LAT527'])

    print(lon0)
    print(lonN)
    print(latN)

