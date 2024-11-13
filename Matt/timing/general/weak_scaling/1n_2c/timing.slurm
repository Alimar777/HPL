#!/bin/bash
#SBATCH --job-name=HPL_timing_analysis
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node 2
#SBATCH --mem=4G

module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores

# Run HPL with the current number of CPUs
srun --mpi=pmi2 xhpl 

