def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', dropdeg=True, overwrite=True)
    exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', dropdeg=True, overwrite=True)


# SB1 may have terrible calibration (is 2x as faint, and wasn't appropriately
# statwt'd b/c it didn't go through the pipeline)
vis = [#'16B-202.sb32532587.eb32875589.57663.07622001157.ms',
       '16B-202.sb32957824.eb33105444.57748.63243916667.ms',
       '16B-202.sb32957824.eb33142274.57752.64119381944.ms',
       '16B-202.sb32957824.eb33234671.57760.62953023148.ms',
      ]
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'

for cvis in vis:
    split(vis=cvis, outputvis="cont_"+cvis, spw=contspw)

cont_vises = ["cont_"+vv for vv in vis]
cont_vis = 'continuum_concatenated.ms'

concat(vis=cont_vises, concatvis=cont_vis)

selfcal_vis = cont_vis

imsize = 7680

for iternum, threshold, caltype, calmode in [(0,'2.5 mJy','phase','p'), # first attempt was 5; too conservative
                                             (1,'1.5 mJy','phase','p'),
                                             (2,'1.0 mJy','phase','p'),
                                             (3,'1.0 mJy','ampphase','ap'),
                                             (4,'0.5 mJy','ampphase','ap'),
                                             (5,'0.25 mJy','ampphase','ap'),
                                            ]:
    for field in ('W51e2w', 'W51 North'):
        field_nospace = field.replace(" ","_")
        output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal{1}'.format(field_nospace, iternum)

        for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                       'image', 'residual'):
            os.system('rm -rf {0}.{1}'.format(output, suffix))

        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=0.0,
               imsize=imsize,
               cell=['0.01 arcsec'],
               threshold=threshold,
               niter=100000,
               gridder='wproject',
               wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='modelcolumn',
               scales=[0,3,9],
               nterms=2,
               selectdata=True)
        makefits(myimagebase)

        caltable = '{2}_{1}_{0}.cal'.format(field_nospace, iternum, caltype)
        rmtables([caltable])
        gaincal(vis=selfcal_vis, caltable=caltable, solint='int',
                gaintype='G', field=field, calmode=calmode)

        applycal(vis=selfcal_vis, field=field, gaintable=[caltable],
                 interp="linear", applymode='calonly', calwt=False)

for field in ('W51e2w', 'W51 North'):
    output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal{1}'.format(field_nospace, iternum+1)

    for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                   'image', 'residual'):
        os.system('rm -rf {0}.{1}'.format(output, suffix))

    tclean(vis=selfcal_vis,
           imagename=imagename,
           field=field,
           spw='',
           weighting='briggs',
           robust=0.0,
           imsize=imsize,
           cell=['0.01 arcsec'],
           threshold=threshold,
           niter=10000,
           gridder='wproject',
           wprojplanes=32,
           specmode='mfs',
           deconvolver='mtmfs',
           outframe='LSRK',
           savemodel='modelcolumn',
           nterms=2,
           selectdata=True)
    makefits(myimagebase)
