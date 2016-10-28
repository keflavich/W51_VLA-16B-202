"""
Calibration following https://casaguides.nrao.edu/index.php?title=EVLA_6cmWideband_Tutorial_SN2010FZ
https://casaguides.nrao.edu/index.php/EVLA_high_frequency_Spectral_Line_tutorial_-_IRC%2B10216-CASA4.5#Bandpass_and_Delay
"""

vis = '16B-202.sb32532587.eb32875589.57663.07622001157.ms'
cont_vis = '16B-202.width8.continuum.ms'
refant = 'ea14'
fluxcal = '0137+331=3C48'
phasecal = 'J1922+1530'
source = 'W51e2w,W51 North'
spwrange = ""
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'

split(vis=vis, outputvis=cont_vis, datacolumn='data', spw=contspw,
      width=8)
flagdata(vis=cont_vis, mode='unflag')
# flag 1st scan (non-science)
flagdata(vis=cont_vis, flagbackup=T, mode='manual', scan='1')
#quack start of scans
flagdata(vis=cont_vis, mode='quack', quackinterval=10.0, quackmode='beg')
# flag pre-pointing obs
flagdata(vis=cont_vis, mode='manual', timerange='01:50:46.0~01:51:44.0')

setjy_dict = setjy(vis=cont_vis, field=fluxcal, scalebychan=True, model='3C48_C.im',
                   usescratch=False, standard='Perley-Butler 2013')
print('setjy: ', setjy_dict)

rmtables(['cal_cont_spws.G0','cal_cont_spws.K0','cal_cont_spws.antpos','cal_cont_spws.gaincurve','cal_cont_spws.G1inf'])
# no antenna offsets found....
# gencal(vis=cont_vis,caltable='cal_cont_spws.antpos',caltype='antpos',antenna='')
gencal(vis=cont_vis,caltable='cal_cont_spws.gaincurve',caltype='gc')
gencal(vis=cont_vis,caltable='cal_cont_spws.requantizer',caltype='rq')

# ea13 is mostly missing, ea21 is partly missing, ea26 is mostly missing
# (these antennae are on the same arm)
# ea27 is mostly missing
gaincal(vis=cont_vis,caltable='cal_cont_spws.G0', field=fluxcal,spw=spwrange,
        gaintable=['cal_cont_spws.gaincurve'],
        gaintype='G', refant=refant, calmode='p', solint='20s', minsnr=2.0,
        combine='scan')
# add in phasecal, so we can use phasecal for delaycal
gaincal(vis=cont_vis,caltable='cal_cont_spws.G0',
        gaintable=['cal_cont_spws.gaincurve'],
        field=phasecal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='10s',gaintype='G',calmode='p',append=True)

gaincal(vis=cont_vis,caltable='cal_cont_spws.K0',
        gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.G0'],
        field=phasecal, # previously used fluxcal, but we want brighter
        spw=spwrange, gaintype='K', refant=refant, combine='scan',
        solint='inf', minsnr=2)

# even with very permissive inputs, bandtype='B' results in major flagging
# ea13 is bad again, ea21 ea26 ea28 have no solutions, ea27 is missing some spws
# using the phasecal, this looks a lot better
bandpass(vis=cont_vis,caltable='cal_cont_spws.B0',
         gaintable=['cal_cont_spws.gaincurve',
                    'cal_cont_spws.G0','cal_cont_spws.K0'],
         field=phasecal,refant=refant,solnorm=False,
         fillgaps=4,
         minsnr=2,
         bandtype='BPOLY', combine='scan', solint='inf,8MHz')


# fluxcal: some solutions flagged (~1/3)
# ea04 is now flagged out...
# ea09 missing data
# ea13, ea21, ea26, ea27, ea28  totally flagged out
# ea15, ea17 mostly flagged out
gaincal(vis=cont_vis,caltable='cal_cont_spws.G1int',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0','cal_cont_spws.B0'],
        field=fluxcal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='20s',gaintype='G',calmode='p')

# phasecal: few solutions flagged (~1/34)
gaincal(vis=cont_vis,caltable='cal_cont_spws.G1int',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0','cal_cont_spws.B0'],
        field=phasecal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='int',gaintype='G',calmode='p',append=True)


# phasecal, inf... no complaints
gaincal(vis=cont_vis,caltable='cal_cont_spws.G1inf',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0','cal_cont_spws.B0'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',gaintype='G',calmode='p')

# fluxcal inf: only one complaint of 34.  Huh.
gaincal(vis=cont_vis, caltable='cal_cont_spws.G2',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0',
                   'cal_cont_spws.B0',
                   'cal_cont_spws.G1int'],
        gainfield=['','',phasecal,phasecal,fluxcal], # changed from fluxcal->phasecal b/c we changed which is being used
        interp=['','','nearest','nearest','nearest'],
        field=fluxcal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a')

# mostly minor?  But it looks like some antennae may have been flagged out
gaincal(vis=cont_vis, caltable='cal_cont_spws.G2',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0',
                   'cal_cont_spws.B0',
                   'cal_cont_spws.G1int'],
        gainfield=['','',phasecal,phasecal,phasecal], # changed from fluxcal->phasecal b/c we changed which is being used
        interp=['','','nearest','nearest','nearest'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',gaintype='G',calmode='a',append=True)


gaincal(vis=cont_vis, caltable='cal_cont_spws.G3',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0','cal_cont_spws.B0','cal_cont_spws.G1int'],
        gainfield=['','',fluxcal,fluxcal,fluxcal],
        interp=['','','nearest','nearest','nearest'],
        field=fluxcal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a')
#
gaincal(vis=cont_vis, caltable='cal_cont_spws.G3',
        gaintable=['cal_cont_spws.gaincurve',
                   'cal_cont_spws.K0','cal_cont_spws.B0','cal_cont_spws.G1int'],
        gainfield=['','',fluxcal,fluxcal,phasecal],
        interp=['','','nearest','nearest','nearest'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a',append=True)

myflux = fluxscale(vis=cont_vis,caltable='cal_cont_spws.G3',
                   fluxtable='cal_cont_spws.F3inc',reference=fluxcal,transfer=phasecal,
                   incremental=True)


# g1int, the flux cal's self-cal, flags out 50% of the data
# maybe we don't care, since we're doing literally nothing with the flux cal data
# now....
applycal(vis=cont_vis,field=fluxcal,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1int','cal_cont_spws.G2'],
         gainfield=['','','','',fluxcal,fluxcal],
         interp=['','','nearest','nearest','nearest','nearest'],
         parang=False,calwt=False)

# G2 flags out 40%.  40% were already flagged for no clear reason.
applycal(vis=cont_vis,field=phasecal,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1int','cal_cont_spws.G2',
                    'cal_cont_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','nearest','nearest',''],
         parang=False,calwt=False)

# again, G2 is the main culprit
applycal(vis=cont_vis,field=source,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1inf','cal_cont_spws.G2',
                    'cal_cont_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','linear','linear',''],
         parang=False,calwt=False)





# quicklook continuum images


imagename = 'W51e2w_QbandAarray_cont_spws_raw_continuum_cal_dirty'
clean(vis=cont_vis,
      imagename=imagename,
      field='W51e2w',
      spw=spwrange,
      weighting='briggs', imsize=[2560,2560], cell=['0.01 arcsec'],
      mode='mfs', threshold='20 mJy', niter=0,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)


imagename = 'W51e2w_QbandAarray_cont_spws_raw_continuum_cal_clean'
clean(vis=cont_vis,
      imagename=imagename,
      field='W51e2w',
      spw=spwrange,
      weighting='briggs', imsize=[2560,2560], cell=['0.01 arcsec'],
      mode='mfs', threshold='1.0 mJy', niter=10000,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)




imagename = 'W51North_QbandAarray_cont_spws_raw_continuum_cal_dirty'
clean(vis=cont_vis,
      imagename=imagename,
      field='W51 North',
      spw=spwrange,
      weighting='briggs', imsize=[2560,2560], cell=['0.01 arcsec'],
      mode='mfs', threshold='20 mJy', niter=0,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)


imagename = 'W51North_QbandAarray_cont_spws_raw_continuum_cal_clean'
clean(vis=cont_vis,
      imagename=imagename,
      field='W51 North',
      spw=spwrange,
      weighting='briggs', imsize=[2560,2560], cell=['0.01 arcsec'],
      mode='mfs', threshold='0.5 mJy', niter=10000,
      selectdata=True)
exportfits(imagename+".image", imagename+".image.fits", overwrite=True, dropdeg=True)
