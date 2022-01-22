############################################################################
# Autor: Luiz Octavio F. dos Santos                                        #
# Doutorando no Programa de Pós-Graduação em Física Ambiental PPGFA/UFMT   #
# Contato: luizpgfa@gmail.com                                              #
# Script para gerar pontos aleatórios em um shapefile                      #
# Mode de uso: inserir o shapefile e definir o número de pontos aleatórios #
#                                                                          #
# Adaptdado de GISDOCTOR                                                   #
############################################################################
# Create random points inside shapefile

# Import modules
import geopandas as gpd
import random
from shapely.geometry import Point
import matplotlib.pyplot as plt

# # Read shapefile
# shapefile = '/home/luiz/Documentos/Shapefiles/sebal_shapes/humaita_sebal/humaita.shp'
# shape = gpd.read_file(shapefile)


# Function for random points
def random_points(shp, n):
    # Get shapefile bounds
    shp_df = shp.bounds.to_dict()
    # transform dataframe in list
    bounds_list = []
    for key, value in shp_df.items():
        bounds_list.append(value)
    bounds_list = [d[0] for d in bounds_list]
    minx, miny, maxx, maxy = bounds_list

    # Create random points equal to n size
    points = []
    while len(points) < n:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        random_point = Point(x, y)
        # Consider only points inside shapefile
        if random_point.within(shp.geometry[0]):
            points.append(random_point)

    return points


# # Use function for random points inside shapefile
# points = random_points(shape, 500)
# # Create dataframe
# df = gpd.GeoDataFrame(geometry=points)
#
# # Plot
# fig, ax = plt.subplots(1, figsize=(10, 10))
# shape.plot(edgecolor='black', color='white', ax=ax)
# df.plot(ax=ax, color='royalblue', markersize=10, marker='o')
# plt.show()
