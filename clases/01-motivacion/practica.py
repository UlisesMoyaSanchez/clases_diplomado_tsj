# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Clase 01 - Motivacion: los datos en el corazon de la IA
#
# Esta practica acompana la clase de motivacion. No entrenamos modelos grandes:
# usamos codigo corto para **demostrar** las ideas centrales de la sesion.
#
# Lo que veremos con codigo:
# 1. Por que la **programacion clasica** (fuerza bruta) no escala: el espacio de
#    busqueda del ajedrez y del Go contra el numero de atomos del universo.
# 2. La diferencia entre **dato** e **informacion**: una imagen es, para la
#    maquina, solo una matriz de numeros.
# 3. Por que el **aprendizaje** gana a las reglas escritas a mano: un mismo
#    problema resuelto con una regla manual y con un modelo de ML.
# 4. La **taxonomia del ML** en accion: aprendizaje supervisado vs no supervisado.
# 5. El reto de los **datos a gran escala**: el crecimiento de datos y parametros
#    en los modelos de lenguaje (LLM).

# %% [markdown]
# ## Objetivos de la practica
#
# - Cuantificar por que algunos problemas son intratables por fuerza bruta.
# - Distinguir dato, informacion y conocimiento con un ejemplo concreto.
# - Comparar empiricamente una regla manual contra un modelo aprendido.
# - Ver un ejemplo de aprendizaje supervisado y uno no supervisado.
# - Visualizar la escala de datos que exigen los modelos modernos.
# - Guardar las figuras generadas en la carpeta figuras/.

# %%
# Imports (stdlib primero, luego externos).
import math
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

# Semilla para resultados reproducibles.
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Carpeta de salida para las figuras (relativa a la carpeta de la clase).
FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras") \
    if "__file__" in globals() else "figuras"
os.makedirs(FIG_DIR, exist_ok=True)
print("Las figuras se guardaran en:", FIG_DIR)

# %% [markdown]
# ## 1. Por que la fuerza bruta no alcanza
#
# La programacion clasica resuelve un problema si podemos escribir las reglas o
# enumerar las opciones. En juegos como el ajedrez o el Go el numero de
# posiciones es tan grande que enumerarlas es **fisicamente imposible**.
# Comparemos esas magnitudes con el numero estimado de atomos en el universo
# observable (~10^80).

# %%
# Tamanos aproximados del espacio de estados (ordenes de magnitud, base 10).
espacios = {
    "Atomos en el\nuniverso": 80,
    "Ajedrez\n(posiciones)": 47,
    "Ajedrez\n(arbol de juego)": 120,
    "Go\n(posiciones)": 170,
}

for nombre, exp in espacios.items():
    print(f"{nombre.replace(chr(10), ' '):28s} ~ 10^{exp}")

# %% [markdown]
# El arbol de juego del ajedrez (~10^120) y el espacio del Go (~10^170) superan
# por muchos ordenes de magnitud al numero de atomos del universo (~10^80). Por
# eso Deep Blue y AlphaGo no "enumeran" todo: **buscan de forma guiada** y, en el
# caso de AlphaGo, **aprenden** de datos y experiencia.

# %%
# Visualizamos los ordenes de magnitud (escala logaritmica implicita: graficamos
# el exponente, no el numero, porque el numero no cabe en ninguna escala).
nombres = list(espacios.keys())
exps = [espacios[n] for n in nombres]
colores = ["#0094A2", "#FE730C", "#FF5A0C", "#532587"]

fig, ax = plt.subplots(figsize=(8, 4.5))
barras = ax.bar(nombres, exps, color=colores)
ax.axhline(80, color="#0094A2", linestyle="--", linewidth=1)
ax.set_ylabel("Orden de magnitud (exponente de 10)")
ax.set_title("Tamano del espacio de busqueda (potencias de 10)")
for b, e in zip(barras, exps):
    ax.text(b.get_x() + b.get_width() / 2, e + 2, f"10^{e}",
            ha="center", va="bottom", fontsize=9)
plt.tight_layout()
ruta = os.path.join(FIG_DIR, "espacio_busqueda.png")
plt.savefig(ruta, dpi=150)
plt.close(fig)
print("Figura guardada:", ruta)

# %% [markdown]
# ## 2. Dato vs informacion: una imagen es solo numeros
#
# Cargamos digitos manuscritos (dataset `digits` de scikit-learn). Cada imagen es
# una matriz de 8x8 con la intensidad de cada pixel: eso es el **dato** en bruto.
# La etiqueta ("es un 5") es la **informacion**. La maquina no "ve" un numero:
# ve una tabla de valores.

# %%
digits = load_digits()
print("Imagenes:", digits.images.shape, "| Etiquetas:", digits.target.shape)

# Tomamos la primera imagen y mostramos su matriz de pixeles (el dato).
img0 = digits.images[0]
etiqueta0 = digits.target[0]
print("\nEsta imagen es, para la maquina, esta matriz 8x8 (el DATO):")
print(img0.astype(int))
print("\nLa INFORMACION (lo que significa) es la etiqueta:", etiqueta0)

# %%
# Mostramos la misma imagen como la ve un humano y como la "ve" la maquina.
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].imshow(img0, cmap="gray_r")
axes[0].set_title(f"Como lo ve el humano\n(informacion: 'es un {etiqueta0}')")
axes[0].axis("off")
im = axes[1].imshow(img0, cmap="viridis")
for i in range(img0.shape[0]):
    for j in range(img0.shape[1]):
        axes[1].text(j, i, int(img0[i, j]), ha="center", va="center",
                     color="white", fontsize=7)
axes[1].set_title("Como lo ve la maquina\n(dato: matriz de pixeles)")
axes[1].axis("off")
plt.tight_layout()
ruta = os.path.join(FIG_DIR, "dato_vs_informacion.png")
plt.savefig(ruta, dpi=150)
plt.close(fig)
print("Figura guardada:", ruta)

# %% [markdown]
# ## 3. Reglas a mano vs aprender de los datos
#
# Intentemos clasificar los digitos como en la **programacion clasica**: con una
# regla escrita a mano. Una idea ingenua: mirar cuantos pixeles estan "encendidos"
# (intensidad alta). Veremos que falla, porque distintos digitos tienen cantidades
# de tinta parecidas.

# %%
# Aplanamos cada imagen 8x8 a un vector de 64 numeros.
X = digits.images.reshape(len(digits.images), -1)
y = digits.target

# Regla manual: contar pixeles "encendidos" y asignar la clase mas frecuente
# para ese conteo (lo aprendemos del conjunto de entrenamiento como tabla).
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y)

tinta_train = (X_train > 5).sum(axis=1)
tinta_test = (X_test > 5).sum(axis=1)

# Para cada nivel de tinta, cual es el digito mas comun en entrenamiento.
tabla = pd.DataFrame({"tinta": tinta_train, "y": y_train})
mapa = tabla.groupby("tinta")["y"].agg(lambda s: s.mode().iloc[0])
clase_mas_comun = int(pd.Series(y_train).mode().iloc[0])

pred_regla = np.array([mapa.get(t, clase_mas_comun) for t in tinta_test])
acc_regla = accuracy_score(y_test, pred_regla)
print(f"Exactitud de la REGLA MANUAL (contar tinta): {acc_regla:.2%}")

# %%
# Ahora dejamos que un modelo APRENDA las reglas a partir de los datos.
modelo = LogisticRegression(max_iter=5000)
modelo.fit(X_train, y_train)
pred_ml = modelo.predict(X_test)
acc_ml = accuracy_score(y_test, pred_ml)
print(f"Exactitud del MODELO APRENDIDO (ML):         {acc_ml:.2%}")
print(f"\nEl ML mejora a la regla manual en {acc_ml - acc_regla:.0%} de exactitud.")

# %%
# Comparacion visual del azar, la regla manual y el modelo aprendido.
metodos = ["Azar\n(1 de 10)", "Regla manual\n(contar tinta)", "Modelo ML\n(aprendido)"]
valores = [0.10, acc_regla, acc_ml]
fig, ax = plt.subplots(figsize=(7, 4.2))
barras = ax.bar(metodos, valores, color=["#9aa0a6", "#FE730C", "#0094A2"])
ax.set_ylim(0, 1)
ax.set_ylabel("Exactitud")
ax.set_title("Escribir reglas a mano vs aprenderlas de los datos")
for b, v in zip(barras, valores):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.0%}",
            ha="center", va="bottom")
plt.tight_layout()
ruta = os.path.join(FIG_DIR, "reglas_vs_ml.png")
plt.savefig(ruta, dpi=150)
plt.close(fig)
print("Figura guardada:", ruta)

# %% [markdown]
# ## 4. Taxonomia del ML: supervisado vs no supervisado
#
# - **Supervisado**: aprendemos con datos *etiquetados* (lo que hicimos arriba con
#   los digitos: cada imagen traia su numero correcto).
# - **No supervisado**: encontramos estructura *sin etiquetas*. Agrupamos los
#   digitos en 10 grupos con K-Means, sin decirle nunca que numero es cada uno.

# %%
# Reducimos a 2 dimensiones con PCA solo para poder dibujar los grupos.
pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_2d = pca.fit_transform(X)

kmeans = KMeans(n_clusters=10, random_state=RANDOM_STATE, n_init=10)
grupos = kmeans.fit_predict(X)
print("K-Means agrupo", len(X), "imagenes en", len(np.unique(grupos)),
      "grupos SIN ver las etiquetas.")

# %%
# Dibujamos: a la izquierda coloreado por la etiqueta real (supervisado),
# a la derecha por el grupo que descubrio K-Means (no supervisado).
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
sc0 = axes[0].scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap="tab10", s=10)
axes[0].set_title("Supervisado: color = etiqueta real")
axes[0].set_xlabel("componente 1")
axes[0].set_ylabel("componente 2")
axes[1].scatter(X_2d[:, 0], X_2d[:, 1], c=grupos, cmap="tab10", s=10)
axes[1].set_title("No supervisado: color = grupo de K-Means")
axes[1].set_xlabel("componente 1")
plt.tight_layout()
ruta = os.path.join(FIG_DIR, "supervisado_vs_no_supervisado.png")
plt.savefig(ruta, dpi=150)
plt.close(fig)
print("Figura guardada:", ruta)

# %% [markdown]
# Aunque K-Means nunca vio las etiquetas, los grupos que forma coinciden en gran
# medida con los digitos reales: hay **estructura en los datos** que el modelo
# descubre solo. Esa es la base del aprendizaje no supervisado y auto-supervisado.

# %% [markdown]
# ## 5. El reto de la escala: datos y parametros de los LLM
#
# Los modelos modernos crecen en dos ejes: **parametros** (tamano del modelo) y
# **datos de entrenamiento** (tokens). Usamos cifras publicas aproximadas, en
# ordenes de magnitud, para ilustrar la tendencia (no son exactas).

# %%
# Cifras aproximadas y publicas (orden de magnitud) de algunos modelos.
modelos = pd.DataFrame({
    "modelo": ["AlexNet", "BERT", "GPT-2", "GPT-3", "Frontera-2024"],
    "anio": [2012, 2018, 2019, 2020, 2024],
    "parametros_millones": [60, 340, 1500, 175000, 1500000],
    "tokens_miles_millones": [0.0, 3.3, 10, 300, 15000],
})
print(modelos.to_string(index=False))

# %%
# Crecimiento de parametros en escala logaritmica.
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(modelos["anio"], modelos["parametros_millones"], "o-",
        color="#532587", linewidth=2, markersize=8)
ax.set_yscale("log")
ax.set_ylabel("Parametros (millones, escala log)")
ax.set_xlabel("Anio")
ax.set_title("Crecimiento del tamano de los modelos")
for _, fila in modelos.iterrows():
    ax.annotate(fila["modelo"],
                (fila["anio"], fila["parametros_millones"]),
                textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=8)
plt.tight_layout()
ruta = os.path.join(FIG_DIR, "crecimiento_parametros.png")
plt.savefig(ruta, dpi=150)
plt.close(fig)
print("Figura guardada:", ruta)

# %% [markdown]
# El salto es de varios ordenes de magnitud en pocos anios. Mas parametros exigen
# **mas datos** y mas computo: por eso el cuello de botella de la IA moderna son
# los datos (volumen, calidad, licencias y frescura).

# %% [markdown]
# ## Conclusiones: que aprendimos
#
# - Hay problemas (ajedrez, Go, vision) donde **enumerar o escribir reglas es
#   imposible**: hay que aprender de datos.
# - Para la maquina una imagen es **solo numeros** (dato); el significado
#   (informacion) lo aporta la etiqueta o el contexto.
# - Un modelo que **aprende** de ejemplos supera con claridad a una regla escrita
#   a mano para el mismo problema.
# - El ML tiene varios estilos: con etiquetas (**supervisado**) y sin ellas
#   (**no supervisado**), entre otros.
# - Los modelos modernos crecen en parametros y datos a un ritmo enorme: gobernar
#   y preparar esos **datos** es el gran reto, y el tema de este diplomado.

# %%
# Listado final de las figuras generadas.
print("Figuras generadas en", FIG_DIR + ":")
for f in sorted(os.listdir(FIG_DIR)):
    if f.endswith(".png"):
        print(" -", f)
