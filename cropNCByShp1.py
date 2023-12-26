import xarray as xr
import rasterio
from rasterio.features import geometry_mask
import fiona
import numpy as np
from rasterio.transform import from_origin

def clip_and_flip_netcdf_by_shapefile(nc_file, shapefile, output_file):
    ds = xr.open_dataset(nc_file)

    with fiona.open(shapefile, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
        with rasterio.open(nc_file) as src:
            mask = geometry_mask(shapes, out_shape=(ds.sizes['lat'], ds.sizes['lon']),
                                  transform=src.transform, invert=True)

            clipped_ds = ds.where(mask)

            clipped_ds.to_netcdf(output_file)
def convert_nc_to_tif(input_nc_file, output_tif_file, variable_name):
    input_shp = 'gadm41_VNM_0.shp'
    output_nc = f'{input_nc_file.replace(".nc", "")}_cropped.nc'

    # Cắt file NC về chuẩn map VN
    clip_and_flip_netcdf_by_shapefile(input_nc_file, input_shp, output_nc)

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
if __name__ == "__main__":
    # Replace the following paths with your NetCDF file, shapefile, and output file paths
    
    input_nc = 'rain_merge_2023111122.nc'
    input_shp = "gadm41_VNM_0.shp"
    output_nc_cropped = 'rain_merge_2023111122_cropped_new.tif'
    variable_name = 'rain'
    convert_nc_to_tif(input_nc, output_nc_cropped, variable_name)



# Thực hiện cắt NetCDF sử dụng Shapefile
