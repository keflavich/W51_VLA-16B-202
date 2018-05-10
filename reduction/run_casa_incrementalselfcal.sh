#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.

WORK_DIR='/lustre/aginsbur/16B-202_W51QKa/merge'
cd ${WORK_DIR}

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa-prerelease --nogui --nologger -c "field_list=['W51e2w']; execfile('$WORK_DIR/imaging_continuum_selfcal_incremental.py')"
xvfb-run -d casa-prerelease --nogui --nologger -c "field_list=['W51 North']; execfile('$WORK_DIR/imaging_continuum_selfcal_incremental.py')"
#xvfb-run casapy --nogui -c "spwlist='0'; $SCRIPTPATH/fullcube_r0.py"
#xvfb-run casa --nogui -c "spwlist='0'; execfile('$SCRIPTPATH/fullcube_r0.py')"
