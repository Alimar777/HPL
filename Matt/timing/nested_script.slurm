#!/bin/bash

#1) chmod +x nested_script.slurm
#2) ./nested_script.slurm

for cpus in 1 2 4 8 16 32; do
    echo "Running with $cpus CPUs"
        
    # Run HPL with the current number of CPUs
	sbatch timing.slurm --ntasks-per-node=$cpus
	sbatch timing.slurm --nodes=2 --ntasks-per-node=$cpus

done