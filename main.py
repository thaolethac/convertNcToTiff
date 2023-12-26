import xarray as xr
from convert_tif_to_nc import convert_tif_to_nc

# Đầu vào là 2 file .nc, 1 file lấy làm chuẩn và 1 file cần đưa về dạng chuẩn
def interpolate_to_standard_grid(standard_file, non_standard_file, output_file):
    standard_data = xr.open_dataset(standard_file)
    non_standard_data = xr.open_dataset(non_standard_file)

    standard_lon = standard_data['lon'].values
    standard_lat = standard_data['lat'].values

    non_standard_data_subset = non_standard_data.sel(
        lon=slice(standard_lon.min(), standard_lon.max()),
        lat=slice(standard_lat.min(), standard_lat.max())
    )

    interpolated_data = non_standard_data_subset.interp(
        lon=standard_lon, lat=standard_lat, method='linear'
    )

    interpolated_data.to_netcdf(output_file)

if __name__ == "__main__":
    # Convert file Tif thành file Nc
    tif_file = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.tif'  # Replace with the path to your GeoTIFF file
    nc_output = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.nc' 
    convert_tif_to_nc(tif_file,nc_output)
    
    standard_file = nc_output
    non_standard_file = '3km.nc'
    output_file = 'file_sau_khi_chuan_hoa_3km.nc'

    interpolate_to_standard_grid(standard_file, non_standard_file, output_file)
