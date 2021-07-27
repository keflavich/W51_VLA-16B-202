# field_list = ('W51e2w', 'W51 North')
if 'field_list' not in locals():
    raise ValueError("Set field_list")
if isinstance(field_list, str):
    raise TypeError("Make field list a list or tuple")

import os

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


vis = [
       '19A-254.sb36820841.eb37001660.58697.18583002315.ms',
       '19A-254.sb36820841.eb37052030.58707.15631115741.ms'
      ]
contspw = '11,12,14,16,17,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,39,40,45,46,49,51,52,57,58,59,60,61'


cont_vis = 'continuum_concatenated.ms'

if not os.path.exists(cont_vis):
    for cvis in vis:
        if not os.path.exists("cont_"+cvis):
            split(vis=cvis, outputvis="cont_"+cvis, spw=contspw)

    cont_vises = ["cont_"+vv for vv in vis]

    assert concat(vis=cont_vises, concatvis=cont_vis)

selfcal_vis = cont_vis

imsize = 10000

mask = None

thresholds = {'W51e2w': (0.7,0.5,0.3,0.2,0.1),
              'W51 North': (0.4,0.3,0.2,0.1),
             }

for field in field_list:

    # must iterate over fields separately because the mask name is being set and reset
    for iternum, nterms, threshold, caltype, calmode, solint, mask in [(0, 2, '{0} mJy','phase','p', 'inf', 'w51e2w_kband_selfcal0_mask.crtf'), # first attempt was 5; too conservative
                                                                       (1, 2, '{0} mJy','phase','p', 'inf', 'w51e2w_kband_selfcal0_mask.crtf'),
                                                                       (2, 2, '{0} mJy','phase','p', 'inf', 'w51e2w_kband_selfcal0_mask.crtf'),
                                                                       (3, 2, '{0} mJy','phase','p', 'int', 'w51e2w_kband_selfcal0_mask.crtf'),
                                                                       (4, 2, '{0} mJy','phase','p', 'int', 'w51e2w_kband_selfcal0_mask.crtf'),
                                                                      ]:
        threshold = threshold.format(thresholds[field][iternum])
        field_nospace = field.replace(" ","_")
        output = myimagebase = imagename = '{0}_KbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_selfcal{1}'.format(field_nospace, iternum)

        if os.path.exists(imagename+".image.tt0"):
            #mask = 'clean_mask_{0}_{1}.mask'.format(iternum, field_nospace)
            print("Skipping {0}".format(imagename))
            continue

        for ttsuffix in ('.tt0', '.tt1', '.tt2'):
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'image{tt}.pbcor',
                           'alpha', ):
                rmfile = "{0}.{1}".format(output, suffix).format(tt=ttsuffix)
                if os.path.exists(rmfile):
                    print("Removing {0}".format(rmfile))
                    os.system('rm -rf {0}'.format(rmfile))

        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=0.0,
               imsize=imsize,
               cell=['0.015 arcsec'],
               threshold=threshold,
               cyclefactor=3,
               niter=100000,
               gridder='standard',
               #wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='modelcolumn',
               scales=[0,3,9],
               nterms=nterms,
               selectdata=True,
               mask=mask,
              )
        makefits(myimagebase)

        caltable = '{2}_{1}_{0}.cal'.format(field_nospace, iternum, caltype)
        rmtables([caltable])
        if 'phase' in caltype:
            gaincal(vis=selfcal_vis, caltable=caltable, solint=solint,
                    combine='spw',
                    gaintype='G', field=field, calmode=calmode)
        elif 'bandpass' in caltype:
            bandpass(vis=selfcal_vis, caltable=caltable,
                     solint='{0},16ch'.format(solint), combine='scan',
                     field=field, refant='ea07')

        applycal(vis=selfcal_vis, field=field, gaintable=[caltable],
                 interp="linear", applymode='calonly', calwt=True)

        # cleanimage = myimagebase+'.image.tt0'
        # ia.open(cleanimage)
        # ia.calcmask(mask=cleanimage+" > {0}".format(float(threshold.split()[0])/1000),
        #             name='clean_mask_iter{0}_{1}'.format(iternum, field_nospace))

        # ia.close()
        # makemask(mode='copy', inpimage=cleanimage,
        #          inpmask=cleanimage+":clean_mask_iter{0}_{1}".format(iternum, field_nospace),
        #          output='clean_mask_{0}_{1}.mask'.format(iternum, field_nospace),
        #          overwrite=True)
        # mask = 'clean_mask_{0}_{1}.mask'.format(iternum, field_nospace)
        # exportfits(mask, mask+'.fits', dropdeg=True, overwrite=True)

        ia.open(myimagebase+".model.tt0")
        stats = ia.statistics()
        if stats['min'] < 0:
            print("Negative model component encountered: {0}.".format(stats['min']))
        print(stats)
        ia.close()



    # final iteration: smaller pixels

    output = myimagebase = imagename = '{0}_KbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_selfcal{1}_final'.format(field_nospace, iternum)

    if os.path.exists(imagename+".image.tt0"):
        #mask = 'clean_mask_{0}_{1}.mask'.format(iternum, field_nospace)
        print("Skipping {0}".format(imagename))
        continue

    for ttsuffix in ('.tt0', '.tt1', '.tt2'):
        for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                       'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                       'image{tt}.pbcor',
                       'alpha', ):
            rmfile = "{0}.{1}".format(output, suffix).format(tt=ttsuffix)
            if os.path.exists(rmfile):
                print("Removing {0}".format(rmfile))
                os.system('rm -rf {0}'.format(rmfile))

    tclean(vis=selfcal_vis,
           imagename=imagename,
           field=field,
           spw='',
           weighting='briggs',
           robust=0.0,
           imsize=15000,
           cell=['0.01 arcsec'],
           threshold=threshold,
           cyclefactor=3,
           niter=100000,
           gridder='standard',
           #wprojplanes=32,
           specmode='mfs',
           deconvolver='mtmfs',
           outframe='LSRK',
           savemodel='modelcolumn',
           scales=[0,3,9],
           nterms=nterms,
           selectdata=True,
           mask=mask,
          )
    makefits(myimagebase)
