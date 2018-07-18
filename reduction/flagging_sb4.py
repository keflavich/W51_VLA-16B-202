from tasks import flagdata
vis='16B-202.sb32957824.eb33234671.57760.62953023148.ms'
flagdata(vis=vis, antenna='ea25', timerange='16:12:00~16:23:00',  mode='manual', action='apply', )
flagdata(vis=vis, antenna='ea14', spw='34~59', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea22', spw='50', correlation='LL', mode='manual',
         action='apply')
flagdata(vis=vis, antenna='ea11', spw='42~43GHz', correlation='LL', mode='manual',
         action='apply')
flagdata(vis=vis, antenna='ea03', spw='42~44GHz', correlation='LL', mode='manual',
         action='apply')
flagdata(vis=vis, antenna='ea17', spw='45~46GHz', correlation='RR',
         mode='manual', action='apply')

# bad phases in baseband B2D2
flagdata(vis=vis, antenna='ea01', spw='50~64', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea26', spw='50~64', mode='manual', action='apply')

# appears to have bad amplitudes when doing selfcal
flagdata(vis=vis, antenna='ea01', spw='18~33', mode='manual', action='apply')

# spw50 is bad for the calibrators for ea24 & ea12
flagdata(vis=vis, antenna='ea12,ea24', spw='50', mode='manual', action='apply')
