import numpy as np
from spectral_cube import SpectralCube
from astropy import units as u
from astropy.io import fits
from astropy.modeling import models, fitting
import gaussfitter
from astropy.table import Table

tbl = Table(names=['Epoch','Line','Velocity','Amplitude','eAmplitude','RA','Dec','eRA','eDec',],
            #unit=[None, None, 'km/s', 'Jy', 'Jy', 'deg', 'deg', 'deg', 'deg'],
            dtype=[int, 'S10', float, float, float, float, float, float, float])


for line, freq, spw in (
                        ('SiO_v=2', 42.82057, 40),
                        ('SiO_v=1', 43.12209, 43),
                        ('SiO_v=0', 43.42385, 46),
                        ('SiO_v=3', 42.51937, 38),
                       ):
    for epoch in range(4):

        output = imagename = myimagebase = 'W51North_QbandAarray_{0}_epoch{1}'.format(line, epoch)
        cube = SpectralCube.read('../FITS/siocutouts/{0}_cutout.image.pbcor.fits'.format(output))

        # get the celestial coordinates
        _, ycoords, xcoords = cube.world[0,:,:]

        # pixel scale to convert pixels to central coords
        pixscale = np.abs(cube.wcs.celestial.pixel_scale_matrix[0,0])

        rms = cube.std()
        print(rms)

        gfits = {}

        fit_p = fitting.LevMarLSQFitter()

        for velo,chan in zip(cube.spectral_axis, cube):
            if chan.max() > 5*rms:
                ycen, xcen = np.unravel_index(np.argmax(chan), dims=cube.shape[1:])

                x_stddev = 1.0 * pixscale
                y_stddev = 1.0 * pixscale
                p_init = models.Gaussian2D(amplitude=chan.max(),
                                           x_mean=xcoords[ycen,xcen],
                                           y_mean=ycoords[ycen,xcen],
                                           x_stddev=x_stddev,
                                           y_stddev=y_stddev)

                params = fit_p(p_init, xcoords.ravel(), ycoords.ravel(),
                               chan.ravel(), weights=1./rms**2)

                params = fit_p(params, xcoords.ravel(), ycoords.ravel(),
                               chan.ravel(), weights=1./rms**2)

                print(line,epoch,velo,params.amplitude,params.x_mean,params.y_mean)

                tbl.add_row([epoch, line, velo,
                             params.amplitude,
                             fit_p.fit_info['param_cov'][0,0]**0.5*u.Jy,
                             params.x_mean,
                             params.y_mean,
                             fit_p.fit_info['param_cov'][1,1]**0.5*u.deg,
                             fit_p.fit_info['param_cov'][2,2]**0.5*u.deg,]
                           )

                ## alternative approach
                #params,eparams = gaussfitter.gaussfit(chan.value, error=rms.value,
                #                                      return_error=True, vheight=False)
                ## get rid of "height" parameter
                #params = params[1:]
                #eparams = eparams[1:]

                #print(line,epoch,velo,params)

                #gfits[(line, epoch, velo)] = \
                #             ([params[0],
                #               np.interp(params[2], range(xcoords.shape[1]), xcoords[0,:]),
                #               np.interp(params[1], range(ycoords.shape[0]), ycoords[:,0]),
                #               params[3] * pixscale,
                #               params[4] * pixscale,
                #               params[5],],
                #               [eparams[0],
                #                eparams[1]*pixscale,
                #                eparams[2]*pixscale,
                #                eparams[3]*pixscale,
                #                eparams[4]*pixscale,
                #                eparams[5]])
tbl.write('../tables/sio_maser_fits.ipac', format='ascii.ipac', overwrite=True)
