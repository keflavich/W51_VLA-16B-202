"""
There is a pointing offset between the ALMA and VLA data.  This code is
intended to measure that offset.
"""
from astropy.io import fits
from astropy import coordinates
from astropy import units as u
from gaussfit_catalog import gaussfit_catalog
import paths
import regions
from astropy import wcs
import warnings

warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning, append=True)

w51north_vla = (paths.dpath('W51_North_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal9.image.tt0.pbcor.fits'))
w51north_alma = (paths.dpath('alma/W51n.cont.image.allEB.fits'))

regs = regions.read_ds9(paths.rpath('w51north_protostars.reg'))

reg = [r for r in regs if r.meta['text'] == '{1}'][0]

fit_vla = gaussfit_catalog(w51north_vla,
                           [regions.PointSkyRegion(coordinates.SkyCoord('19:23:40.117 +14:31:05.779',
                                                                        frame='fk5',
                                                                        unit=(u.hour,u.deg)), meta={'text':'1'})],
                           radius=0.2*u.arcsec,
                           max_offset_in_beams=4, max_radius_in_beams=1.2,
                           savepath='./', prefix='vla_source1_fit')['1']
fit_alma = gaussfit_catalog(w51north_alma, [reg], radius=0.1*u.arcsec, savepath='./', prefix='alma_source1_fit')['1']

coord_vla = coordinates.SkyCoord(fit_vla['center_x'], fit_vla['center_y'])
coord_alma = coordinates.SkyCoord(fit_alma['center_x'], fit_alma['center_y'])

offset = (coord_vla.separation(coord_alma).to(u.arcsec))
print(offset)
assert (offset > 0.005*u.arcsec) and (offset < 0.006*u.arcsec)

vlacrd_reg = regions.PointSkyRegion(coord_vla)
almacrd_reg = regions.PointSkyRegion(coord_alma)

def correct_header_to_vla(header):
    w = wcs.WCS(header)

    pixcrd = vlacrd_reg.to_pixel(w)

    header['CRPIX1'] = pixcrd.center.x
    header['CRPIX2'] = pixcrd.center.y
    header['CRVAL1'] = coord_vla.ra.deg
    header['CRVAL2'] = coord_vla.dec.deg

    return header

def correct_header_to_alma(header):
    w = wcs.WCS(header)

    pixcrd = almacrd_reg.to_pixel(w)

    header['CRPIX1'] = float(pixcrd.center.x)
    header['CRPIX2'] = float(pixcrd.center.y)
    header['CRVAL1'] = coord_alma.ra.deg
    header['CRVAL2'] = coord_alma.dec.deg

    return header
