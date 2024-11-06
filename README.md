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

<img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/loc_area/loc_areas_novf.png?raw=true" width="300">

### 4. Create the envelopes
```
cd ../envelopes/
python generate_envelopes.py ${input_file}
``` 
where `inp_file=MEs_novf_gosi10_025_4env_2930_r12_r16-r075-r040-r035_it2-r030.inp` is the file used to create the defintive version of the 
envelopes that are used in GOSI10. 

In order to reduce horizontal pressure gradient errors, envelopes are smoothed using the iterative preocedure detailed in Appendix C of [Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893), which uses the [Martinho and Batteen (2006)](https://www.sciencedirect.com/science/article/pii/S1463500306000060) smoothing algorithm  to reduce the local slope parameter $r$ below multiple user defined $r_{max}$ values, effectively allowing one to apply distinct level of smoothing in different areas of the model domain. In the case of GOSI10, increasingly more severe $r_{max}$ values were applied only in those grid points where spurious currents were $\geq 0.025$ $m s^{-1}$.

The three months long tests to assess the horizontal pressure gradient (HPG) errors were conducted with the [u-di990@301896](https://code.metoffice.gov.uk/trac/roses-u/browser/d/i/9/9/0/trunk?rev=301896) suite. Since the `u-di990` suite was based on GOSIp1, it didn't include the `key_qco` which is part of GOSI10p2. Therefore, given the importance of the `key_qco`, I reconducted the final HPG test with the [u-dk586@302161](https://code.metoffice.gov.uk/trac/roses-u/browser/d/k/5/8/6/trunk?rev=302161) suite (which is based on GOSI10p2). The suite u-dk586@302161 can replicate the results of u-di990@301896. 

The output of this step is a file including the bathymetry, the localisaztion masks and the envelope surfaces that will be used to define the localised multi-envelope terrain-following vertical levels in the proximity of the Greenland-Scotland ridge region.  

### 5. Generate the vertical grid
The vertical grid of GOSI10 with local ME s-levels in the Nordic overflows area is generated using the [423-adding-more-flexibility-to-me-gvcs@17eae5a7](https://forge.nemo-ocean.eu/nemo/nemo/-/commit/17eae5a707b9d46b81e31a2827ec00a7e181d0ae) development branch of the DOMAINcfg tool.

The `namelist_ref` and `namelist_cfg` used to configure the vertical grid of GOSI10 can be found in [namelists](https://github.com/JMMP-Group/GO-novf/tree/main/src/namelists).

### 6. Horizontal pressure gradient error

<img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/hpge_timeseries.png?raw=true" width="500">

<img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/maximum_max_hpge_1_MEs_3months.png?raw=true" width="500">

### 7. Comparison with GOSI9

#### GOSI9
<p float="left">
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/zps_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" />
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/sco_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" /> 
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/zps_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/sco_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/zps_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/sco_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
</p>

#### GOSI10

<p float="left">
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/zps_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" />
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/sco_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" /> 
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/zps_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/sco_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/zps_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/sco_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
</p>

### 8
