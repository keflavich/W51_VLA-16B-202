import numpy as np
from astropy.io import fits
import pyregion
import os
from taskinit import msmdtool, iatool, casalog
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
import casac
tb = casac.casac().table()
ia = iatool()
msmd = msmdtool()

# field_list = ('W51e2w', 'W51 North')
if 'field_list' not in locals():
    raise ValueError("Set field_list")
if isinstance(field_list, str):
    raise TypeError("Make field list a list or tuple")
if 're_clear' not in locals():
    re_clear = True

casalog.post("Field list is: {0}".format(str(field_list)), origin='imaging_continuum_selfcal_incremental')

def makefits(myimagebase, cleanup=True):
    if os.path.exists(myimagebase+'.image.tt0'):
        impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
        exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', overwrite=True) # export the corrected image
        exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', overwrite=True) # export the corrected image
        exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', overwrite=True)
        exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', overwrite=True)

        if cleanup:
            for ttsuffix in ('.tt0', '.tt1', '.tt2'):
                for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                               'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                               'alpha', 'alpha.error'):
                    os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))
    elif os.path.exists(myimagebase+'.image'):
        impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
        exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True) # export the corrected image
        exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', overwrite=True) # export the PB image
        exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True) # export the PB image

        if cleanup:
            ttsuffix=''
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'alpha', 'alpha.error'):
                os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))
    else:
        raise IOError("No image file found matching {0}".format(myimagebase))



# SB1 may have terrible calibration (is 2x as faint, and wasn't appropriately
# statwt'd b/c it didn't go through the pipeline)
vis = [#'16B-202.sb32532587.eb32875589.57663.07622001157.ms',
       '16B-202.sb32957824.eb33105444.57748.63243916667.ms',
       '16B-202.sb32957824.eb33142274.57752.64119381944.ms',
       '16B-202.sb32957824.eb33234671.57760.62953023148.ms',
      ]
contspw = '2,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,22,23,24,25,26,28,29,30,31,32,34,35,36,37,39,42,44,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64'
# really want 8-80, 100-120, but need jumps of 16...
#contspw = ",".join(["{0}:8~72;104~120".format(xx)
#                    if xx == "50" else
#                    "{0}:8~120".format(xx)
#                    for xx in contspw.split(",")])
flagchans = ",".join(["{0}:0~5;123~128".format(xx) for xx in
                      contspw.split(',')])



base_cont_vis = 'continuum_concatenated_incremental.ms'

for field, field_nospace in (('W51e2w', 'W51e2w'),
                             ('W51 North', 'W51North')):
    if field not in field_list:
        casalog.post("Skipping {0}".format(field), origin='imaging_continuum_selfcal_incremental')
        continue


    for cvis in vis:
        new_ms = field_nospace+"_cont_"+cvis
        if not os.path.exists(new_ms):
            casalog.post("Splitting file {0}".format(new_ms), origin='imaging_continuum_selfcal_incremental')

            flagdata(vis=cvis, mode='manual', spw=flagchans)
            flagdata(vis=cvis, mode='manual', spw='50:80~100')

            # actual bad data; redundant with flagging_sbXX.py
            #flagdata(vis=cvis, mode='manual', antenna='ea01', spw='50~64,18~33')

            split(vis=cvis, outputvis=new_ms, spw=contspw,
                  width=16, field=field)

            flagdata(vis=cvis, mode='unflag', spw='50:80~100')

    cont_vises = [field_nospace+"_cont_"+vv for vv in vis]
    cont_vis = field_nospace+'_'+base_cont_vis

    if not os.path.exists(cont_vis):
        assert concat(vis=cont_vises, concatvis=cont_vis)

selfcal_vis = cont_vis


#(this should already be done, but you might want to double-check...)
# # flag out two basebands for antenna ea01
# tb.open(selfcal_vis+"/SPECTRAL_WINDOW")
# spwnames = tb.getcol('NAME')
# tb.close()
# flag_windows = ",".join([str(ii) for ii,xx in enumerate(spwnames) if 'B2D2' in xx or 'A2C2' in xx])
# casalog.post("Flagging windows {0} for antenna ea01".format(flag_windows), origin='imaging_continuum_selfcal_incremental')
# flagdata(vis=selfcal_vis, antenna='ea01', spw=flag_windows, mode='manual')


caltables = []
calinfo = {}

# don't clean too shallowly first time: it takes forever to fix.
thresholds = {'W51e2w': (2.5,2.5,1.5,1.0,1.0,1.0,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25),
              'W51 North': (2.5,1.5,1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25),
             }
imsize = {'W51e2w': 256,
          'W51 North': 1024}
phasecenter = {'W51e2w': 'J2000 19h23m43.910 +14d30m34.593',
               'W51 North': 'J2000 19h23m39.959 +14d31m06.687',}


msmd.open(selfcal_vis)
nspws = msmd.nspw()
msmd.close()

for field in field_list:
    casalog.post("Beginning main loop for field: {0}".format(field), origin='imaging_continuum_selfcal_incremental')
    field_nospace = field.replace(" ","")

    selfcal_vis = field_nospace + "_" + base_cont_vis

    if re_clear:
        clearcal(vis=selfcal_vis, field=field)

    # create a dirty image for masking
    cleanbox_mask_image = 'cleanbox_mask_{0}.image'.format(field_nospace)
    imagename = '{0}_QbandAarray_cont_spws_continuum_cal_dirty_2terms_robust0'.format(field_nospace)
    if not os.path.exists('{0}.image.tt0.pbcor.fits'.format(imagename)):
        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=0.0,
               phasecenter=phasecenter[field],
               imsize=imsize[field],
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
    for iternum, nterms, threshold, caltype, calmode, solint, combine in [#(0, 2, '{0} mJy','amp','a', 'inf', 'spw',),
                                                                          #(1, 2, '{0} mJy','bandpass', 'ap', 'inf', '',),
                                                                          #(2, 2, '{0} mJy','amp','a', '240s', 'scan',),
                                                                          #(2, 2, '{0} mJy','phase','p', '240s', 'scan',),
                                                                          #(3, 2, '{0} mJy','ampphase','ap', 'inf', '',),
                                                                          (0, 2, '{0} mJy','phase','p', 'inf', '',),
                                                                          (1, 2, '{0} mJy','phase','p', 'inf', '',),
                                                                          (2, 2, '{0} mJy','phase','p', '240s', '',),
                                                                          (3, 2, '{0} mJy','phase','p', '240s', '',),
                                                                          (4, 2, '{0} mJy','phase','p', '240s', '',),
                                                                          (5, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (6, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (7, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (8, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (9, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (10, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (11, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          (12, 2, '{0} mJy','phase','p', '20s', '',),
                                                                          (13, 2, '{0} mJy','phase','p', '20s', '',),
                                                                          (14, 2, '{0} mJy','phase','p', '10s', '',),
                                                                          (15, 2, '{0} mJy','phase','p', '10s', '',),
                                                                          #(16, 2, '{0} mJy','amp','a', 'inf', 'scan',),
                                                                          #(17, 2, '{0} mJy','amp','a', 'inf', 'scan',),
                                                                          # bandpass goes wanky (16, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (17, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (18, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (19, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (20, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (21, 2, '{0} mJy','bandpass','', 'inf', 'scan,obs',),
                                                                          # bandpass goes wanky (22, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          # bandpass goes wanky (23, 2, '{0} mJy','phase','p', '30s', '',),
                                                                          #(20, 2, '{0} mJy','bandpass','', 'inf', 'scan',),
                                                                          #(7, 2, '{0} mJy','ampphase', 'ap', 'inf', '',),
                                                                          #(8, 2, '{0} mJy','ampphase', 'ap', 'inf', '',),
                                                                          #(9, 3, '{0} mJy','ampphase', 'ap', 'inf', '',),
                                                                          #(10, 3, '{0} mJy','ampphase', 'ap', 'inf', '',),
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
        casalog.post("Working on {0}".format(myimagebase), "INFO", "IncrementalSelfcalScript")

        if os.path.exists(imagename+".image.tt0"):
            #mask = 'clean_mask_{0}_{1}.mask'.format(iternum, field_nospace)
            #outputvis = selfcal_vis.replace(".ms", "_{1}_selfcal{0}.ms".format(iternum, field_nospace))
            #selfcal_vis = outputvis
            caltable = '{2}_{1}_{0}.cal'.format(field_nospace, iternum, caltype)
            if not os.path.exists(caltable):
                print('Does caltable {0} exist? {1}'.format(caltable, os.path.exists(caltable)))
                print(os.listdir(caltable))
                print(os.listdir(imagename+".image.tt0"))
                casalog.post("Calibration table {1} does not exist but image does.  Remove images with "
                             "suffix {0}".format(imagename, caltable), "SEVERE", "IncrementalSelfcalScript")
                raise ValueError("Calibration table {1} does not exist but image does.  Remove images with "
                                 "suffix {0}".format(imagename, caltable))
            caltables.append(caltable)
            calinfo[iternum] = {'combine':combine,}
            casalog.post("Skipping {0}".format(myimagebase), "INFO", "IncrementalSelfcalScript")
            casalog.post("caltables set to {0}, calinfo set to {1}"
                         .format(caltables, calinfo), "INFO",
                         "IncrementalSelfcalScript")
            print("Skipping {0}".format(imagename))
            continue

        if len(caltables) > 0:
            print("Applying caltables {0}".format(caltables))
            casalog.post("Applying caltables {0}".format(caltables), "INFO", "IncrementalSelfcalScript")
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
               phasecenter=phasecenter[field],
               imsize=imsize[field],
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
                    minsnr=1.5,
                    spwmap=[[0]*nspws if calinfo[ii]['combine']=='spw' else [] for ii in range(len(caltables))],
                    interp='linear,linear',
                    solnorm=True)
            if 'amp' in caltype:
                # avoid extreme outliers: assume anything going more than 2x in either direction is wrong
                flagdata(caltable, mode='clip', clipminmax=[0.5, 2.0], datacolumn='CPARAM')
        elif 'bandpass' in caltype:
            bandpass(vis=selfcal_vis, caltable=caltable,
                     solint='{0},16ch'.format(solint), combine=combine,
                     field=field,
                     #refant='ea07',
                     gaintable=caltables,
                     minsnr=1.5,
                     spwmap=[[0]*nspws if calinfo[ii]['combine']=='spw' else [] for ii in range(len(caltables))],
                     interp='linear,linear',
                     solnorm=True)
            # avoid extreme outliers: assume anything going more than 2x in either direction is wrong
            flagdata(caltable, mode='clip', clipminmax=[0.5, 2.0], datacolumn='CPARAM')

        if not os.path.exists(caltable):
            casalog.post("Calibration table {0} does not exist".format(caltable), "ERROR", "IncrementalSelfcalScript")
            raise ValueError("Calibration table {0} does not exist".format(caltable))

        caltables.append(caltable)
        calinfo[iternum] = {'combine':combine,}
        print("Calibration Information exists for these: {0}".format(calinfo.keys()))
        casalog.post("Calibration Information exists for these: {0}".format(calinfo.keys()), "INFO", "IncrementalSelfcalScript")

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




# make some smaller diagnostic images
for field in field_list:
    for robust in (-2, 0, 2):
        field_nospace = field.replace(" ","")
        selfcal_vis = field_nospace + "_" + base_cont_vis
        msmd.open(selfcal_vis)
        summary = msmd.summary()
        msmd.close()

        for baseband in ('A1C1', 'A2C2', 'B1D1', 'B2D2'):
            spws = ",".join([x for x in np.unique(summary['spectral windows']['names'])
                             if baseband in x])

            output = myimagebase = imagename = '{0}_QbandAarray_spw{2}_continuum_cal_clean_2terms_robust{robust}_selfcal{1}_final'.format(field_nospace, iternum+1, baseband,
                                                                                                                                          robust=robust)
            if not os.path.exists(imagename+".image.pbcor.fits"):
                casalog.post("Cleaning: {0}".format(output), origin='imaging_continuum_selfcal_incremental')

                tclean(vis=cont_vis,
                       imagename=imagename,
                       field=field,
                       spw=spws,
                       imsize=[1000,1000],
                       cell='0.01arcsec',
                       niter=1000,
                       threshold='1mJy',
                       robust=robust,
                       gridder='standard',
                       deconvolver='multiscale',
                       specmode='mfs',
                       nterms=1,
                       weighting='briggs',
                       pblimit=0.2,
                       interactive=False,
                       outframe='LSRK',
                       savemodel='none',
                       scales=[0,3,9],
                      )
                casalog.post("FITSing: {0}".format(output), origin='imaging_continuum_selfcal_incremental')
                makefits(imagename, cleanup=False)



for field in field_list:
    for robust in (-2, 0, 2):
        field_nospace = field.replace(" ","")
        selfcal_vis = field_nospace + "_" + base_cont_vis
        msmd.open(selfcal_vis)
        summary = msmd.summary()
        msmd.close()

        for spw in summary['spectral windows']['names']:

            output = myimagebase = imagename = '{0}_QbandAarray_spw{2}_continuum_cal_clean_2terms_robust{robust}_selfcal{1}_final'.format(field_nospace, iternum+1, spw,
                                                                                                                                          robust=robust)
            if not os.path.exists(imagename+".image.pbcor.fits"):
                casalog.post("Cleaning: {0}".format(output), origin='imaging_continuum_selfcal_incremental')

                tclean(vis=selfcal_vis,
                       imagename=imagename,
                       field=field,
                       spw=spw,
                       imsize=[1000,1000],
                       cell='0.01arcsec',
                       niter=1000,
                       threshold='1mJy',
                       robust=robust,
                       gridder='standard',
                       deconvolver='multiscale',
                       specmode='mfs',
                       nterms=1,
                       weighting='briggs',
                       pblimit=0.2,
                       interactive=False,
                       outframe='LSRK',
                       savemodel='none',
                       scales=[0,3,9],
                      )
                casalog.post("FITSing: {0}".format(output), origin='imaging_continuum_selfcal_incremental')
                makefits(imagename, cleanup=True)


for field in field_list:
    for robust in (-2, 0, 2):
        field_nospace = field.replace(" ","")
        output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust{robust}_selfcal{1}_final'.format(field_nospace, iternum+1,
                                                                                                                                         robust=robust)
        casalog.post("Cleaning: {0}".format(output), origin='imaging_continuum_selfcal_incremental')

        for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                       'image', 'residual'):
            os.system('rm -rf {0}.{1}'.format(output, suffix))

        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=robust,
               imsize=8000,
               cell=['0.01 arcsec'],
               threshold='0.2mJy',
               niter=100000,
               #gridder='wproject',
               #wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='none',
               nterms=2,
               scales=[0,3,9],
               mask=mask,
               selectdata=True)
        casalog.post("FITSing: {0}".format(output), origin='imaging_continuum_selfcal_incremental')
        makefits(myimagebase)

        output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_noshortbaseline_robust{2}_selfcal{1}_final'.format(field_nospace, iternum+1, robust)
        casalog.post("Cleaning: {0}".format(output), origin='imaging_continuum_selfcal_incremental')

        for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                       'image', 'residual'):
            os.system('rm -rf {0}.{1}'.format(output, suffix))

        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw='',
               weighting='briggs',
               robust=robust,
               uvrange='600~1000000klambda',
               imsize=8000,
               cell=['0.01 arcsec'],
               threshold='0.2mJy',
               niter=100000,
               #gridder='wproject',
               #wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='none',
               nterms=2,
               scales=[0,3,9],
               mask=mask,
               selectdata=True)
        casalog.post("FITSing: {0}".format(output), origin='imaging_continuum_selfcal_incremental')
        makefits(myimagebase)





    field_nospace = field.replace(" ","")
    output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_supernatural_selfcal{1}_final'.format(field_nospace, iternum+1,)
    casalog.post("Cleaning: {0}".format(output), origin='imaging_continuum_selfcal_incremental')

    for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                   'image', 'residual'):
        os.system('rm -rf {0}.{1}'.format(output, suffix))

    tclean(vis=selfcal_vis,
           imagename=imagename,
           field=field,
           spw='',
           weighting='briggs',
           robust=2,
           uvrange='0~1200klambda',
           imsize=4000,
           cell=['0.02 arcsec'],
           threshold='0.2mJy',
           niter=100000,
           #gridder='wproject',
           #wprojplanes=32,
           specmode='mfs',
           deconvolver='mtmfs',
           outframe='LSRK',
           savemodel='none',
           nterms=2,
           scales=[0,3,9],
           mask=mask,
           selectdata=True)
    casalog.post("FITSing: {0}".format(output), origin='imaging_continuum_selfcal_incremental')
    makefits(myimagebase)


