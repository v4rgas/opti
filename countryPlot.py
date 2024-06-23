import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from os.path import join

# Cargar datos
provincias = pd.read_csv(join('data', 'datos_provincias.csv'))
operaciones = pd.read_csv(join('outputs', 'op_provincias.csv'))

# Obtener nombres de provincias como array y formato para geocoding
provincias_name = provincias['NOMBRE PROVINCIA'].tolist()
provincias_name = [f"Provincia de {x.capitalize()}, Chile" for x in provincias_name]

# Obtener valores máximos
max_solar = operaciones['SOLAR FINAL'].max()
max_eolica = operaciones['EÓLICA FINAL'].max()
max_hydro = operaciones['HIDRO FINAL'].max()

# Crear geodataframe con las provincias y proyectar
all_provinces = ox.geocode_to_gdf(provincias_name)
all_provinces = ox.project_gdf(all_provinces)

# Crear geodataframe con los centroides de las provincias
all_provinces_centroids = all_provinces.copy()
all_provinces_centroids['geometry'] = all_provinces_centroids.centroid
all_provinces_centroids = all_provinces_centroids.set_geometry('geometry')

# Crear figura: mapa de Chile subdividido por provincias
ax = all_provinces.plot(facecolor='none', edgecolor='black', figsize=(10, 10))

# Agregar puntos de acuerdo a la capacidad instalada para cada tipo de energía
all_provinces_centroids.plot(ax=ax, color='red', markersize=(operaciones['SOLAR FINAL']*1000)/max_solar, alpha=0.5)
all_provinces_centroids.plot(ax=ax, color='blue', markersize=(operaciones['HIDRO FINAL']*1000)/max_hydro, alpha=0.5)
all_provinces_centroids.plot(ax=ax, color='green', markersize=(operaciones['EÓLICA FINAL']*1000)/max_eolica, alpha=0.5)

# Plotear
plt.title('Distribución de energías renovables en Chile\n'
          'Tamaño de los puntos proporcional a la capacidad instalada\n'
          'Rojo: Solar, Azul: Hidro, Verde: Eólica')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid()
plt.show()