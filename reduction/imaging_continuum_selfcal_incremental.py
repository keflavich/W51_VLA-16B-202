import numpy as np
from astropy.io import fits
import pyregion
import os
from taskinit import msmdtool, iatool
from split import split
from concat import concat
from bandpass import bandpass
from makemask import makemask
from gaincal import gaincal
from applycal import applycal
from tclean import tclean
from exportfits import exportfits
from importfits import importfits
from impbcor import impbcor
ia = iatool()
msmd = msmdtool()

# field_list = ('W51e2w', 'W51 North')
if 'field_list' not in locals():
    raise ValueError("Set field_list")
if isinstance(field_list, str):
    raise TypeError("Make field list a list or tuple")

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
    if not os.path.exists("cont_"+cvis):
        split(vis=cvis, outputvis="cont_"+cvis, spw=contspw)

cont_vises = ["cont_"+vv for vv in vis]
cont_vis = 'continuum_concatenated_incremental.ms'

if not os.path.exists(cont_vis):
    assert concat(vis=cont_vises, concatvis=cont_vis)

selfcal_vis = cont_vis

imsize = 8000

caltables = []
calinfo = {}

thresholds = {'W51e2w': (5,2.5,1.5,1.0,1.0,1.0,0.5,0.25,0.25,0.25,0.25,0.25,0.25),
              'W51 North': (2.5,1.5,1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5,0.5,0.5,0.5),
             }


msmd.open(selfcal_vis)
nspws = msmd.nspw()
msmd.close()

for field in field_list:
    field_nospace = field.replace(" ","_")

    # create a dirty image for masking
    imagename = '{0}_QbandAarray_cont_spws_continuum_cal_dirty_2terms_robust0'.format(field_nospace)
    if not os.path.exists('{0}.image.tt0.pbcor.fits'.format(imagename)):
        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=0.0,
               imsize=imsize,
               cell=['0.01 arcsec'],
               threshold='1 Jy',
               niter=0,
               #gridder='wproject',
               gridder='standard',
               #wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='none',
               scales=[0,3,9],
               nterms=2,
               selectdata=True,
              )
        makefits(imagename)

    dirtyimage = imagename+'.image.tt0'
    ia.open(dirtyimage)
    ia.calcmask(mask=dirtyimage+" > 0.0025",
                name='dirty_mask_{0}'.format(field_nospace))

    ia.close()
    makemask(mode='copy', inpimage=dirtyimage,
             inpmask=dirtyimage+":dirty_mask_{0}".format(field_nospace),
             output='dirty_mask_{0}.mask'.format(field_nospace),
             overwrite=True)
    mask = 'dirty_mask_{0}.mask'.format(field_nospace)
    exportfits(mask, mask+'.fits', dropdeg=True, overwrite=True)

    exportfits(dirtyimage, dirtyimage+".fits", overwrite=True)
    reg = pyregion.open('cleanbox_regions_{0}.reg'.format(field_nospace))
    imghdu = fits.open(dirtyimage+".pbcor.fits")[0]
    imghdu2 = fits.open(dirtyimage+".fits")[0]
    mask = reg.get_mask(imghdu)[None, None, :, :]
    imghdu2.data = mask.astype('int16')
    imghdu2.header['BITPIX'] = 16
    imghdu2.writeto('cleanbox_mask_{0}.fits'.format(field_nospace), clobber=True)
    cleanbox_mask_image = 'cleanbox_mask_{0}.image'.format(field_nospace)
    importfits(fitsimage='cleanbox_mask_{0}.fits'.format(field_nospace),
               imagename=cleanbox_mask_image,
               overwrite=True)
    #ia.open(cleanbox_mask_image)
    #im = ia.adddegaxes(spectral=True, stokes='I', overwrite=True)
    #ia.close()
    #os.system('rm -rf {0}'.format(cleanbox_mask_image))
    #os.system('mv tmp_{0} {0}'.format(cleanbox_mask_image))
    ia.open(cleanbox_mask_image)
    ia.calcmask(mask=cleanbox_mask_image+" > 0.5",
                name='cleanbox_mask_{0}'.format(field_nospace))

    ia.close()
    cleanbox_mask = 'cleanbox_mask_{0}.mask'.format(field_nospace)
    makemask(mode='copy', inpimage=cleanbox_mask_image,
             inpmask=cleanbox_mask_image+":cleanbox_mask_{0}".format(field_nospace),
             output=cleanbox_mask,
             overwrite=True)

    mask = cleanbox_mask_image



    # must iterate over fields separately because the mask name is being set and reset
    for iternum, nterms, threshold, caltype, calmode, solint, combine in [(0, 2, '{0} mJy','amp','a', 'inf', 'spw',),
                                                                          (1, 2, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                          (2, 2, '{0} mJy','amp','a', '240s', 'scan',),
                                                                          (3, 2, '{0} mJy','ampphase','ap', 'inf', '',),
                                                                          (4, 2, '{0} mJy','phase','p', 'inf', '',),
                                                                          (5, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (6, 2, '{0} mJy','phase','p', 'int', '',),
                                                                          (7, 3, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                          (8, 3, '{0} mJy','ampphase', 'ap', 'inf', '',),
                                                                          (9, 3, '{0} mJy','ampphase', 'ap', 'inf', '',),
                                                                          #(5, 2, '{0} mJy','ampphase','ap', '120s', '',),
                                                                          #(6, 2, '{0} mJy','ampphase','ap', '120s', '',),
                                                                          #(7, 2, '{0} mJy','ampphase','ap', '120s', '',),
                                                                          #(8, 2, '{0} mJy','ampphase','ap', '30s', '',),
                                                                          #(9, 2, '{0} mJy','ampphase','ap', 'int', '',),
                                                                          #(10, 3, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                          #(11, 3, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                          #(12, 3, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                         ]:
        threshold = threshold.format(thresholds[field][iternum])
        output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_{2}terms_robust0_incrementalselfcal{1}'.format(field_nospace, iternum, nterms)

        print("Working on {0}".format(myimagebase))

        if os.path.exists(imagename+".image.tt0"):
            #mask = 'clean_mask_{0}_{1}.mask'.format(iternum, field_nospace)
            #outputvis = selfcal_vis.replace(".ms", "_{1}_selfcal{0}.ms".format(iternum, field_nospace))
            #selfcal_vis = outputvis
            caltable = '{2}_{1}_{0}.cal'.format(field_nospace, iternum, caltype)
            caltables.append(caltable)
            calinfo[iternum] = {'combine':combine,}
            print("Skipping {0}".format(imagename))
            continue

        if len(caltables) > 0:
            print("Applying caltables {0}".format(caltables))
            applycal(vis=selfcal_vis,
                     field=field,
                     gaintable=caltables,
                     spwmap=[[0]*nspws if calinfo[ii]['combine']=='spw' else [] for ii in range(len(caltables))],
                     interp='linear,linear', #['linearperobs,linear' if combine=='spw' else 'linearperobs,linear']*len(caltables),
                     applymode='calonly', calwt=True)



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
               cell=['0.01 arcsec'],
               threshold=threshold,
               niter=100000,
               #gridder='wproject',
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
        if 'phase' in caltype or 'amp' in caltype:
            gaincal(vis=selfcal_vis, caltable=caltable, solint=solint,
                    combine=combine,
                    gaintype='G', field=field, calmode=calmode,
                    gaintable=caltables,
                    spwmap=[[0]*nspws if calinfo[ii]['combine']=='spw' else [] for ii in range(len(caltables))],
                    interp='linear,linear',
                    solnorm=True)
        elif 'bandpass' in caltype:
            bandpass(vis=selfcal_vis, caltable=caltable,
                     solint='{0},16ch'.format(solint), combine='obs',
                     field=field, refant='ea07',
                     gaintable=caltables,
                     spwmap=[[0]*nspws if calinfo[ii]['combine']=='spw' else [] for ii in range(len(caltables))],
                     interp='linear,linear',
                     solnorm=True)

        caltables.append(caltable)
        calinfo[iternum] = {'combine':combine,}
        print("Calibration Information exists for these: {0}".format(calinfo.keys()))

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

        #outputvis = selfcal_vis.replace(".ms", "_{1}_selfcal{0}.ms".format(iternum, field_nospace))
        #split(vis=selfcal_vis, outputvis=outputvis, field=field,
        #      datacolumn='corrected')
        #selfcal_vis = outputvis



#for field in field_list:
#    field_nospace = field.replace(" ","_")
#    output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal{1}'.format(field_nospace, iternum+1)
#
#    for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
#                   'image', 'residual'):
#        os.system('rm -rf {0}.{1}'.format(output, suffix))
#
#    tclean(vis=selfcal_vis,
#           imagename=imagename,
#           field=field,
#           spw='',
#           weighting='briggs',
#           robust=0.0,
#           imsize=imsize,
#           cell=['0.01 arcsec'],
#           threshold=threshold,
#           niter=10000,
#           gridder='wproject',
#           wprojplanes=32,
#           specmode='mfs',
#           deconvolver='mtmfs',
#           outframe='LSRK',
#           savemodel='modelcolumn',
#           nterms=2,
#           selectdata=True)
#    makefits(myimagebase)
