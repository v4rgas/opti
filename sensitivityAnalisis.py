import sys
import gurobipy as gp
import main
import paramLoading as pl
import matplotlib.pyplot as plt
from gurobipy import GRB, Model, quicksum


def generateGraphics(k_values, z_values, modified_value_name):
    # Graficar
    plt.plot(k_values, z_values, color = 'b', linestyle = '-', 
            marker = 'o',label = "z vs k") 

    plt.xticks(rotation = 25) 
    plt.xlabel('Valor de multiplicador') 
    plt.ylabel('Valor óptimo') 
    plt.title(f'Valor óptimo en función de multiplicador que altera {modified_value_name}', fontsize = 20)
    plt.grid() 
    plt.legend()
    # Guardar gráfico como png
    plt.savefig(f'outputs/sensitivity_analysis_{modified_value_name}.png')


def sensitivityCIpet(k):
    # Nuevo objetivo ajustando CI
    # Funcion Objetivo

    print(f"Current value of multiplier: {k}")
    main.objetivo2 = quicksum(quicksum(quicksum(pl.CM(e , t) * main.s[p, e, t] + pl.CI(p, e, t) * k
                                                * main.r[p, e, t] for t in range(main.T))
                                                for e in range(main.E)) for p in range(main.P))
    main.objetivo = main.objetivo1 - main.objetivo2 - main.objetivo3 - main.objetivo4

    main.model.setObjective(main.objetivo, GRB.MAXIMIZE)
    main.optimizeAndPrintResults()

    # Cada vez que modelo optimiza, guardar en lista valor óptimo y multiplicador:
    return main.model.objVal


def sensitivityB(k, B):
    main.pl.B = lambda p, e, t: B(p,e,t) * (1 + k)
    main.optimizeAndPrintResults()

    return main.model.objVal

def sensitivityTM(k, TM):
    main.pl.TM = lambda e: TM(e) * (1 + k)
    main.optimizeAndPrintResults()

    return main.model.objVal

def sensitivityPE(k, PE):
    main.pl.PE = lambda t: PE(t) * (1 + k)
    main.optimizeAndPrintResults()

    return main.model.objVal


if __name__ == "__main__":

    parameter = sys.argv[1]

    if parameter == "CI":
        # Alterar valores de CI
        k_values = []
        z_values = []
        K = [1e1, 1e2, 1e3, 1e4]
        for k in K:
            obj_val = sensitivityCIpet(k)
            k_values.append(k), z_values.append(obj_val)

        generateGraphics(k_values, z_values, "CI")

    if parameter == "B":
        # Alterar valores de B
        k_values = []
        z_values = []
        K = [-0.5, -0.25, 0.25, 0.5]
        B = pl.B
        for k in K:
            obj_val = sensitivityB(k, B)
            k_values.append(k), z_values.append(obj_val)

        print(k_values, z_values)

        generateGraphics(k_values, z_values, "B")

    if parameter == "TM":
        # Alterar valores de TM
        k_values = []
        z_values = []
        K = [-0.5, -0.25, 0.25, 0.5]
        TM = pl.TM
        for k in K:
            obj_val = sensitivityTM(k, TM)
            k_values.append(k), z_values.append(obj_val)

        print(k_values, z_values)

        generateGraphics(k_values, z_values, "TM")

    if parameter == "PE":
        # Alterar valores de PE
        k_values = []
        z_values = []
        K = [-0.5, -0.25, 0.25, 0.5]
        PE = pl.PE
        for k in K:
            obj_val = sensitivityPE(k, PE)
            k_values.append(k), z_values.append(obj_val)

        print(k_values, z_values)

        generateGraphics(k_values, z_values, "PE")