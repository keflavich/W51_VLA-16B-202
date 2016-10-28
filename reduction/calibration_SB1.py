"""
Calibration following https://casaguides.nrao.edu/index.php?title=EVLA_6cmWideband_Tutorial_SN2010FZ
https://casaguides.nrao.edu/index.php/EVLA_high_frequency_Spectral_Line_tutorial_-_IRC%2B10216-CASA4.5#Bandpass_and_Delay
"""

vis = '16B-202.sb32532587.eb32875589.57663.07622001157.ms'
full_vis = vis
refant = 'ea14'
fluxcal = '0137+331=3C48'
phasecal = 'J1922+1530'
source = 'W51e2w,W51 North'
spwrange = ""
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'
linespw = ",".join([str(x) for x in range(2,65) if x not in map(int, contspw.split(","))])
linespw = '3,11,20,21,27,33,38,40,41,43,46,61,18,23,42' # add 18, 23, 42 for OCS, H51a

contspwlist = list(map(int, contspw.split(',')))
def findprev(val):
    while val not in contspwlist:
        val = val - 1
        if val <= 0:
            return 0
    return val
spwmap = [(x) if x in contspwlist else (findprev(x)) for x in range(0,65)]

#split(vis=vis, outputvis=full_vis, datacolumn='data', spw='2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19',
#      width=8)
flagdata(vis=full_vis, mode='unflag')
# flag 1st scan (non-science)
flagdata(vis=full_vis, flagbackup=T, mode='manual', scan='1')
#quack start of scans
flagdata(vis=full_vis, mode='quack', quackinterval=10.0, quackmode='beg')
# flag pre-pointing obs
flagdata(vis=full_vis, mode='manual', timerange='01:50:46.0~01:51:44.0')

setjy_dict = setjy(vis=full_vis, field=fluxcal, scalebychan=True, model='3C48_C.im',
                   usescratch=False, standard='Perley-Butler 2013')
print('setjy: ', setjy_dict)

rmtables(['cal_all_spws.G0',
          'cal_all_spws.K0',
          'cal_all_spws.antpos',
          'cal_all_spws.gaincurve',
          'cal_all_spws.G1inf',
          'cal_all_spws.G2',
          'cal_all_spws.G3',
          'cal_all_spws.requantizer',
         ])
# no antenna offsets found....
# gencal(vis=full_vis,caltable='cal_all_spws.antpos',caltype='antpos',antenna='')
gencal(vis=full_vis,caltable='cal_all_spws.gaincurve',caltype='gc')
gencal(vis=full_vis,caltable='cal_all_spws.requantizer',caltype='rq')

# ea13 is mostly missing, ea21 is partly missing, ea26 is mostly missing
# (these antennae are on the same arm)
# ea27 is mostly missing
gaincal(vis=full_vis,caltable='cal_all_spws.G0', field=fluxcal,spw=spwrange,
        gaintable=['cal_all_spws.gaincurve'],
        gaintype='G', refant=refant, calmode='p', solint='20s', minsnr=2.0,
        combine='scan')
# add in phasecal, so we can use phasecal for delaycal
gaincal(vis=full_vis,caltable='cal_all_spws.G0',
        gaintable=['cal_all_spws.gaincurve'],
        field=phasecal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='10s',gaintype='G',calmode='p',append=True)

gaincal(vis=full_vis,caltable='cal_all_spws.K0',
        gaintable=['cal_all_spws.gaincurve','cal_all_spws.G0'],
        field=phasecal, # previously used fluxcal, but we want brighter
        spw=spwrange, gaintype='K', refant=refant, combine='scan',
        solint='inf', minsnr=2)

# even with very permissive inputs, bandtype='B' results in major flagging
# ea13 is bad again, ea21 ea26 ea28 have no solutions, ea27 is missing some spws
# using the phasecal, this looks a lot better
bandpass(vis=full_vis,caltable='cal_all_spws.B0',
         gaintable=['cal_all_spws.gaincurve',
                    'cal_all_spws.G0','cal_all_spws.K0'],
         field=phasecal,refant=refant,solnorm=False,
         fillgaps=8,
         minsnr=2,
         bandtype='BPOLY', combine='scan', solint='inf,1MHz')


# fluxcal: some solutions flagged (~1/3)
# ea04 is now flagged out...
# ea09 missing data
# ea13, ea21, ea26, ea27, ea28  totally flagged out
# ea15, ea17 mostly flagged out
gaincal(vis=full_vis,caltable='cal_all_spws.G1int',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0','cal_all_spws.B0'],
        field=fluxcal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='20s',gaintype='G',calmode='p')

# phasecal: few solutions flagged (~1/34)
gaincal(vis=full_vis,caltable='cal_all_spws.G1int',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0','cal_all_spws.B0'],
        field=phasecal,refant=refant,solnorm=False,
        spw=spwrange,
        solint='int',gaintype='G',calmode='p',append=True)


# phasecal, inf... no complaints
gaincal(vis=full_vis,caltable='cal_all_spws.G1inf',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0','cal_all_spws.B0'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',gaintype='G',calmode='p')

# fluxcal inf: only one complaint of 34.  Huh.
gaincal(vis=full_vis, caltable='cal_all_spws.G2',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0',
                   'cal_all_spws.B0',
                   'cal_all_spws.G1int'],
        gainfield=['','',phasecal,phasecal,fluxcal], # changed from fluxcal->phasecal b/c we changed which is being used
        interp=['','','nearest','nearest','nearest'],
        field=fluxcal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a')

# mostly minor?  But it looks like some antennae may have been flagged out
gaincal(vis=full_vis, caltable='cal_all_spws.G2',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0',
                   'cal_all_spws.B0',
                   'cal_all_spws.G1int'],
        gainfield=['','',phasecal,phasecal,phasecal], # changed from fluxcal->phasecal b/c we changed which is being used
        interp=['','','nearest','nearest','nearest'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',gaintype='G',calmode='a',append=True)


gaincal(vis=full_vis, caltable='cal_all_spws.G3',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0','cal_all_spws.B0','cal_all_spws.G1int'],
        gainfield=['','',fluxcal,fluxcal,fluxcal],
        interp=['','','nearest','nearest','nearest'],
        field=fluxcal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a')
#
gaincal(vis=full_vis, caltable='cal_all_spws.G3',
        gaintable=['cal_all_spws.gaincurve',
                   'cal_all_spws.K0','cal_all_spws.B0','cal_all_spws.G1int'],
        gainfield=['','',fluxcal,fluxcal,phasecal],
        interp=['','','nearest','nearest','nearest'],
        field=phasecal,refant=refant,solnorm=F,
        spw=spwrange,
        solint='inf',combine='scan',gaintype='G',calmode='a',append=True)

myflux = fluxscale(vis=full_vis,caltable='cal_all_spws.G3',
                   fluxtable='cal_all_spws.F3inc',reference=fluxcal,transfer=phasecal,
                   incremental=True)


# g1int, the flux cal's self-cal, flags out 50% of the data
# maybe we don't care, since we're doing literally nothing with the flux cal data
# now....
applycal(vis=full_vis,field=fluxcal,
         gaintable=['cal_all_spws.gaincurve','cal_all_spws.K0',
                    'cal_all_spws.B0','cal_all_spws.G1int','cal_all_spws.G2'],
         gainfield=['','','','',fluxcal,fluxcal],
         interp=['','','nearest','nearest','nearest','nearest'],
         parang=False,calwt=False)

# G2 flags out 40%.  40% were already flagged for no clear reason.
applycal(vis=full_vis,field=phasecal,
         gaintable=['cal_all_spws.gaincurve','cal_all_spws.K0',
                    'cal_all_spws.B0','cal_all_spws.G1int','cal_all_spws.G2',
                    'cal_all_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','nearest','nearest',''],
         parang=False,calwt=False)

# again, G2 is the main culprit
applycal(vis=full_vis,field=source,
         gaintable=['cal_all_spws.gaincurve','cal_all_spws.K0',
                    'cal_all_spws.B0','cal_all_spws.G1inf','cal_all_spws.G2',
                    'cal_all_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','linearPD,linear','linearPD,linear',''],
         spwmap=[[], [], [], spwmap, spwmap, spwmap],
         parang=False,calwt=False)
