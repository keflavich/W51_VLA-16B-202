from matplotlib.lines import Line2D
import pylab as pl
from astropy.io import fits
from astropy import wcs
from astropy.table import Table
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

for epoch, color in enumerate(['r','g','b','m']):
    for line, marker in [('SiO_v=0','d'),
                         ('SiO_v=1','o'),
                         ('SiO_v=2','s'),
                         ('SiO_v=3','h'),
                        ]:

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
           Line2D((0,),(0,),color='k',marker='d',linestyle='none'),
           Line2D((0,),(0,),color='k',marker='o',linestyle='none'),
           Line2D((0,),(0,),color='k',marker='s',linestyle='none'),
           Line2D((0,),(0,),color='k',marker='h',linestyle='none'),
          ],
          ['Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', "SiO v=0", "SiO v=1", "SiO v=2", "SiO v=3", ],
           loc='upper left',)


ax.axis([pmask2.bbox.ixmin-pmask.bbox.ixmin,
         pmask2.bbox.ixmax-pmask.bbox.ixmin,
         pmask2.bbox.iymin-pmask.bbox.iymin,
         pmask2.bbox.iymax-pmask.bbox.iymin])
ax.set_aspect('equal')

fig.savefig("../figures/masers_on_continuum_epochs.pdf", bbox_inches='tight')



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

epoch = 2
line = 'SiO_v=2'
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

fig.savefig("../figures/masers_on_continuum_velocities.pdf", bbox_inches='tight')
