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

plt.plot(op_values[0], op_values[1], op_values[2])
plt.xlabel('Meses')
plt.ylabel('Bloques operacionales')
plt.legend(["Solar", "Eólica", "Hidro"])
plt.show()