import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import glob # helps with building file lists
import matplotlib.cm as cm  # Import the colormap module
from matplotlib.colors import LogNorm  # Import LogNorm for logarithmic scaling

# simple read
def read_raw_image(fits_file,get_header=0):
    # returns an index and the fluxes
    # Open the FITS file
    hdulist = fits.open(fits_file)
    header = hdulist[0].header
    # Assuming the spectrum data is in the first extension (HDU index 0)
    data = hdulist[0].data
#    xaxis= list(range(len(data)))
    if(get_header==0):
        return data
    if(get_header==1):
        return data,header

# simple write
def write_fits_image(target_file,data,header=[]):
    if(header==[]):
        hdu=fits.hdu.hdulist.PrimaryHDU(data)
    else:
        hdu=fits.hdu.hdulist.PrimaryHDU(data,header)
    hdul = fits.hdu.HDUList([hdu])
    hdul.writeto(target_file,overwrite=True)
    print('wrote ',target_file)
    
# print header of fits file
#def print_header(file,keywords_list = ['OBJECT', 'FLTRNM', 'TM-EXPOS'],l=0):
def print_header(file,keywords_list = ['OBJECT'],l=0):

    fits_file = fits.open(file)
    header = fits_file[0].header
    # print ALL:
    if(l==1):
        print(repr(header))
    else:
        result=''
        for keyword in keywords_list:
            if keyword in header:
#                print(header[keyword])
#                print(type(str(header[keyword])))
                result=result+' '+str(header[keyword])
            else:
                print(f'{keyword:8s} = Not found in header')
        print(result)
        
def get_stats(file):
    # returns 
    # filename, number of pixels (nx*ny), mean, dispersion (sigma), min, max
    data=read_raw_image(file)
    nx,ny=np.shape(data)
    return [file,nx*ny,np.average(data),np.std(data),np.min(data),np.max(data)]

def get_scaling(data):
    # useful to set vmin,vmax in plt.imshow
    vmin=np.average(data)-2.*np.std(data)
    vmax=np.average(data)+2.*np.std(data)
    return vmin,vmax    

def plot_image(data):
    plt.figure(figsize=(7,7))
    vmin,vmax=get_scaling(data)
    plt.imshow(data,origin='lower',aspect='auto',vmin=vmin,vmax=vmax)
    plt.show()