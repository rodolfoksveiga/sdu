# Autor: Rayner Mauricio e Lucas Verdade 06/05/2020 LabEEE - PRJEEESD2020

from mpi4py import MPI
import time
from datetime import datetime
import random
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
processor_name = MPI.Get_processor_name()

size = comm.Get_size()
x = np.array_split(range(144), size) # 144 escolhido para que metade dos processadores executem 2 vezes 

print(f"Size do get_size() = {size}\n") # será sempre nodes*ntasks-per-node

x_chunk = x[rank]
r_chunk = x_chunk.tolist()

for i, line in enumerate(x_chunk):
    time.sleep(1)
    r_chunk[i] = processor_name + ',' + str(rank) + ',' + str(line) + ',' + datetime.now().strftime("%H:%M:%S") + '\n'

r = comm.allreduce(r_chunk)
r = ['processor_name,', 'rank,', 'line,', 'datetime\n'] + r

with open(f'resultados_do_teste-{sys.argv[1]}.csv', 'w') as f:
    f.writelines(r)
