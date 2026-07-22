# %% [markdown]
# # Clase 05 -- Cultura de datos
#
# Practica de tres ideas centrales de la cultura de datos:
#
# 1. **Gramatica compartida**: el mismo dato presentado para un humano
#    (legible) y para una maquina (JSON tipado con esquema), y una version con
#    gramatica deficiente para contrastar.
# 2. **Correlacion no es causalidad**: simulamos ventas de helado y
#    ahogamientos, ambas explicadas por la temperatura (variable confusora), y
#    medimos su correlacion.
# 3. **Como mentir con estadisticas** (Darrell Huff): comparamos un eje Y
#    honesto contra un eje Y truncado (gee-whiz graph) con la misma serie, y
#    comparamos media vs mediana en salarios con un outlier.
#
# Uso:
#     python practica.py
# Genera datasets en datos/ y graficas en figuras/.

# %%
# Imports (stdlib y externos)
import json
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

rng = np.random.default_rng(5)

# %% [markdown]
# ## 1. Gramatica compartida: el mismo dato, tres presentaciones
#
# Preparamos una venta trimestral por region. La mostramos legible para un
# humano, estructurada con esquema para una maquina, y con una gramatica
# deficiente (ambigua e inconsistente) para ver como se rompe en ambos casos.

# %%
# Version "para humano": tabla legible, unidades y fecha en lenguaje natural
ventas_humano = pd.DataFrame({
    "Region": ["Guadalajara", "Ciudad de Mexico", "Monterrey"],
    "Ventas": ["$180,000", "$210,000", "$320,000"],
    "Periodo": ["1er trimestre 2026", "1er trimestre 2026", "1er trimestre 2026"],
})
print("Para humano (legible):")
print(ventas_humano.to_string(index=False))

# %%
# Version "para maquina": JSON tipado, claves normalizadas y esquema explicito
ventas_maquina = [
    {"region": "GDL", "ventas": 180000, "unidad": "MXN", "periodo": "2026-Q1"},
    {"region": "CDMX", "ventas": 210000, "unidad": "MXN", "periodo": "2026-Q1"},
    {"region": "MTY", "ventas": 320000, "unidad": "MXN", "periodo": "2026-Q1"},
]
esquema = {
    "region": "str (codigo de 3-4 letras)",
    "ventas": "int (unidad ver campo 'unidad')",
    "unidad": "str (ISO 4217)",
    "periodo": "str (ISO 8601, YYYY-Qn)",
}
(DATOS / "ventas_maquina.json").write_text(
    json.dumps({"datos": ventas_maquina, "esquema": esquema},
               ensure_ascii=True, indent=2))
print("\nPara maquina (JSON + esquema), guardado en datos/ventas_maquina.json:")
print(json.dumps(ventas_maquina[0], indent=2))

# %%
# Version con gramatica deficiente: columnas ambiguas y formatos inconsistentes
ventas_mala_gramatica = pd.DataFrame({
    "reg": ["Guadalajara (GDL)", "cdmx", "MTY"],
    "monto": ["180000 pesos", "$210,000.00", "320k"],
    "fecha": ["01/2026", "2026-02-15", "marzo 2026"],
})
print("\nCon gramatica deficiente (evitar esto):")
print(ventas_mala_gramatica.to_string(index=False))
print("\nProblema: 'reg' mezcla nombre y codigo, 'monto' usa 3 formatos "
      "distintos, y 'fecha' no distingue mes de captura vs periodo de venta.")
print("Ni una persona ni un programa pueden confiar en esta tabla sin "
      "normalizarla primero.")

# %% [markdown]
# ## 2. Correlacion no es causalidad: helados y ahogamientos
#
# Generamos 12 meses de temperatura promedio, y a partir de ella, ventas de
# helado y ahogamientos -ambas variables suben con la temperatura, pero no se
# causan entre si. Medimos la correlacion entre las tres variables.

# %%
# Temperatura mensual (variable confusora oculta) con forma de campana anual
meses = np.arange(1, 13)
temperatura = 18 + 10 * np.sin((meses - 3) * np.pi / 6) + rng.normal(0, 0.6, 12)

# Ventas de helado y ahogamientos: ambas dependen de la temperatura + ruido
ventas_helado = 200 + 15 * temperatura + rng.normal(0, 20, 12)
ahogamientos = 2 + 0.3 * temperatura + rng.normal(0, 0.8, 12)
ahogamientos = np.clip(ahogamientos, 0, None)

clima = pd.DataFrame({
    "mes": meses, "temperatura_c": temperatura.round(1),
    "ventas_helado": ventas_helado.round(0).astype(int),
    "ahogamientos": ahogamientos.round(1),
})
clima.to_csv(DATOS / "clima_helados_ahogamientos.csv", index=False)
print("Datos simulados (primeras filas):")
print(clima.head())

# %%
# Correlacion entre las tres variables
corr = clima[["temperatura_c", "ventas_helado", "ahogamientos"]].corr()
print("\nMatriz de correlacion:")
print(corr.round(3))
print(f"\nVentas de helado vs ahogamientos: r = "
      f"{corr.loc['ventas_helado', 'ahogamientos']:.3f} (correlacion alta)")
print("Pero ninguna causa a la otra: ambas responden a la temperatura "
      "(variable confusora).")

# %%
# Graficamos las tres series para ver que se mueven juntas por el clima
fig, ax1 = plt.subplots(figsize=(6.5, 4))
ax1.plot(clima["mes"], clima["ventas_helado"], color="#0094A2",
         marker="o", label="Ventas helado")
ax1.set_xlabel("Mes")
ax1.set_ylabel("Ventas helado", color="#0094A2")
ax2 = ax1.twinx()
ax2.plot(clima["mes"], clima["ahogamientos"], color="#FE730C",
         marker="s", linestyle="--", label="Ahogamientos")
ax2.set_ylabel("Ahogamientos", color="#FE730C")
fig.suptitle("Ventas de helado y ahogamientos: se mueven juntos por el clima")
fig.tight_layout()
fig.savefig(FIGURAS / "helados_ahogamientos.png", dpi=130)
plt.close(fig)
print("Figura guardada: figuras/helados_ahogamientos.png")

# %% [markdown]
# ## 3. Como mentir con estadisticas
#
# ### 3a. La grafica que impresiona (gee-whiz graph)
#
# La misma serie de ventas anuales, graficada con un eje Y honesto (desde
# cero) y con un eje Y truncado que exagera un cambio pequeno.

# %%
# Serie con un cambio real de solo ~3% entre anios
anios = ["2023", "2024", "2025", "2026"]
ventas_anuales = np.array([100.0, 101.2, 102.0, 103.0])  # ~3% de crecimiento
print("Ventas anuales (indice, 2023=100):", ventas_anuales)

# %%
# Graficamos lado a lado: eje honesto (desde 0) vs eje truncado (desde 98)
fig, (ax_honesto, ax_truncado) = plt.subplots(1, 2, figsize=(8, 3.8))
ax_honesto.bar(anios, ventas_anuales, color="#0094A2")
ax_honesto.set_ylim(0, 110)
ax_honesto.set_title("Eje honesto (0-110)")

ax_truncado.bar(anios, ventas_anuales, color="#FE730C")
ax_truncado.set_ylim(98, 104)
ax_truncado.set_title("Eje truncado (98-104): exagera")

fig.suptitle("Mismo dato (+3%), dos impresiones muy distintas")
fig.tight_layout()
fig.savefig(FIGURAS / "gee_whiz_graph.png", dpi=130)
plt.close(fig)
print("Figura guardada: figuras/gee_whiz_graph.png")
print("El crecimiento real es de solo 3%, pero el eje truncado lo hace ver "
      "como si se hubiera triplicado.")

# %% [markdown]
# ### 3b. El promedio bien elegido: media vs mediana
#
# Simulamos el salario de 9 empleados y un directivo con un ingreso mucho
# mayor. La media queda inflada por ese unico valor; la mediana describe
# mejor al empleado tipico.

# %%
# Salarios: 9 empleados similares + 1 directivo con ingreso muy alto
salarios_empleados = rng.normal(15000, 1200, 9).round(0)
salario_directivo = np.array([180000.0])
salarios = np.concatenate([salarios_empleados, salario_directivo])

salarios_df = pd.DataFrame({"salario": salarios})
salarios_df.to_csv(DATOS / "salarios.csv", index=False)

media = salarios.mean()
mediana = np.median(salarios)
print(f"Salarios (n={len(salarios)}): {sorted(salarios.astype(int))}")
print(f"Media (promedio bien elegido para 'impresionar'): ${media:,.0f}")
print(f"Mediana (describe mejor al empleado tipico): ${mediana:,.0f}")
print("El directivo, por si solo, infla la media muy por encima de lo que "
      "gana la mayoria: elegir 'el promedio' correcto importa.")

# %% [markdown]
# ## Conclusiones
#
# - **Gramatica compartida (cultura de datos)**: una tabla con columnas
#   ambiguas y formatos inconsistentes rompe tanto la lectura humana como el
#   procesamiento automatico; un esquema explicito (tipos, unidades, formato
#   ISO) sirve a ambos consumidores.
# - **Correlacion no es causalidad**: ventas de helado y ahogamientos
#   correlacionan fuertemente (r alto) sin que una cause a la otra; ambas
#   responden a una tercera variable, la temperatura.
# - **Como mentir con estadisticas**: el mismo cambio de 3% se ve plano o
#   enorme segun donde se trunque el eje Y, y "el salario promedio" cambia
#   drasticamente segun se use la media o la mediana.
# - La cultura de datos exige elegir la representacion, la grafica y el
#   promedio que **describen honestamente** el dato, no los que mas
#   convencen.
