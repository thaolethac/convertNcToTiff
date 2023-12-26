import xarray as xr

def convert_to_standard_grid(input_file, standard_file, output_file):
    # Đọc dữ liệu từ file chuẩn
    standard_data = xr.open_dataset(standard_file)

    # Đọc dữ liệu từ file chưa chuẩn
    input_data = xr.open_dataset(input_file)

    # Lấy các chiều dài và chiều rộng từ file chuẩn
    lon_standard = standard_data['lon']
    lat_standard = standard_data['lat']

    # Chọn và cắt dữ liệu từ file chưa chuẩn để phù hợp với ô lưới của file chuẩn
    input_data_subset = input_data.interp(lon=lon_standard, lat=lat_standard)

    # Lưu kết quả vào file mới
    input_data_subset.to_netcdf(output_file)

    # Đóng các file đã mở
    standard_data.close()
    input_data.close()

standard_tif_file = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.nc'
input_nc_file = 'canh_bao_08-10-2023-030000_CDH_IFS_1_0.9.nc'
output_nc_file = 'file_chuan_aaa.nc'

convert_to_standard_grid(standard_tif_file, input_nc_file, output_nc_file)
