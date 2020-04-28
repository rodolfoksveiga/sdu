#!/bin/bash --login
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --cpus-per-task=1
#SBATCH -o output.%J              #Job output
#SBATCH -p cpu

module purge
module load gnu-parallel/20160922
module load energyplus/8.5
module load python/2.7.12

echo $SLURM_JOB_NODELIST

# Define srun arguments:
srun="srun -n1 -N1 --exclusive"
# --exclusive     ensures srun uses distinct CPUs for each job step
# -N1 -n1         allocates a single core to each task

# Define parallel arguments:
parallel="parallel -N 1 --delay .2 -j 24 --joblog parallel_joblog --resume"
# -N 1              is number of arguments to pass to each job
# --delay .2        prevents overloading the controlling node on short jobs
# -j $SLURM_NTASKS  is the number of concurrent tasks parallel runs, so number of CPUs allocated
# --joblog name     parallel's log file of tasks it has run
# --resume          parallel can use a joblog and this to continue an interrupted run (job resubmitted)

# Run the tasks:
echo === CALL RUNTASK.SH ===
$parallel "$srun ./runtask.sh {1}" :::: casos.txt

# in this case, we are running a script named runtask, and passing it a single argument
# {1} is the first argument
# parallel uses ::: to separate options. Here {1..32} is a shell expansion defining the values for
#    the first argument, but could be any shell command
#
# so parallel will run the runtask script for the numbers 1 through 32, with a max of 12 running 
#    at any one time
#
# as an example, the first job will be run like this:
#    srun -N1 -n1 --exclusive ./runtask arg1:1
