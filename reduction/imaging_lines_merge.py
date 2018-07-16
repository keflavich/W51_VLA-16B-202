import os
"""
OCS 4-3 = 48.6516043 GHz A1/C1 
HC3N 5-4 = 45.490316 GHz B1/D1
H51a = 48.153597 GHz
H52a = 45.453719 GHz
H53a = 42.951967 GHz
CCS 43-32 = 45.379029 GHz B1/D1
CH3OH = 48.372467 A1/C1 overlap
CH3OH = 48.376889 A1/C1 overlap
"""

#line_vis = '16B-202.lines.ms'
vis = [#'16B-202.sb32532587.eb32875589.57663.07622001157.ms', # skip this one b/c not calibrated
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
                        ('CH3OH707-616', 44.06941, 50), # broadband window
                        ('NH3_17-17', 42.83992, 41),
                        ('NH3_18-18', 46.1227, 3),
                        ('NH3_19-19', 49.83768, 33),
                        ('H2CO_413-414', 48.28455, 20),
                        ('CS_1-0', 48.990957, 27), # missed the line by a lot.
                        ('PN_1-0', 46.99026, 11),
                        # ('OCS_4-3', 48.6516043, 23), # not observed in line mode
                        #45.490316
                        ('HC3N_5-4', 45.490316, 61), # missed the line by a lot
                        ('H52a', 45.453719, 61),
                        ('CH3OH_1-0a', 48.372467, 21),
                        ('CH3OH_1-0b', 48.376889, 21),
                        ('CCS_43-32', 45.379029, 61), # barely in-band
                        ('H51a', 48.153597, 18), # not observed in line mode
                        ('H53a', 42.951967, 42), # not observed in line mode
                        ('Unknown_spw13', 47.274, 13), # not observed in line mode
                       ):

    print("Starting {0}".format(line))

    output = imagename = myimagebase = 'W51betweene1ande8_QbandAarray_{0}'.format(line)

    if not os.path.exists(imagename+".image.pbcor.fits"):
        os.system('rm -rf ' + output + '*/')

        print(imagename)

        tclean(vis=line_vis,
               imagename=imagename,
               field='W51e2w',
               phasecenter='J2000 19h23m43.908 +14d30m31.105',
               spw='{0}'.format(spw),
               weighting='briggs',
               robust=0.0,
               imsize=[640,640],
               cell=['0.01 arcsec'],
               threshold='50 mJy',
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

    print("Completed {0}".format(line))


    output = imagename = myimagebase = 'W51e2w_QbandAarray_{0}'.format(line)

    if not os.path.exists(imagename+".image.pbcor.fits"):
        os.system('rm -rf ' + output + '*/')

        print(imagename)

        tclean(vis=line_vis,
               imagename=imagename,
               field='W51e2w',
               spw='{0}'.format(spw),
               weighting='briggs',
               robust=0.0,
               imsize=[512,512],
               cell=['0.01 arcsec'],
               threshold='50 mJy',
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



    output = imagename = myimagebase = 'W51North_QbandAarray_{0}'.format(line)

    if not os.path.exists(imagename+".image.pbcor.fits"):
        os.system('rm -rf ' + output + '*/')

        print(imagename)

        tclean(vis=line_vis,
               imagename=imagename,
               field='W51 North',
               phasecenter='J2000 19h23m39.933 +14d31m05.28',
               spw='{0}'.format(spw),
               weighting='briggs',
               robust=0.0,
               imsize=[768,768],
               cell=['0.01 arcsec'],
               threshold='50 mJy',
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



    output = imagename = myimagebase = 'W51e1e8_QbandAarray_{0}'.format(line)

    if not os.path.exists(imagename+".image.pbcor.fits"):
        os.system('rm -rf ' + output + '*/')

        print(imagename)

        tclean(vis=line_vis,
               imagename=imagename,
               field='W51e2w',
               phasecenter='J2000 19h23m43.818 +14d30m27.082',
               spw='{0}'.format(spw),
               weighting='briggs',
               robust=0.0,
               imsize=[640,640],
               cell=['0.01 arcsec'],
               threshold='50 mJy',
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

    print("Completed {0}".format(line))

# full-field imaging of selected lines
for field in ('W51 North', 'W51e2w'):
    line, frequency, spw = ('CH3OH707-616', 44.06941, 50)
    output = imagename = myimagebase = '{1}_QbandAarray_{0}_fullfield'.format(line, field.replace(" ",""))

    spw = '50:81~99'

    if not os.path.exists(imagename+".image.pbcor.fits"):
        os.system('rm -rf ' + output + '*/')

        print(imagename)

        tclean(vis=line_vis,
               imagename=imagename,
               field=field,
               spw=spw,
               weighting='briggs',
               robust=0.0,
               imsize=[8000,8000],
               cell=['0.01 arcsec'],
               threshold='20 mJy', # 20 is about e2w...
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
