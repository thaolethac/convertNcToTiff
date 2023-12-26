import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from geopy.distance import geodesic
import cv2
convert = 111.32
lon_min, lon_max, lat_min, lat_max = 0,0,0,0
def convert_netcdf_to_image(netcdf_file, variable_name, output_image):
    dataset = xr.open_dataset(netcdf_file)
    print(dataset)

    variable_data = dataset[variable_name]
    print(variable_data[1])
    dataset.close()
    # Tính kích thước pixel
    lon_min = dataset['longitude'].min().values
    lon_max = dataset['longitude'].max().values
    lat_min = dataset['latitude'].min().values
    lat_max = dataset['latitude'].max().values
    lon_x = dataset['longitude'].values[0]
    # target_lon = 102.12845191122113231213123

    # # Tìm vị trí của target_lon trong mảng lon_values
    # index_of_target_lon = np.where(lon_x == target_lon)[0]

    # # In ra kết quả
    # print("Vị trí của lon có giá trị", target_lon, "là:", index_of_target_lon)
    # distance = geodesic((lat_min, lon_min), (lat_min, lon_max)).kilometers
    lon_resolution_deg = (lon_max - lon_min) / (len(dataset['longitude']) - 1)
    # print(lon_min)
    # print(lon_max)
    # Chuyển đổi từ độ sang km
    lon_resolution_km = lon_resolution_deg * convert
    dis_lon = (lon_max-lon_min)*convert / lon_resolution_km
    dis_lat = (lat_max-lat_min)*convert / lon_resolution_km
    print(dis_lon)
    print(dis_lat)

    # Tính kích thước của hình ảnh trong đơn vị km
    image_height_km = abs(variable_data.latitude.diff('latitude').sum().values)*convert
    image_width_km = abs(
        variable_data.longitude.diff('longitude').sum().values)*convert
    lon_diff = variable_data.longitude.diff('longitude')

    # Display the result
    # print("Difference in longitude values:")
    # print(lon_diff)
    #
    fig, ax = plt.subplots(facecolor='black')

    im = plt.imshow(variable_data, cmap='viridis', extent=(variable_data.longitude.min(),
                                                                   variable_data.longitude.max(),
                                                                   variable_data.latitude.min(),
                                                                   variable_data.latitude.max()),
               vmin=variable_data.min(), vmax=variable_data.max())
    # plt.colorbar(label=variable_name)

    fig.patch.set_facecolor('black')

    plt.xticks([])
    plt.yticks([])

    plt.axis('off')

    print(
        f"Kích thước của mỗi ô lưới : {lon_resolution_km:.2f} km")

    print(f"Kích thước của hình ảnh theo chiều cao: {image_height_km} km")
    print(f"Kích thước của hình ảnh theo chiều rộng: {image_width_km} km")

    plt.savefig(output_image, facecolor=fig.get_facecolor()) 
    plt.show()


    dataset.close()

if __name__ == "__main__":
    netcdf_file = 'AWS_ADJ_202311100000_01H.nc'

    variable_name = '202311100000'
    output_image = 'file_chuan.png'

    convert_netcdf_to_image(netcdf_file, variable_name, output_image)