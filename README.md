# GO-novf
Code to generate localized ME s-coordinates ([Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893)) in the Greenland-Scotland ridge region of GOSI configurations to better represent the Nordic overflows.

## Quick-start

#### 1. Clone the repository
```
git clone https://github.com/JMMP-Group/GO-novf.git
cd GO-novf
```
#### 2. Create and activate conda environment
```
conda env create -f pyogcm.yml
conda activate pyogcm
```
#### 3. Create the localisation area
```
cd src/loc_area/
python generate_loc_msk.py loc_area_novf_gosi10_025.inp 
```
As we can see from the `loc_area_novf_gosi10_025.inp` input file, in GOSI10 we use a wider localisation area than in 
[Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893) - here we target the 2930m isobath instead of the 2800m one.

The output of this tep is `bathymetry.loc_area-nord_ovf_025.dep2930_sig1_stn9_itr1.nc`.

#### 4. Create the envelopes
```
cd ../envelopes/
python generate_envelopes.py ${input_file}
``` 
where `inp_file=MEs_novf_gosi10_025_4env_2930_r12_r16-r075-r040-r035_it2-r030.inp` is the file used to create the defintive version of the 
envelopes that are used in GOSI10. 

As explained in Appendix C of [Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893), the envelopes are smoothed for 
with an iterative algorithm that ensures that the slope parameter is smaller than multiple user defined threshold $r_{max}$. 
