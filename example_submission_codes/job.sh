#!/bin/bash
#SBATCH --nodes=10                                #Numero de Nos
#SBATCH --ntasks-per-node=24                      #Numero de tarefas por Nos
#SBATCH --ntasks=240                              #Numero total de tarefas MPI
#SBATCH -p cpu_long                               #Fila (partition) a ser utilizada
#SBATCH -J Neural_Network                         #Nome job
#SBATCH --exclusive                               #Utilizacao exclusiva dos nos durante a execucao do job

#Exibe os nos alocados para o Job
echo $SLURM_JOB_NODELIST
nodeset -e $SLURM_JOB_NODELIST

cd $SLURM_SUBMIT_DIR

#Configura os compiladores
source /scratch/app/modulos/intel-psxe-2016.2.062.sh
module load bullxmpi/bullxmpi-1.2.8.4
module load R/3.3.1_intel

source /scratch/app/modulos/gcc-5.3.sh

#Configura o executavel
EXEC=/scratch/prjeeesd/marcio.sorgato/ann_brasilia/resfriamento/

#exibe informacoess sobre o executavel
/usr/bin/ldd $EXEC

mpiexec -np $SLURM_NTASKS R --slave -f treinamento.r


