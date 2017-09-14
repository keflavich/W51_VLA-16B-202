
# Notes for my own future reference: this is how you select data as you would in, e.g., plotms
from taskinit import mstool, msmdtool, tbtool

ms = mstool()
msmd = msmdtool()
tb = tbtool()

ms.open('continuum_concatenated_incremental.ms')
ms.msselect({'field':'W51e2w', 'antenna':'ea07', 'spw':'40'})
data = ms.getdata2(['amplitude', 'model_amplitude', 'corrected_amplitude', 'time', 'uvdist'])

data['corrected_amplitude'][0,64,:50]
data['amplitude'][0,64,:50]

amps = data['amplitude'].mean(axis=1)
modamps = data['model_amplitude'].mean(axis=1)
corramps = data['corrected_amplitude'].mean(axis=1)

msmd.open('continuum_concatenated_incremental.ms')
antnames = dict(zip(msmd.antennaids(), msmd.antennanames()))
antids = dict(zip(msmd.antennanames(), msmd.antennaids()))


tb.open('amp_0_W51e2w.cal')
caldata = tb.getcol('CPARAM')
caldataea07pol1 = caldata[0,0,:][tb.getcol('ANTENNA1') == antids['ea07']]
caldataea07pol2 = caldata[1,0,:][tb.getcol('ANTENNA1') == antids['ea07']]
time = tb.getcol('TIME')
trunctime = time[tb.getcol('ANTENNA1') == antids['ea07']]

import pylab as pl
pl.figure(5).clf()

pl.plot(data['time'], amps[0,:],'r,', zorder=100)
pl.plot(data['time'], corramps[0,:],'b,', zorder=100)
pl.plot(trunctime, caldataea07pol1, '-')

pl.figure(6).clf()
pl.plot(amps[0,:], corramps[0,:], ',')

# CASA <107>: data['corrected_amplitude'][0,64,:50]
# Out[107]:
# array([  1.69480658,   0.43195304,   1.67787671,   1.18837261,
#          1.02634859,   1.20447636,   2.74002862,   0.38599899,
#          1.35817456,   1.714661  ,   0.66638207,   0.83096397,
#          0.21277297,   1.65768516,   1.36873472,   1.20742619,
#          0.4319576 ,   0.20891276,   1.28528607,   7.88275433,
#          1.42366099,   1.41124368,   0.54489815,   2.51553106,
#          0.48172712,   1.28474486,   1.03982306,   0.30572888,
#          1.09383035,   1.24217343,   1.7345295 ,   1.1307435 ,
#          1.25737977,   0.64590186,   0.85527778,   0.23288976,
#          0.51941407,   1.79689765,   2.45769787,   1.40475905,
#          1.06468666,   1.27297592,   2.02189112,   1.69107938,
#         13.21118164,   0.75052673,   1.41372693,   0.67022479,
#          0.98968971,   0.98809171])
# 
# CASA <108>: data['amplitude'][0,64,:50]
# Out[108]:
# array([  1.69480658,   0.43195304,   1.67787671,   1.18837261,
#          1.02634859,   1.20447636,   2.74002862,   0.38599899,
#          1.35817456,   1.714661  ,   0.66638207,   0.83096397,
#          0.21277297,   1.65768516,   1.36873472,   1.20742619,
#          0.4319576 ,   0.20891276,   1.28528607,   7.88275433,
#          1.42366099,   1.41124368,   0.54489815,   2.51553106,
#          0.48172712,   1.28474486,   1.03982306,   0.30572888,
#          1.09383035,   1.24217343,   1.7345295 ,   1.1307435 ,
#          1.25737977,   0.64590186,   0.85527778,   0.23288976,
#          0.51941407,   1.79689765,   2.45769787,   1.40475905,
#          1.06468666,   1.27297592,   2.02189112,   1.69107938,
#         13.21118164,   0.75052673,   1.41372693,   0.67022479,
#          0.98968971,   0.98809171])
