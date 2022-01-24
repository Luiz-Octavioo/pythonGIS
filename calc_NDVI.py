# Import Modules
import rasterio as rio
from rasterio.fill import fillnodata
import numpy as np
import matplotlib.pyplot as plt

R_path = '/home/luiz/Python/Python-Geo-Utils/LC08_L1TP_226071_20200804_20200821_01_T1_sr_band4.tif'
NIR_path = '/home/luiz/Python/Python-Geo-Utils/LC08_L1TP_226071_20200804_20200821_01_T1_sr_band5.tif'


# Define Functions to calculate NDVI from Landsat8
def NDVI(R, NIR, fill_data=False, save_raster=False, raster_path=None):
    # Open rasters
    R = rio.open(R)
    NIR = rio.open(NIR)
    # Get band values
    R_array = R.read(1).astype(np.float32)
    NIR_array = NIR.read(1).astype(np.float32)
    # Calculate NDVI
    NDVI_array = np.divide(np.subtract(NIR_array, R_array), np.add(NIR_array, R_array),
                           where=np.subtract(NIR_array, R_array) != 0)

    # Remove nodata values
    NDVI_array[NDVI_array == 0] = np.nan
    if fill_data:
        # fill nodata values using rasterio.fillnodata
        NDVI_array = fillnodata(NDVI_array, mask=(~np.isnan(NDVI_array)),
                                max_search_distance=100, smoothing_iterations=0)

    ### Settings params to save raster
    meta = R.meta.copy()
    meta.update(dtype=np.float32, height=NDVI_array.shape[0], width=NDVI_array.shape[1])
    # Save NDVI raster
    if save_raster:
        with rio.open(raster_path, 'w', **meta) as dest:
            dest.write(NDVI_array, 1)

    # Return NDVI array
    return NDVI_array


# call function
NDVI_array = NDVI(R_path, NIR_path)

# Plot NDVI
fig, ax = plt.subplots()
cs = ax.imshow(NDVI_array, cmap='RdYlGn', vmax=1, vmin=-1)
# Colorbar
cbar = plt.colorbar(cs, ax=ax)
cbar.ax.set_ylabel('NDVI',
                   fontdict={'fontsize': 10, 'fontweight': 'bold'})
plt.show()
