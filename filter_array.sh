#!/bin/bash
#SBATCH -J filter_array
#SBATCH -o filter_array.%A_%a.out
#SBATCH -e filter_array.%A_%a.err
#SBATCH -p normal               # Use normal (CPU) queue
#SBATCH -t 00:20:00             # Adjust time as needed
#SBATCH -A ATM23014
#SBATCH -N 1                    # One node
#SBATCH -n 1
#SBATCH --array=0-19             # Set based on number of folders

# Optional: load Python environment
# module load python3/3.9.2

# Change to the scratch working directory
cd $SCRATCH

# use below command on terinal to create fathom_folder_list.txt
# find /scratch/07474/tiwari13/FloodMapping/Data_raw/ -mindepth 1 -maxdepth 1 -type d | sort | head -10 > fathom_folder_list.txt

# Full path to folder list file (each line = one folder path)
FOLDER_LIST="/scratch/07474/tiwari13/FloodMapping/fathom_folder_list.txt"

# Read the folder name for this task
INPUT_DIR=$(sed -n "$((SLURM_ARRAY_TASK_ID+1))p" "$FOLDER_LIST")
OUTPUT_ROOT="/scratch/07474/tiwari13/FloodMapping/Data_filter"

# Run the Python script
python /work/07474/tiwari13/ls6/Documents/packages/FloodMapping/FATHOM_30m/filter.py "$INPUT_DIR" "$OUTPUT_ROOT"
