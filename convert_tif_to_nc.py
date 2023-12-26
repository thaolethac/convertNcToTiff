import rioxarray
import xarray as xr

def convert_tif_to_nc(tif_file, nc_output):
    # Open the GeoTIFF file using rioxarray
    tif_data = rioxarray.open_rasterio(tif_file)
    lon = tif_data['x'].values
    lat = tif_data['y'].values
    # Save the data to NetCDF file
    ds_new = xr.Dataset({'rain': (['lat', 'lon'], tif_data.values[0])},
                    coords={'lon': ('lon', lon),
                            'lat': ('lat', lat)})
    ds_new.to_netcdf(nc_output, format="NETCDF4")

if __name__ == "__main__":
    tif_file = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.tif'  # Replace with the path to your GeoTIFF file
    nc_output = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.nc'      # Replace with the desired output NetCDF file name

    convert_tif_to_nc(tif_file, nc_output)