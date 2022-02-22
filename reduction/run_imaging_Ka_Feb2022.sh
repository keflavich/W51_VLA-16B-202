#!/bin/bash
#SBATCH --mail-type=NONE          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=adamginsburg@ufl.edu     # Where to send mail	
#SBATCH --ntasks=8
#SBATCH --mem=256gb # Job memory request PER NODE
#SBATCH --nodes=1 # exactly 1 node
#SBATCH --time=96:00:00               # Time limit hrs:min:sec
#SBATCH --qos=adamginsburg-b
#SBATCH --account=adamginsburg
#SBATCH --output=w51lb_b3_feb2022_lb_%j.log
#SBATCH --job-name=sw51lb_b3_feb2022_lb
#SBATCH --export=ALL


# inherited? export SLURM_NTASKS=64

export FIELD_ID="W51_LB"
export BAND_TO_IMAGE=VLA
export LOGFILENAME="casa_log_w51_${FIELD_ID}_VLA_12M_$(date +%Y-%m-%d_%H_%M_%S).log"

WORK_DIR='/orange/adamginsburg/w51/vla/W51_VLA-16B-202_analysis'
SCRIPT_DIR='/orange/adamginsburg/w51/vla/W51_VLA-16B-202_analysis'
WORK_DIR='/blue/adamginsburg/adamginsburg/w51-imaging/'

# "copy" the MS (on orange)
# ln -s /orange/adamginsburg/salt/s255ir/2019.1.00492.S/science_goal.uid___A001_X1465_X2dfc/group.uid___A001_X1465_X2dfd/member.uid___A001_X1465_X2dfe/calibrated/calibrated_final.ms ${WORK_DIR}/
# actually copy (on blue)

# cp -r /orange/adamginsburg/salt/s255ir/2019.1.00492.S/science_goal.uid___A001_X1465_X2dfc/group.uid___A001_X1465_X2dfd/member.uid___A001_X1465_X2dfe/calibrated/calibrated_final.ms ${WORK_DIR}/

if [[ ! $CASAVERSION ]]; then
    CASAVERSION=casa-6.4.3-4
    echo "Set CASA version to default ${CASAVERSION}"
fi
echo "CASA version = ${CASAVERSION}"

export CASA=/orange/adamginsburg/casa/${CASAVERSION}/bin/casa
export MPICASA=/blue/adamginsburg/adamginsburg/casa/${CASAVERSION}/bin/mpicasa


env
pwd; hostname; date
echo "Memory=${MEM}"

module load git
module load cuda/11.0.207  gcc/9.3.0 openmpi/4.0.4

which python
which git

git --version
echo "git version: $?"

if [ -z $SLURM_NTASKS ]; then
    echo "FAILURE - SLURM_NTASKS=${SLURM_NTASKS}, i.e., empty"
    exit
fi



# not using almaimf pipeline for this
#export ALMAIMF_ROOTDIR="/orange/adamginsburg/ALMA_IMF/reduction/reduction"
#cd ${ALMAIMF_ROOTDIR}
#python getversion.py
#export PYTHONPATH=$ALMAIMF_ROOTDIR

imaging_script=/orange/adamginsburg/w51/vla/W51_VLA-16B-202_analysis/reduction/imaging_continuum_selfcal_19A-254_Ka.py

cd ${WORK_DIR}
echo ${WORK_DIR}
pwd

OMPI_COMM_WORLD_SIZE=$SLURM_NTASKS

echo Running command: ${MPICASA} -n ${SLURM_NTASKS} ${CASA} --nogui --nologger --logfile=${LOGFILENAME} -c "execfile('${imaging_script}')" &

${MPICASA} -n ${SLURM_NTASKS} ${CASA} --nogui --nologger --logfile=${LOGFILENAME} -c "execfile('${imaging_script}')" &
ppid="$!"; childPID="$(ps -C ${CASA} -o ppid=,pid= | awk -v ppid="$ppid" '$1==ppid {print $2}')"
echo PID=${ppid} childPID=${childPID}

ps -C ${CASA} -o ppid=,pid= | awk -v ppid="$ppid" '$1==ppid {print $2}'

if [[ ! -z $childPID ]]; then 
    /orange/adamginsburg/miniconda3/bin/python ${ALMAIMF_ROOTDIR}/slurm_scripts/monitor_memory.py ${childPID}
else
    echo "FAILURE: PID=$PID was not set."
fi

wait $ppid
exitcode=$?

cd -
