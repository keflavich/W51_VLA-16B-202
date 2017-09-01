from tasks import flagdata
vis='16B-202.sb32957824.eb33142274.57752.64119381944.ms'
flagdata(vis=vis, antenna='ea25', timerange='16:48:00~18:00:00', mode='manual',
         action='apply', )
flagdata(vis=vis, antenna='ea12', spw='46~48GHz', mode='manual',
         action='apply', )
flagdata(vis=vis, antenna='ea24', spw='44.15~44.55GHz', correlation='LL',
         mode='manual', action='apply', )
flagdata(vis=vis, antenna='ea12', spw='46~48GHz', mode='manual',
         action='apply', )

# B1D1: bad amplitudes in LL pol on ea03
flagdata(vis=vis, antenna='ea03', correlation='LL', spw='34~49', mode='manual',
         action='apply', )

# B2D2 bad amplitudes ea17 RR
flagdata(vis=vis, antenna='ea17', spw='50~64', correlation='RR', mode='manual',
         action='apply')
