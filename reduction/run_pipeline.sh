#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.

cd ${WORK_DIR}

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa-pipe --nogui --nologger -c "execfile('$WORK_DIR/casa_pipescript.py')"

#export CASAPATH=/home/casa/packages/RHEL6/release/casa-release-5.1.0-74
#export PATH=${CASAPATH}/bin:$PATH
#
#export CASACMD="execfile('$REDUCTION_DIR/scriptForImaging_lines.py')"
#echo $CASACMD
#
#mpicasa -machinefile $PBS_NODEFILE casa -quiet --nogui --nologger --log2term -c "${CASACMD}"
