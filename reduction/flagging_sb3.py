vis='16B-202.sb32957824.eb33142274.57752.64119381944.ms'
flagdata(vis=vis, antenna='ea25', timerange='16:48:00~18:00:00',
         mode='manual', action='apply', )
flagdata(vis=vis, antenna='ea12', spw='46~48GHz',
         mode='manual', action='apply', )
flagdata(vis=vis, antenna='ea24', spw='44.15~44.55GHz',
         corr='LL',
         mode='manual', action='apply', )

