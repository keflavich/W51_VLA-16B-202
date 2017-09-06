import numpy as np
from spectral_cube import SpectralCube
from astropy import units as u
import pyregion

regs = pyregion.open('recomb_cutouts.reg')

files = [
    "W51e1e8_QbandAarray_H51a.image.pbcor.fits",
    "W51e1e8_QbandAarray_H52a.image.pbcor.fits",
    "W51e1e8_QbandAarray_H53a.image.pbcor.fits",
    "W51e2w_QbandAarray_H51a.image.pbcor.fits",
    "W51e2w_QbandAarray_H52a.image.pbcor.fits",
    "W51e2w_QbandAarray_H53a.image.pbcor.fits",
    "W51North_QbandAarray_H51a.image.pbcor.fits",
    "W51North_QbandAarray_H52a.image.pbcor.fits",
    "W51North_QbandAarray_H53a.image.pbcor.fits",
]

for fn in files:
    cube = SpectralCube.read(fn)

    refvel = (42.95197*u.GHz if 'H53a' in fn else
              45.45372*u.GHz if 'H52a' in fn else
              48.1536*u.GHz if 'H51a' in fn else
              np.nan)
    if np.isnan(refvel):
        raise ValueError("Bad fn")

    for reg in regs:

        try:
            scube = (cube
                     .subcube_from_ds9region(pyregion.ShapeList([reg]))
                     .with_spectral_unit(u.km/u.s, velocity_convention='radio',
                                         rest_value=refvel))
        except ValueError as ex:
            if "derived subset" in str(ex):
                print("skipping {0} for {1}".format(reg, fn))
                continue
            else:
                print(ex)
                continue
            

        name = reg.attr[1]['text']

        scube[27:-27,:,:].write('recomb_cutouts/{0}_{1}'.format(name, fn),
                                overwrite=True)
