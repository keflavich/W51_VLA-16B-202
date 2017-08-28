import numpy as np
from matplotlib.lines import Line2D
import datetime
import pylab as pl
from astropy import units as u
from astropy.io import fits
from astropy import wcs
from astropy.table import Table, Column
import regions

tbl = Table.read('../tables/sio_maser_fits.ipac', format='ascii.ipac')

north = fits.open('../FITS/W51_North_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal9.image.tt0.pbcor.fits')
reg = regions.read_ds9('../regions/siomaserbox.reg')[0]
reg2 = regions.read_ds9('../regions/siomaserboxzoom.reg')[0]

mywcs = wcs.WCS(north[0].header)
preg = reg.to_pixel(mywcs)
pmask = preg.to_mask()
pmask2 = reg2.to_pixel(mywcs).to_mask()

cutout = pmask.cutout(north[0].data)
mywcs.wcs.crpix[0] -= pmask.bbox.ixmin
mywcs.wcs.crpix[1] -= pmask.bbox.iymin

markerlist = [('SiO_v=0','d'),
              ('SiO_v=1','o'),
              ('SiO_v=2','s'),
              ('SiO_v=3','h'),
             ]
markerdict = dict(markerlist)

for line in ("SiO_v=0", "SiO_v=1", "SiO_v=2", "SiO_v=3", ):
    fig = pl.figure(1)
    fig.clf()

    ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=mywcs)
    ax.contour(cutout, colors='k')

    tick_fontsize=12
    ra = ax.coords['ra']
    ra.set_major_formatter('hh:mm:ss.sss')
    dec = ax.coords['dec']
    ra.set_axislabel("RA (J2000)", fontsize=pl.rcParams['axes.labelsize'],)
    dec.set_axislabel("Dec (J2000)", fontsize=pl.rcParams['axes.labelsize'], minpad=0)
    ra.ticklabels.set_fontsize(tick_fontsize)
    ra.set_ticks(exclude_overlapping=True)
    dec.ticklabels.set_fontsize(tick_fontsize)
    dec.set_ticks(exclude_overlapping=True)

    marker = markerdict[line]

    for epoch, color in enumerate(['r','g','b','m']):

            mask = (tbl['Epoch']==epoch) & (tbl['Line']==line)
            ax.errorbar(tbl[mask]['RA'],
                        tbl[mask]['Dec'],
                        linestyle='none',
                        color=color,
                        marker=marker,
                        xerr=tbl[mask]['eRA'],
                        yerr=tbl[mask]['eDec'],
                        transform=ax.get_transform('fk5'),
                       )
    ax.legend([Line2D((0,),(0,),color='r',linewidth=3),Line2D((0,),(0,),color='g',linewidth=3),Line2D((0,),(0,),color='b',linewidth=3), Line2D((0,),(0,),color='m',linewidth=3),
               # Line2D((0,),(0,),color='k',marker='d',linestyle='none'),
               # Line2D((0,),(0,),color='k',marker='o',linestyle='none'),
               # Line2D((0,),(0,),color='k',marker='s',linestyle='none'),
               # Line2D((0,),(0,),color='k',marker='h',linestyle='none'),
              ],
              ['Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', ],
              loc='upper left',)


    ax.axis([pmask2.bbox.ixmin-pmask.bbox.ixmin,
             pmask2.bbox.ixmax-pmask.bbox.ixmin,
             pmask2.bbox.iymin-pmask.bbox.iymin,
             pmask2.bbox.iymax-pmask.bbox.iymin])
    ax.set_aspect('equal')

    fig.savefig("../figures/masers_on_continuum_epochs_{0}.pdf".format(line),
                bbox_inches='tight')



for epoch in range(4):
    fig = pl.figure(1)
    fig.clf()

    ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=mywcs)
    ax.contour(cutout, colors='k')

    tick_fontsize=12
    ra = ax.coords['ra']
    ra.set_major_formatter('hh:mm:ss.sss')
    dec = ax.coords['dec']
    ra.set_axislabel("RA (J2000)", fontsize=pl.rcParams['axes.labelsize'],)
    dec.set_axislabel("Dec (J2000)", fontsize=pl.rcParams['axes.labelsize'], minpad=0)
    ra.ticklabels.set_fontsize(tick_fontsize)
    ra.set_ticks(exclude_overlapping=True)
    dec.ticklabels.set_fontsize(tick_fontsize)
    dec.set_ticks(exclude_overlapping=True)

    for (line, marker),color,zorder in zip(markerlist, ['r','g','b','m'], [10,5,1,10]):

            mask = (tbl['Epoch']==epoch) & (tbl['Line']==line)
            ax.errorbar(tbl[mask]['RA'],
                        tbl[mask]['Dec'],
                        linestyle='none',
                        color=color,
                        marker=marker,
                        zorder=zorder,
                        xerr=tbl[mask]['eRA'],
                        yerr=tbl[mask]['eDec'],
                        transform=ax.get_transform('fk5'),
                       )
    ax.legend([#Line2D((0,),(0,),color='r',linewidth=3),Line2D((0,),(0,),color='g',linewidth=3),Line2D((0,),(0,),color='b',linewidth=3), Line2D((0,),(0,),color='m',linewidth=3),
               Line2D((0,),(0,),color='r',marker='d',linestyle='none'),
               Line2D((0,),(0,),color='g',marker='o',linestyle='none'),
               Line2D((0,),(0,),color='b',marker='s',linestyle='none'),
               Line2D((0,),(0,),color='m',marker='h',linestyle='none'),
              ],
              #['Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', ],
              ("SiO v=0", "SiO v=1", "SiO v=2", "SiO v=3", ),
              loc='upper left',)


    ax.axis([pmask2.bbox.ixmin-pmask.bbox.ixmin,
             pmask2.bbox.ixmax-pmask.bbox.ixmin,
             pmask2.bbox.iymin-pmask.bbox.iymin,
             pmask2.bbox.iymax-pmask.bbox.iymin])
    ax.set_aspect('equal')

    fig.savefig("../figures/masers_on_continuum_epoch{0}.pdf".format(epoch+1),
                bbox_inches='tight')




for epoch in (1,2,3,4):
    for line in ('SiO_v=1', 'SiO_v=2', 'SiO_v=3'):
        fig = pl.figure(2)
        fig.clf()

        ax = fig.add_axes([0.15, 0.1, 0.7, 0.8], projection=mywcs)
        ax.contour(cutout, colors='k')

        tick_fontsize=12
        ra = ax.coords['ra']
        ra.set_major_formatter('hh:mm:ss.sss')
        dec = ax.coords['dec']
        ra.set_axislabel("RA (J2000)", fontsize=pl.rcParams['axes.labelsize'],)
        dec.set_axislabel("Dec (J2000)", fontsize=pl.rcParams['axes.labelsize'], minpad=0)
        ra.ticklabels.set_fontsize(tick_fontsize)
        ra.set_ticks(exclude_overlapping=True)
        dec.ticklabels.set_fontsize(tick_fontsize)
        dec.set_ticks(exclude_overlapping=True)

        #epoch = 2
        #line = 'SiO_v=2'
        marker = 'o'

        mask = (tbl['Epoch']==epoch) & (tbl['Line']==line)
        for row in tbl[mask]:
            ax.errorbar(row['RA'],
                        row['Dec'],
                        linestyle='none',
                        color=pl.cm.jet((row['Velocity']-50)/20.),
                        marker=marker,
                        xerr=row['eRA'],
                        yerr=row['eDec'],
                        transform=ax.get_transform('fk5'),
                       )

        ax.axis([pmask2.bbox.ixmin-pmask.bbox.ixmin,
                 pmask2.bbox.ixmax-pmask.bbox.ixmin,
                 pmask2.bbox.iymin-pmask.bbox.iymin,
                 pmask2.bbox.iymax-pmask.bbox.iymin])
        ax.set_aspect('equal')
        sm = pl.cm.ScalarMappable(cmap=pl.cm.jet, norm=pl.Normalize(50,70))
        sm._A = []
        cb = fig.colorbar(sm,
                          fig.add_axes([0.90, 0.1, 0.05, 0.8]))
        cb.set_label("Velocity (km/s)")

        fig.savefig("../figures/masers_on_continuum_velocities_epoch{0}_{1}.pdf".format(epoch, line),
                    bbox_inches='tight')


epochs = ['02-Oct-2016', '26-Dec-2016', '30-Dec-2016', '07-Jan-2017']
epochs = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in epochs]

tbl.add_column(Column(name='Date', data=[epochs[row['Epoch']] for row in tbl], dtype='datetime64[s]'))

times = [datetime.datetime.utcfromtimestamp((dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
         for dt64 in tbl['Date']]

cho_jtok = 11.6 * u.Jy / u.K
cho_data = {'091202': {'v=1': {'amp': 0.12*u.K, 'vel': 48.8*u.km/u.s}, 'v=2': {'amp': 0.08*u.K, 'vel': 48.5*u.km/u.s}},
            '100227': {'v=1': {'amp': 0.11*u.K, 'vel': 48.6*u.km/u.s}, 'v=2': {'amp': 0.09*u.K, 'vel': 37.7*u.km/u.s}},
            '100323': {'v=1': {'amp': 0.13*u.K, 'vel': 48.5*u.km/u.s}, 'v=2': {'amp': 0.07*u.K, 'vel': 68.2*u.km/u.s}},
            '100513': {'v=1': {'amp': 0.10*u.K, 'vel': 48.0*u.km/u.s}, 'v=2': {'amp': 0.00*u.K, 'vel': np.nan*u.km/u.s}},
            '100622': {'v=1': {'amp': 0.13*u.K, 'vel': 48.5*u.km/u.s}, 'v=2': {'amp': 0.00*u.K, 'vel': np.nan*u.km/u.s}},
           }

for linename in ('v=1', 'v=2'):
    fig = pl.figure(3)
    fig.clf()
    ax = fig.gca()

    mask = tbl['Line'] == 'SiO_{0}'.format(linename)
    for time,row,mm in zip(times, tbl, mask):
        if mm:
            ax.errorbar(time, row['Amplitude'], yerr=row['eAmplitude'],
                        linestyle='none', color=pl.cm.jet((row['Velocity']-50)/20.),
                        marker='o',
                       )
    for date, values in cho_data.items():
        ax.errorbar(datetime.datetime.strptime(date, '%y%m%d'),
                    (values[linename]['amp']*cho_jtok).value,
                    linestyle='none',
                    color=pl.cm.jet((values[linename]['vel'].value-50)/20.),
                    marker='o',
                   )

    fig.savefig('../figures/maser_timeseries_{0}.png'.format(linename))
