#!/bin/sh

now=$(date +"%T")
echo Iniciando $1 - $now >> $2

# this script echoes some useful output so we can see what parallel
# and srun are doing

sleepsecs=$[ ( $RANDOM % 10 ) + 10 ]s

# $1 is arg1:{1} from parallel.
# $PARALLEL_SEQ is a special variable from parallel. It the actual sequence
# number of the job regardless of the arguments given
# We output the sleep time, hostname, and date for more info
echo task $1 seq:$PARALLEL_SEQ sleep:$sleepsecs date:$(date)

# sleep a random amount of time
sleep $sleepsecs

now=$(date +"%T")
echo Finalizando $1 - $now >> $2
