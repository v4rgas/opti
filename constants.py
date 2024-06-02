# Párametros
SOLAR = 0
EOLIC = 1
HYDRO = 2

# Conversión de unidades de potenciales a kW / m2 para todos los tipos de energía

SOLAR_POTENTIAL_CONVERSION = 1 # kW/m2 (ya estaba en esa unidad)
EOLIC_POTENTIAL_CONVERSION = 531 / (7.5 * (50**2 * 3.1415)) # m/s --> kW/m2 (531 kW / (7.5 m/s * 50^2 * pi m2)) (https://eolico.minenergia.cl/potencia)
HYDRO_POTENTIAL_CONVERSION = 1000 / (30 * 415) # m3/s --> kW/m2 (1000 kW / (30 m3/s * 415 m2)) (Kaplan turbine https://renewablesfirst.co.uk/renewable-energy-technologies/hydropower/hydropower-turbines/)

# Horas de generación por energía por mes

HOURS_GENERATING_SOLAR = 12 * 30 # 12 horas de sol al día
HOURS_GENERATING_EOLIC = 24 * 30 # 24 horas de viento al día
HOURS_GENERATING_HYDRO = 24 * 30 # 24 horas de agua al día

# Fracción del área total de la provincia que se puede usar para instalar energía. MAXIMO VALOR POSIBLE (Arbitrario)

MAX_AREA_PERCENTAGE = 0.4

# IPC anual proyectado para todos los proximos 4 años
#https://www.hacienda.cl/areas-de-trabajo/politicas-macroeconomicas/escenario-macroeconomico

YEARLY_INFLATION = 1.03 # 3% de inflación anual
MONTHLY_INFLATION = YEARLY_INFLATION**(1/12)

# Conversión dolar peso utilizada: 903 pesos por dolar al 28 de mayo.
USD_TO_CLP = 903

# Precio de la electricidad en el SEN en el último periodo disponible (08 Mayo 2024)
# https://www.cne.cl/precio-medio-de-mercado-2/

ELECTRICITY_PRICE = 103.098 # CLP/kWh

# Población total de Chile en el 2017
# http://resultados.censo2017.cl/

TOTAL_POPULATION = 17574003

# Demanda proyectada en GWh para los próximos 20 años
# http://energiaabierta.cl/categorias-estadistica/electricidad/?sf_paged=3

ASSIGNED_DEMAND_PONDERATOR = 0.1 # cubre el 30%? de la demanda proyectada cada año

#GWh
DEMAND = [
    78.784, # 2024
    80.532, # 2025
    82.058, # 2026
    83.047, # 2027
    84.328, # 2028
    85.726, # 2029
    87.608, # 2030
    89.147, # 2031
    91.187, # 2032
    93.409, # 2033
    95.736, # 2034
    98.182, # 2035
    101.007, # 2036
    103.907, # 2037
    106.855, # 2038
    109.792, # 2039
    112.760, # 2040
    117.494, # 2041
    123.090, # 2042
    124.890, # 2043
    128.438, # 2044
    131.985, # 2045
    135.532, # 2046
    139.080, # 2047
    142.627, # 2048
    146.174, # 2049
    147.254  # 2050
]

# PARA TAMAÑO DE BLOQUES Y COSTOS
# fuente: "DETERMINACION DE LOS COSTOS DE INVERSION Y COSTOS FIJOS DE OPERACION DE LA UNIDAD DE PUNTA DEL SEN Y DE LOS SSMM", CNE, MARZO 2021.
# https://www.cne.cl/wp-content/uploads/2021/06/03-ITP-Estudio-de-la-Unidad-de-Punta_VF.pdf

# Tamaños de los bloques de energía en m2

SOLAR_CONST = 1/70  # Regla de 3 entre el tamaño de una planta de 70 MW y la de 1 MW, en base a diferentes fuentes
EOLIC_CONST = 1.2/70 # Regla de 3 entre el tamaño de una planta de 70 MW y la de 1.2 MW (la mas pequeña en Chile segun Wikipedia)
HYDRO_CONST = 20/264 # Regla de 3 entre el tamaño de una planta de 264 MW y la de 20 MW, en base a la planta el Alfalfal II y 
                     #https://sea.gob.cl/sites/default/files/imce/archivos/2021/03/12/guia_centrales_hidroelectricas_pdf_publicacion_compressed.pdf

MINIMUM_REQUIRED_SPACE_SOLAR_INSTALLATION = 185000 * SOLAR_CONST # Tamaño de la instalacion en m2 (185000 m2 de una planta de 70 MW)
MINIMUM_REQUIRED_SPACE_EOLIC_INSTALLATION = 201800 * EOLIC_CONST # Tamaño de la instalacion en m2 (201800 m2 de una planta de 70 MW)
MINIMUM_REQUIRED_SPACE_HYDRO_INSTALLATION  = 109669 * HYDRO_CONST # Tamaño de la instalacion en m2 (109669 m2 de una planta de 264 MW)

# Tamaños de bloques de energia en m2

MINIMUM_INITIAL_BLOCKS_REQUIRED_SOLAR = 4
MINIMUM_INITIAL_BLOCKS_REQUIRED_EOLIC = 4
MINIMUM_INITIAL_BLOCKS_REQUIRED_HYDRO = 4

SOLAR_BLOCK_SIZE = MINIMUM_REQUIRED_SPACE_SOLAR_INSTALLATION / MINIMUM_INITIAL_BLOCKS_REQUIRED_SOLAR # m2
EOLIC_BLOCK_SIZE = MINIMUM_REQUIRED_SPACE_EOLIC_INSTALLATION / MINIMUM_INITIAL_BLOCKS_REQUIRED_EOLIC # m2
HYDRO_BLOCK_SIZE = MINIMUM_REQUIRED_SPACE_HYDRO_INSTALLATION / MINIMUM_INITIAL_BLOCKS_REQUIRED_HYDRO # m2

# UNIDAD: $/BLOQUE
OPERATING_COST_SOLAR = (USD_TO_CLP*(516960 + 2832343 + 27758)/12) * SOLAR_CONST
OPERATING_COST_EOLIC = (USD_TO_CLP*(516960 + 4045443 + 29539)/12) * EOLIC_CONST
OPERATING_COST_HYDRO = (USD_TO_CLP*(2344000)/12) * HYDRO_CONST # https://www.cne.cl/wp-content/uploads/2020/07/Informe-Final-Estudio-de-Costos-de-Inversi%C3%B3n-2019.pdf (pag 35 o 39)
                                                               # Se puede cambiar a 1639000
MANTAINANCE_COST_SOLAR = (USD_TO_CLP*33640/12) * SOLAR_CONST
MANTAINANCE_COST_EOLIC = (USD_TO_CLP*33640/12) * EOLIC_CONST    # Son lo mismo segun la fuente
MANTAINANCE_COST_HYDRO = (USD_TO_CLP * 0.02) * 20 # https://www.ffla.net/wp-content/uploads/2021/04/parte_ii_58_-_115-min.pdf

#Costo de transmitir un kWh por km 
#Capacidad de transimsion: 1000MW
#Carga promedio 50%
#Costo anual de construccion y mantenimiento:
#Costo anual = Costo construccion/Vida util + costo de construccion * tasa de mantencion) = 500 000USD/40 años + (500 000 * 0.02) = 12 500 USD/año + 10 000 USD/año
#Transmision anual =  capacidad * carga promedio * horas en un año
#1 000 000 KW * 0.5 *8760 horas = 4 380 000 000 KWh/año
#Costo por kWh pr km = costo anual por km/ Transmision anual por km = 22 500 USD/año / 4 380 000 000 kWh/año = 0.00000514 USD/KWh/Km


TRANSMISION_COST = 0.0046 # CLP/kWh/km

MAX_BLOCK_PER_MONTH = 10