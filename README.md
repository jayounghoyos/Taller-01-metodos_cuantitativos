# Taller 01 — Métodos Cuantitativos

Planeación de producción multiperiodo de la empresa **JCR**, modelada como un problema de
**Programación Lineal Entera Mixta** y resuelta en Python con la librería
[PuLP](https://coin-or.github.io/pulp/).

Profesor: Juan Carlos Rivera Agudelo — Universidad EAFIT.

> El desarrollo completo del modelo (formulación, supuestos, restricciones y análisis de
> resultados) está en el informe: [`Metodos_Cuantitativos__Taller_1.pdf`](Metodos_Cuantitativos__Taller_1.pdf).

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

## 3. Cómo clonar y ejecutar

Requiere **Python 3.12 o superior**. El solver CBC viene incluido con PuLP, no hay que
instalarlo aparte.

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/jayounghoyos/Taller-01-metodos_cuantitativos.git
cd Taller-01-metodos_cuantitativos
```

### Paso 2 — Instalar las dependencias y ejecutar

El proyecto usa [uv](https://docs.astral.sh/uv/), que crea el entorno virtual e instala las
dependencias automáticamente en un solo comando:

```bash
uv run taller1.py
```

<details>
<summary>¿No tienes uv? Instálalo así</summary>

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
</details>

<details>
<summary>Alternativa sin uv, con pip</summary>

```bash
python -m venv .venv
source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install pulp matplotlib plotly
python taller1.py
```
</details>

### Paso 3 — Ver los resultados

El script imprime en consola el reporte completo: producción y lotes por mes, demanda
entregada / diferida / perdida, inventarios, compras de materia prima, uso de capacidad y
cobertura de la demanda.

```
Estado del solver: Optimal
Utilidad optima total (Z) = $158,797,994
```

## 4. Estructura del repositorio

```
.
├── taller1.py                            # Modelo completo (parámetros, variables, restricciones y reporte)
├── Metodos_Cuantitativos__Taller_1.pdf   # Informe con la formulación y el análisis
├── pyproject.toml                        # Dependencias del proyecto
├── uv.lock                               # Versiones exactas de las dependencias
├── .python-version                       # Versión de Python usada (3.12)
└── README.md
```
