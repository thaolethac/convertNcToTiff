import xarray as xr

def crop_netcdf(netcdf_file, variable_name, lon_min, lon_max, lat_min, lat_max):
    # Mở file netCDF
    dataset = xr.open_dataset(netcdf_file)

    # Chọn phần của dữ liệu trong khoảng giới hạn kinh độ và vĩ độ
    cropped_data = dataset[variable_name].sel(
        lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))

    # Lưu dữ liệu đã cắt vào file mới
    cropped_data.to_netcdf('cropped_' + netcdf_file)

    # Đóng file netCDF
    dataset.close()

# Sử dụng hàm để cắt file .nc
netcdf_file = 'rain_merge_2023111123.nc'
variable_name = 'rain'
lon_min, lon_max = 102.14458465500007, 109.46917000000008  # Điều chỉnh theo nhu cầu
lat_min, lat_max = 8.381355000000099, 23.39269256700004    # Điều chỉnh theo nhu cầu

crop_netcdf(netcdf_file, variable_name, lon_min, lon_max, lat_min, lat_max)
