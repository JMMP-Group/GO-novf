#!/usr/bin/env

import sys
import numpy as np
import xarray as xr

# ==============================================================================

if len(sys.argv) == 1:
   print("usage: python generate_Cdmin_field.py <CONF>,  with CONF = 025 or 12")
   quit()

if sys.argv[1] == "025":
   loc_file = "/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/bathymetry.loc_area-nord_ovf_025.dep2930_sig1_stn9_itr1.nc"
elif sys.argv[1] == "12":
   loc_file = "/data/users/dbruciaf/GOSI10_input_files/eORCA12/MEs_novf/bathymetry.loc_area-nord_ovf_12.dep2930_sig2_stn9_itr4.nc"
else:
   print("Error: only orca025 or orca12 configurations are supported.")

# Load localisation file

ds_loc = xr.open_dataset(loc_file)
ds_cdm = ds_loc[['s2z_msk']]
ds_cdm = ds_cdm.rename({'s2z_msk':'bfr_cdmin'})

ds_cdm['bfr_cdmin'] = xr.where(ds_loc['s2z_msk'] == 2, 0.0025, 0.001)
ds_cdm['bfr_cdmin'] = xr.where(ds_loc['s2z_msk'] == 1, ds_loc['s2z_wgt']*0.0025+(1.-ds_loc['s2z_wgt'])*0.001, ds_cdm['bfr_cdmin'])

ds_cdm.to_netcdf('bfr_eORCA'+ sys.argv[1] + '_cdmin_2d_001-0025_r42.nc')
