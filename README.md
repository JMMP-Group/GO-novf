# GO-novf
Code to generate localized ME s-coordinates ([Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893)) in the Greenland-Scotland ridge region of GOSI configurations to better represent the Nordic overflows.

## Quick-start

### 1. Clone the repository
```
git clone https://github.com/JMMP-Group/GO-novf.git
cd GO-novf
```
### 2. Create and activate conda environment
```
conda env create -f pyogcm.yml
conda activate pyogcm
```
### 3. Create the localisation area
```
cd src/loc_area/
python generate_loc_msk.py loc_area_novf_gosi10_025.inp 
```
As we can see from the `loc_area_novf_gosi10_025.inp` input file, in GOSI10 we use a wider localisation area than in 
[Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893) - here we target the 2930m isobath instead of the 2800m one.

The output of this step is `bathymetry.loc_area-nord_ovf_025.dep2930_sig1_stn9_itr1.nc`.

### 4. Create the envelopes
```
cd ../envelopes/
python generate_envelopes.py ${input_file}
``` 
where `inp_file=MEs_novf_gosi10_025_4env_2930_r12_r16-r075-r040-r035_it2-r030.inp` is the file used to create the defintive version of the 
envelopes that are used in GOSI10. 

In order to reduce horizontal pressure gradient errors, envelopes are smoothed using the iterative preocedure detailed in Appendix C of [Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893), which uses the [Martinho and Batteen (2006)](https://www.sciencedirect.com/science/article/pii/S1463500306000060) smoothing algorithm  to reduce the local slope parameter $r$ below multiple user defined $r_{max}$ values, effectively allowing one to apply distinct level of smoothing in different areas of the model domain. In the case of GOSI10, increasingly more severe $r_{max}$ values were applied only in those grid points where spurious currents were $\geq 0.025$ $m s^{-1}$.

The output of this step is a file including the bathymetry, the localisaztion masks and the envelope surfaces that will be used to define the localised multi-envelope terrain-following vertical levels in the proximity of the Greenland-Scotland ridge region.  

### 5. Generating the vertical grid
The vertical grid of GOSI10 with local ME s-levels in the Nordic overflows area is generated using the [423-adding-more-flexibility-to-me-gvcs@17eae5a7](https://forge.nemo-ocean.eu/nemo/nemo/-/commit/17eae5a707b9d46b81e31a2827ec00a7e181d0ae) development branch of the DOMAINcfg tool.  
