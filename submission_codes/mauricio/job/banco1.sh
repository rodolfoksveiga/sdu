#!/bin/bash

#SBATCH --nodes=25
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=25
#SBATCH --cpus-per-task=24
#SBATCH -p cpu
#SBATCH --time=48:00:00
#SBATCH --exclusive
#SBATCH -o output.%J              #Job output

module purge
module load gnu-parallel/20160922
module load energyplus/8.5
module load python/3.5.2

srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_001 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_002 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_003 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_004 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_005 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_006 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_007 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_008 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_009 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_010 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_011 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_012 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_013 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_014 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_015 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_016 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_017 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_018 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_019 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_020 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_021 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_022 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_023 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_024 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/roberto.lamberts/banco1/grupos/grupo_025 &


wait
