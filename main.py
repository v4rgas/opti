from gurobipy import GRB, Model, quicksum
import paramLoading as pl
import numpy as np
import os


#Crea un modelo vacio
model = Model()
model.setParam("TimeLimit", 60) # Limite de tiempo de ejecucion para gurobi

#Rangos

P = len(pl.provincias)
E = 3
T = 25 * 12

BigM = 10**7

# Instancia variables de decisiones

## s_pet: Cantidad de bloques de una planta de energia e en la provincia p hasta el mes t.
s = model.addVars(P, E, T, vtype=GRB.SEMIINT, name = "s")

## r_pet: Cantidad de bloques nuevos de una planta de energia e en la provincia p en el mes t.
r = model.addVars(P, E, T, vtype=GRB.SEMIINT, name = "r")  

## op_pet: Cantidad de bloques operacionales de la energia e en la provincia p en el mes t.
op = model.addVars(P, E, T, vtype=GRB.SEMIINT, name = "op")

## et_pp't: Energıa en kWh transmitida desde la provincia p a la provincia p′ en el tiempo t
et = model.addVars(P, P, T, vtype=GRB.SEMICONT, name = "et") 

## y_pet: existencia de tipo de energia en provincia en un tiempo
y = model.addVars(P, E, T, vtype=GRB.BINARY, name = "w")

model.update()

#Restricciones

##R1
model.addConstrs((s[p, e, t]* pl.GR(e) <= pl.A(p, e) for p in range(P) for e in range(E) for t in range(T)), name ="R1")

##R2
model.addConstrs((s[p, e, t] == s[p, e, (t - 1)] + r[p, e, t] for p in range(P) for e in range(E) for t in range(1, T)), name = "R2")

##R3
model.addConstrs((s[p, e, 0] == r[p, e, 0] for p in range(P) for e in range(E)), name = "R3")

##R4
model.addConstrs((op[p, e, t] <= s[p, e, t] for p in range(P) for e in range(E) for t in range(T)), name = "R4")

##R5
model.addConstrs(quicksum(et[p, q, t] for q in range(P)) <= quicksum(pl.B(p, e, t) * op[p, e, t] * pl.GR(e) for e in range(E) ) for p in range(P) for t in range(T))  # q = p' :)

##R6
model.addConstrs((quicksum(quicksum(s[p, e, t] * pl.GR(e) * pl.B(p, e, t) for p in range(P)) for e in range(E)) >= pl.MC(t) for t in range(T)))

##R7
model.addConstrs((quicksum(pl.B(p, e, t) * op[p, e, t] * pl.GR(e) for e in range(E)) + quicksum(et[q, p, t] - et[p, q, t] for q in range(P)) >= pl.D(p, t) for p in range(P) for t in range(T)), name = "R7")

##R8
model.addConstrs((s[p, e, t] >= pl.TM(e) * y[p, e, t] for p in range(P) for e in range(E) for t in range(T)), name = "R8")

##R9
model.addConstrs((s[p, e, t] <= y[p, e, t] * BigM for p in range(P) for e in range(E) for t in range(T)), name = "R9a")
model.addConstrs((y[p, e, t] <= s[p, e, t] for p in range(P) for e in range(E) for t in range(T)), name = "R9b")

##R10
model.addConstrs((quicksum(r[p, e, t] for e in range(E) for p in range(P)) <= (6_500 * P) for t in range(T)), name = "R10")

##Naturaleza de las Variables
model.addConstrs((et[p, q, t] >= 0 for p in range(P) for q in range(P) for t in range(T)), name="R10")


#Funcion Objetivo

objetivo1 = quicksum(quicksum(quicksum(op[p, e, t] * pl.GR(e) * pl.B(p, e, t) * pl.PE(t) for t in range(T)) for e in range(E)) for p in range(P))
objetivo2 = quicksum(quicksum(quicksum(pl.CM(e , t) * s[p, e, t] + pl.CI(p, e, t) * r[p, e, t] for t in range(T)) for e in range(E)) for p in range(P))
objetivo3 = quicksum(quicksum(quicksum(et[p, q, t] * pl.CT(t) * pl.DT(p, q) for t in range(T)) for q in range(P) if p != q) for p in range(P)) 
objetivo4 = quicksum(quicksum(quicksum(pl.CO(e, t) * op[p, e, t] for t in range(T)) for e in range(E) if e != 3) for p in range(P))

objetivo = objetivo1 - objetivo2 - objetivo3 - objetivo4

model.setObjective(objetivo, GRB.MAXIMIZE)
model.optimize()

#Guarda los valores de las variables de decision
s_values_array = np.zeros((P, E, T))
op_values_array = np.zeros((P, E, T))
for p in range(P):
    for e in range(E):
        for t in range(T):
            s_values_array[p, e, t] = s[p, e, t].X
            op_values_array[p, e, t] = op[p, e, t].X

np.save(os.path.join("outputs", "op_values"), op_values_array)

#model.computeIIS()
#archivo = "encontrar_infactibilidad"
#model.write(f"{archivo}.ilp")