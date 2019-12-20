#!/bin/bash -l

## job name
#SBATCH --job-name=ets_uq

## stdout and stderr files
#SBATCH --output=logs/test.out.%j
#SBATCH --error=logs/test.err.%j

## wall time in format MINUTES:SECONDS
#SBATCH --time=02:00:00

## number of nodes and tasks per node
#SBATCH --nodes=1
#SBATCH --tasks-per-node=40

## queue name
#SBATCH --partition=medium

## grant
#SBATCH --mail-user=ljala@rzg.mpg.de

export SYS=COBRA
export LD_LIBRARY_PATH=${FFTW_HOME}/lib:${LD_LIBRARY_PATH}
export MPICMD=srun
source tests/custom_encoder/easypj_sample_config.sh

python3 test/custom_encoder/test_executor_custom_encoder.py > logs/test.${SLURM_JOBID}.log
