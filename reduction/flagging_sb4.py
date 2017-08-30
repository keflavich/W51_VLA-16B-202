vis='16B-202.sb32957824.eb33234671.57760.62953023148.ms'
flagdata(vis=vis, antenna='ea25', timerange='16:12:00~16:23:00',  mode='manual', action='apply', )
flagdata(vis=vis, antenna='ea14', spw='34~59', mode='manual', action='apply')
flagdata(vis=vis, antenna='ea22', spw='50', correlation='LL', mode='manual',
         action='apply')
flagdata(vis=vis, antenna='ea11', spw='42~43GHz', correlation='LL', mode='manual',
         action='apply')
