import numpy as np

import regions
import radio_beam
from astropy import units as u
from astropy import log
from astropy import wcs
from astropy.stats import mad_std
from astropy.io import fits
from astropy.table import Table,Column

import paths
#import masscalc

def photometry(data, mywcs, regs, beam, alphamap=None, alphaerrmap=None,
               parsuffix=''):
    results = {}
    for ii,reg in enumerate(regs):
        if 'text' not in reg.meta:
            name = str(ii)
        else:
            name = reg.meta['text'].strip("{}")

        # all regions are points: convert them to 0.5" circles
        phot_reg = regions.CircleSkyRegion(center=reg.center, radius=0.5*u.arcsec)
        pixreg = phot_reg.to_pixel(mywcs)

        bgreg = regions.CircleSkyRegion(center=reg.center, radius=1.5*u.arcsec).to_pixel(mywcs)

        log.info("Name={0} color={1}".format(name, reg.visual['color']))

        mask = pixreg.to_mask()
        cutout = mask.cutout(data) * mask.data

        # how do I make an annulus?
        bgmask = bgreg.to_mask()
        
        # manualannulus
        diff = bgmask.shape[0]-mask.shape[0]
        bgm = bgmask.data.astype('bool')
        bgm[int(diff/2):-int(diff/2), int(diff/2):-int(diff/2)] ^= mask.data.astype('bool')
        assert bgm.sum() == bgmask.data.sum() - mask.data.sum()

        bgcutout = bgmask.cutout(data) * bgm


        results[name] = {'peak'+parsuffix: cutout.max(),
                         'sum'+parsuffix: cutout.sum(),
                         'bgrms'+parsuffix: bgcutout.std(),
                         'bgmad'+parsuffix: mad_std(bgcutout),
                         'npix'+parsuffix: mask.data.sum(),
                         'beam_area'+parsuffix: beam.sr,
                         'RA'+parsuffix: reg.center.ra[0],
                         'Dec'+parsuffix: reg.center.dec[0],
                         'color'+parsuffix: reg.visual['color'],
                        }

        if alphamap is not None and alphaerrmap is not None:
            alphacutout = mask.cutout(alphamap) * mask.data
            alphaerrcutout = mask.cutout(alphaerrmap) * mask.data
            argmax = np.unravel_index(cutout.argmax(), cutout.shape)
            results[name]['alpha'] = alphacutout[argmax]
            results[name]['alphaerror'] = alphaerrcutout[argmax]

    return results


if __name__ == "__main__":
    regs = regions.read_ds9(paths.rpath('w51north_protostars.reg'))

    w51north_alma = fits.open(paths.dpath('alma/W51n.cont.image.allEB.fits'))
    w51north_vla = fits.open(paths.dpath('W51_North_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal9.image.tt0.pbcor.fits'))

    from determine_offset import correct_header_to_alma

    w51north_vla[0].header = correct_header_to_alma(w51north_vla[0].header)

    units = {'peak':u.Jy/u.beam,
             'sum':u.Jy/u.beam,
             'npix':u.dimensionless_unscaled,
             'beam_area':u.sr,
             'bgmad':u.Jy/u.beam,
             'peak_mass_20K':u.M_sun,
             'peak_col_20K':u.cm**-2,
             'peak_mass_40K':u.M_sun,
             'peak_col_40K':u.cm**-2,
             'RA': u.deg,
             'Dec': u.deg,
            }

    results_vla = photometry(w51north_vla[0].data.squeeze(),
                             wcs.WCS(w51north_vla[0].header), regs,
                             radio_beam.Beam.from_fits_header(w51north_vla[0].header),
                             parsuffix='.45GHz',
                            )
    results_alma = photometry(w51north_alma[0].data.squeeze(),
                              wcs.WCS(w51north_alma[0].header), regs,
                              radio_beam.Beam.from_fits_header(w51north_alma[0].header),
                              parsuffix='.226GHz',
                             )

    results = results_vla
    for key in results:
        results[key].update(results_alma[key])

    # invert the table to make it parseable by astropy...
    # (this shouldn't be necessary....)
    results_inv = {'name':{}}
    columns = {'name':[]}
    for k,v in results.items():
        results_inv['name'][k] = k
        columns['name'].append(k)
        for kk,vv in v.items():
            if kk in results_inv:
                results_inv[kk][k] = vv
                columns[kk].append(vv)
            else:
                results_inv[kk] = {k:vv}
                columns[kk] = [vv]

    for c in columns:
        if c.split(".")[0] in units:
            columns[c] = u.Quantity(columns[c], units[c.split(".")[0]])

    tbl = Table([Column(data=columns[k],
                        name=k)
                 for k in ['name'] + [x+suffix for x in ('RA', 'Dec', 'peak',
                                                         'sum',
                                                         'npix',
                                                         'beam_area', 'bgmad',
                                                         'color',
                                                        )
                                      for suffix in ('.45GHz','.226GHz')]])

    #peak_brightness = (tbl['peak']*u.beam).to(u.K,
    #                                          u.brightness_temperature(u.Quantity(tbl['beam_area']),
    #                                                                   masscalc.centerfreq))
    #tbl.add_column(Column(data=peak_brightness, name='peak_K', unit=u.K))

    #tbl.sort('peak_mass_40K')
    #tbl = tbl[::-1]
    #tbl.write(paths.tpath("continuum_photometry.ipac"), format='ascii.ipac',
    #          overwrite=True)
