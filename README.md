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

In order to reduce horizontal pressure gradient errors, envelopes are smoothed using the iterative preocedure detailed in Appendix C of [Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893), which uses the [Martinho and Batteen (2006)](https://www.sciencedirect.com/science/article/pii/S1463500306000060) smoothing algorithm  to reduce the local slope parameter $r$ below multiple user defined $r_{max}$ values, effectively allowing one to apply distinct level of smoothing in different areas of the model domain. For GOSI10, we decided to apply increasingly more severe $r_{max}$ values only in those grid points where spurious currents were $\geq 0.025$ $m s^{-1}$.
