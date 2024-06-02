import pandas as pd
import numpy as np
from os.path import join


inversiones_df = pd.read_csv(join("data", "inversiones.csv"))

region_to_index = {
    "ARICA Y PARINACOTA": 1,
    "TARAPACÁ": 2,
    "ANTOFAGASTA": 3,
    "ATACAMA": 4,
    "COQUIMBO": 5,
    "VALPARAÍSO": 6,
    "METROPOLITANA": 7,
    "O'HIGGINS": 8,
    "MAULE": 9,
    "ÑUBLE": 10,
    "BIOBÍO": 11,
    "ARAUCANÍA": 12,
    "LOS RÍOS": 13,
    "LOS LAGOS": 14,
    "AYSÉN": 15,
    "MAGALLANES": 16
}

df = inversiones_df.groupby(['REGION', "TIPO"], as_index=False).mean()

df['REGION_INDEX'] = df['REGION'].apply(lambda x: region_to_index[x])

hidro = df[df['TIPO'] == 'Hidro']
solar = df[df['TIPO'] == 'Solar']
eolica = df[df['TIPO'] == 'Eólica']



for region in region_to_index.keys():
    if region not in hidro['REGION'].values:
        new_df = pd.DataFrame([[region, 'Hidro', np.nan, np.nan, region_to_index[region]]], columns=['REGION', 'TIPO', 'MW', 'MM USD', 'REGION_INDEX'])
        df = pd.concat([df, new_df], ignore_index=True)
    if region not in solar['REGION'].values:
        new_df = pd.DataFrame([[region, 'Solar', np.nan, np.nan, region_to_index[region]]], columns=['REGION', 'TIPO', 'MW', 'MM USD', 'REGION_INDEX'])
        df = pd.concat([df, new_df], ignore_index=True)
    if region not in eolica['REGION'].values:
        new_df = pd.DataFrame([[region, 'Eólica', np.nan, np.nan, region_to_index[region]]], columns=['REGION', 'TIPO', 'MW', 'MM USD', 'REGION_INDEX'])
        df = pd.concat([df, new_df], ignore_index=True)
    

df.sort_values(by=['REGION_INDEX'], inplace=True)

df.interpolate(method='linear', limit_direction='both', inplace=True)

df.to_csv(join("data", "inversiones_por_region.csv"), index=False)