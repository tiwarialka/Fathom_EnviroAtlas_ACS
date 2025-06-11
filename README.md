# Fathom_EnviroAtlas_ACS

Step1: Download AFTHOM 30 m data - i got it from BEG shared link
Step2: transfer all that to scratch drive
Step3: FIlter the data for 15 cm using filter.py script
  
  # use below command on terinal to create fathom_folder_list.txt
  # find /scratch/07474/tiwari13/FloodMapping/Data_raw/ -mindepth 1 -maxdepth 1 -type d | sort | head -10 > fathom_folder_list.txt
  To filter the 19 folders use filter_array.sh
  chmod +x filter_array.sh
  check all the directory location is correct

  then sbatch filter_array.sh [uses CPU with array]
  
Step4:
