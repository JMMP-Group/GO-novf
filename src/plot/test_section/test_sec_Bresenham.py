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

def bresenham_line(x0, x1, y0, y1):
    '''
    point0 = (y0, x0), point1 = (y1, x1)

    It determines the points of an n-dimensional raster that should be 
    selected in order to form a close approximation to a straight line 
    between two points. Taken from the generalised algotihm on

    http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    '''
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
       # swap(x0, y0)
       t  = y0
       y0 = x0
       x0 = t
       # swap(x1, y1)    
       t  = y1
       y1 = x1
       x1 = t

    if x0 > x1:
       # swap(x0, x1)
       t  = x1
       x1 = x0
       x0 = t
       # swap(y0, y1)
       t  = y1
       y1 = y0
       y0 = t
    
    deltax = np.fix(x1 - x0)
    deltay = np.fix(abs(y1 - y0))
    error  = 0.0

    deltaerr = deltay / deltax
    y = y0

    if y0 < y1:
       ystep = 1
    else:
       ystep = -1

    c=0
    pi = np.zeros(shape=[x1-x0+1])
    pj = np.zeros(shape=[x1-x0+1])
    for x in np.arange(x0,x1+1) :
        if steep:
           pi[c]=y
           pj[c]=x
        else:
           pi[c]=x
           pj[c]=y
        error = error + deltaerr
        if error >= 0.5:
           y = y + ystep
           error = error - 1.0
        c += 1

    return pj, pi


def get_poly_line_ij(points_i, points_j):
    '''
    get_poly_line_ij draw rasterised line between vector-points
    
    Description:
    get_poly_line_ij takes a list of points (specified by 
    pairs of indexes i,j) and draws connecting lines between them 
    using the Bresenham line-drawing algorithm.
    
    Syntax:
    line_i, line_j = get_poly_line_ij(points_i, points_i)
    
    Input:
    points_i, points_j: vectors of equal length of pairs of i, j
                        coordinates that define the line or polyline. The
                        points will be connected in the order they're given
                        in these vectors. 
    Output:
    line_i, line_j: vectors of the same length as the points-vectors
                    giving the i,j coordinates of the points on the
                    rasterised lines. 
    '''
    line_i=[]
    line_j=[]

    line_n=0

    if len(points_i) == 1:
       line_i = points_i
       line_j = points_j
    else:
       for fi in np.arange(len(points_i)-1):
           # start point of line
           i1 = points_i[fi]
           j1 = points_j[fi]
           # end point of line
           i2 = points_i[fi+1]
           j2 = points_j[fi+1]
           # 'draw' line from i1,j1 to i2,j2
           pj, pi = bresenham_line(i1,i2,j1,j2)
           if pi[0] != i1 or pj[0] != j1:
              # beginning of line doesn't match end point, 
              # so we flip both vectors
              pi = np.flipud(pi)
              pj = np.flipud(pj)

           plen = len(pi)

           for PI in np.arange(plen):
               line_n = PI
               if len(line_i) == 0 or line_i[line_n-1] != pi[PI] or line_j[line_n-1] != pj[PI]:
                  line_i.append(int(pi[PI]))
                  line_j.append(int(pj[PI]))


    return line_j, line_i


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

    ds_tgt = nrst_nghbr(target_lons, target_lats, grids, 't')
    pnts_x_t, pnts_y_t = (ds_tgt[f"{i}_index"].data for i in ("x", "y"))
    line_y_t, line_x_t = get_poly_line_ij(pnts_x_t, pnts_y_t)
    ds_pnt_t = grids['t'].isel(x = xr.DataArray(line_x_t, dims="points"), 
                               y = xr.DataArray(line_y_t, dims="points"))
    ds_pnt_t["x_index"] = xr.DataArray(line_x_t, dims="points")
    ds_pnt_t['y_index'] = xr.DataArray(line_y_t, dims="points")
    ds_pnt_t = ds_pnt_t.assign_coords({'points': ds_pnt_t.points})

    # Compute diff and find max index of each pair
    ds_diff = ds_pnt_t.diff('points')
    ds_roll = ds_pnt_t.rolling({'points': 2}).max().dropna('points')

    #print(ds_diff)
    #print(ds_roll)

    # TO BE ADAPTED FOR OUR CASE
    # Fill dictionary
    ds_dict = {}

    for grid in ("u", "v", "f"):

        # Apply mask
        # Meridional: v
        # Zonal: u
        # diagonal: f
        if grid == "f":
           ds = ds_roll.where(
                   np.logical_and(ds_diff['y_index'],ds_diff['x_index']), drop=True
                )
        elif grid == "u": 
           ds = ds_roll.where(
                   np.logical_and(ds_diff['x_index']!=0, ds_diff['y_index']==0), drop=True
                )
        elif grid == "v":
           ds = ds_roll.where(
                   np.logical_and(ds_diff['y_index']!=0, ds_diff['x_index']==0), drop=True
                )

        #print(grid)
        #print(ds['points'].values)

        da_dim = ds['points'].values

        if not ds.sizes['points']:
           # Empty: either zonal or meridional
           continue

        # Find new lat/lon
        if grid == "f":
           sx=-1
           sy=-1
        elif grid == "u":
           sx=-1
           sy=0
        elif grid == "v":
           sx=0
           sy=-1

        ds = grids[grid].isel(
                x=xr.DataArray(ds["x_index"].astype(int)+sx, dims='points'),
                y=xr.DataArray(ds["y_index"].astype(int)+sy, dims='points'),
             )
        ds = nrst_nghbr(ds["lon"], ds["lat"], grids, grid)

        # Assign coordinate - useful to concatenate u and v after extraction
        ds_dict[grid] = ds.assign_coords({'points': da_dim}) # - 1})

    if 'f' in ds_dict.keys(): ds_pnt_f = ds_dict['f']
    if 'u' in ds_dict.keys(): ds_pnt_u = ds_dict['u']
    if 'v' in ds_dict.keys(): ds_pnt_v = ds_dict['v']

    #ax.plot(target_lons, target_lats, 'v-', transform=transform)

    ax.plot(ds_pnt_t.lon, 
            ds_pnt_t.lat,
            'b+', transform=transform)
     
    if 'f' in ds_dict.keys():
       #print(ds_pnt_f.y_index)
       #print(ds_pnt_f.x_index)
       ax.plot(ds_pnt_f.lon,  
               ds_pnt_f.lat,
               'mo', transform=transform)

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

out_name ='test_Bresenham.png'
plt.savefig(out_name,bbox_inches="tight", pad_inches=0.1)
plt.close()



