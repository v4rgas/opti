import pandas as pd
import numpy as np
import constants as c
import os

# Cargar datos en un DataFrame

provincias = pd.read_csv(os.path.join("data", "datos_provincias.csv"))
inversiones_region = pd.read_csv(os.path.join("data", "inversiones_por_region.csv"))

def p_to_name(p):
    return provincias.iloc[p]["NOMBRE PROVINCIA"]

def e_to_name(e):
    return ["SOLAR kWhr/m2", "EÓLICO m/s", "HIDROELÉCTRICO m3/s"][e] 

def haversine(lat1, lon1, lat2, lon2): #Para calcular distancias en la tierra
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    
    # Compute differences
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c * 1000
    
    return distance

def int_to_energy(e):
    return ["solar", "eolic", "hydro"][e]

##Area incial disponible en m2 en la provincia p para instalar la energia e.
def A(p, e):
    percentages_per_energy = {
        c.SOLAR: c.MAX_AREA_PERCENTAGE*0.5,
        c.EOLIC: c.MAX_AREA_PERCENTAGE*0.3,
        c.HYDRO: c.MAX_AREA_PERCENTAGE*0.2
    }
    
    return percentages_per_energy[e] * provincias.iloc[p]["SUPERFICIE km2"] * 10**6

# kWh/m2
def base_energy_potential(p, e):
    potential_conversion = [c.SOLAR_POTENTIAL_CONVERSION, c.EOLIC_POTENTIAL_CONVERSION, c.HYDRO_POTENTIAL_CONVERSION]

    return provincias.iloc[p]["POTENCIAL " + e_to_name(e)] * potential_conversion[e]

##Potencial de generacion en kWh/m2 de la energia e en la provincia p durante el mes t.
def B(p, e, t):
    # Enero, Febrero, Marzo, Abril, Mayo, Junio, Julio, Agosto, Septiembre, Octubre, Noviembre, Diciembre

    # Explicacion de las desviaciones potenciales por mes para Chile:

    # Energia Solar:
    # - Enero, Febrero: +30% (Alta radiacion solar en verano)
    # - Marzo: +25% (Transicion al otoño, aun alta radiacion)
    # - Abril: +20% (Otoño, disminucion de la radiacion solar)
    # - Mayo: +10% (Radiacion solar baja, mes equilibrado)
    # - Junio, Julio: -25% (Invierno, baja radiacion solar)
    # - Agosto: -25% (Fin del invierno, aumento de la radiacion solar)
    # - Septiembre: -20% (Primavera, aumento de la radiacion solar)
    # - Octubre: -10% (Primavera, alta radiacion solar)
    # - Noviembre: +15% (Alta radiacion solar a finales de primavera)
    # - Diciembre: +25% (Alta radiacion solar en verano)

    # Energia Eolica:
    # - Enero, Febrero: -15% (Generalmente menor velocidad del viento en verano)
    # - Marzo: -15% (Periodo de transicion, velocidad del viento equilibrada)
    # - Abril: +10% (Aumento de la velocidad del viento en otoño)
    # - Mayo: +20% (Mayor velocidad del viento en otoño)
    # - Junio, Julio: +25% (Alta velocidad del viento en invierno)
    # - Agosto: +30% (Alta velocidad del viento a finales de invierno)
    # - Septiembre: +30% (Disminucion de la velocidad del viento en primavera)
    # - Octubre: +25% (Velocidad del viento equilibrada en primavera)
    # - Noviembre, Diciembre: +10% (Mayor velocidad del viento en primavera/verano)

    # Energia Hidraulica:
    # - Enero, Febrero: -25% (Bajo caudal de los rios en verano)
    # - Marzo: -25% (Disminucion del caudal de los rios a finales de verano)
    # - Abril: -15% (Caudal de los rios equilibrado en otoño)
    # - Mayo: +10% (Aumento del caudal de los rios a finales de otoño)
    # - Junio, Julio: +35% (Alto caudal de los rios en invierno debido a lluvias y deshielo)
    # - Agosto: +35% (Alto caudal de los rios a finales de invierno)
    # - Septiembre: +25% (Disminucion del caudal de los rios en primavera)
    # - Octubre: +15% (Caudal de los rios equilibrado en primavera)
    # - Noviembre: +10% (Aumento del caudal de los rios a finales de primavera)
    # - Diciembre: -15% (Bajo caudal de los rios en verano)

    potential_deviation_per_month = {
        c.SOLAR: [30, 30, 25, 20, 10, -25, -25, -20, -10, 15, 25, 30],
        c.EOLIC: [-15, -15, 10, 20, 25, 30, 30, 25, 20, 10, -15, -15],
        c.HYDRO: [-25, -25, -15, 10, 25, 35, 35, 25, 15, 10, -15, -25]
    }

    month = t % 12

    hours_generating_per_month = [c.HOURS_GENERATING_SOLAR, c.HOURS_GENERATING_EOLIC, c.HOURS_GENERATING_HYDRO]

    return base_energy_potential(p, e) * (potential_deviation_per_month[e][month]+100)/100 * hours_generating_per_month[e]

##Precio de venta de 1 kWh de energia en la provincia p en el tiempo t.
def PE(t):
    return c.ELECTRICITY_PRICE * c.MONTHLY_INFLATION**t

##Demanda de energia en kWh de la provincia p en el mes t.
def D(p, t):
    return (provincias.iloc[p]["TOTAL POBLACIÓN EFECTIVAMENTE CENSADA"] / c.TOTAL_POPULATION) * (c.DEMAND[t//12]) * 10**6

##Costo de transmitir 1 kWh por 1 km.
def CT(t):
    return c.TRANSMISION_COST * c.MONTHLY_INFLATION**t

##Distancia en km entre la provincia p y la provincia q.
def DT(p, q):
    return haversine(provincias.iloc[p]["CENTROIDE_LAT"], provincias.iloc[p]["CENTROIDE_LON"], provincias.iloc[q]["CENTROIDE_LAT"], provincias.iloc[q]["CENTROIDE_LON"])

##Costo de operacion por bloque de la energia e en la provincia p durante el mes t.
def CO(e, t):
    # fuente: "DETERMINACION DE LOS COSTOS DE INVERSION Y COSTOS FIJOS DE OPERACION DE LA UNIDAD DE PUNTA DEL SEN Y DE LOS SSMM", CNE, MARZO 2021.
    # https://www.cne.cl/wp-content/uploads/2021/06/03-ITP-Estudio-de-la-Unidad-de-Punta_VF.pdf
    # De acuerdo a esta fuente, NO existe variacion de costos de operacion por localizacion para proyectos de igual tamaño.

    cost_deviation_per_month = {
        # Supone aumentos significativos en meses de mantenimiento intensivo y menor generación solar.
        c.SOLAR: [1.00, 1.00, 1.20, 1.20, 1.50, 1.00, 1.00, 1.00, 1.20, 1.20, 1.00, 1.50],
        # Supone costos muy altos en meses con menor viento y mantenimientos críticos.
        c.EOLIC: [1.20, 1.20, 1.10, 1.10, 1.00, 1.20, 1.20, 1.00, 1.20, 1.20, 1.50, 1.50],
        # Supone aumentos en costos durante meses de alta variabilidad hídrica y gestión intensiva.
        c.HYDRO: [1.50, 1.50, 1.50, 1.20, 1.20, 1.00, 1.00, 1.00, 1.50, 1.50, 1.20, 1.20]
    }

    month = t % 12

    operational_costs = [c.OPERATING_COST_SOLAR, c.OPERATING_COST_EOLIC, c.OPERATING_COST_HYDRO]
    return operational_costs[e] * c.MONTHLY_INFLATION**t * cost_deviation_per_month[e][month]
##Costo de mantencion por bloque de la energia e en la provincia p en el mes t.
def CM(e, t):
    # fuente: "DETERMINACION DE LOS COSTOS DE INVERSION Y COSTOS FIJOS DE OPERACION DE LA UNIDAD DE PUNTA DEL SEN Y DE LOS SSMM", CNE, MARZO 2021.
    # https://www.cne.cl/wp-content/uploads/2021/06/03-ITP-Estudio-de-la-Unidad-de-Punta_VF.pdf
    # De acuerdo a esta fuente, no existe variacion de costos de mantencion por localizacion para proyectos de igual tamaño.

    # https://www.cne.cl/wp-content/uploads/2020/03/ICTG-Marzo-2020.pdf
    # En esta fuente se establece el costo unitario por inversion en cada kW de energia por hidroelectrica de embalse (5.205 US$/kW, con
    # para capacidad de 78.3 MW) y de pasada (2 opciones: 4.601 US$/kW para capacidad de 52 MW, y 4.014 US$/kW para capacidad de 2.9 MW)
    # (Pagina 31 del pdf).

    # https://www.cne.cl/wp-content/uploads/2020/03/ICTG-Marzo-2020.pdf
    # En esta fuente se establece el costo variable unitario, por MWh, de mantencion para una hidraulica de pasada (>20MW), mini-hidraulica (<20MW)
    # y de embalse es de 1.3 US$/MWh. Por otro lado, el costo fijo total de tecnologia, que incluye la operacion y la mantencion,
    # corresponde a un 1% de la inversion realizada en cualquier tipo de central hidraulica.}
    # (Pagina 40 del pdf).
    mantainance_costs = [c.MANTAINANCE_COST_SOLAR, c.MANTAINANCE_COST_EOLIC, c.MANTAINANCE_COST_HYDRO]
    return mantainance_costs[e] * c.MONTHLY_INFLATION ** t


##Costo de instalacion por bloque en la provincia p de la energia e.
def CI(p, e, t):
    region = provincias.iloc[p]["REGION"]
    energy_type = ["Solar", "Eólica", "Hidro"][e]
    try:
        cost_per_w = inversiones_region[(inversiones_region["REGION"] == region) & (inversiones_region["TIPO"] == energy_type)]["USD/W"].values[0]
    except IndexError:
        print(f"Error: No se encontró el costo de instalación para la región {region} y la energía {energy_type}.")
        exit()
    return base_energy_potential(p, e) * cost_per_w * 1000 * c.MONTHLY_INFLATION**t * GR(e)

##Capacidad minima en kWh que se necesita instalada a nivel nacional en el mes t.
def MC(t):
    # La demanda anual del pais (c.DEMAND[t//12]) se convierte de GWh a kWh multiplicando por 10**6.   
    # El siguiente link senala que el 2024 se lleva un 24% de generacion electrica por energia renovable. 
    # https://energia.gob.cl/noticias/nacional/ernc-y-otro-record-generacion-electrica-en-base-este-tipo-de-energia-llego-al-41-en-lo-que-va-de-2024#:~:text=Esto%20%C3%BAltimo%20lo%20confirman%20las,la%20energ%C3%ADa%20producida%20en%20Chile.
    # Imponiendo un c.ASSIGNED_DEMAND_PONDERATOR * 100% de generacion por energia renovable en los proximos 300 meses se obtiene la ecuacion 
    # de la recta: y = 0.001966*t + 0.4102. 
    # La capacidad suele ser el doble de la demanda, gracias a lo descrito 
    # en el excel "se_demanda_max_sobre_cap_instalada_anuario_2019". Por ende la ecuacion se multiplica por 2. 
    # return c.DEMAND[t//12] * 10**6 * (0.00393 * t + 0.8204) * c.ASSIGNED_DEMAND_PONDERATOR
    return c.DEMAND[t//12] * 10**6 * (t/300)**2 * c.ASSIGNED_DEMAND_PONDERATOR

##Bloques (unidad minima) en m2 en que se puede crecer una planta de tipo e.
def GR(e):
    sizes = [c.SOLAR_BLOCK_SIZE, c.EOLIC_BLOCK_SIZE, c.HYDRO_BLOCK_SIZE]
    return sizes[e] 

##Tamaño minimo en bloques que tiene que tener una planta de cada energia e.
def TM(e):
    sizes = [c.MINIMUM_REQUIRED_SPACE_SOLAR_INSTALLATION,
             c.MINIMUM_REQUIRED_SPACE_EOLIC_INSTALLATION,
             c.MINIMUM_REQUIRED_SPACE_HYDRO_INSTALLATION]
    return sizes[e]

if __name__ == "__main__":
    print("Testing functions...")
    print("p_to_name(0):", p_to_name(0))
    print("e_to_name(0):", e_to_name(0))
    print("haversine(0, 0, 0, 0):", haversine(0, 0, 0, 0))
    print("int_to_energy(0):", int_to_energy(0))
    print("A(0, 0):", A(0, 0))
    print("base_energy_potential(0, 0):", base_energy_potential(0, 0))
    print("B(0, 0, 0):", B(0, 0, 0))
    print("PE(0):", PE(0))
    print("D(0, 0):", D(0, 0))
    print("CT(0):", CT(0))
    print("DT(0, 0):", DT(0, 0))
    print("CO(0, 0):", CO(0, 0))
    print("CO(1, 0):", CO(1, 0))
    print("CO(2, 0):", CO(2, 0))
    print("CM(0, 0):", CM(0, 0))
    print("CI(0, 0, 0):", CI(0, 0, 0))
    print("CI(0, 1, 0):", CI(0, 1, 0))
    print("CI(0, 2, 0):", CI(0, 2, 0))
    
    print("MC(0):", MC(0))
    print("GR(0):", GR(0))
    print("TM(0):", TM(0))
    print("Done!")

    # sanity check
    biobio = 5
    print("A(5, 0):", A(biobio, 0))

    print("B(5, 0, 6):", B(biobio, 0, 6))
    print("B(5, 1, 6):", B(biobio, 1, 6))
    print("B(5, 2, 6):", B(biobio, 2, 6))
    print("Costos totales (5, 0, 6):", CI(biobio, 0, 6) + CO(0, 6) + CM(0, 6))
    print("Costos totales (5, 1, 6):", CI(biobio, 1, 6) + CO(1, 6) + CM(1, 6))
    print("Costos totales (5, 2, 6):", CI(biobio, 2, 6) + CO(2, 6) + CM(2, 6))

    net_solar = 0
    net_eolic = 0
    net_hydro = 0
    for i in range(12):
        net_solar += B(biobio, 0, i) * PE(i) / (CI(biobio, 0, i) + CO(0, i) + CM(0, i))
        net_eolic += B(biobio, 1, i) * PE(i) / (CI(biobio, 1, i) + CO(1, i) + CM(1, i))
        net_hydro += B(biobio, 2, i) * PE(i) / (CI(biobio, 2, i) + CO(2, i) + CM(2, i))

    print("Ratio SOLAR", net_solar/12)
    print("Ratio EOLICO", net_eolic/12)
    print("Ratio HIDRO", net_hydro/12)