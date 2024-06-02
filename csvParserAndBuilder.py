import pandas as pd
from os.path import join
import numpy as np


def find_region_for_province(province):
    try:
        df = pd.read_csv(join('data', 'regiones-chile-upper.csv'))

        return df[df['PROVINCIA'] == province]['REGIÓN'].values[0]
    except IndexError: 
        return "NOTFOUND"

# Read the data
poblacion = pd.read_csv(join('data', 'poblacion.csv'))
potencial = pd.read_csv(join('data', 'potencial_prov.csv'))


poblacion = poblacion[poblacion["EDAD"] == "Total Provincia"]
poblacion = poblacion[["NOMBRE PROVINCIA", "TOTAL POBLACIÓN EFECTIVAMENTE CENSADA"]]
poblacion["NOMBRE PROVINCIA"] = poblacion["NOMBRE PROVINCIA"].apply(lambda x: x.upper())
poblacion["TOTAL POBLACIÓN EFECTIVAMENTE CENSADA"] = poblacion["TOTAL POBLACIÓN EFECTIVAMENTE CENSADA"].str.replace(".", "").astype(int)
poblacion.sort_values(by="NOMBRE PROVINCIA", inplace=True)
poblacion.reset_index(drop=True, inplace=True)
poblacion.to_csv(join("data", "poblacion_provincias.csv"), index=False)

potencial.sort_values(by="NOMBRE PROVINCIA", inplace=True)
potencial.reset_index(drop=True, inplace=True)
potencial["NOMBRE PROVINCIA"] = potencial["NOMBRE PROVINCIA"].apply(lambda x: x.upper())

potencial.to_csv(join("data", "potencial_provincias.csv"), index=False)

mergedDataFrames = pd.merge(poblacion, potencial, on="NOMBRE PROVINCIA", how="inner")

mergedDataFrames["REGION"] = mergedDataFrames["NOMBRE PROVINCIA"].apply(find_region_for_province)

mergedDataFrames.sort_values(by="NOMBRE PROVINCIA", inplace=True)
mergedDataFrames.reset_index(drop=True, inplace=True)


mergedDataFrames.replace(0, np.nan, inplace=True)
mergedDataFrames.interpolate(method='linear', inplace=True, limit_direction='both')
mergedDataFrames.to_csv(join("data", "datos_provincias.2.csv"), index=False)


print(mergedDataFrames["NOMBRE PROVINCIA"])