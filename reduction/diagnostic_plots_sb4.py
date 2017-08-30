vis='16B-202.sb32957824.eb33234671.57760.62953023148.ms'
fields = ['1331+305=3C286', 'J1751+0939', 'J1922+1530', 'W51 North', 'W51e2w']
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'

antennae = ["ea01", "ea02", "ea03", "ea04", "ea05", "ea06", "ea07", "ea08",
            "ea09", "ea10", "ea11", "ea13", "ea14", "ea15", "ea16", "ea17",
            "ea18", "ea19", "ea20", "ea21", "ea22", "ea24", "ea25", "ea26",
            "ea27", "ea28",]
sb = 4

for corr in ('RR','LL'):
    for field in fields:
        plotms(vis=vis, field=field, xaxis='uvdist', yaxis='amp', avgtime='100000',
               spw=contspw,
               correlation=corr,
               avgchannel='1024', coloraxis='ant1', showgui=False,
               plotfile='sb{sb}_amp_vs_uvdist_{0}_{1}.png'.format(field.replace(" ","_"),
                                                                  corr,
                                                                  sb=sb),
               overwrite=True)

        for antenna in antennae:
            plotms(vis=vis, field=field, antenna=antenna, xaxis='freq', yaxis='amp', avgtime='100000',
                   spw=contspw,
                   correlation=corr,
                   avgchannel='8', coloraxis='ant2', showgui=False,
                   plotfile='sb{sb}_amp_vs_freq_{0}_{1}_{2}.png'.format(field.replace(" ","_"),
                                                                        antenna,
                                                                        corr,
                                                                        sb=sb),
                   overwrite=True)

    for antenna in antennae:
        plotms(vis=vis, antenna=antenna, xaxis='time', yaxis='amp', avgtime='30',
               spw=contspw,
               correlation=corr,
               avgchannel='1024', coloraxis='ant2', showgui=False,
               plotfile='sb{sb}_amp_vs_time_{0}_{1}.png'.format(antenna, corr,
                                                                sb=sb),
               overwrite=True)


