# %% [markdown]
# # Clase 04 -- Ciclo de vida de los datos (Parte II)
#
# Practica de las etapas **03 acceso/seguridad**, **04 limpieza/analisis/
# visualizacion** y **05 archivado/eliminacion**. Vamos a:
#
# 1. **Seguridad y privacidad (03)**: anonimizar datos personales (PII) con
#    hashing (SHA-256) y enmascarado, para poder usarlos sin exponer identidades.
# 2. **EDA (04)**: describir, contar faltantes, detectar outliers con la regla
#    del IQR y medir correlacion. Ademas, el **cuarteto de Anscombe** muestra por
#    que SIEMPRE hay que visualizar.
# 3. **Archivado y eliminacion (05)**: atender una solicitud **ARCO de
#    cancelacion** (borrar un registro) y archivar el resto comprimido con un
#    JSON de metadatos (fecha, responsable, razon).
#
# Uso:
#     python practica.py
# Genera datasets en datos/ (incluido el archivo comprimido) y graficas en figuras/.

# %%
# Imports (stdlib y externos)
import gzip
import hashlib
import json
from datetime import date
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

rng = np.random.default_rng(11)

# %% [markdown]
# ## 1. Seguridad y privacidad (etapa 03): anonimizar PII
#
# Antes de compartir datos, hay que proteger la informacion personal (PII).
# Creamos una tabla de clientes con nombre, correo, edad e ingreso, y la
# anonimizamos: el nombre+correo se convierten en un seudonimo con SHA-256 y el
# correo se enmascara. Asi se puede analizar sin revelar identidades.

# %%
# Tabla de clientes con datos personales (PII)
clientes = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "nombre": ["Ana Ruiz", "Luis Gil", "Mara Paz", "Beto Lima",
               "Eva Soto", "Noe Diaz", "Ivan Mora", "Sara Vega"],
    "email": ["ana@mail.com", "luis@mail.com", "mara@mail.com", "beto@mail.com",
              "eva@mail.com", "noe@mail.com", "ivan@mail.com", "sara@mail.com"],
    "edad": [34, 29, 41, 23, 52, 38, 45, None],          # un faltante
    "ingreso": [12000, 18000, 15000, 9000, 25000, 16000, 200000, 14000],  # un outlier
})
print("Clientes con PII (NO se debe compartir asi):")
print(clientes[["id", "nombre", "email"]])


# %%
# Funciones de anonimizacion: seudonimo (hash) y enmascarado del correo
def seudonimo(texto: str) -> str:
    # SHA-256 produce un identificador estable y no reversible; tomamos 10 chars
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:10]

def enmascarar_email(email: str) -> str:
    # deja la primera letra y oculta el resto del usuario: a***@mail.com
    usuario, dominio = email.split("@")
    return usuario[0] + "***@" + dominio

anon = clientes.copy()
anon["seudonimo"] = (anon["nombre"] + anon["email"]).map(seudonimo)
anon["email"] = anon["email"].map(enmascarar_email)
anon = anon.drop(columns=["nombre"])    # quitamos el nombre real
anon.to_csv(DATOS / "clientes_anon.csv", index=False)
print("Datos anonimizados (listos para analizar/compartir):")
print(anon[["id", "seudonimo", "email", "edad", "ingreso"]])

# %% [markdown]
# ## 2. EDA (etapa 04): describir, faltantes, outliers y correlacion
#
# Con los datos ya anonimizados hacemos un analisis exploratorio basico.

# %%
# Resumen descriptivo de las variables numericas
print("Resumen descriptivo:")
print(anon[["edad", "ingreso"]].describe())
print("\nValores faltantes por columna:")
print(anon.isna().sum())

# %%
# Deteccion de outliers en el ingreso con la regla 1.5 x IQR
q1 = anon["ingreso"].quantile(0.25)
q3 = anon["ingreso"].quantile(0.75)
iqr = q3 - q1
bajo, alto = q1 - 1.5 * iqr, q3 + 1.5 * iqr
atipicos = anon[(anon["ingreso"] < bajo) | (anon["ingreso"] > alto)]
print(f"Limites normales de ingreso: [{bajo:,.0f} , {alto:,.0f}]")
print("Outliers detectados:")
print(atipicos[["id", "seudonimo", "ingreso"]])

# %%
# Correlacion entre edad e ingreso (ignorando el faltante)
correlacion = anon[["edad", "ingreso"]].corr()
print("Matriz de correlacion edad-ingreso:")
print(correlacion.round(3))

# %% [markdown]
# ### ?`Por que SIEMPRE visualizar? El cuarteto de Anscombe
#
# Los cuatro conjuntos de Anscombe tienen casi las mismas estadisticas (media,
# desviacion, correlacion y recta de regresion) pero formas muy distintas. Lo
# comprobamos numericamente y luego lo graficamos.

# %%
# Cuarteto de Anscombe (valores clasicos)
x123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
anscombe = pd.DataFrame({
    "x1": x123, "y1": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
    "x2": x123, "y2": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
    "x3": x123, "y3": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
    "x4": [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
    "y4": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
})
for i in range(1, 5):
    x, y = anscombe[f"x{i}"], anscombe[f"y{i}"]
    print(f"Set {i}: media_y={y.mean():.2f}, std_y={y.std(ddof=1):.2f}, "
          f"corr={x.corr(y):.3f}")

# %%
# Graficamos los cuatro conjuntos: misma estadistica, formas distintas
fig, axes = plt.subplots(2, 2, figsize=(7, 5.5))
colores = ["#0094A2", "#FE730C", "#FEB200", "#532587"]
for i, ax in enumerate(axes.flat, start=1):
    x, y = anscombe[f"x{i}"], anscombe[f"y{i}"]
    ax.scatter(x, y, color=colores[i - 1])
    # recta de regresion (identica en los cuatro): y = 3 + 0.5 x
    xs = np.array([3, 20])
    ax.plot(xs, 3 + 0.5 * xs, color="gray", linewidth=1, linestyle="--")
    ax.set_title(f"Set {i}")
    ax.set_xlim(2, 20)
    ax.set_ylim(2, 14)
fig.suptitle("Cuarteto de Anscombe: misma estadistica, formas distintas")
fig.tight_layout()
fig.savefig(FIGURAS / "anscombe.png", dpi=130)
plt.close(fig)
print("Figura guardada: figuras/anscombe.png")

# %% [markdown]
# ## 3. Archivado y eliminacion (etapa 05)
#
# ### 3a. Solicitud ARCO de cancelacion
#
# Un cliente ejerce su derecho de **cancelacion** (eliminacion). Borramos su
# registro de la base activa, dejando constancia de la operacion.

# %%
# El cliente con id=4 solicita la eliminacion de sus datos
id_baja = 4
antes = len(anon)
activos = anon[anon["id"] != id_baja].copy()
print(f"Registros antes: {antes}; despues de la cancelacion: {len(activos)}")
print("?`Sigue el id=4 en la base activa?", bool((activos['id'] == id_baja).any()))
activos.to_csv(DATOS / "clientes_activos.csv", index=False)

# %% [markdown]
# ### 3b. Archivar el resto comprimido y con metadatos
#
# Los registros que se conservan se archivan **comprimidos** (ahorro de espacio)
# y acompanados de un JSON de **metadatos** que documenta la operacion: cuando,
# quien y por que (clave para auditoria y cumplimiento).

# %%
# Guardamos el archivo comprimido (almacenamiento "frio")
ruta_archivo = DATOS / "clientes_archivo.csv.gz"
with gzip.open(ruta_archivo, "wt") as f:
    activos.to_csv(f, index=False)

# Metadatos de la operacion de archivado (para auditoria)
contenido = ruta_archivo.read_bytes()
metadatos = {
    "fecha": date.today().isoformat(),
    "responsable": "equipo_datos",
    "razon": "archivado de clientes activos; baja ARCO del id 4",
    "n_registros": int(len(activos)),
    "archivo": ruta_archivo.name,
    "sha256": hashlib.sha256(contenido).hexdigest(),  # huella de integridad
}
(DATOS / "clientes_archivo.meta.json").write_text(
    json.dumps(metadatos, ensure_ascii=True, indent=2))
print("Metadatos del archivado:")
print(json.dumps(metadatos, ensure_ascii=True, indent=2))

# %% [markdown]
# ## Conclusiones
#
# - **Seguridad (03)**: anonimizar PII (seudonimos con hash y enmascarado)
#   permite analizar los datos sin exponer identidades.
# - **EDA (04)**: describir, contar faltantes, detectar outliers con el IQR y
#   medir correlaciones son los primeros pasos de todo analisis.
# - **Visualizar siempre**: el cuarteto de Anscombe tiene la misma estadistica
#   pero formas muy distintas; sin graficar, no se nota.
# - **Archivado/eliminacion (05)**: atender solicitudes ARCO de cancelacion y
#   archivar comprimido con metadatos (fecha, responsable, razon, huella SHA-256)
#   deja una operacion trazable y auditable.
