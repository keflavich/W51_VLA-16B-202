import numpy as np
import astropy
from astropy import coordinates, units as u
from astropy.io import fits
from astropy import wcs
from astropy.nddata import Cutout2D
import pylab as pl

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

coords = {'W51e2': coordinates.SkyCoord('19:23:43.910 +14:30:34.500', frame='fk5',
                                        unit=(u.hour, u.deg)),
          'W51_North': coordinates.SkyCoord('19:23:40.000 +14:31:05.000',
                                            frame='fk5', unit=(u.hour, u.deg))
         }

vmin = -0.0001
vmax = 0.002

for sourcename in ("W51e2w", "W51_North"):
    fig = pl.figure(1)
    fig.clf()
    for iternum in range(0,13):
        fh = fits.open(filename_template.format(source=sourcename,
                                                selfcaliter=iternum))

        mywcs = wcs.WCS(fh[0].header)
        center = coords[sourcename]
        size = 5*u.arcsec
        cutout_im = Cutout2D(fh[0].data, position=center, size=size, wcs=mywcs)

        ax = pl.subplot(7,2,iternum+1)

        im = ax.imshow(cutout_im.data*1e3, cmap='gray',
                       norm=astropy.visualization.simple_norm(fh[0].data,
                                                              stretch='asinh',
                                                              min_cut=vmin*1e3,
                                                              max_cut=vmax*1e3,
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


    fig.savefig("selfcal_progression_{0}.pdf".format(sourcename),
                bbox_inches='tight', dpi=300)
