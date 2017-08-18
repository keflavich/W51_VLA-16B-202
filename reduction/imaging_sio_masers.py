import os

#line_vis = '16B-202.lines.ms'
vis = ['16B-202.sb32532587.eb32875589.57663.07622001157.ms', # skip this one b/c not calibrated
       '16B-202.sb32957824.eb33105444.57748.63243916667.ms',
       '16B-202.sb32957824.eb33142274.57752.64119381944.ms',
       '16B-202.sb32957824.eb33234671.57760.62953023148.ms',
      ]
line_vis = vis

for line, freq, spw in (
                        ('SiO_v=2', 42.82057, 40),
                        ('SiO_v=1', 43.12209, 43),
                        ('SiO_v=0', 43.42385, 46),
                        ('SiO_v=3', 42.51937, 38),
                       ):
    for epoch,vis in enumerate(line_vis):


        output = imagename = myimagebase = 'W51North_QbandAarray_{0}_epoch{1}'.format(line, epoch)

        if not os.path.exists(imagename+".image.pbcor.fits"):
            os.system('rm -rf ' + output + '*/')

            # no need to specify velocity channels because it's so narrow
            tclean(vis=vis,
                   imagename=imagename,
                   field='W51 North',
                   phasecenter='J2000 19h23m40.050 +14d31m05.467',
                   spw='{0}'.format(spw),
                   weighting='briggs',
                   robust=0.0,
                   imsize=[200,200],
                   cell=['0.005 arcsec'],
                   threshold='50 mJy',
                   reffreq='{0}GHz'.format(freq),
                   niter=1000,
                   gridder='standard',
                   specmode='cube',
                   outframe='LSRK',
                   savemodel='none',
                   selectdata=True)
            impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
            exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
            exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
            exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)

            for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                           'image', 'residual'):
                os.system('rm -rf {0}.{1}'.format(output, suffix))

