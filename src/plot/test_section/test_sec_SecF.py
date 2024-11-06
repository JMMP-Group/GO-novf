#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import xarray as xr
from nsv import SectionFinder
import cartopy.crs as ccrs
import cartopy.feature as feature
import xoak

def nrst_nghbr(lons, lats, grids: dict, grid: str) -> xr.Dataset:
        """
        Given the coordinates defining a section, find the nearest points
        on a model grid.

        Args:
            lons (1D array-like): Longitudes defining a section
            lats (1D array-like): Latitudes defining a section
            grids (dict) : dict of the grids of the model
            grid (string): Model grid `{"u", "v", "t", "f"}`

        Returns:
            Dataset: Dataset with model coordinates and indexes
        """
        
        grids[grid].xoak.set_index(("lat", "lon"), "sklearn_geo_balltree")

        return grids[grid].xoak.sel(lat=xr.DataArray(lats), lon=xr.DataArray(lons))


# Define the section we want to plot:
list_sec = [
            {'lon':[ 0.34072625, -3.56557722,-18.569585  ,-26.42872351, -30.314948] , 
             'lat':[68.26346438, 65.49039963, 60.79252542, 56.24488972,  52.858934]}, # Iceland-Faroe Ridge
            {'lon':[-10.84451672, -25.30818606, -35., -44.081319] , 
             'lat':[71.98049514,  66.73449533,  61.88833838,  56.000932]}, # Denmark Strait
            {'lon':[-43.23, -0.61] ,
             'lat':[ 62.33, 62.20]}
           ] 

proj = ccrs.Mercator()

domcfg = '/data/users/dbruciaf/GOSI10_input_files/MEs_novf/025/domain_cfg_MEs_novf_4env_2930_r12_r12-r075-r040-035_it2.nc'

ds_dom = xr.open_dataset(domcfg, drop_variables=("x", "y","nav_lev")).squeeze()
ds_dom = ds_dom.rename({"nav_lev": "z"})

# Extracting only the part of the domain we need

ds_dom = ds_dom.isel(x=slice(880,1150), y=slice(880,1140))

LLcrnrlon = -46.00 #-43. #-46.00
LLcrnrlat =  55    # 60. # 57.00
URcrnrlon = -8.   # -26. #-14.
URcrnrlat =  71    # 64. # 70.0

map_lims = [LLcrnrlon, URcrnrlon, LLcrnrlat, URcrnrlat]

fig = plt.figure(figsize=(25, 25), dpi=100)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[:1], projection=proj)
ax.coastlines(linewidth=4, zorder=6)
ax.add_feature(feature.LAND, color='gray',edgecolor='black',zorder=5)

# Drawing settings
transform = ccrs.PlateCarree()

ax.plot(ds_dom.glamt, ds_dom.gphit, 'k+', transform=transform)

grids = {}
for grid in ("u", "v", "t", "f"):
    ds = xr.Dataset(
       coords={
               "lon": ds_dom[f"glam{grid}"],
               "lat": ds_dom[f"gphi{grid}"],
       }
    )
    ds = ds.squeeze(drop=True)
    for key, value in ds.sizes.items():
        ds[f"{key}_index"] = xr.DataArray(range(value), dims=key)
    grids[grid] = ds.cf.guess_coord_axis()

for sec in list_sec:

    target_lons = sec['lon']
    target_lats = sec['lat']

    finder = SectionFinder(ds_dom)

    ds_pnt_t = finder.zigzag_section(lons=target_lons,
                                     lats=target_lats,
                                     grid='t'
               )

    # Find dimension name
    dim = list(ds_pnt_t.dims)[0]
    ds_pnt_t[dim] = ds_pnt_t[dim]

    # Compute diff and find max index of each pair
    ds_diff = ds_pnt_t.diff(dim)
    ds_roll = ds_pnt_t.rolling({dim: 2}).max().dropna(dim)

    #print(ds_diff)
    #print(ds_roll)

    # TO BE ADAPTED FOR OUR CASE
    # Fill dictionary
    ds_dict = {}

    for grid in ("u", "v"):

        # Apply mask
        # Meridional: v
        # Zonal: u
        if grid == "u": 
           ds = ds_roll.where(
                   np.logical_and(ds_diff['x_index']!=0, ds_diff['y_index']==0), drop=True
                )
        elif grid == "v":
           ds = ds_roll.where(
                   np.logical_and(ds_diff['y_index']!=0, ds_diff['x_index']==0), drop=True
                )

        #print(grid)
        #print(ds['points'].values)

        da_dim = ds[dim].values

        if not ds.sizes[dim]:
           # Empty: either zonal or meridional
           continue

        # Find new lat/lon
        if grid == "u":
           sx=-1
           sy=0
        elif grid == "v":
           sx=0
           sy=-1

        ds = grids[grid].isel(
                x=xr.DataArray(ds["x_index"].astype(int)+sx, dims=dim),
                y=xr.DataArray(ds["y_index"].astype(int)+sy, dims=dim),
             )
        ds = nrst_nghbr(ds["lon"], ds["lat"], grids, grid)

        # Assign coordinate - useful to concatenate u and v after extraction
        ds_dict[grid] = ds.assign_coords({dim: da_dim}) # - 1})

    if 'u' in ds_dict.keys(): ds_pnt_u = ds_dict['u']
    if 'v' in ds_dict.keys(): ds_pnt_v = ds_dict['v']

    #ax.plot(target_lons, target_lats, 'v-', transform=transform)

    ax.plot(ds_pnt_t.lon, 
            ds_pnt_t.lat,
            'b+', transform=transform)
     
    if 'u' in ds_dict.keys():
       #print(ds_pnt_u.y_index)
       #print(ds_pnt_u.x_index)
       ax.plot(ds_pnt_u.lon,
               ds_pnt_u.lat,
               '>r', transform=transform)

    if 'v' in ds_dict.keys(): 
       #print(ds_pnt_v) 
       ax.plot(ds_pnt_v.lon,
               ds_pnt_v.lat,
               '^g', transform=transform)

ax.set_extent(map_lims)

out_name ='test_SecF.png'
plt.savefig(out_name,bbox_inches="tight", pad_inches=0.1)
plt.close()



