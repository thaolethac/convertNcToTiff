import geopandas as gpd
from shapely.geometry import box
from cropNcByShp import cropNcByShp
def convertNcToTif(shapefile_path,input_nc,output_nc,variable_name):

    # Đọc toàn bộ file shapefile
    gdf = gpd.read_file(shapefile_path)

    # Lấy hình chữ nhật bao quanh dữ liệu
    bounding_box = gdf.total_bounds
    minx, miny, maxx, maxy = bounding_box

    # Tạo đối tượng hình chữ nhật từ tọa độ
    rectangle = box(minx, miny, maxx, maxy)
    cropNcByShp(input_nc,output_nc,variable_name, minx, maxx, miny, maxy)
    
if __name__ == "__main__":
    shapefile_path = 'gadm41_VNM_0.shp'

    input_nc = 'rain_merge_2023111122.nc'

    output_nc = 'rain_merge_2023111122_cropped.nc'
    variable_name = 'rain'

    convertNcToTif(shapefile_path,input_nc,output_nc,variable_name)
    
