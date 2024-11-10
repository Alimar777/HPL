#!/bin/bash
#SBATCH --job-name=HPL_timing_analysis
#SBATCH --partition=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node = 32
#SBATCH --mem=16GB
#SBATCH --output=timing_%dcpu.out
#SBATCH --error=timing_%dcpu.err

module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores
0
# Loop over CPU counts from 1 to 32, doubling each time
for cpus in 1 2 4 8 16 32; do
    echo "Running with $cpus CPUs"
    
    export OMP_NUM_THREADS=$cpus
    
    # Run HPL with the current number of CPUs
    srun --mpi=pmi2 --ntasks=1 --cpus-per-task=$cpus xhpl
    
    # Save the output for review
    mv debug.out timing_${cpus}cpu.out
    mv debug.err timing_${cpus}cpu.err
done