# This piece of code shows how to convert the format of Aurelie spectro
# to what our data reduction software expects
# The current (as of 2023) output of Aurelie is a list of hdus
# containing lists of data. Such depth is not required here.
# So we extract the data and write it as a single hdu with a single vector containing the spectrum.

import astropy.io.fits as io
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import glob;
import os;

files=glob.glob('thar*_?????.fits')

#files
for f in files:
    print(f)
    filename, file_ext=os.path.splitext(f)
    newf=filename+"_1d"+file_ext
    print(newf)
    hduori=io.open(f)
    exp=(hduori[0].header['EXPOSURE'])
    data=hduori[0].data
    data=data[0][0]
    hdu=io.PrimaryHDU(data)
    hdul = io.HDUList([hdu])
    hdu.header.set('EXPOSURE',exp,"[s]")
    hdul.writeto(newf)
