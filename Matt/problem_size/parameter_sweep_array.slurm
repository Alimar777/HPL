#!/bin/bash

#SBATCH --job-name HPL_ParamSweep
#SBATCH --partition general
#SBATCH --time 00:15:00
#SBATCH --nodes 1
#SBATCH --cpus-per-node 32
#SBATCH --mem 0
#SBATCH --array 1-20

# Load the required packages (gcc 11 and HPL)
module load gcc/11.2.0-655h hpl

export OMP_PROC_BIND=TRUE
export OMP_PLACES=cores
export OMP_NUM_THREADS=4

# Set a place to record the results
RESULTS_FILE=$SLURM_SUBMIT_DIR/HPL_results.csv

PARAMS_FILE=$SLURM_SUBMIT_DIR/HPL_params.csv
TEMPLATE_FILE=$SLURM_SUBMIT_DIR/HPL_template.dat

# Check for errors
if test -f $PARAMS_FILE; then
    echo Using parameter file $PARAMS_FILE
else
    echo Error $PARAMS_FILE not found
    exit 1
fi

if test -f $TEMPLATE_FILE; then
    echo Using template file $TEMPLATE_FILE
else
    echo Error $TEMPLATE_FILE not found
    exit 2
fi
    
# Get the Nth line from our parameter file - where N is the array ID
PARAMS=$(head -n $SLURM_ARRAY_TASK_ID $PARAMS_FILE | tail -n 1)
echo Read param line $SLURM_ARRAY_TASK_ID: $PARAMS

# Get the Xth element of that line (comma separated)
PROBLEM_SIZE=$(echo $PARAMS | awk -F"," '{print $1}')
BLOCK_SIZE=$(echo $PARAMS | awk -F"," '{print $2}')
echo Read param PROBLEM_SIZE: $PROBLEM_SIZE
echo Read param BLOCK_SIZE: $BLOCK_SIZE

# Create a new working directory for each instance of xhpl since it needs it expects it's own HPL.dat
SCRATCH_DIR=/carc/scratch/users/$USER

# Make a temporary directory for our work - we will delete this at the end
TMP_DIR=$(mktemp --directory -p $SCRATCH_DIR)
echo Temp directory: $TMP_DIR

# Make a subdirectory with the SLURM array task id to make debugging easier
TMP_WORKING_DIR=$TMP_DIR/$SLURM_ARRAY_TASK_ID
mkdir -p $TMP_WORKING_DIR
echo Created temporary working directory: $TMP_WORKING_DIR

# Make the new working directory the current directory so xhpl runs in there
cd $TMP_WORKING_DIR
echo Now running in $PWD

# Substitute the parameter values read from the PARAMS file above into the HLP.dat for this instance
# Copy the template file into the temp working directory
cp $TEMPLATE_FILE $TMP_WORKING_DIR/HPL.dat
# Substitute the new problem size and block size in for the strings
sed -i "s/<PROBLEM_SIZE>/$PROBLEM_SIZE/g" HPL.dat
sed -i "s/<BLOCK_SIZE>/$BLOCK_SIZE/g" HPL.dat

echo Running xhpl in $TMP_WORKING_DIR...
srun --mpi=pmi2 xhpl
echo xhpl finished

# The HPL.dat file tells xhpl to write to HPL.out.
# Extract the throughput and time with grep and awk

# 1. Find the line containing Gflops and Time and print it and the following lines
RESULT_HEADER_AND_DATA_LINES=$(grep --after 2 "Gflops|Time" HPL.out)
echo Results: $RESULT_HEADER_AND_DATA_LINES

# 2. Get just the data line
RESULT_DATA_LINE=$(echo $RESULT_HEADER_AND_DATA_LINES | tail -n 1)
echo Results data: $RESULT_DATA_LINE

# 3. Get the Gflops and Time values from the data line
GFLOPS=$(echo $RESULT_DATA_LINE | awk -F" " '{print $NF}')
TIME=$(echo $RESULT_DATA_LINE | awk -F" " '{print $(NF-1)}')
echo Results Gflops: $GFLOPS
echo Results Time: $TIME

echo Writing input parameters, gflops, and time to $RESULTS_FILE
echo $PROBLEM_SIZE, $BLOCK_SIZE, $GFLOPS, $TIME >> $RESULTS_FILE

# Clean up the temporary working directory

