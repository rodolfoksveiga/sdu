#!/bin/bash

#SBATCH --nodes=20
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=24
#SBATCH -p cpu
#SBATCH --exclusive
#SBATCH -o output.%J              #Job output

module purge
module load gnu-parallel/20160922
module load energyplus/8.5
module load python/2.7.12

srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_001 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_002 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_003 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_004 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_005 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_006 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_007 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_008 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_009 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup.sh /scratch/prjeeesd/marcio.sorgato/floripa/grupos/grupo_010 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_001 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_002 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_003 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_004 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_005 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_006 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_007 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_008 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_009 &
srun  --nodes 1 --ntasks=1 --cpus-per-task $SLURM_CPUS_PER_TASK ./rungroup1.sh /scratch/prjeeesd/marcio.sorgato/curitiba/grupos/grupo_010 &

wait
