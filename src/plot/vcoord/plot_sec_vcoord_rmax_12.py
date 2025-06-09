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

fig_path = './'

# 1. INPUT FILES

vvar = None #"r0x" # None
fig_path = './'

# ----- GOSI10
#domcfg = ['/scratch/dbruciaf/GOSI10p3_12/r12-r12-r065/domain_cfg_12_MEs_novf_4env_2930_r12_r12-r065.nc']
#fbathy = ['/data/users/dbruciaf/GOSI10_input_files/eORCA12/MEs_novf/bathymetry.loc_area-nord_ovf_12.dep2930_sig2_stn9_itr4.MEs_novf_gosi10_12_4env_2930_r12_r12-r065.nc',
#          None]

# ----- GOSI9
domcfg = ['/data/scratch/diego.bruciaferri/GOSI9/domaincfg_eORCA12_v3.0.nc']
fbathy = [None]

# Define the section we want to plot:
list_sec = [
            {'lon':[ 0.34072625, -3.56557722,-18.569585  ,-26.42872351, -30.314948] , 
             'lat':[68.26346438, 65.49039963, 60.79252542, 56.24488972,  52.858934]}, # Iceland-Faroe Ridge
            {'lon':[-10.84451672, -25.30818606, -35., -44.081319] , 
             'lat':[71.98049514,  66.73449533,  61.88833838,  56.000932]}, # Denmark Strait
            {'lon':[-0.7549, -22.222, -24.9836, -28.4769, -44.081319] ,
             'lat':[70.528, 68.5597,  67.1603,  65.4224,  56.000932]}, # Denmark Strait new
            #{'lon':[-43.23, -0.61] ,
            # 'lat':[ 62.33, 62.20]}
            #{'lon':[-35.5961, -34.8232] ,
            # 'lat':[ 59.9577,  51.2308]}, # i = 1010
            #{'lon':[-35.3125, -34.5621] , 
            # 'lat':[ 59.9678,  51.2357]}, # i = 1011
            #{'lon':[-35.0288, -34.3009] ,
            # 'lat':[ 59.9777,  51.2405]}, # i = 1012
            #{'lon':[-20.4412, -0.7618] ,
            # 'lat':[ 72.0003,  70.9567]}, # j = 1058
           ]

list_idx = [
            {'i':[ 1073, 1105] ,
             'j':[  992,  987]}
           ]

i1 = 2500
i2 = 3600
j1 = 2700
j2 = 3400

# ==============================================================================

for exp in range(len(domcfg)):

    # Loading domain geometry
    ds_dom, hbatt, vcoor = prepare_domcfg(domcfg[exp], fbathy[exp], [i1, i2, j1, j2])

    hbatt = [] # TODO: use realistic envelopes

    # Computing slope paramter of model levels if needed
    r0_3D = ds_dom.gdept_0 * 0.0
    if vvar is not None:
       r0_3D = r0_3D.rename(vvar)
       for k in range(r0_3D.shape[0]):
           r0 = calc_r0(ds_dom.gdept_0.isel(z=k))
           r0_3D[k,:,:] = r0
    else:
       vvar = 'dummy'
    r0_3D = r0_3D.where(ds_dom.tmask > 0)
    ds_dom[vvar] = r0_3D

    # Extracting variables for the specific type of section
    var_list = ["gdepu_0" , "gdepuw_0", "gdepv_0" , "gdepvw_0",
                "gdept_0" , "gdepw_0" , "gdepf_0" , "gdepfw_0",
                "glamt"   , "glamu"   , "glamv"   , "glamf"   ,
                "gphit"   , "gphiu"   , "gphiv"   , "gphif"   ,
                "gdepw_1d", "loc_msk" , vvar]

    for coord_sec in list_sec:
    
        sec_lon = coord_sec['lon']
        sec_lat = coord_sec['lat']
    
        print ('section through lon:', sec_lon)
        print ('                lat:', sec_lat)
    
        ds_sec = ds_dom[var_list]
        ds_var = ds_dom[var_list]
    
        sec_name = str(sec_lon[0])+'-'+str(sec_lat[0])+'_'+str(sec_lon[-1])+'-'+str(sec_lat[-1])
    
        if vvar == "dummy":
           fig_name = vcoor+'_section_'+sec_name+'.png'
        else:
           fig_name = vcoor+'_section_'+vvar+'_'+sec_name+'.png'
        plot_sec(fig_name, fig_path, ds_sec, ds_var, vvar, sec_lon, sec_lat, hbatt, imap=True)

    #for indx_sec in list_idx:

    #    sec_lon = []
    #    sec_lat = []
    #    for n in range(len(indx_sec['i'])):
    #        sec_lon.append(ds_dom.glamt.data[indx_sec['j'][n],indx_sec['i'][n]])
    #        sec_lat.append(ds_dom.gphit.data[indx_sec['j'][n],indx_sec['i'][n]])

    #    print ('section through lon:', sec_lon)
    #    print ('                lat:', sec_lat)

    #    ds_sec = ds_dom[var_list]
    #    ds_var = ds_dom[var_list]

    #    sec_name = str(sec_lon[0])+'-'+str(sec_lat[0])+'_'+str(sec_lon[-1])+'-'+str(sec_lat[-1])

    #    if vvar == "dummy":
    #       fig_name = vcoor+'_section_'+sec_name+'.png'
    #    else:
    #       fig_name = vcoor+'_section_'+vvar+'_'+sec_name+'.png'
    #    plot_sec(fig_name, fig_path, ds_sec, ds_var, vvar, sec_lon, sec_lat, hbatt, imap=True)
