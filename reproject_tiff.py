import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject, Resampling

def reproject_tiff(input_tif_file, output_tif_file, dst_crs):
    with rasterio.open(input_tif_file) as src:
        # Tính toán transform mới
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)

        # Mở tệp đầu ra với hệ tọa độ mới
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(output_tif_file, 'w', **kwargs) as dst:
            # Thực hiện chuyển đổi tọa độ
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest
            )

if __name__ == "__main__":
    input_tif_file = 'input.tif'  # Thay bằng đường dẫn tới tệp TIFF của bạn
    output_tif_file = 'output_vn1993.tif'  # Tên tệp TIFF đầu ra mong muốn
    dst_crs = 'EPSG:4754'  # Hệ tọa độ Địa Lý Việt Nam 1993 (VN1993)

    reproject_tiff(input_tif_file, output_tif_file, dst_crs)