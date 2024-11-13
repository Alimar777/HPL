#!/bin/bash
#SBATCH --job-name=HPL_timing_analysis
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node 32
#SBATCH --mem=0G
#SBATCH --output timing_${SLURM_NNODES}_${SLURM_NTASKS_PER_NODE}cpu.out

module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores

# Loop over CPU counts from 1 to 32, doubling each time

echo "Running with $cpus CPUs"

# Run HPL with the current number of CPUs
srun --mpi=pmi2 xhpl 

