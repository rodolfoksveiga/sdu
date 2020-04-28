#!/bin/bash

echo GROUP_FILE=$1

BASEDIR=$(dirname "$0")
LOGS_DIR=$BASEDIR/logs/$SLURM_JOB_ID

mkdir -p $LOGS_DIR

GROUP_NAME=$(basename "$1")
echo NOME_DO_GRUPO=$GROUP_NAME

PARALLEL_LOG=$LOGS_DIR/$GROUP_NAME.parallel_log
echo Parallel log in $PARALLEL_LOG

TEMPOS=$LOGS_DIR/$GROUP_NAME.tempos
echo Tempos em $TEMPOS

parallel="parallel -N 1 --delay .2 -j $SLURM_CPUS_PER_TASK --joblog $PARALLEL_LOG"
$parallel "./runsimulation.sh {1} {2}" :::: $1 ::: $TEMPOS
