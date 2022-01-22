import rasterio as rio
from rasterio.plot import show
import seaborn as sns
import matplotlib.pyplot as plt

# Open the raster file
raster = '/media/luiz/Luiz_Octavio/Sebal_Carlos/Humaita_2019/NDVI_Humaita_2019.tif'

with rio.open(raster) as src:
    # Transform the raster
    transform = src.transform
    # Get the raster data
    img = src.read(1)
    # Get the raster profile
    profile = src.profile

# plot the raster
fig, ax = plt.subplots()
cs = ax.imshow(img, cmap='RdYlGn', vmin=0, vmax=1)
# cs = show(img, cmap='RdYlGn', vmin=0, vmax=1)
# insert colorbar
cbar = fig.colorbar(cs, ax=ax)
# set the title of colorbar
cbar.set_label('NDVI')
# show the plot
plt.show()

# # plot the histogram
fig, ax = plt.subplots()
sns.histplot(img.flatten(), kde=True, ax=ax)
ax.set_title('Histogram')
ax.set_xlabel('NDVI values')
# Show the plot
plt.show()

# print(img.shape)