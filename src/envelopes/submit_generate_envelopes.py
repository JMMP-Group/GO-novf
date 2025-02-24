#!/bin/bash -l

#SBATCH --qos=normal                
#SBATCH --mem=150000                    
#SBATCH --ntasks=8                   
#SBATCH --output=gen_env_12.out       
#SBATCH --time=360                    

#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr1.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr2.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr2_nohal.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr3.inp
inpfile=MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr3-r010.inp


#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030-r015.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030-r015-r012.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030-r015-r012-r008_itr1.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030-r015-r012-r008_itr2.inp
#inpfile=MEs_novf_gosi10_12_4env_2930_r12_r12-r065-r030-r015-r012-r008_itr3.inp

python generate_envelopes_noplt.py $inpfile
