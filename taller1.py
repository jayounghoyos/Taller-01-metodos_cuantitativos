"""
TALLER 1 - METODOS CUANTITATIVOS  (Profesor: Juan Carlos Rivera Agudelo)
Planeacion de produccion multiperiodo de la empresa JCR.
Modelo de Programacion Lineal resuelto con PuLP.

Parametros del equipo:
    s = 3
    d = 97 + 97 + 08 = 202

SUPUESTOS DE MODELACION (declarados en el informe):
 1. VENTA PERDIDA: la capacidad total (aprox. 720 horas) cubre solo el 25%
    de las horas que exige la demanda (aprox. 2936 horas), por lo que el
    problema es infactible si se obliga a satisfacerla toda. Se permite
    demanda no atendida (variable u, sin ingreso).
 2. BACKORDER: se permite diferir demanda al mes siguiente con descuento
    de 0.1*d % = 20.2% sobre el precio vigente, aplicado por unidad
    diferida. No puede quedar backorder al final del horizonte.
 3. ALMACENAMIENTO: s% del precio base (productos) o del costo de compra
    (materias primas), cobrado sobre el inventario final de cada mes.
 4. LOTES: la produccion es en lotes, x = L * n con n entero
    (producto 1: lotes de 5, producto 2: de 1, producto 3: de 7).
"""

import pulp

# 1. PARAMETROS DEL EQUIPO
s = 3            # numero de integrantes
d = 97 + 97 + 8  # suma de las dos ultimas cifras de las cedulas = 202

# 2. CONJUNTOS (indices)
I = [1, 2, 3]      # productos
J = [1, 2]         # materias primas
T = [1, 2, 3, 4]   # periodos (meses)

# 3. DATOS Y PARAMETROS DERIVADOS
pb    = {1: 600_000, 2: 550_000, 3: 700_000}          # precio base de venta
alpha = 0.01 + 0.005 * s                              # tasa de incremento = 0.025
g     = {t: (1 + alpha) ** (t - 1) for t in T}        # factor de precio del mes
p     = {(i, t): pb[i] * g[t] for i in I for t in T}  # precio vigente en el mes

h  = {1: 3, 2: 4, 3: 2}                               # horas de proceso por unidad
C  = {t: 180 + ((-1) ** (t - 1)) * d / 100 for t in T}  # capacidad en horas del mes
L  = {1: 5, 2: 1, 3: 7}                               # tamano de lote

k  = {1: {1: 2, 2: 1},                                # k[i][j]: materia prima j
      2: {1: 1, 2: 3},                                #   que consume cada unidad
      3: {1: 2, 2: 2}}                                #   del producto i

A  = {1: 600 - 12 * s, 2: 480 + 8 * s}                # compra maxima mensual: 564 / 504
u_ = {1: 50_000, 2: 70_000}                           # costo de compra de materia prima
H0 = {1: 40, 2: 30}                                   # inventario inicial de materia prima

D  = {1: {1: 120, 2: 72,  3: 100, 4: 60},             # demanda D[i][t]
      2: {1: 60,  2: 80,  3: 130, 4: 62},
      3: {1: 72,  2: 60,  3: 80,  4: 68}}

I0 = {1: 20, 2: 24, 3: 16}                            # inventario inicial de producto
ca   = {i: (s / 100) * pb[i] for i in I}              # costo almacenamiento producto (3%)
caMP = {j: (s / 100) * u_[j] for j in J}              # costo almacenamiento materia prima
rho  = 0.001 * d                                      # descuento por entrega tardia = 0.202
INV_FINAL = 20                                        # inventario minimo al final del mes 4

# 4. MODELO
m = pulp.LpProblem("Taller1_JCR", pulp.LpMaximize)

x  = pulp.LpVariable.dicts("x",  (I, T), lowBound=0)                # produccion (unidades)
n  = pulp.LpVariable.dicts("n",  (I, T), lowBound=0, cat="Integer") # numero de lotes (entera)
y  = pulp.LpVariable.dicts("y",  (J, T), lowBound=0)                # compra de materia prima
v  = pulp.LpVariable.dicts("v",  (I, T), lowBound=0)                # ventas (entregas)
Iv = pulp.LpVariable.dicts("Iv", (I, T), lowBound=0)                # inventario de producto
H  = pulp.LpVariable.dicts("H",  (J, T), lowBound=0)                # inventario de materia prima
b  = pulp.LpVariable.dicts("b",  (I, T), lowBound=0)                # backorder (demanda diferida)
u  = pulp.LpVariable.dicts("u",  (I, T), lowBound=0)                # venta perdida

# Funcion objetivo: maximizar utilidad
m += (
    pulp.lpSum(p[(i, t)] * v[i][t]         for i in I for t in T)   # ingresos por ventas
    - pulp.lpSum(u_[j] * y[j][t]           for j in J for t in T)   # costo de compra de materia prima
    - pulp.lpSum(ca[i] * Iv[i][t]          for i in I for t in T)   # almacenamiento de producto
    - pulp.lpSum(caMP[j] * H[j][t]         for j in J for t in T)   # almacenamiento de materia prima
    - pulp.lpSum(rho * p[(i, t)] * b[i][t] for i in I for t in T)   # descuento por entrega tardia
), "Utilidad_total"

# Restricciones
for i in I:
    for t in T:
        # R1: la produccion se realiza en lotes completos
        m += x[i][t] == L[i] * n[i][t], f"R1_lotes_{i}_{t}"

for t in T:
    # R2: capacidad de horas del mes
    m += pulp.lpSum(h[i] * x[i][t] for i in I) <= C[t], f"R2_capacidad_{t}"

for i in I:
    for t in T:
        Iv_prev = I0[i] if t == 1 else Iv[i][t - 1]
        b_prev  = 0     if t == 1 else b[i][t - 1]
        # R3: balance de inventario de producto terminado
        m += Iv_prev + x[i][t] == v[i][t] + Iv[i][t], f"R3_balance_producto_{i}_{t}"
        # R4: la demanda del mes se entrega, se difiere o se pierde
        m += D[i][t] + b_prev == v[i][t] + b[i][t] + u[i][t], f"R4_demanda_{i}_{t}"

for j in J:
    for t in T:
        H_prev = H0[j] if t == 1 else H[j][t - 1]
        # R5: balance de inventario de materia prima
        m += H_prev + y[j][t] == pulp.lpSum(k[i][j] * x[i][t] for i in I) + H[j][t], f"R5_balance_materia_{j}_{t}"
        # R6: limite de compra mensual de materia prima
        m += y[j][t] <= A[j], f"R6_compra_maxima_{j}_{t}"

for i in I:
    # R7: inventario minimo al cierre del horizonte
    m += Iv[i][4] >= INV_FINAL, f"R7_inventario_final_{i}"
    # Cierre del horizonte: no puede quedar demanda diferida pendiente
    m += b[i][4] == 0, f"R8_cierre_backorder_{i}"

# 5. RESOLVER
m.solve(pulp.PULP_CBC_CMD(msg=False))

# 6. REPORTE DE RESULTADOS
print("TALLER 1: Planeacion de produccion de la empresa JCR")
print(f"Numero de integrantes (s) = {s}")
print(f"Suma de cifras de cedulas (d) = {d}")
print(f"Tasa de incremento de precios (alpha) = {alpha} ({alpha:.1%} mensual)")
print(f"Descuento por entrega tardia = {rho:.1%}")
print("Capacidad de cada mes en horas: "
      + ", ".join(f"mes {t}: {C[t]:.2f}" for t in T))
print()
print(f"Estado del solver: {pulp.LpStatus[m.status]}")
print(f"Utilidad optima total (Z) = ${pulp.value(m.objective):,.0f}")
print()

print("PRODUCCION: unidades fabricadas y numero de lotes por producto y mes")
for i in I:
    fila = "   ".join(
        f"mes {t}: {pulp.value(x[i][t]):.0f} unidades ({pulp.value(n[i][t]):.0f} lotes)"
        for t in T)
    print(f"  Producto {i}:  {fila}")
print()

print("DEMANDA: unidades entregadas, diferidas (backorder) y perdidas por mes")
for i in I:
    for t in T:
        print(f"  Producto {i}, mes {t}: entrega {pulp.value(v[i][t]):.0f} unidades, "
              f"difiere {pulp.value(b[i][t]):.0f}, pierde {pulp.value(u[i][t]):.0f} "
              f"(demanda del mes: {D[i][t]})")
print()

print("INVENTARIO de producto terminado al final de cada mes (unidades)")
for i in I:
    valores = ", ".join(f"mes {t}: {pulp.value(Iv[i][t]):.0f}" for t in T)
    print(f"  Producto {i} (inicial: {I0[i]}):  {valores}")
print()

print("COMPRAS de materia prima por mes (unidades)")
for j in J:
    valores = ", ".join(f"mes {t}: {pulp.value(y[j][t]):.0f}" for t in T)
    print(f"  Materia prima {j} (compra maxima mensual: {A[j]}):  {valores}")
print()

print("INVENTARIO de materia prima al final de cada mes (unidades)")
for j in J:
    valores = ", ".join(f"mes {t}: {pulp.value(H[j][t]):.0f}" for t in T)
    print(f"  Materia prima {j} (inicial: {H0[j]}):  {valores}")
print()

print("USO DE CAPACIDAD: horas de produccion utilizadas frente a las disponibles")
for t in T:
    usadas = sum(h[i] * pulp.value(x[i][t]) for i in I)
    print(f"  Mes {t}: utiliza {usadas:.1f} horas de {C[t]:.2f} disponibles "
          f"({usadas / C[t]:.1%} de ocupacion)")
print()

print("COBERTURA DE DEMANDA en todo el horizonte de planeacion")
for i in I:
    demanda_total  = sum(D[i][t] for t in T)
    entrega_total  = sum(pulp.value(v[i][t]) for t in T)
    print(f"  Producto {i}: entrega {entrega_total:.0f} de {demanda_total} unidades "
          f"demandadas ({entrega_total / demanda_total:.1%} de cobertura)")
