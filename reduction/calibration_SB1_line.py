"""
Calibration following https://casaguides.nrao.edu/index.php?title=EVLA_6cmWideband_Tutorial_SN2010FZ
https://casaguides.nrao.edu/index.php/EVLA_high_frequency_Spectral_Line_tutorial_-_IRC%2B10216-CASA4.5#Bandpass_and_Delay
"""

vis = '16B-202.sb32532587.eb32875589.57663.07622001157.ms'
line_vis = '16B-202.lines.ms'
refant = 'ea14'
fluxcal = '0137+331=3C48'
phasecal = 'J1922+1530'
source = 'W51e2w,W51 North'
spwrange = ""
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'
linespw = ",".join([str(x) for x in range(2,65) if x not in map(int, contspw.split(","))])
linespw = '3,11,20,21,27,33,38,40,41,43,46,61,18,23,42' # add 18, 23, 42 for OCS, H51a


split(vis=vis, outputvis=line_vis, datacolumn='data', spw=linespw)
flagdata(vis=line_vis, mode='unflag')
# flag 1st scan (non-science)
flagdata(vis=line_vis, flagbackup=T, mode='manual', scan='1')
#quack start of scans
flagdata(vis=line_vis, mode='quack', quackinterval=10.0, quackmode='beg')
# flag pre-pointing obs
flagdata(vis=line_vis, mode='manual', timerange='01:50:46.0~01:51:44.0')

setjy_dict = setjy(vis=line_vis, field=fluxcal, scalebychan=True, model='3C48_C.im',
                   usescratch=False, standard='Perley-Butler 2013')
print('setjy: ', setjy_dict)

# g1int, the flux cal's self-cal, flags out 50% of the data
# maybe we don't care, since we're doing literally nothing with the flux cal data
# now....
applycal(vis=line_vis,field=fluxcal,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1int','cal_cont_spws.G2'],
         gainfield=['','','','',fluxcal,fluxcal],
         interp=['','','nearest','nearest','nearest','nearest'],
         parang=False,calwt=False)

# G2 flags out 40%.  40% were already flagged for no clear reason.
applycal(vis=line_vis,field=phasecal,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1int','cal_cont_spws.G2',
                    'cal_cont_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','nearest','nearest',''],
         parang=False,calwt=False)

# again, G2 is the main culprit
applycal(vis=line_vis,field=source,
         gaintable=['cal_cont_spws.gaincurve','cal_cont_spws.K0',
                    'cal_cont_spws.B0','cal_cont_spws.G1inf','cal_cont_spws.G2',
                    'cal_cont_spws.F3inc'],
         gainfield=['','','','',phasecal,phasecal,phasecal],
         interp=['','','nearest','nearest','linear','linear',''],
         parang=False,calwt=False)



