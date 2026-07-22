# %% [markdown]
# # Clase 03 -- Ciclo de vida de los datos (Parte I)
#
# Practica de las etapas **01 Creacion y captura** y **02 Transmision y
# almacenamiento**. Vamos a:
#
# 1. **Captura**: simular la obtencion de datos con los errores tipicos
#    (faltantes, duplicados, fecha como texto, espacios sobrantes).
# 2. **Censo vs encuesta**: estimar la media de una poblacion con una muestra,
#    calcular su intervalo de confianza del 95% y verificar empiricamente que
#    ~95 de cada 100 muestras "atrapan" el valor real.
# 3. **ETL**: Extraer los datos crudos, Transformarlos (limpiar) y Cargarlos en
#    una mini-bodega SQLite, sobre la que corremos una consulta SQL.
# 4. **Almacenamiento**: comparar el tamano del mismo dato en CSV, CSV.gz y JSON,
#    y recordar la regla 3-2-1.
#
# Uso:
#     python practica.py
# Genera datasets en datos/ (incluida la bodega SQLite) y graficas en figuras/.

# %%
# Imports (stdlib y externos)
import gzip
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # backend sin ventana: guardamos las figuras a archivo
import matplotlib.pyplot as plt

# %%
# Carpetas de salida. Como script usamos __file__; como notebook, el cwd.
try:
    BASE = Path(__file__).resolve().parent
except NameError:
    BASE = Path.cwd()
DATOS = BASE / "datos"
FIGURAS = BASE / "figuras"
DATOS.mkdir(exist_ok=True)
FIGURAS.mkdir(exist_ok=True)

# Reproducibilidad
rng = np.random.default_rng(7)

# %% [markdown]
# ## 1. Captura: datos crudos con errores tipicos
#
# Simulamos la captura de respuestas de una encuesta de ingresos. Como en la
# realidad, los datos llegan "sucios": campos vacios, filas duplicadas, fechas
# escritas como texto en formatos distintos y espacios sobrantes en el texto.

# %%
# Construimos un pequeno dataset crudo "como se capturo"
crudo = pd.DataFrame({
    "id": [1, 2, 3, 4, 4, 5, 6],                     # el 4 viene duplicado
    "nombre": [" Ana", "Luis ", "Mara", "Beto", "Beto", "  Eva", " Noe"],
    "ciudad": ["GDL", "CDMX", "gdl", "MTY", "MTY", "CDMX", None],  # falta una
    "ingreso": [12000, 18000, None, 9000, 9000, 25000, 15000],     # falta uno
    "fecha_captura": ["2026-01-15", "15/01/2026", "2026-01-16",    # formatos mixtos
                      "2026-01-16", "2026-01-16", "2026-01-17", "2026-01-17"],
})
crudo.to_csv(DATOS / "captura_cruda.csv", index=False)
print("Datos crudos capturados:")
print(crudo)

# %%
# Diagnostico rapido de problemas de captura
print("Filas duplicadas:", int(crudo.duplicated().sum()))
print("Valores faltantes por columna:")
print(crudo.isna().sum())

# %% [markdown]
# ## 2. Censo vs encuesta: muestreo e intervalo de confianza
#
# Un **censo** mide a toda la poblacion; una **encuesta** mide solo una muestra
# y *infiere*. Creamos una "poblacion" completa (lo que daria un censo) y vemos
# que tan bien la estima una sola encuesta.

# %%
# "Censo": toda la poblacion (valor real conocido)
poblacion = rng.normal(loc=15000, scale=4000, size=100_000)
media_real = poblacion.mean()
print(f"Media REAL de la poblacion (censo): {media_real:,.1f}")

# "Encuesta": una muestra aleatoria de 1000 personas
muestra = rng.choice(poblacion, size=1000, replace=False)
media_muestra = muestra.mean()
error_std = muestra.std(ddof=1) / np.sqrt(len(muestra))
ic_bajo = media_muestra - 1.96 * error_std
ic_alto = media_muestra + 1.96 * error_std
print(f"Media estimada (encuesta n=1000): {media_muestra:,.1f}")
print(f"IC 95%: [{ic_bajo:,.1f} , {ic_alto:,.1f}]")
print("?`El IC contiene la media real?", bool(ic_bajo <= media_real <= ic_alto))

# %% [markdown]
# ### ?`Que significa "95% de confianza"?
#
# Si repitieramos la encuesta muchas veces, ~95% de los intervalos contendrian
# la media real. Lo verificamos con 100 muestras y lo graficamos.

# %%
# Repetimos el muestreo 100 veces y contamos cuantos IC atrapan la media real
n_rep = 100
contiene = 0
intervalos = []
for _ in range(n_rep):
    m = rng.choice(poblacion, size=1000, replace=False)
    mu = m.mean()
    se = m.std(ddof=1) / np.sqrt(len(m))
    lo, hi = mu - 1.96 * se, mu + 1.96 * se
    intervalos.append((lo, mu, hi))
    if lo <= media_real <= hi:
        contiene += 1
print(f"De {n_rep} encuestas, {contiene} atraparon la media real (esperado ~95)")

# %%
# Graficamos los 100 intervalos: en gris los que atrapan la media, rojo los que no
plt.figure(figsize=(6, 4))
for i, (lo, mu, hi) in enumerate(intervalos):
    ok = lo <= media_real <= hi
    plt.plot([lo, hi], [i, i], color="#0094A2" if ok else "#FE730C", linewidth=0.8)
plt.axvline(media_real, color="#532587", linewidth=1.5, label="media real")
plt.xlabel("ingreso estimado")
plt.ylabel("encuesta #")
plt.title(f"100 encuestas: {contiene} IC del 95% atrapan la media real")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURAS / "intervalos_confianza.png", dpi=130)
plt.close()
print("Figura guardada: figuras/intervalos_confianza.png")

# %% [markdown]
# ## 3. ETL: Extract -- Transform -- Load
#
# Movemos los datos crudos hacia una mini-bodega. **Extract**: leer el CSV crudo.
# **Transform**: limpiar (quitar duplicados, normalizar texto y fechas, imputar
# faltantes). **Load**: guardar en una base SQLite (nuestra bodega de datos).

# %%
# EXTRACT: leer los datos crudos tal como se capturaron
extraido = pd.read_csv(DATOS / "captura_cruda.csv")
print("Extract: filas leidas =", len(extraido))

# %%
# TRANSFORM: limpieza paso a paso
t = extraido.copy()
t = t.drop_duplicates()                                  # quita filas repetidas
t["nombre"] = t["nombre"].str.strip()                    # espacios sobrantes
t["ciudad"] = t["ciudad"].str.upper()                    # normaliza mayusculas
# fechas a formato ISO (acepta los dos formatos capturados)
t["fecha_captura"] = pd.to_datetime(t["fecha_captura"], format="mixed", dayfirst=True)
# imputa el ingreso faltante con la mediana
t["ingreso"] = t["ingreso"].fillna(t["ingreso"].median())
# imputa la ciudad faltante con una etiqueta explicita
t["ciudad"] = t["ciudad"].fillna("DESCONOCIDA")
print("Transform: datos limpios")
print(t)

# %%
# LOAD: cargar la tabla limpia en una bodega SQLite y consultarla con SQL
bodega = DATOS / "bodega.sqlite"
with sqlite3.connect(bodega) as con:
    t.to_sql("encuesta", con, if_exists="replace", index=False)
    consulta = "SELECT ciudad, COUNT(*) AS n, AVG(ingreso) AS ingreso_prom " \
               "FROM encuesta GROUP BY ciudad ORDER BY ingreso_prom DESC"
    reporte = pd.read_sql_query(consulta, con)
print("Load + consulta SQL (ingreso promedio por ciudad):")
print(reporte)

# %% [markdown]
# ## 4. Almacenamiento: formatos y la regla 3-2-1
#
# El mismo dato ocupa distinto espacio segun el formato. Comparamos CSV, CSV
# comprimido (gzip) y JSON. En produccion ademas se aplica la regla **3-2-1**:
# 3 copias, en 2 medios distintos, con 1 copia fuera del sitio.

# %%
# Generamos un dataset mas grande para que las diferencias se noten
grande = pd.DataFrame({
    "id": np.arange(20_000),
    "valor": rng.normal(size=20_000).round(4),
    "categoria": rng.choice(["A", "B", "C"], size=20_000),
})

ruta_csv = DATOS / "grande.csv"
ruta_gz = DATOS / "grande.csv.gz"
ruta_json = DATOS / "grande.json"

grande.to_csv(ruta_csv, index=False)
with gzip.open(ruta_gz, "wt") as f:
    grande.to_csv(f, index=False)
grande.to_json(ruta_json, orient="records")

for ruta in (ruta_csv, ruta_gz, ruta_json):
    print(f"{ruta.name:14s}: {ruta.stat().st_size/1024:8.1f} KB")

# %% [markdown]
# ## Conclusiones
#
# - En la **captura**, los datos casi siempre llegan sucios: duplicados,
#   faltantes y formatos inconsistentes. Diagnosticarlos es el primer paso.
# - Una **encuesta** estima a la poblacion con una muestra; el intervalo de
#   confianza del 95% atrapa el valor real ~95 de cada 100 veces (lo vimos).
# - El **ETL** ordena el flujo: extraer, transformar (limpiar) y cargar en una
#   bodega (aqui SQLite) lista para consultarse con SQL.
# - El **formato de almacenamiento** importa: comprimir (gzip) ahorra mucho
#   espacio frente a CSV o JSON; y siempre conviene respaldar con la regla 3-2-1.
