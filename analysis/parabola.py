import os
from astropy.io import fits
from astropy import wcs
from astropy import units as u
import regions
import numpy as np
import pylab as pl

if not os.path.exists('W51e2w_ALMAB3_cutout.fits'):
    fh = fits.open('/Users/adam/work/w51/alma/FITS/longbaseline/w51e2_sci.spw0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17_18_19.mfs.I.manual.image.tt0.pbcor.fits')
    ww = wcs.WCS(fh[0].header).celestial
    pr0 = regions.read_ds9('/Users/adam/work/w51/vla_q/regions/e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    img_95ghz = msk.multiply(fh[0].data.squeeze())

    header = fh[0].header
    ww_cutout = ww[msk.bbox.slices]
    header.update(ww_cutout.to_header())
    fits.PrimaryHDU(data=img_95ghz, header=header).writeto('W51e2w_ALMAB3_cutout.fits', overwrite=True)
else:
    img_95ghz = fits.getdata('W51e2w_ALMAB3_cutout.fits')

if not os.path.exists('W51e2w_ALMAB6_cutout.fits'):
    fh = fits.open('/Users/adam/work/w51/alma/FITS/longbaseline/W51e2_cont_briggsSC_tclean_allspw.image.fits')
    ww = wcs.WCS(fh[0].header).celestial
    pr0 = regions.read_ds9('/Users/adam/work/w51/vla_q/regions/e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    img_224ghz = msk.multiply(fh[0].data.squeeze())

    header = fh[0].header
    ww_cutout = ww[msk.bbox.slices]
    header.update(ww_cutout.to_header())
    fits.PrimaryHDU(data=img_224ghz, header=header).writeto('W51e2w_ALMAB6_cutout.fits', overwrite=True)
else:
    img_224ghz = fits.getdata('W51e2w_ALMAB6_cutout.fits')


if not os.path.exists('W51e2w_VLA_Q_cutout.fits'):
    fh = fits.open('/Users/adam/work/w51/vla_q/FITS/W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal9.image.tt0.pbcor.fits')
    ww = wcs.WCS(fh[0].header).celestial
    pr0 = regions.read_ds9('/Users/adam/work/w51/vla_q/regions/e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    img_45ghz = msk.multiply(fh[0].data.squeeze())

    header = fh[0].header
    ww_cutout = ww[msk.bbox.slices]
    header.update(ww_cutout.to_header())
    fits.PrimaryHDU(data=img_45ghz, header=header).writeto('W51e2w_VLA_Q_cutout.fits', overwrite=True)
else:
    img_45ghz = fits.getdata('W51e2w_VLA_Q_cutout.fits')

cy,cx = 127,42
angle = (180+315) * u.deg

xx = np.linspace(0,50,1000)
yy = xx**2 / 28

xx_, yy_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [xx,yy])
xx2_, yy2_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [-xx,yy])

pl.figure(3)
pl.clf()
pl.imshow(img_95ghz, origin='lower', interpolation='none')
pl.plot(xx_+cx,yy_+cy, linewidth=0.5, color='w', linestyle='--')
pl.plot(xx2_+cx,yy2_+cy, linewidth=0.5, color='w', linestyle='--')

data_on_path = img_95ghz[(yy_+cy).astype('int'), (xx_+cx).astype('int')]
data_on_path2 = img_95ghz[(yy_+cy).astype('int'), (-xx_+cx).astype('int')]
prj_dist = (xx**2+yy**2)**0.5

pl.figure(4)
pl.clf()
pl.plot(prj_dist, data_on_path)
pl.plot(prj_dist, data_on_path2)
core = data_on_path[:10].mean()
profile = (core*(prj_dist/prj_dist[250])**-0.1 * (prj_dist >= prj_dist[250])/10.
           + core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])
           )
profile = core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])

pl.plot(prj_dist, profile)


cy,cx = 62,23

xx = np.linspace(0,25,1000)
yy = xx**2 / 17

xx_, yy_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [xx,yy])
xx2_, yy2_ = np.dot([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]], [-xx,yy])

pl.figure(1)
pl.clf()
pl.imshow(img_45ghz, origin='lower', interpolation='none')
pl.plot(xx_+cx,yy_+cy, linewidth=0.5, color='w', linestyle='--')
pl.plot(xx2_+cx,yy2_+cy, linewidth=0.5, color='w', linestyle='--')

data_on_path = img_45ghz[(yy_+cy).astype('int'), (xx_+cx).astype('int')]
data_on_path2 = img_45ghz[(yy_+cy).astype('int'), (-xx_+cx).astype('int')]
prj_dist = (xx**2+yy**2)**0.5

pl.figure(2)
pl.clf()
pl.plot(prj_dist, data_on_path)
pl.plot(prj_dist, data_on_path2)
core = data_on_path[:10].mean()
profile = (core*(prj_dist/prj_dist[250])**-0.1 * (prj_dist >= prj_dist[250])/10.
           + core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])
           )
profile = core * (1-(prj_dist/prj_dist[580])**2) * (prj_dist<=prj_dist[580])

pl.plot(prj_dist, profile)
