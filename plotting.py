import numpy as np
import matplotlib.pyplot as plt
import os


op_values = np.load(os.path.join('outputs', 'op_values.npy'))

# Ordenar el array para obtener las 5 provincias con más operación

# op_values = np.sort(op_values, axis=0)
# op_values = op_values[:5, :, :]

# Crear un gráfico de barras para mostrar la evolución de la operación en las 5 provincias con más operación

op_values = op_values[5]

print(op_values)

fig, axes = plt.subplots(3, 1, figsize=(10, 15))  # 3 rows, 1 column

# Plot each series on a separate subplot
axes[0].plot(op_values[0], label="Solar")
axes[0].set_xlabel('Meses')
axes[0].set_ylabel('Bloques operacionales')
axes[0].legend()

axes[1].plot(op_values[1], label="Eólica")
axes[1].set_xlabel('Meses')
axes[1].set_ylabel('Bloques operacionales')
axes[1].legend()

axes[2].plot(op_values[2], label="Hidro")
axes[2].set_xlabel('Meses')
axes[2].set_ylabel('Bloques operacionales')
axes[2].legend()

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()