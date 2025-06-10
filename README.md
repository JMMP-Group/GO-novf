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

### 3. Ancillary files needed to generate localization masks and envelopes
The localisaztion masks that will be used to define the localised multi-envelope terrain-following vertical levels in the proximity of the Greenland-Scotland ridge region and all the ancillary files needed to generate and optimise the envelopes of `GOSI10p3.0-eORCA025` and `GOSI10p3.0-eORCA12` can be found at the following zenodo archives:

1) `GOSI10p3.0-eORCA025:`https://zenodo.org/records/15625102
2) `GOSI10p3.0-eORCA12:`https://zenodo.org/uploads/15633874

For the bathymetry files, `GOSI10p3.0` uses the [Storkey et al. 2024](https://github.com/JMMP-Group/GLOBAL_BATHYMETRY/releases/tag/v1.0.0) bottom topography files:

1) `GOSI10p3.0-eORCA025:`https://zenodo.org/records/15494369
2) `GOSI10p3.0-eORCA12:`https://zenodo.org/records/15495870

### 4. Create the localisation area
```
cd src/loc_area/
python generate_loc_msk.py ${loc_area_novf} 
```
where `loc_area_novf=`[loc_area_novf_gosi10_025.inp](https://github.com/JMMP-Group/GO-novf/blob/main/src/loc_area/loc_area_novf_gosi10_025.inp) in the case of eORCA025 and `loc_area_novf=`[loc_area_novf_gosi10_12.inp](https://github.com/JMMP-Group/GO-novf/blob/main/src/loc_area/loc_area_novf_gosi10_12.inp) for eORCA12.

As we can see from the `${loc_area_novf}` input files, in GOSI10 we use a wider localisation area than in 
[Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893) - here we target the 2930m isobath instead of the 2800m one.

<img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/loc_area/loc_areas_novf.png?raw=true" width="300">

### 5. Create the envelopes
```
cd ../envelopes/
python generate_envelopes.py ${input_file}
``` 
where `inp_file=`[MEs_novf_gosi10_025_4env_2930_r12_r16-r075-r040-r035_it2-r030.inp](https://github.com/JMMP-Group/GO-novf/blob/main/src/envelopes/MEs_novf_gosi10_025_4env_2930_r12_r16-r075-r040-r035_it2-r030.inp) for the case of `GOSI10p3.0-eORCA025` while `inp_file=`[MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr3-r010.inp](https://github.com/JMMP-Group/GO-novf/blob/main/src/envelopes/MEs_novf_gosi10_12_4env_2930_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr3-r010.inp) for `GOSI10p3.0-eORCA12`. 

In order to reduce horizontal pressure gradient (HPG) errors, envelopes are smoothed using the iterative preocedure detailed in Appendix C of [Bruciaferri et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003893), which uses the [Martinho and Batteen (2006)](https://www.sciencedirect.com/science/article/pii/S1463500306000060) smoothing algorithm  to reduce the local slope parameter $r$ below multiple user defined $r_{max}$ values, effectively allowing one to apply distinct level of smoothing in different areas of the model domain. In the case of GOSI10, increasingly more severe $r_{max}$ values were applied only in those grid points where spurious currents were $\geq 0.025$ $m s^{-1}$. 

The three months long tests to assess the horizontal pressure gradient (HPG) errors were conducted with 

1) `GOSI10p3.0-eORCA025`: [u-dl766@312554](https://code.metoffice.gov.uk/trac/roses-u/browser/d/l/7/6/6/trunk?rev=312554) suite.
2) `GOSI10p3.0-eORCA12`: [u-dn555@311670](https://code.metoffice.gov.uk/trac/roses-u/browser/d/n/5/5/5/trunk?rev=311670) suite.

### 6. Generate the vertical grid
The vertical grid of GOSI10 with local ME s-levels in the Nordic overflows area is generated using the [423-adding-more-flexibility-to-me-gvcs@17eae5a7](https://forge.nemo-ocean.eu/nemo/nemo/-/commit/17eae5a707b9d46b81e31a2827ec00a7e181d0ae) development branch of the DOMAINcfg tool - this has now be merged in the main, see `main@8e326e96b546251509d8d5a4db484500817ef784` commit.

The `namelist_ref` and `namelist_cfg` used to configure the vertical grid of GOSI10 can be found in [namelists](https://github.com/JMMP-Group/GO-novf/tree/main/src/namelists).

The output of this step is a domain_cfg.nc file - the files for `GOSI10@1/4` and `GOSI10@1/12` can be found at the following zenodo archives:

1) `GOSI10p3.0-eORCA025:`https://zenodo.org/uploads/15634496
2) `GOSI10p3.0-eORCA12:`https://zenodo.org/uploads/15634622

### 7. Horizontal pressure gradient error

Left is `GOSI10p3.0-eORCA025`, right `GOSI10p3.0-eORCA12`.

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/eORCA025/hpge_timeseries.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/eORCA12/hpge_timeseries.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/eORCA025/maximum_max_hpge_1_MEs_3months.png?raw=true" width="300">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/hpge/eORCA12/maximum_max_hpge_1_MEs_3months.png?raw=true" width="300">
</p>

### 8. Comparison with GOSI9

#### GOSI9 - eORCA025 --------------------------
<p float="left">
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/zps_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" />
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/sco_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" /> 
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/zps_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/sco_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/zps_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/sco_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
</p>

#### GOSI10 - eORCA025 --------------------------

<p float="left">
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/zps_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" />
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/sco_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" /> 
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/zps_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/sco_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/zps_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_025/sco_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
</p>

The strange canyon that can be seen in the first sections of GOSI9 are due to the fact that in the case of GOSI9 the bathymetry has been modified by hand as shown in the following map:

<img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi9/orca_025/gosi9_model_bathymetry.png?raw=true" width="400">

#### GOSI10 - eORCA12 --------------------------

<p float="left">
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/zps_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" />
  <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/sco_section_-0.7549-70.528_-44.081319-56.000932.png?raw=true" width="400" /> 
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/zps_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/sco_section_-10.84451672-71.98049514_-44.081319-56.000932.png?raw=true" width="400" />
</p>

<p float="left">
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/zps_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
   <img src="https://github.com/JMMP-Group/GO-novf/blob/main/src/plot/vcoord/gosi10/orca_12/sco_section_0.34072625-68.26346438_-30.314948-52.858934.png?raw=true" width="400" />
</p>

### 9. INITIAL CONDITION FOR GOSI WITH LOCALISED ME s-coordinates

Because of the way NEMO interpolates the T&S fields passed in input when initialising from rest (`ln_tsd_init=.true.`), the following two important point MUST be considered when initilising a model with localised ME levels (`ln_sco=.true.` and `ln_loczgr=.true.`):

1) Since the land-sea mask will be different in the localisation area, The T&S used to initialise the model should be flooded, i.e., continents should be filled with value from the ocean to avoid issue when interpolating in the vertical.

2) When using local GVC s-coord, the last level must be a copy of previous level:
```
ori_S=woa13v2.omip-clim.abs_sal_gosi10p1-025_flooded.nc
new_S=woa13v2.omip-clim.abs_sal_gosi10p1-025_flooded.MEs.nc
ori_T=woa13v2.omip-clim.con_tem_gosi10p1-025_flooded.nc
new_T=woa13v2.omip-clim.con_tem_gosi10p1-025_flooded.MEs.nc

ncap2 -O -s 'so_abs(:,74,:,:)=so_abs(:,73,:,:)' ${ori_S} ${new_S}
ncap2 -O -s 'thetao_con(:,74,:,:)=thetao_con(:,73,:,:)' ${ori_T} ${new_T}
``` 
