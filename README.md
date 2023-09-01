# astronomical_data_reduction
repo for astronomical data reduction software, python notebooks to be used in M2 class at Observatoire astronomique de Strasbourg

Soft contains the software (mostly):
  - IMAGE:
    --Generation of master frames bias and flat
  - reduction of observed image
  - re-alignment of observed images to a common reference frame for stacking
      
  - SPECTRO:
  - also contains linelists from NIST for ThAr calibration lamp in the 6000-7000 Angstrom range
  - Generation of master frames bias and flat
  - => producing reduced uncalibrated spectra
  - Computation of a dispersion relation using arc lamp and line atlas
  - Application of dispersion relation to uncalibrated spectra
  - Analysis of spectra: gaussian line fitting

data contains OHP year 2011 data: 
  - photo for images, including offsets and flats, for OHP 120cm
  - spectro for OHP T152 Aurelie, including offsets, flats and ThAr lamp

License for this work is CC-by, i.e. creative commons, free to reuse and reproduce with obligation to credit author.
    
