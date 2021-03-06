vis = '16B-202.sb32957824.eb33105444.57748.63243916667.ms'
fields = ['1331+305=3C286', 'J1751+0939', 'J1922+1530', 'W51 North', 'W51e2w']
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'

# sb2 does not have ea12
antennae = ["ea01", "ea02", "ea03", "ea04", "ea05", "ea06", "ea07", "ea08",
            "ea09", "ea10", "ea11", "ea13", "ea14", "ea15", "ea16", "ea17",
            "ea18", "ea19", "ea20", "ea21", "ea22", "ea24", "ea25", "ea26",
            "ea27", "ea28",]

sb = 2

from diagnostic_plots import diagnostic_plots

diagnostic_plots(vis=vis, fields=fields, contspw=contspw, antennae=antennae,
                 sb=sb)
