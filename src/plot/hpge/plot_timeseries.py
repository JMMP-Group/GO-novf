#!/usr/bin/env python

#     |------------------------------------------------------------|
#     | This module creates a 2D field of maximum spurious current |
#     | in the vertical and in time after an HPGE test.            |
#     | The resulting file can be used then to optimise the rmax   |
#     | of Multi-Envelope vertical grids.                          |
#     |                                                            |
#     | Author: Diego Bruciaferri                                  |
#     | Date and place: 07-09-2021, Met Office, UK                 |
#     |------------------------------------------------------------|


import os
from os.path import join, isfile, basename, splitext
import glob
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import xarray as xr

# ==============================================================================
# Input files
# ==============================================================================

# Folder path containing HPGE spurious currents velocity files 
# eORCA025
#MAINdir = '/data/users/dbruciaf/GOSI10_input_files/MEs_novf'
#HPGElst = '025/test'
#FileVel = 'hpge_timeseries_r12_r12-r075-r040-r035_it2-r030.nc'

# eORCA12
MAINdir = '/data/users/dbruciaf/GOSI10_input_files/eORCA12/MEs_novf'
HPGElst = 'r12_r16'
FileVel = 'hpge_timeseries_r12_r16-r075-r040-r035-r030-r025-r020-r015_itr3-r010.nc'

# ==============================================================================
# OPENING fig
fig, ax = plt.subplots(figsize=(16,9))

# Loading timeseries
ds  = xr.open_dataset(join(join(MAINdir,HPGElst),FileVel)).squeeze()

ax.plot(np.arange(1,len(ds.max_u_loc)+1), ds.max_u_loc*100., linestyle="-", linewidth=5, color='blue', label='max{$| \mathbf{u} |$}')
ax.plot(np.arange(1,len(ds.max_u_loc)+1), ds.u_99p_loc*100., linestyle="--", linewidth=5, color='gold', label='99%{$| \mathbf{u} |$}')
ax.plot(np.arange(1,len(ds.max_u_loc)+1), ds.avg_u_loc*100., linestyle="--", linewidth=5, color='red', label='$V_L^{-1} \int_{V_L} | \mathbf{u} | \mathrm{d}V$')
       
plt.rc('legend', **{'fontsize':35})
ax.legend(loc=1, ncol=1, frameon=False)
ax.set_xlabel('Days', fontsize=35)
ax.set_ylabel('[$cm\;s^{-1}$]', fontsize=35)
ax.tick_params(axis='both',which='major', labelsize=30)
ax.set_xlim(1.,len(ds.max_u_loc)+1)
ax.set_ylim(0.,5.)
ax.grid(True)
name = 'hpge_timeseries.png'
plt.savefig(name, bbox_inches="tight")
