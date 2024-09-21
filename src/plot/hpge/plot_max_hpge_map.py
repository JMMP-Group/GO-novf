#!/usr/bin/env python

#     |------------------------------------------------------------|
#     | Author: Diego Bruciaferri                                  |
#     | Date and place: 07-09-2021, Met Office, UK                 |
#     |------------------------------------------------------------|


import os
from os.path import join, isfile, basename, splitext
import glob
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import xarray as xr
from xnemogcm import open_domain_cfg
import cartopy.crs as ccrs
import cmocean
from utils import plot_hpge

# ------------------------------------------------------------------------------------------
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

# ==============================================================================
# Input parameters

# 1. INPUT FILES

vcoord = ['MEs']
DOMCFG_file = ["/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/test/domain_cfg_MEs_novf_4env_2930_r12_r16-r075-r040-r035_it2-r030.nc"]
HPGE_list = ["/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/test/maximum_hpge_r12_r16-r075-r040-r035_it2-r030.nc"]

# 3. PLOT
lon0 = -45.
lon1 =  5.0
lat0 =  50.
lat1 =  72.
proj = ccrs.Mercator() #ccrs.Robinson()

# ==============================================================================

for vco in range(len(vcoord)):

    HPGE_file = HPGE_list[vco]

    # Loading domain geometry
    ds_dom  = open_domain_cfg(files=[DOMCFG_file[vco]])
    for i in ['bathy_metry']:
        for dim in ['x','y']:
            ds_dom[i] = ds_dom[i].rename({dim: dim+"_c"})

    ds_hpge  = xr.open_dataset(HPGE_file)

    # Extracting only the part of the domain we need

    ds_dom  = ds_dom.isel(x_c=slice(880,1200),x_f=slice(880,1200),
                          y_c=slice(880,1140),y_f=slice(880,1140))
    #ds_dom = ds_dom.isel(x_c=slice(920,1220), x_f=slice(920,1220), 
    #                     y_c=slice(905,1140), y_f=slice(905,1140))
    ds_hpge =  ds_hpge.isel(x=slice(880,1200),y=slice(880,1140))

    # Plotting ----------------------------------------------------------

    bathy = ds_dom["bathy_metry"]#.isel(x_c=slice(1, None), y_c=slice(1, None))
    varss = list(ds_hpge.keys())

    for env in range(len(varss)):

        if vco == 4:
           fig_name = 'colorbar.png'
        else:
           fig_name = varss[env] + '_' + vcoord[vco] + '_3months.png'

        fig_path = "./"
        lon = ds_dom["glamf"]
        lat = ds_dom["gphif"]
        var = ds_hpge[varss[env]] * 100. # in cm/s 
        colmap = truncate_colormap(plt.get_cmap('nipy_spectral'), minval=0.0, maxval=0.9, n=100) #'gnuplot2' #truncate_colormap(plt.get_cmap('hot'), minval=0.0, maxval=0.9, n=100) #'CMRmap' #'viridis' #'gnuplot2' #'hot' #cmocean.cm.ice
        vmin = 0.0
        vmax = 5.
        cbar_extend = 'max' #"max"
        #if vco == 4:
        if vco == 0:
           cbar_label = r"$\times 10^{-2}$ [$m\;s^{-1}$]"
        else:
           cbar_label = ""
        cbar_hor = 'horizontal'
        map_lims = [lon0, lon1, lat0, lat1]
        cn_lev = [1000., 2000., 3000.]

        plot_hpge(fig_name, fig_path, lon, lat, var, proj, colmap, 
                  vmin, vmax, cbar_extend, cbar_label, cbar_hor, map_lims, bathy, cn_lev)

 
