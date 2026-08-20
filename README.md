# Taller 01 — Métodos Cuantitativos

Planeación de producción multiperiodo de la empresa **JCR**, modelada como un problema de
**Programación Lineal Entera Mixta** y resuelta en Python con la librería
[PuLP](https://coin-or.github.io/pulp/) (solver CBC).

Profesor: Juan Carlos Rivera Agudelo — Universidad EAFIT.

---

## 1. ¿Qué hace este proyecto?

El archivo [`taller1.py`](taller1.py) construye y resuelve un modelo que decide, para un
horizonte de **4 meses**:

- cuánto producir de cada uno de los **3 productos** (en lotes completos),
- cuánta **materia prima** comprar (2 insumos),
- cuánto **vender**, cuánto dejar en **inventario**, cuánta demanda **diferir** (backorder)
  y cuánta demanda **perder**,

todo con el objetivo de **maximizar la utilidad total** del horizonte.

## 2. Parámetros del equipo

| Parámetro | Valor | Significado |
|---|---|---|
| `s` | 3 | Número de integrantes del equipo |
| `d` | 202 | Suma de las dos últimas cifras de las cédulas (97 + 97 + 08) |

De estos dos números se derivan la tasa de incremento de precios (2.5 % mensual), la capacidad
mensual en horas, el costo de almacenamiento (3 %), el descuento por entrega tardía (20.2 %) y
los límites de compra de materia prima.

## 3. El modelo en resumen

**Función objetivo (maximizar):**

```
Utilidad = ingresos por ventas
         − costo de compra de materia prima
         − costo de almacenamiento de producto terminado
         − costo de almacenamiento de materia prima
         − descuento por entregas tardías
```

**Variables de decisión** (para cada producto `i`, materia prima `j` y mes `t`):

| Variable | Descripción |
|---|---|
| `x[i][t]` | Unidades producidas |
| `n[i][t]` | Número de lotes producidos (**entera**) |
| `y[j][t]` | Materia prima comprada |
| `v[i][t]` | Unidades vendidas / entregadas |
| `Iv[i][t]` | Inventario final de producto terminado |
| `H[j][t]` | Inventario final de materia prima |
| `b[i][t]` | Demanda diferida al mes siguiente (backorder) |
| `u[i][t]` | Demanda perdida (no atendida) |

**Restricciones:**

| Código | Restricción |
|---|---|
| R1 | La producción se hace en lotes completos: `x = L · n` (lotes de 5, 1 y 7) |
| R2 | Las horas de producción del mes no superan la capacidad disponible |
| R3 | Balance de inventario de producto terminado |
| R4 | La demanda del mes se entrega, se difiere o se pierde |
| R5 | Balance de inventario de materia prima |
| R6 | Límite máximo de compra mensual de materia prima |
| R7 | Inventario mínimo de 20 unidades por producto al cierre del mes 4 |
| R8 | No puede quedar demanda diferida pendiente al final del horizonte |

## 4. Supuestos de modelación

1. **Venta perdida.** La capacidad total (≈ 720 horas) solo alcanza para cubrir ~25 % de las
   horas que exigiría atender toda la demanda (≈ 2 936 horas). Si se obligara a satisfacerla
   por completo, el problema sería **infactible**. Por eso se permite demanda no atendida
   (variable `u`), que simplemente no genera ingreso.
2. **Backorder.** Se puede diferir demanda al mes siguiente con un descuento de
   `0.1 · d % = 20.2 %` sobre el precio vigente.
3. **Almacenamiento.** Cuesta `s % = 3 %` del precio base (productos) o del costo de compra
   (materias primas), cobrado sobre el inventario final de cada mes.
4. **Lotes.** La producción es en lotes enteros, lo que convierte el modelo en entero mixto.

## 5. Cómo ejecutarlo

El proyecto usa [uv](https://docs.astral.sh/uv/) para manejar dependencias.

```bash
# 1. Clonar el repositorio
git clone https://github.com/jayounghoyos/Taller-01-metodos_cuantitativos.git
cd Taller-01-metodos_cuantitativos

# 2. Ejecutar (uv instala las dependencias automáticamente)
uv run taller1.py
```

<details>
<summary>¿No usas uv? Alternativa con pip</summary>

```bash
python -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install pulp matplotlib plotly
python taller1.py
```
</details>

Requiere **Python 3.12 o superior**. El solver CBC viene incluido con PuLP, no hay que
instalarlo aparte.

## 6. Resultado

El script imprime en consola un reporte completo: producción y lotes por mes, demanda
entregada / diferida / perdida, inventarios, compras de materia prima, uso de capacidad y
cobertura de la demanda.

```
Estado del solver: Optimal
Utilidad optima total (Z) = $158,797,994
```

Los meses operan al **100 % de su capacidad** de horas, lo que confirma que la capacidad es
el recurso que limita el sistema: la empresa produce lo más rentable por hora disponible
(principalmente el producto 3) y deja de atender el resto de la demanda.

## 7. Estructura del repositorio

```
.
├── taller1.py        # Modelo completo (parámetros, variables, restricciones y reporte)
├── pyproject.toml    # Dependencias del proyecto
├── uv.lock           # Versiones exactas de las dependencias
├── .python-version   # Versión de Python usada (3.12)
└── README.md
```
