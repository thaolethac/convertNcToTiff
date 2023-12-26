import geopandas as gpd
from fiona.crs import from_epsg

def add_crs_to_shapefile(shapefile_path, crs_epsg):
    # Đọc shapefile
    gdf = gpd.read_file(shapefile_path)

    # Kiểm tra xem CRS đã tồn tại trong shapefile chưa
    if gdf.crs is None:
        # Thêm thông tin CRS nếu nó chưa tồn tại
        gdf.crs = from_epsg(crs_epsg)

        # Lưu shapefile với CRS mới
        gdf.to_file(shapefile_path)
        print(f"CRS information added to {shapefile_path}")
    else:
        print("CRS information already exists in the shapefile.")

# if __name__ == "__main__":
#     shapefile_path = 'your_shapefile.shp'  # Thay 'your_shapefile.shp' bằng đường dẫn tới file shapefile của bạn
#     crs_epsg = 4326  # Thay thế bằng mã EPSG của hệ tọa độ bạn muốn thêm

#     add_crs_to_shapefile(shapefile_path, crs_epsg)
