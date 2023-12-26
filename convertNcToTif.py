import xarray as xr
import rasterio
from rasterio.transform import from_origin
import geopandas as gpd
from shapely.geometry import box
import os
# from common import file_extent_shp_vietnam

def cropNcByShp(shapefile_path,input_nc,output_nc, variable_name):
    gdf = gpd.read_file(shapefile_path)

    bounding_box = gdf.total_bounds
    lon_min, lat_min, lon_max, lat_max = bounding_box

    rectangle = box(lon_min, lat_min, lon_max, lat_max)
    dataset = xr.open_dataset(input_nc, engine='netcdf4')
    cropped_data = dataset[variable_name].sel(
        lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))

    # Lưu dữ liệu đã cắt vào file mới
    cropped_data.to_netcdf(output_nc)
    found = True
    for name, value in dataset.data_vars.items():
        if variable_name in name:
            try:
                cropped_data = dataset[name].sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))
            except:
                cropped_data = dataset[name].sel(longitude=slice(lon_min, lon_max), latitude=slice(lat_min, lat_max))
            cropped_data.to_netcdf(output_nc)

    dataset.close()

import numpy as np

def convert_nc_to_tif(input_nc_file, output_tif_file, variable_name):
    input_shp = 'gadm41_VNM_0.shp'
    output_nc = f'{input_nc_file.replace(".nc", "")}_cropped.nc'

    # Cắt file NC về chuẩn map VN
    cropNcByShp(input_shp, input_nc_file, output_nc, variable_name)

    # Convert file NC to TIFF
    nc_data = xr.open_dataset(output_nc)
    data_variable = None
    for name, value in nc_data.data_vars.items():
        if variable_name in name:
            data_variable = nc_data[name]

    # Get coordinate values
    lats = np.array(data_variable.lat)
    lons = np.array(data_variable.lon)
    print(lats)
    print(lons)
    # Create transform using the first and last lat/lon values
    transform = from_origin(lons.min(), lats.max(), lons[1] - lons[0], lats[1] - lats[0])


    with rasterio.open(output_tif_file, 'w', driver='GTiff',
                       height=data_variable.shape[0], width=data_variable.shape[1],
                       count=1, dtype=str(data_variable.dtype),
                       transform=transform) as dst:
        dst.write(data_variable.data, 1)

    nc_data.close()
    # os.remove(output_nc)

if __name__ == "__main__":
    input_nc = 'rain_merge_2023111122.nc'
    output_tif = 'rain_merge_2023111122.tif'
    variable_name = 'rain'

    convert_nc_to_tif(input_nc, output_tif, variable_name)
