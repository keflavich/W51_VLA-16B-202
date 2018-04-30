from astropy.io import fits
from astropy import wcs
import pylab as pl
import regions
import numpy as np
from astropy import units as u
import radio_beam

fns = {95*u.GHz: '/lustre/aginsbur/w51/2017.1.00293.S/2017.1.00293.S_2017_11_29T13_39_36.232/SOUS_uid___A001_X1290_X4/GOUS_uid___A001_X1290_X5/MOUS_uid___A001_X1290_X6/products/w51e2_sci.spw0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17_18_19.mfs.I.manual.image.tt0.pbcor.fits',
       42.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_42-43.image.tt0.pbcor.fits',
       43.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_43-44.image.tt0.pbcor.fits',
       44.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_44-45.image.tt0.pbcor.fits',
       45.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_45-46.image.tt0.pbcor.fits',
       46.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_46-47.image.tt0.pbcor.fits',
       47.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_47-48.image.tt0.pbcor.fits',
       48.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_48-49.image.tt0.pbcor.fits',
       49.5*u.GHz: 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcalLAST_49-50.image.tt0.pbcor.fits',
       13.5*u.GHz: 'W51Ku_BDarray_continuum_2048_both_uniform.hires.clean.image.fits',
       25*u.GHz: 'W51-25GHzcont-large-pb.map.image.fits',
       27*u.GHz: 'W51-27GHzcont-large-pb.map.image.fits',
       29*u.GHz: 'W51-29GHzcont-large-pb.map.image.fits',
       33*u.GHz: 'W51-33GHzcont-pb.map.image.fits',
       36*u.GHz: 'W51-36GHzcont-pb.map.image.fits',
      }

sed = {}
img = {}

fig = pl.figure(1)
fig.clf()

for ii,(frq,fn) in enumerate(fns.items()):
    fh = fits.open(fn)
    ww = wcs.WCS(fh[0].header).celestial
    beam = radio_beam.Beam.from_fits_header(fh[0].header)
    ppbeam = (beam.sr / (wcs.utils.proj_plane_pixel_area(ww)*u.deg**2)).decompose()
    jtok = beam.jtok(frq)
    pr0 = regions.read_ds9('e2w_ellipse.reg')[0].to_pixel(ww)
    pr0.width *= 2.5
    pr0.height *= 2.5
    msk = pr0.to_mask()
    weighted = msk.multiply(fh[0].data.squeeze())
    sed[frq] = (weighted.sum()/ppbeam)
    img[frq] = weighted
    print(frq, weighted.max() * jtok, jtok)

    ax = fig.add_subplot(4,4,ii+1)
    ax.imshow(weighted, origin='lower', interpolation='none')
    ax.set_title(frq)

fig2 = pl.figure(2)
fig2.clf()
ax = fig2.gca()

ax.plot(u.Quantity(list(sed.keys())), u.Quantity(list(sed.values())), 's')
