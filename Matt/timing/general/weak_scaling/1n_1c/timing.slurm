#!/bin/bash
#SBATCH --job-name=HPL_wtiming_analysis
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node 1
#SBATCH --mem=2G

module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores

# Run HPL with the current number of CPUs
srun --mpi=pmi2 xhpl 

