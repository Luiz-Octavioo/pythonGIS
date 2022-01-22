from random_points import random_points
import geopandas as gpd
import rasterio as rio
import rasterstats as rs

# Create geodataframe with random points
# Read shapefile
shapefile = '/home/luiz/Documentos/Shapefiles/sebal_shapes/humaita_sebal/humaita.shp'
shape = gpd.read_file(shapefile)

# Use function for random points inside shapefile
points = random_points(shape, 100)
# Create dataframe
gdf = gpd.GeoDataFrame(geometry=points)

# open raster with rasterio
raster = '/media/luiz/Luiz_Octavio/Sebal_Carlos/Humaita_2019/Rn_Humaita_2019.tif'
with rio.open(raster) as src:
    affine = src.transform
    profile = src.profile  # Get raster profile
    img = src.read(1)  # read raster values

print('Informações sobre o raster: ', profile)


# Raster and shapefile must have the same
gdf.set_crs(epsg=4326, inplace=True)
gdf.to_crs(epsg=32620, inplace=True)
print('CRS do Shapefile: ', gdf.crs)
print('CRS do Raster: ', profile['crs'])

# Extract values from raster using rasterstats
extract = rs.point_query(gdf, img, affine=affine, nodata=-9999)
gdf['Value'] = extract

print(gdf)





