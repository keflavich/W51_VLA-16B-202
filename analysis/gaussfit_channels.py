import numpy as np
from spectral_cube import SpectralCube
from astropy.io import fits
from astropy.modeling import models, fitting


cube = SpectralCube.read('../FITS/W51North_QbandAarray_SiO_v=1_velocitycutout_small.fits')

# get the celestial coordinates
_, ycoords, xcoords = cube.world[0,:,:]

# pixel scale to convert pixels to central coords
pixscale = np.abs(cube.wcs.celestial.pixel_scale_matrix[0,0])

rms = cube.std()

gfits = {}

fit_p = fitting.LevMarLSQFitter()

for velo,chan in zip(cube.spectral_axis, cube):
    if chan.max() > 3*rms:
        ycen, xcen = np.unravel_index(np.argmax(chan), dims=cube.shape[1:])

        x_stddev = 1.0 * pixscale
        y_stddev = 1.0 * pixscale
        p_init = models.Gaussian2D(amplitude=chan.max(),
                                   x_mean=xcoords[ycen,xcen],
                                   y_mean=ycoords[ycen,xcen],
                                   x_stddev=x_stddev,
                                   y_stddev=y_stddev)

        params = fit_p(p_init, xcoords, ycoords, chan)

        gfits[velo] = params
