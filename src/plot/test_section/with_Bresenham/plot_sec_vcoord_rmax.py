#!/usr/bin/env python

#     |------------------------------------------------------------|
#     | Author: Diego Bruciaferri                                  |
#     | Date and place: 13-08-2024, Met Office, UK                 |
#     |------------------------------------------------------------|


import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import xarray as xr
from utils import calc_r0, prepare_domcfg, plot_sec

# ==============================================================================
# Input parameters

# 1. INPUT FILES

vvar   = "r0x"
fig_path = './'

domcfg = ['/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/domain_cfg_MEs_novf_4env_2930_r12_r12-r075-r040-035_it2_cut_novf.nc',]
         # '/data/users/dbruciaf/GOSI10_input_files/p1.0/domcfg_eORCA025_v3.1_r42.nc']
fbathy = ['/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/bathymetry.loc_area-nord_ovf_025.dep2930_sig1_stn9_itr1.MEs_novf_gosi10_025_4env_2930_r12_r12-r075-r040-r035_it2_cut_novf.nc',]
         # None]

# Define the section we want to plot:
list_sec = [
            {'lon':[ 0.34072625, -3.56557722,-18.569585  ,-26.42872351, -30.314948] ,
             'lat':[68.26346438, 65.49039963, 60.79252542, 56.24488972,  52.858934]}, # Iceland-Faroe Ridge
            {'lon':[-10.84451672, -25.30818606, -35., -44.081319] ,
             'lat':[71.98049514,  66.73449533,  61.88833838,  56.000932]}, # Denmark Strait
            {'lon':[-43.23, -0.61] ,
             'lat':[ 62.33, 62.20]}
           ]

# ==============================================================================

for exp in range(len(domcfg)):

    # Loading domain geometry
    ds_dom, hbatt, vcoor = prepare_domcfg(domcfg[exp], fbathy[exp])

    hbatt = [] # TODO: use realistic envelopes

    # Computing slope paramter of model levels
    r0_3D = ds_dom.gdept_0 * 0.0
    r0_3D = r0_3D.rename("r0x")
    for k in range(r0_3D.shape[0]):
        r0 = calc_r0(ds_dom.gdept_0.isel(z=k))
        r0_3D[k,:,:] = r0
    r0_3D = r0_3D.where(ds_dom.tmask > 0)
    ds_dom[vvar] = r0_3D
    ds_dom = ds_dom.assign_coords({'z': ds_dom.z})

    # Extracting variables for the specific type of section
    var_list = ["gdepu_0" , "gdepuw_0", "gdepv_0" , "gdepvw_0",
                "gdept_0" , "gdepw_0" , "gdepf_0" , "gdepfw_0",
                "glamt"   , "glamu"   , "glamv"   , "glamf"   ,
                "gphit"   , "gphiu"   , "gphiv"   , "gphif"   ,
                "gdepw_1d", "loc_msk" , "r0x"]

    for coord_sec in list_sec:

        sec_lon = coord_sec['lon']
        sec_lat = coord_sec['lat']

        print ('section through lon:', sec_lon)
        print ('                lat:', sec_lat)

        ds_sec = ds_dom[var_list]
        ds_var = ds_dom[var_list]

        sec_name = str(sec_lon[0])+'-'+str(sec_lat[0])+'_'+str(sec_lon[-1])+'-'+str(sec_lat[-1])

        fig_name = vcoor+'_section_'+vvar+'_'+sec_name+'.png'
        plot_sec(fig_name, fig_path, ds_sec, ds_var, vvar, sec_lon, sec_lat, hbatt, imap=True)

