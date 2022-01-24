# Import Modules
import matplotlib.pyplot as plt
from matplotlib import colors
import rasterio as rio
import numpy as np
from scipy.stats import pearsonr

# City
city = 'Humaita'
year = '2019'
varx = 'ALFA'
vary = 'Rn'

# Rasters path
raster_X = f'/media/luiz/Luiz_Octavio/Sebal_Carlos/{city}_2019/{varx}_{city}_2019.tif'
raster_Y = f'/media/luiz/Luiz_Octavio/Sebal_Carlos/{city}_2019/{vary}_{city}_2019.tif'
#########################################################################
# read rasters
X = rio.open(raster_X)
Y = rio.open(raster_Y)
########################################################################
# Read rasters data bands
X_array = X.read(1).astype(np.float)  # Get the first band
Y_array = Y.read(1).astype(np.float)  # Get the first band

# Flaten arrays
X_array = X_array.flatten()
Y_array = Y_array.flatten()
#########################################################################
# Regression Params
# Remove autodetected range of [nan, nan] is not finite
x = X_array[np.isfinite(X_array)]
y = Y_array[np.isfinite(X_array)]

# Mask array based another array
mask = np.isnan(y)
x[mask] = y[mask]
# Remove nan values
x = x[~np.isnan(x)]
y = y[~np.isnan(y)]

nbins = 200
Y, xi, yi = np.histogram2d(x, y, bins=nbins, density=False)

# Correlation
alpha = 0.05
stat, p = pearsonr(x, y)

# Regression model [numpy]
m, b = np.polyfit(x, y, 1)
# Perfect Linear Model
mi, bi = np.polyfit(xi, yi, 1)

# Params for create box
bbox = dict(boxstyle="round",
            facecolor='white',
            edgecolor='black')
arrowprops = dict(
    arrowstyle="->",
    connectionstyle="angle, angleA = 0, angleB = 90,\
    rad = 10")


# Plot Regression line with dispersion
def regression_plot(x, y, nbins, xlabel, ylabel, ax, cmap='jet'):
    # Histogram 2D
    cs = ax.hist2d(x, y,
                   bins=nbins,
                   cmap=cmap,
                   norm=colors.LogNorm())
    # Plot Regression line
    ax.plot(x, m * x + b, color='black', linestyle='-')  # Regression line
    # ax.plot(xi, mi * xi + bi, color='black', linestyle='--')
    # ax.axhline(0, color='k', linestyle='--', zorder=3, linewidth=0.5)
    # ax.axvline(0, color='k', linestyle='--', zorder=3, linewidth=0.5)
    ax.minorticks_on()
    ax.tick_params(axis='x', which='both', direction='in', bottom=True, top=True)
    ax.tick_params(axis='y', which='both', direction='in', bottom=False, top=False, right=True)
    ax.annotate('R = {:.2f} \np-valor = {:.2f}'.format(stat, p),
                xy=(0.25, 0.88), xycoords='axes fraction',
                bbox=bbox, arrowprops=arrowprops)
    ax.set_xlabel(xlabel, fontdict={'fontsize': 10, 'fontweight': 'bold'})
    ax.set_ylabel(ylabel, fontdict={'fontsize': 10, 'fontweight': 'bold'})
    # Add colorbar
    cbar = plt.colorbar(cs[3], ax=ax)
    cbar.ax.set_ylabel('Density', fontdict={'fontsize': 10, 'fontweight': 'bold'})
    plt.show()


# Call function
fig, ax = plt.subplots()
regression_plot(x, y, nbins, varx, vary, ax=ax)
