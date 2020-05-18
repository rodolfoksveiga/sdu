# Autor: Rayner Mauricio e Lucas Verdade 06/05/2020 LabEEE - PRJEEESD2020

# Teste em máquina local digitando no terminal o comando 'mpiexec -n 2 RScript teste.r'
# '-n' é o número de nucleos
# 'mpiexec' pode ter outros nomes como 'mpirun'

library(Rmpi)
library(readr)

sequence = 1:10
factors = 1:mpi.comm.size(0)
lista2use = suppressWarnings(split(sequence, factors, drop = TRUE))
rank = mpi.comm.rank(0) + 1
processor_name = mpi.get.processor.name(0)

for(i in lista2use[[rank]]){
  line = paste0("Using the core ", rank, " from processor ",  processor_name, " to process the value ", i, "\n")
  cat(line)
}

mpi.quit()