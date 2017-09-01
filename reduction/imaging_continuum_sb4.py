vis = '16B-202.sb32957824.eb33234671.57760.62953023148.ms'
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'
execfile('flagging_sb4.py')
sbnum = 4

from imaging_continuum_sb import imaging_continuum_sb

imaging_continuum_sb(vis=vis, contspw=contspw, sbnum=sbnum)
