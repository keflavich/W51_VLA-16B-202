from tasks import flagdata
vis = '16B-202.sb32957824.eb33105444.57748.63243916667.ms'
# the amplitudes look bad for these low frequencies
flagdata(vis=vis, antenna='ea05', spw='34~44', mode='manual', action='apply')
# amps start dipping after this time (pointing floppy?)
flagdata(vis=vis, antenna='ea25', timerange='16:55:12~17:00:00', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea07', timerange='15:00:00~15:30:00', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea17', spw='50~64', correlation='RR', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea04', spw='45.4~46GHz', correlation='RR', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea24', spw='44.0~44.6GHz', correlation='LL', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea27', spw='18~33', correlation='LL', mode='manual', action='apply')

# bad phases in baseband A2C2 and B2D2
flagdata(vis=vis, antenna='ea01', spw='50~64', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea01', spw='18~33', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea26', spw='50~64', mode='manual', action='apply')

# these are regions where the two polarizations diverge in their poln solutions
#flagdata(vis=vis, antenna='ea04', polarization='1', spw='2~17', mode='manual', action='apply')
#flagdata(vis=vis, antenna='ea04', polarization='1', spw='2~32', mode='manual', action='apply')
#flagdata(vis=vis, antenna='ea03', polarization='', spw='18~32', mode='manual', action='apply')
