# %% [markdown]
# # Clase 02 -- Tipos de datos y gramatica de los datos
#
# En esta practica vamos a:
#
# 1. Reconocer los tipos de datos (cualitativo/cuantitativo, nominal/ordinal...).
# 2. Ver el mismo hecho como dato estructurado, semi-estructurado y no estructurado.
# 3. Entender como se representan numericamente una imagen y un texto.
# 4. Aplicar la gramatica "tidy": pasar una tabla de formato ancho (wide) a
#    formato ordenado (tidy) con pandas.
# 5. Reproducir malas practicas tipicas de hoja de calculo (columnas que inician
#    con numero, fechas como texto, y el famoso bug de los nombres de genes) y
#    corregirlas.
#
# Uso:
#     python practica.py
# Genera los datasets en datos/ y las graficas en figuras/.

# %%
# Imports (stdlib, externos)
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # backend sin ventana: guardamos las figuras a archivo
import matplotlib.pyplot as plt

# %%
# Carpetas de salida (relativas a este archivo).
# Como script usamos __file__; como notebook, el directorio de trabajo.
try:
    BASE = Path(__file__).resolve().parent
except NameError:
    BASE = Path.cwd()
DATOS = BASE / "datos"
FIGURAS = BASE / "figuras"
DATOS.mkdir(exist_ok=True)
FIGURAS.mkdir(exist_ok=True)

# Reproducibilidad
np.random.seed(42)

# %% [markdown]
# ## 1. Tipos de datos por su naturaleza
#
# Construimos una tabla pequena de personas. Cada columna es de un tipo distinto:
# nominal (ciudad), ordinal (satisfaccion), cuantitativo discreto (hijos),
# cuantitativo continuo (estatura), fecha y booleano. Pandas infiere un `dtype`
# para cada columna; ese dtype es la primera pista del tipo de dato.

# %%
# Tabla didactica con tipos variados
personas = pd.DataFrame({
    "nombre": ["Ana", "Luis", "Mara", "Beto"],          # nominal (texto)
    "ciudad": ["GDL", "CDMX", "GDL", "MTY"],             # nominal
    "satisfaccion": ["alto", "bajo", "medio", "alto"],   # ordinal
    "hijos": [2, 0, 1, 3],                                # cuantitativo discreto
    "estatura_m": [1.62, 1.78, 1.55, 1.80],              # cuantitativo continuo
    "es premium": [False, True, False, True],            # booleano; nombre con espacio: mala practica
    "fecha_alta": ["2026-01-15", "2026-02-03",           # fecha (aun como texto)
                   "2026-02-20", "2026-03-01"],
})
print(personas)
print()
print("dtypes inferidos por pandas:")
print(personas.dtypes)

# %% [markdown]
# Nota: la columna `satisfaccion` es **ordinal** (bajo < medio < alto), no un
# simple texto. Se lo decimos a pandas con un tipo `Categorical` ordenado, para
# que las comparaciones tengan sentido.

# %%
# Convertimos satisfaccion a categoria ORDENADA
orden = ["bajo", "medio", "alto"]
personas["satisfaccion"] = pd.Categorical(
    personas["satisfaccion"], categories=orden, ordered=True
)
print("Ahora 'alto' > 'bajo' es:", personas["satisfaccion"][0] > personas["satisfaccion"][1])
print("dtype de satisfaccion:", personas["satisfaccion"].dtype)

# %% [markdown]
# ## 2. El mismo hecho en tres estructuras
#
# Un mismo registro se puede guardar como dato **estructurado** (una fila de
# tabla), **semi-estructurado** (JSON con jerarquia) o **no estructurado**
# (texto libre). A mas estructura, mas facil de consultar; a menos estructura,
# mas riqueza pero mas trabajo de preparacion.

# %%
# Estructurado: una fila de la tabla
estructurado = personas.iloc[[0]][["nombre", "ciudad", "hijos"]]
print("ESTRUCTURADO (tabla):")
print(estructurado)

# Semi-estructurado: JSON con una lista anidada
semi = {"nombre": "Ana", "ciudad": "GDL", "hijos": 2, "hobbies": ["correr", "leer"]}
print("\nSEMI-ESTRUCTURADO (JSON):")
print(json.dumps(semi, ensure_ascii=True, indent=2))

# No estructurado: texto libre
no_estructurado = "Ana vive en GDL, tiene 2 hijos y le gusta correr y leer."
print("\nNO ESTRUCTURADO (texto):")
print(no_estructurado)

# %% [markdown]
# ## 3. Representacion numerica: imagen y texto
#
# Para que un modelo procese un dato hay que volverlo numeros. Una **imagen** es
# una matriz de pixeles; un **texto** es una secuencia de codigos. Veamos ambos.

# %%
# Una imagen en escala de grises es una matriz HxW de enteros 0-255.
# Creamos un degradado de 8x8 para inspeccionar su forma.
imagen = np.linspace(0, 255, 64).reshape(8, 8).astype(int)
print("Imagen 8x8 (matriz de pixeles 0-255):")
print(imagen)
print("\nforma (shape):", imagen.shape, "-> alto x ancho")
print("una imagen 640x640 a color tiene", 640 * 640 * 3, "numeros")

# %%
# Guardamos la imagen como figura para verla
plt.figure(figsize=(3, 3))
plt.imshow(imagen, cmap="gray", vmin=0, vmax=255)
plt.title("Imagen = matriz de pixeles")
plt.axis("off")
plt.tight_layout()
plt.savefig(FIGURAS / "imagen_matriz.png", dpi=130)
plt.close()
print("Figura guardada: figuras/imagen_matriz.png")

# %%
# Un texto se vuelve numeros: cada caracter tiene un codigo (aqui, su code point).
texto = "el gato"
codigos = [ord(c) for c in texto]
print("texto :", texto)
print("codigos:", codigos)
print("(los modelos reales usan 'tokens' y 'embeddings', pero la idea es la misma:")
print(" texto -> numeros)")

# %% [markdown]
# ## 4. Gramatica de los datos: de wide a tidy
#
# Regla **tidy** (Hadley Wickham): cada variable una columna, cada observacion
# una fila. Primero creamos una tabla en formato **ancho (wide)**, con los anios
# como columnas (mala practica: el anio es un valor, no una variable), la
# guardamos como CSV y luego la ordenamos.

# %%
# Tabla wide: temperatura promedio por ciudad y anio (anios como columnas)
wide = pd.DataFrame({
    "ciudad": ["GDL", "CDMX", "MTY"],
    "2020": [28.1, 17.5, 31.2],
    "2021": [28.7, 17.9, 31.6],
    "2022": [29.0, 18.2, 32.1],
})
wide.to_csv(DATOS / "temperaturas_wide.csv", index=False)
print("WIDE (anios como columnas):")
print(wide)

# %%
# melt: "alargamos" la tabla a formato tidy (una observacion por fila)
tidy = wide.melt(id_vars="ciudad", var_name="anio", value_name="temp")
tidy["anio"] = tidy["anio"].astype(int)  # el anio debe ser numero, no texto
tidy = tidy.sort_values(["ciudad", "anio"]).reset_index(drop=True)
tidy.to_csv(DATOS / "temperaturas_tidy.csv", index=False)
print("TIDY (una observacion por fila):")
print(tidy)

# %% [markdown]
# Con los datos tidy, agrupar y graficar es trivial. Calculamos la temperatura
# promedio por ciudad y la guardamos como grafica.

# %%
# Agregacion sencilla sobre datos tidy
prom = tidy.groupby("ciudad")["temp"].mean().sort_values()
print("Temperatura promedio por ciudad:")
print(prom)

plt.figure(figsize=(5, 3))
prom.plot(kind="bar", color="#0094A2")
plt.ylabel("Temp promedio (C)")
plt.title("Promedio por ciudad (datos tidy)")
plt.tight_layout()
plt.savefig(FIGURAS / "temp_por_ciudad.png", dpi=130)
plt.close()
print("Figura guardada: figuras/temp_por_ciudad.png")

# %% [markdown]
# ## 5. Malas practicas de hoja de calculo (y su arreglo)
#
# ### 5a. Nombres de columna que inician con numero o tienen espacios
#
# Nombres como `2020` o `alta_ debit` complican el procesamiento. Los
# normalizamos a identificadores seguros (minusculas, sin espacios, con prefijo
# si inician con numero).

# %%
def limpiar_nombre(col: str) -> str:
    # minusculas, espacios -> guion bajo, sin espacios al inicio/fin
    nuevo = col.strip().lower().replace(" ", "_")
    # si inicia con numero, le anteponemos un prefijo
    if nuevo[0].isdigit():
        nuevo = "anio_" + nuevo
    return nuevo

cols_malas = list(wide.columns) + ["es premium"]
print("antes :", cols_malas)
print("despues:", [limpiar_nombre(c) for c in cols_malas])

# %% [markdown]
# ### 5b. Fechas como texto
#
# La columna `fecha_alta` se leyo como texto. Si la queremos ordenar o restar,
# hay que convertirla a tipo fecha. Siempre formato ISO (`AAAA-MM-DD`).

# %%
personas["fecha_alta"] = pd.to_datetime(personas["fecha_alta"])
print("dtype de fecha_alta:", personas["fecha_alta"].dtype)
# Ahora si: cuantos dias entre el primer y el ultimo registro
dias = (personas["fecha_alta"].max() - personas["fecha_alta"].min()).days
print("Dias entre el primer y el ultimo registro:", dias)

# %% [markdown]
# ### 5c. El bug de los nombres de genes (Excel los vuelve fechas)
#
# Simbolos como `SEPT2` o `MARCH1` son nombres de genes reales. Las hojas de
# calculo los "autocorregian" a fechas (`2-Sep`), corrompiendo datasets
# cientificos. Reproducimos el problema y mostramos la prevencion: importar la
# columna SIEMPRE como texto.

# %%
genes = ["SEPT2", "MARCH1", "BRCA1", "TP53", "DEC1"]

# Simulamos lo que hace una hoja de calculo: convierte algunos a "fecha"
def como_lo_arruina_excel(simbolo: str) -> str:
    meses = {"SEPT": "Sep", "MARCH": "Mar", "DEC": "Dec"}
    for clave, mes in meses.items():
        if simbolo.startswith(clave):
            numero = simbolo[len(clave):] or "1"
            return f"{numero}-{mes}"  # p.ej. SEPT2 -> "2-Sep"
    return simbolo

corrompidos = [como_lo_arruina_excel(g) for g in genes]
comparacion = pd.DataFrame({"original": genes, "tras_excel": corrompidos})
print(comparacion)
print()
n_danados = (comparacion["original"] != comparacion["tras_excel"]).sum()
print(f"{n_danados} de {len(genes)} simbolos quedaron corrompidos por la autocorreccion")

# %%
# Prevencion: al leer un CSV, forzar la columna de genes como texto (str).
# Guardamos y releemos con dtype=str para conservar los simbolos intactos.
pd.DataFrame({"gene": genes}).to_csv(DATOS / "genes.csv", index=False)
seguro = pd.read_csv(DATOS / "genes.csv", dtype={"gene": str})
print("Releido con dtype=str (intacto):")
print(seguro["gene"].tolist())

# %% [markdown]
# ## Conclusiones
#
# - El **tipo** de un dato (nominal, ordinal, discreto, continuo, fecha...)
#   decide que operaciones y graficas tienen sentido; conviene declararlo
#   explicitamente (p.ej. categorias ordenadas, fechas reales).
# - Un mismo hecho puede ser estructurado, semi-estructurado o no estructurado;
#   y todo dato (imagen, texto) termina representado como numeros.
# - La gramatica **tidy** (una variable por columna, una observacion por fila)
#   convierte el analisis en algo directo: `melt` ordena, `groupby` resume.
# - Las hojas de calculo invitan a errores caros: nombres invalidos, fechas
#   ambiguas y autocorrecciones como la de los genes. La prevencion es declarar
#   los tipos y nunca dejar que la herramienta "adivine".
