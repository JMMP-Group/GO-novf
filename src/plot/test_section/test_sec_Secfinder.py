#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import xarray as xr
from nsv import SectionFinder
import cartopy.crs as ccrs
import cartopy.feature as feature


# Define the section we want to plot:
list_sec = [
            #{'lon':[ 0.34072625, -3.56557722,-18.569585  ,-26.42872351, -30.314948] , 
            # 'lat':[68.26346438, 65.49039963, 60.79252542, 56.24488972,  52.858934]}, # Iceland-Faroe Ridge
            {'lon':[-10.84451672, -25.30818606, -35., -44.081319] , 
             'lat':[71.98049514,  66.73449533,  61.88833838,  56.000932]}, # Denmark Strait
            #{'lon':[-43.23, -0.61] ,
            # 'lat':[ 62.33, 62.20]}
           ] 


proj = ccrs.Mercator()

domcfg = '/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/domain_cfg_MEs_novf_4env_2930_r12_r12-r075-r040-035_it2.nc'

ds_dom = xr.open_dataset(domcfg, drop_variables=("x", "y","nav_lev")).squeeze()
ds_dom = ds_dom.rename({"nav_lev": "z"})

# Extracting only the part of the domain we need

ds_dom = ds_dom.isel(x=slice(880,1150), y=slice(880,1140))

LLcrnrlon = -43. #-46.00
LLcrnrlat =  60. # 57.00
URcrnrlon = -26. #-14.
URcrnrlat =  64. # 70.0

map_lims = [LLcrnrlon, URcrnrlon, LLcrnrlat, URcrnrlat]

fig = plt.figure(figsize=(25, 25), dpi=100)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[:1], projection=proj)
ax.coastlines(linewidth=4, zorder=6)
ax.add_feature(feature.LAND, color='gray',edgecolor='black',zorder=5)

# Drawing settings
transform = ccrs.PlateCarree()

ax.plot(ds_dom.glamt, ds_dom.gphit, 'k+', transform=transform)

for sec in list_sec:

    target_lons = sec['lon']
    target_lats = sec['lat']

    finder = SectionFinder(ds_dom)

    pnts_UV = finder.velocity_points_along_zigzag_section(
                                        lons=target_lons,
                                        lats=target_lats,
              )

    print(pnts_UV['u'].y_index)
    print(pnts_UV['u'].x_index)

    pnts_F = finder.zigzag_section(lons=target_lons,
                                   lats=target_lats,
                                   grid='f'
             )

    print(pnts_F.y_index)
    print(pnts_F.x_index)

    pnts_T = finder.zigzag_section(lons=target_lons,
                                   lats=target_lats,
                                   grid='t'
             )

    ax.plot(target_lons, target_lats, 'v-', transform=transform)

    print(len(ds_dom.glamt.isel(x=pnts_T.x_index,y=pnts_T.y_index)))
    print(len(ds_dom.gphit.isel(x=pnts_T.x_index,y=pnts_T.y_index)))

    ax.plot(ds_dom.glamt.isel(x=pnts_T.x_index,
                              y=pnts_T.y_index
                             ), 
            ds_dom.gphit.isel(x=pnts_T.x_index,
                              y=pnts_T.y_index
                             ),
            'b+', transform=transform)

    ax.plot(ds_dom.glamf.isel(x=pnts_F.x_index,
                              y=pnts_F.y_index
                             ),
            ds_dom.gphif.isel(x=pnts_F.x_index,
                              y=pnts_F.y_index
                             ),
            'mo', transform=transform)

    ax.plot(ds_dom.glamu.isel(x=pnts_UV['u'].x_index,
                              y=pnts_UV['u'].y_index
                             ),
            ds_dom.gphiu.isel(x=pnts_UV['u'].x_index,
                              y=pnts_UV['u'].y_index
                             ),
            'g>', transform=transform)
    ax.plot(ds_dom.glamv.isel(x=pnts_UV['v'].x_index,
                              y=pnts_UV['v'].y_index
                             ),
            ds_dom.gphiv.isel(x=pnts_UV['v'].x_index,
                              y=pnts_UV['v'].y_index
                             ),
            'r^', transform=transform)

ax.set_extent(map_lims)

out_name ='test.png'
plt.savefig(out_name,bbox_inches="tight", pad_inches=0.1)
plt.close()



