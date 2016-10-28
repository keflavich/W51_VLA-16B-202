vis = '16B-202.sb32532587.eb32875589.57663.07622001157.ms'
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'


"""
Normal, shallow tclean imaging of both fields
"""
output = myimagebase = imagename = 'W51e2w_QbandAarray_cont_spws_raw_continuum_cal_clean'
tclean(vis=vis,
       imagename=imagename,
       field='W51e2w',
       spw=contspw,
       weighting='briggs',
       robust=0.0,
       imsize=[2560,2560],
       cell=['0.01 arcsec'],
       threshold='1.0 mJy',
       niter=10000,
       gridder='mosaic',
       specmode='mfs',
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

output = myimagebase = imagename = 'W51North_QbandAarray_cont_spws_raw_continuum_cal_clean'
tclean(vis=vis,
       imagename=imagename,
       field='W51 North',
       spw=contspw,
       weighting='briggs',
       robust=0.0,
       imsize=[2560,2560],
       cell=['0.01 arcsec'],
       threshold='1.0 mJy',
       niter=10000,
       gridder='mosaic',
       specmode='mfs',
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


"""
nterms=2, spectral slope cleaning
"""
output = myimagebase = imagename = 'W51e2w_QbandAarray_cont_spws_continuum_cal_clean_2terms'
tclean(vis=vis,
       imagename=imagename,
       field='W51e2w',
       spw=contspw,
       weighting='briggs',
       robust=0.0,
       imsize=[2560,2560],
       cell=['0.01 arcsec'],
       threshold='1.0 mJy',
       niter=10000,
       gridder='mosaic',
       specmode='mfs',
       outframe='LSRK',
       savemodel='none',
       nterms=2,
       selectdata=True)

# not sure what to use hereimpbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
# not sure what to use hereexportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
# not sure what to use hereexportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
# not sure what to use hereexportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)

# for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
#                'image', 'residual'):
#     os.system('rm -rf {0}.{1}'.format(output, suffix))

output = myimagebase = imagename = 'W51North_QbandAarray_cont_spws_continuum_cal_clean_2terms'
tclean(vis=vis,
       imagename=imagename,
       field='W51 North',
       spw=contspw,
       weighting='briggs',
       robust=0.0,
       imsize=[2560,2560],
       cell=['0.01 arcsec'],
       threshold='1.0 mJy',
       niter=10000,
       gridder='mosaic',
       specmode='mfs',
       outframe='LSRK',
       savemodel='none',
       nterms=2,
       selectdata=True)

# not sure what to use impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
# not sure what to use exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
# not sure what to use exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
# not sure what to use exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)
# not sure what to use 
# not sure what to use for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
# not sure what to use                'image', 'residual'):
# not sure what to use     os.system('rm -rf {0}.{1}'.format(output, suffix))
