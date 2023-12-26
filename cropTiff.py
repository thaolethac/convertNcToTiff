from osgeo import gdal, ogr, osr
from shapely.geometry import mapping, shape
import fiona

# Đường dẫn đến file TIFF và Shapefile
tiff_path = 'duong_dan_den_file.tiff'
shp_path = 'duong_dan_den_file.shp'

# Đường dẫn đến file đầu ra (kết quả cắt)
output_path = 'duong_dan_den_file_ket_qua.tiff'

# Mở file TIFF và Shapefile
tiff_dataset = gdal.Open(tiff_path)
shp_dataset = ogr.Open(shp_path)
shp_layer = shp_dataset.GetLayer()

# Lấy hệ tọa độ từ Shapefile
spatial_ref = shp_layer.GetSpatialRef()

# Tạo một bộ chuyển đổi từ hệ tọa độ của Shapefile sang hệ tọa độ của TIFF
transform = osr.CoordinateTransformation(shp_layer.GetSpatialRef(), tiff_dataset.GetProjection())

# Lấy đối tượng đường biên từ Shapefile
feature = shp_layer.GetNextFeature()
geom = feature.GetGeometryRef()
geom.Transform(transform)
boundary = shape(mapping(geom))

# Lấy thông tin vùng quét (extent) của file TIFF
x_min, x_max, y_min, y_max = tiff_dataset.GetGeoTransform()[0], tiff_dataset.GetGeoTransform()[0] + tiff_dataset.RasterXSize * tiff_dataset.GetGeoTransform()[1], tiff_dataset.GetGeoTransform()[3] + tiff_dataset.RasterYSize * tiff_dataset.GetGeoTransform()[5], tiff_dataset.GetGeoTransform()[3]

# Cắt file TIFF theo đường biên của Shapefile
x_res = int((x_max - x_min) / tiff_dataset.GetGeoTransform()[1])
y_res = int((y_max - y_min) / tiff_dataset.GetGeoTransform()[5])

gdal.Warp(output_path, tiff_dataset, format='GTiff', outputBounds=(boundary.bounds[0], boundary.bounds[1], boundary.bounds[2], boundary.bounds[3]), width=x_res, height=y_res)

# Đóng tất cả dataset
tiff_dataset = None
shp_dataset = None
