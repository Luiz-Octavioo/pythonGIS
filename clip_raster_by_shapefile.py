# Import modules
import rasterio
import geopandas as gpd
from rasterio.plot import show
from rasterio.mask import mask

# Input raster and shapefile
raster = '/media/luiz/Luiz_Octavio/Sebal_Carlos/Humaita_2019/NDVI_Humaita_2019.tif'
shapefile = '/home/luiz/Documentos/Shapefiles/sebal_shapes/humaita_sebal/humaita.shp'
# Read shapefile
shape = gpd.read_file(shapefile)

# Read raster
raster = rasterio.open(raster)

# Raster and shapefile must have the same projection
shape.set_crs(epsg=4326, inplace=True)
shape.to_crs(epsg=32620, inplace=True)

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(shape)

# Clip the raster with Polygon
out_img, out_transform = mask(dataset=raster, shapes=coords, crop=True)
out_meta = raster.meta.copy()

# Save the clipped raster
with rasterio.open('clip_raster.tif', 'w', **out_meta) as dest:
    dest.write(out_img)

# Show the clipped raster
show(out_img, cmap='RdYlGn')