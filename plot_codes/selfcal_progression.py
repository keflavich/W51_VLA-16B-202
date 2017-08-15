import numpy as np
import astropy
from astropy import coordinates, units as u
from astropy.io import fits
from astropy import wcs
from astropy.nddata import Cutout2D
import astropy.visualization
import pylab as pl

import warnings
warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning, append=True)

def hide_labels(ax):
    lon = ax.coords['RA']
    lat = ax.coords['Dec']

    lon.set_ticks_visible(False)
    lon.set_ticklabel_visible(False)
    lat.set_ticks_visible(False)
    lat.set_ticklabel_visible(False)
    lon.set_axislabel('')
    lat.set_axislabel('')


filename_template = "{source}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal{selfcaliter}.image.tt0.pbcor.fits"

coords = {'W51e2w': coordinates.SkyCoord('19:23:43.910 +14:30:34.500', frame='fk5',
                                         unit=(u.hour, u.deg)),
          'W51_North': coordinates.SkyCoord('19:23:40.050 +14:31:05.467',
                                            frame='fk5', unit=(u.hour, u.deg)),
          'W51d2': coordinates.SkyCoord('19:23:39.818 +14:31:04.799',
                                        frame='fk5', unit=(u.hour, u.deg))
         }

vmin = -0.0001
vmax = {'W51e2w': 0.02,
        'W51_North': 0.002,
        'W51d2': 0.02,
       }
namelist = [('W51e2w','W51e2w'),
            ('W51_North','W51_North'),
            ('W51_North','W51d2'),
           ]

for fsourcename, sourcename in namelist:
    fig = pl.figure(1, figsize=(24,6), dpi=75)
    fig.clf()
    for iternum in range(0,13):
        try:
            fh = fits.open(filename_template.format(source=fsourcename,
                                                    selfcaliter=iternum))
        except FileNotFoundError:
            print("Did not find "
                  "{0}".format(filename_template.format(source=fsourcename,
                                                        selfcaliter=iternum)))
            continue

        mywcs = wcs.WCS(fh[0].header)
        center = coords[sourcename]
        size = 1*u.arcsec
        cutout_im = Cutout2D(fh[0].data, position=center, size=size, wcs=mywcs)

        std = astropy.stats.mad_std(fh[0].data[np.isfinite(fh[0].data)])
        peak = cutout_im.data.max()
        print("iter{3} Peak = {0}, RMS = {1}, S/N = {2}"
              .format(peak,
                      std,
                      peak/std,
                      iternum))

        ax = fig.add_subplot(2,7,iternum+1, projection=cutout_im.wcs)

        im = ax.imshow(cutout_im.data*1e3, cmap='gray',
                       norm=astropy.visualization.simple_norm(fh[0].data,
                                                              stretch='asinh',
                                                              min_cut=vmin*1e3,
                                                              max_cut=vmax[sourcename]*1e3,
                                                              asinh_a=0.001),
                       transform=ax.get_transform(cutout_im.wcs),
                       origin='lower',)

        hide_labels(ax)


    x1 = ax.bbox.x1 / (fig.bbox.x1-fig.bbox.x0)
    # y0 = ax.bbox.y0 / (fig.bbox.y1-fig.bbox.y0)
    y0 = ax.bbox.y0 / (fig.bbox.y1-fig.bbox.y0)
    # single-ax version height = (ax.bbox.y1-ax.bbox.y0) / (fig.bbox.y1-fig.bbox.y0)
    height = (ax.bbox.y1-ax.bbox.y0) / (fig.bbox.y1-fig.bbox.y0)
    cax_bbox = [x1 + 0.02, y0, 0.02, height]
    cb = pl.colorbar(mappable=im, cax=fig.add_axes(cax_bbox))
    cb.set_label('mJy/beam')

    fig.subplots_adjust(wspace=0, hspace=0)
    fig.canvas.draw()

    fig.savefig("selfcal_progression_{0}.pdf".format(sourcename),
                bbox_inches='tight', dpi=300)
