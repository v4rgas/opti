import pandas as pd
import numpy as np

inversiones_df = pd.read_excel('inversiones.xlsx')

# Mapping of region names to their corresponding numbers
region_mapping = {
    'Tarapacá': 2, 
    'Antofagasta': 3,
    'Atacama': 4,
    'Coquimbo': 5,
    'Valparaíso': 6,
    "O'Higgins": 8, #
    'Maule': 9, #
    'Biobío': 11,
    'La Araucanía': 12,
    'Los Lagos': 14,
    'Aysén': 15,
    'Magallanes': 16,
    'Metropolitana': 7,
    'Los Ríos': 13,
    'Arica y Parinacota': 1,
    'Ñuble': 10 #
}

# Correct any potential typos in the REGION column before mapping
inversiones_df['REGION'] = inversiones_df['REGION'].replace({
    'O\'Higpns': "O'Higgins",
    'Biobio': 'Biobío'
})

# Map the region names to numbers
inversiones_df['REGION'] = inversiones_df['REGION'].map(region_mapping)


print(inversiones_df)



df = inversiones_df.groupby(['REGION', "TIPO"], as_index=False).mean()

hidro = df[df['TIPO'] == 'Hidro']
solar = df[df['TIPO'] == 'Solar']
eolica = df[df['TIPO'] == 'Eólica']

biobio_hidro = hidro[hidro['REGION'] == 11.0]
biobio_solar = solar[solar['REGION'] == 11.0]
biobio_eolica = eolica[eolica['REGION'] == 11.0]

#print(biobio_hidro, biobio_solar, biobio_eolica)


# #print(df.mean())

# print(biobio)
# #print(df.loc['Metropolitana'])


for col in ['MW', 'MM USD', 'USD/W']:
    # print(biobio[col].values[2])
    # print(df[col], biobio[col], "printed")
    # print(hidro[col])
    # print(biobio_eolica[col].values[0])
    hidro[col] = hidro[col] / biobio_hidro[col].values[0] # normalización de usd/w
    solar[col] = solar[col] / biobio_solar[col].values[0] # normalización de usd/w
    eolica[col] = eolica[col] / biobio_eolica[col].values[0] # normalización de usd/w
    # exit()

#print(hidro)
#print('\n ')
#print(solar)
#print('\n ')
#print(eolica)


# print(df_divided)



# crear lista con region, ponderador
hidro_df = hidro.filter(['REGION', 'USD/W'], axis = 1)

region_list_hidro = hidro_df['REGION'].tolist()
#print(region_list)
for x in range(1,17):
    if float(x) not in region_list_hidro:
        hidro_df.loc[-1] = [float(x), np.nan]
        hidro_df.index = hidro_df.index + 1

hidro_df = hidro_df.sort_values(by = ['REGION'])
#print(hidro_df)
#interpolacion:
hidro_df['USD/W'] = hidro_df['USD/W'].interpolate(method ='linear', limit_direction ='backward')
hidro_df['USD/W'] = hidro_df['USD/W'].interpolate(method ='linear', limit_direction ='forward')  

# repetir 

solar_df = solar.filter(['REGION', 'USD/W'], axis = 1)

region_list_solar = solar_df['REGION'].tolist()
#print(region_list)
for x in range(1,17):
    if float(x) not in region_list_solar:
        solar_df.loc[-1] = [float(x), np.nan]
        solar_df.index = solar_df.index + 1

solar_df = solar_df.sort_values(by = ['REGION'])
#print(solar_df)
#interpolacion:
solar_df['USD/W'] = solar_df['USD/W'].interpolate(method ='linear', limit_direction ='backward') 
solar_df['USD/W'] = solar_df['USD/W'].interpolate(method ='linear', limit_direction ='forward') 


eolica_df = eolica.filter(['REGION', 'USD/W'], axis = 1)

region_list_eolica = eolica_df['REGION'].tolist()
#print(region_list)
for x in range(1,17):
    if float(x) not in region_list_eolica:
        eolica_df.loc[-1] = [float(x), np.nan]
        eolica_df.index = eolica_df.index + 1

eolica_df = eolica_df.sort_values(by = ['REGION'])
#print(eolica_df)
#interpolacion:
eolica_df['USD/W'] = eolica_df['USD/W'].interpolate(method ='linear', limit_direction ='backward') 
eolica_df['USD/W'] = eolica_df['USD/W'].interpolate(method ='linear', limit_direction ='forward') 

print(hidro_df)
print(solar_df)
print(eolica_df)

# TODO: YA JUAN SOLO FALTA LO SIGUIENTE. 
# ya estan los ponderadores para todas las regiones (numeradas en forma GEOGRÁFICA pa poder interpolar bn)
# solo falta: PASAR DE REGIÓN A PROVINCIA y asignar los ponderadores segun la región a la q pertenece la provincia.
# y chantar ese resultado en los COSTOS DE INSTALACIÓN.