line_vis = vis = '16B-202.sb32532587.eb32875589.57663.07622001157.ms'

imagename = myimagebase = output = 'J1922+1530_spw40'

if not os.path.exists(imagename+".image.pbcor.fits"):
    os.system('rm -rf ' + output + '*/')

    tclean(vis=line_vis,
           imagename=imagename,
           field='J1922+1530',
           spw='40',
           weighting='briggs',
           robust=0.0,
           imsize=[512,512],
           cell=['0.01 arcsec'],
           threshold='50 mJy',
           niter=1000,
           gridder='mosaic',
           specmode='mfs',
           outframe='LSRK',
           savemodel='modelcolumn',
           selectdata=True)
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)

imagename = myimagebase = output = 'J1922+1530_allspw'

if not os.path.exists(imagename+".image.pbcor.fits"):
    os.system('rm -rf ' + output + '*/')

    tclean(vis=line_vis,
           imagename=imagename,
           field='J1922+1530',
           spw='',
           weighting='briggs',
           robust=0.0,
           imsize=[512,512],
           cell=['0.01 arcsec'],
           threshold='50 mJy',
           niter=1000,
           gridder='mosaic',
           specmode='mfs',
           outframe='LSRK',
           savemodel='modelcolumn',
           selectdata=True)
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)



os.system('rm -rf J1922+1530_selfcal_phase.cal')
gaincal(vis=vis, caltable="J1922+1530_selfcal_phase.cal", field="J1922+1530",
        solint='int', calmode="p", refant="", gaintype="G")
plotcal(caltable="J1922+1530_selfcal_phase.cal",
        xaxis="time", yaxis="phase", subplot=331,
        iteration="antenna", plotrange=[0,0,-30,30], markersize=5,
        fontsize=10.0,)

plotcal(caltable="J1922+1530_selfcal_phase.cal",
        xaxis="time", yaxis="phase", subplot=331,
        iteration="antenna", plotrange=[0,0,-30,30], markersize=5,
        fontsize=10.0, spw='40')


#only do this after sanity-checking...
# applycal(vis=full_vis,field=source,
#          gaintable=['cal_all_spws.gaincurve','cal_all_spws.K0',
#                     'cal_all_spws.B0_nopoly','cal_all_spws.G1inf','cal_all_spws.G2',
#                     'cal_all_spws.F3inc', 'J1922+1530_selfcal_phase.cal'],
#          gainfield=['',phasecal,phasecal,phasecal,phasecal,phasecal,phasecal,phasecal],
#          interp=['','','nearest','nearest','linearPD,linear','linearPD,linear','','linearPD,linear'],
#          #spwmap=[[], [], [], spwmap, spwmap, spwmap, []],
#          parang=False,calwt=False)
