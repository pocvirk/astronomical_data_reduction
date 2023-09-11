# => makes the plot interactive
#%matplotlib notebook 
# inline makes the plots static
#%matplotlib inline 

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import warnings
# filter astropy warning on fits headers
warnings.filterwarnings('ignore', category=UserWarning, append=True)

def plot_spectrum_panels(xaxis,data,num_panels=2):
    # not that useful, interactive plotting is better
    spectrum_data=np.copy(data)

    # Divide the spectrum into four panels
    panel_height = len(spectrum_data) // num_panels

    # Create subplots
    fig, axs = plt.subplots(num_panels, 1, figsize=(15, 6*num_panels))

    # Plot each panel
    for i in range(num_panels):
        start_idx = i * panel_height
        end_idx = (i + 1) * panel_height
        xaxis= list(range(len(spectrum_data)))
        axs[i].plot(xaxis[start_idx:end_idx],spectrum_data[start_idx:end_idx])
#        axs[i].set_xlabel('Wavelength (Angstroms)')
        axs[i].set_ylabel('counts(ADU)')
        axs[i].set_title(f'Panel {i + 1}')
        axs[i].grid(True)


def read_raw_spectrum(fits_file,get_header=0):
    # returns an index and the fluxes
    # Open the FITS file
    hdulist = fits.open(fits_file)
    header = hdulist[0].header
    # Assuming the spectrum data is in the first extension (HDU index 0)
    data = hdulist[0].data[0]
    xaxis= list(range(len(data)))
    if(get_header==0):
        return xaxis,data
    if(get_header==1):
        return xaxis,data,header

def write_fits_spectrum(target_file,data,header=[]):
    if(header==[]):
        hdu=fits.hdu.hdulist.PrimaryHDU([data])
    else:
        hdu=fits.hdu.hdulist.PrimaryHDU([data],header)
    hdul = fits.hdu.HDUList([hdu])
    hdul.writeto(target_file,overwrite=True)
    print('wrote ',target_file)

def read_calibrated_spectrum(fits_file):
    # Open the FITS file
    with fits.open(fits_file) as hdul:
        # Extract the data and header from the primary HDU
        data = hdul[0].data[0]
        header = hdul[0].header

        # Extract necessary header keywords for calibration
        crval1 = header['CRVAL1']  # Reference value of the first pixel (wavelength)
        cdelt1 = header['CDELT1']  # Pixel scale (wavelength per pixel)
        naxis1 = header['NAXIS1']  # Number of pixels in the spectral axis

        # Create an array of calibrated wavelengths
        wavelengths = crval1 + np.arange(naxis1) * cdelt1
    return wavelengths,data


# Define the Gaussian function
def gaussian(x, *params):
    result= np.full(len(x),0.)
    for i in range(0, len(params), 3):
        amp, cen, wid = params[i:i+3]
        result += amp * np.exp(-(x - cen) ** 2 / (2 * wid ** 2))
    return result

def generate_first_guess(peaks):
#    npeaks=len(peaks[:3])
    npeaks=len(peaks)
    initial_cen=peaks
    initial_amp=np.full(npeaks,20000.)
    initial_wid=np.full(npeaks,1.)
#    print(initial_cen)
#    print(initial_amp)
#    print(initial_wid)
    first_guess=np.full((npeaks,3),0.)
    for i in range(npeaks):
        first_guess[i,0]=initial_amp[i]
        first_guess[i,1]=initial_cen[i]
        first_guess[i,2]=initial_wid[i]
    first_guess=np.reshape(first_guess,3*npeaks)
#    print(first_guess)
    return first_guess


