# field_list = ('W51e2w', 'W51 North')
if 'field_list' not in locals():
    raise ValueError("Set field_list")
if isinstance(field_list, str):
    raise TypeError("Make field list a list or tuple")


def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', overwrite=True)
    exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', overwrite=True)


selfcal_vis = cont_vis = 'continuum_concatenated_incremental.ms'

iternum = "LAST"

ms.open(selfcal_vis)
mssum = ms.getspectralwindowinfo()
ms.close()

imsize = 7680

for field in field_list:
    #for frequency_range in ('40-45', '45-50'):
    #    minfreq, maxfreq = map(float, frequency_range.split("-"))
    for minfreq, maxfreq in [(42,43), (43,44), (44,45), (45,46), (46,47), (47,48), (48,49), (49,50)]:

        spws = [spwid for spwid in mssum
                if ((mssum[spwid]['Chan1Freq'] > minfreq*1e9) and
                    (mssum[spwid]['Chan1Freq'] < maxfreq*1e9))]

        field_nospace = field.replace(" ","_")
        output = myimagebase = imagename = '{0}_QbandAarray_cont_spws_continuum_cal_clean_2terms_robust0_wproj_selfcal{1}_{2}-{3}'.format(field_nospace, iternum, minfreq, maxfreq)

        for ttsuffix in ('.tt0', '.tt1', 'tt2'):
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'alpha', ):
                os.system('rm -rf {0}.{1}'.format(output, suffix).format(tt=ttsuffix))


        tclean(vis=selfcal_vis,
               imagename=imagename,
               field=field,
               spw=",".join(spws),
               weighting='briggs',
               robust=0.0,
               imsize=imsize,
               cell=['0.01 arcsec'],
               threshold='0.25mJy',
               niter=10000,
               gridder='wproject',
               wprojplanes=32,
               specmode='mfs',
               deconvolver='mtmfs',
               outframe='LSRK',
               savemodel='none',
               nterms=2,
               selectdata=True)
        makefits(myimagebase)
