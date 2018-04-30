import fix_intents

__rethrow_casa_exceptions = True
context = h_init()
context.set_state('ProjectSummary', 'proposal_code', 'VLA/')
context.set_state('ProjectSummary', 'observatory', 'Karl G. Jansky Very Large Array')
context.set_state('ProjectSummary', 'telescope', 'EVLA')
context.set_state('ProjectSummary', 'piname', 'Adam Ginsburg')
context.set_state('ProjectSummary', 'proposal_title', 'W51 16B-202')
try:
    vis = '16B-202.sb32957824.eb33234671.57760.62953023148.ms'
    try:
        fix_intents.fix_intents(vis)
    except ValueError:
        pass
    matched_fields_badintents, field_intents = fix_intents.check_intents(vis)
    assert matched_fields_badintents == {}
    clearcal(vis=vis)
    listobs(vis=vis, listfile=vis+".listobs.beforeimport", overwrite=True)
    hifv_importdata(vis=[vis], session=['session_1'])
    listobs(vis=vis, listfile=vis+".listobs.afterimport", overwrite=True)
    #hifv_hanning(pipelinemode="automatic")
    hifv_flagdata(intents='*POINTING*,*FOCUS*,*ATMOSPHERE*,*SIDEBAND_RATIO*, *UNKNOWN*, *SYSTEM_CONFIGURATION*, *UNSPECIFIED#UNSPECIFIED*', hm_tbuff='1.5int')
    hifv_vlasetjy(pipelinemode="automatic")
    hifv_priorcals(pipelinemode="automatic")
    hifv_testBPdcals(pipelinemode="automatic")
    hifv_flagbaddef(pipelinemode="automatic")
    hifv_checkflag(pipelinemode="automatic")
    hifv_semiFinalBPdcals(pipelinemode="automatic")
    hifv_checkflag(checkflagmode='semi')
    hifv_semiFinalBPdcals(pipelinemode="automatic")
    hifv_solint(pipelinemode="automatic")
    hifv_fluxboot(pipelinemode="automatic")
    hifv_finalcals(pipelinemode="automatic")
    hifv_applycals(pipelinemode="automatic")
    #hifv_targetflag(intents='*CALIBRATE*,*TARGET*')
    hifv_targetflag(intents='*CALIBRATE*')
    #hifv_statwt(pipelinemode="automatic")
    hifv_plotsummary(pipelinemode="automatic")
    hif_makeimlist(intent='PHASE,BANDPASS,TARGET')
    hif_makeimages(hm_masking='none')
finally:
    h_save()

