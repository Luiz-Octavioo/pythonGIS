# Import Modules
import rasterio
import geopandas as gpd
from rasterio.mask import mask


def clip_raster_shp(raster, shape, out_path, save_raster=True):
    """
    Clip raster to shapefile

    raster: rasterio object

    shape: shapefile object

    out_path: path to save clipped raster

    save_raster: boolean, if True save clipped raster

    returns: clipped raster, metadata
    """
    # Open raster
    src = rasterio.open(raster)
    # Open shapefile
    shp = gpd.read_file(shape)
    # Raster and shapefile must have the same projection
    shp.set_crs(epsg=4326, inplace=True)
    shp.to_crs(src.crs, inplace=True)
    # Clip raster to shapefile
    out_image, out_transform = mask(src, shp.geometry, crop=True, nodata=-9999, all_touched=True)
    # Write clipped raster
    out_meta = src.meta.copy()  # Copy metadata
    if save_raster:
        with rasterio.open(out_path, 'w', **out_meta) as dest:
            dest.write(out_image)
    return out_image, out_meta
