import numpy as np

def check_intents(vis,
                  bad_intent='CALIBRATE_BANDPASS#UNSPECIFIED,CALIBRATE_FLUX#UNSPECIFIED',
                  replacement_intent='CALIBRATE_FLUX#UNSPECIFIED'):
    """
    Search for Jethro Tull
    """

    tb.open(vis+"/STATE", nomodify=False)

    obs_mode = tb.getcol("OBS_MODE")

    tb.close()

    match = obs_mode == bad_intent
    if not match.any():
        print("No matches to intent {0} found.".format(bad_intent))
        #raise ValueError("No matches to intent {0} found.".format(bad_intent))

    bad_state_id_nums = np.where(match)

    tb.open(vis)
    state_id_data = tb.getcol('STATE_ID')
    field_id_data = tb.getcol('FIELD_ID')
    tb.close()

    field_ids = []
    for idnum in bad_state_id_nums:
        match = state_id_data == idnum
        field_ids += list(np.unique(field_id_data[match]))

    tb.open(vis+'/FIELD')
    fieldnames = tb.getcol("NAME")
    tb.close()

    matched_fields_badintents = {fid:fieldnames[fid] for fid in field_ids}

    field_intents = {fieldnames[fid]:obs_mode[sid] for fid,sid in zip(field_id_data, state_id_data)}

    return matched_fields_badintents, field_intents


def fix_intents(vis,
                bad_intent='CALIBRATE_BANDPASS#UNSPECIFIED,CALIBRATE_FLUX#UNSPECIFIED',
                replacement_intent='CALIBRATE_FLUX#UNSPECIFIED'):
    """
    With lots of inspiration from Todd Hunter's editIntents
    """

    tb.open(vis+"/STATE", nomodify=False)

    obs_mode = tb.getcol("OBS_MODE")

    match = obs_mode == bad_intent
    if not match.any():
        raise ValueError("No matches to intent {0} found.".format(bad_intent))

    obs_mode[match] = replacement_intent

    tb.putcol('OBS_MODE', obs_mode)
    tb.close()


"""
if __name__ == "__main__":
for ms in mses:
    try:
        needs_fixing = check_intents(ms)
    except ValueError:
        print("{0} is OK").format(ms)
        continue
    if needs_fixing == {0: '1331+305=3C286'}:
        fix_intents(ms)
        print("Fixed {0}".format(ms))
        try:
            check_intents(ms)
            print("FAILURE: fix didn't work for {0}".format(ms))
        except ValueError:
            pass
    else:
        print("FAILURE: {0} needs fixing but not for 3c286".format(ms))
"""
