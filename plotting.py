import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd


op_values = np.load(os.path.join('outputs', 'op_values.npy'))

# Crear un gráfico de barras para mostrar la evolución de la operación en las 5 provincias con más operación

df = pd.read_csv(os.path.join('data', 'datos_provincias.csv'))

nombres_provincias = df['NOMBRE PROVINCIA'].values

# Crear un DataFrame vacío
op_df = pd.DataFrame()

# Insertar los valores en el DataFrame
op_df.insert(0, "PROVINCIA", nombres_provincias)
op_df.insert(1, "SOLAR MITAD", op_values[:, 0, 150])
op_df.insert(2, "EÓLICA MITAD", op_values[:, 1, 150])
op_df.insert(3, "HIDRO MITAD", op_values[:, 2, 150])
op_df.insert(4, "SOLAR FINAL", op_values[:, 0, 299])
op_df.insert(5, "EÓLICA FINAL", op_values[:, 1, 299])
op_df.insert(6, "HIDRO FINAL", op_values[:, 2, 299])

# Guardar el DataFrame en un archivo CSV
op_df.to_csv(os.path.join('outputs', 'op_provincias.csv'), index=False)

sum_op_values = np.sum(op_values, axis=0)

def operation_plot(operation_array, plot_name, save=False):
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))  # 3 rows, 1 column

    # Set figure name
    fig.suptitle(plot_name)

    # Plot each series on a separate subplot
    axes[0].plot(operation_array[0], label="Solar")
    axes[0].set_xlabel('Meses')
    axes[0].set_ylabel('Bloques operacionales')
    axes[0].legend()

    axes[1].plot(operation_array[1], label="Eólica")
    axes[1].set_xlabel('Meses')
    axes[1].set_ylabel('Bloques operacionales')
    axes[1].legend()

    axes[2].plot(operation_array[2], label="Hidro")
    axes[2].set_xlabel('Meses')
    axes[2].set_ylabel('Bloques operacionales')
    axes[2].legend()

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    if save:
        plt.savefig(os.path.join('outputs', f'{plot_name}.png'))

operation_plot(sum_op_values, "Operación total")

operation_plot(op_values[0], nombres_provincias[0], True) # Provincia 0 --> Antofagasta
operation_plot(op_values[5], nombres_provincias[5], True) # Provincia 5 --> BioBío
operation_plot(op_values[-1], nombres_provincias[-1], True) # Provincia -1 --> Última esperanza

# Show the plots
plt.show()