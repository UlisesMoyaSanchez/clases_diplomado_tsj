# %% [markdown]
# # Clase 02 (Parte II) -- Datos para humanos vs datos para maquinas
#
# Un mismo conjunto de datos se organiza distinto segun quien lo consume.
# En esta practica vamos a:
#
# 1. Tomar un dataset de ventas por region.
# 2. **Para humanos**: generar una grafica y un resumen narrativo (de un vistazo).
# 3. **Para maquinas**: exportar JSON estructurado con un *diccionario de datos*
#    (tipos, unidades y descripcion de cada campo).
# 4. **Herramientas con contrato**: funciones tipadas que un agente podria invocar
#    de forma confiable.
# 5. **Mini-agente por reglas** (sin LLM real): dada una pregunta, elige la
#    herramienta y responde, ilustrando el ciclo percibir -> pensar -> actuar.
#
# Uso:
#     python practica.py
# Genera datasets en datos/ (JSON + diccionario) y una grafica en figuras/.

# %%
# Imports (stdlib y externos)
import json
from pathlib import Path

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

# %% [markdown]
# ## 0. El dato base
#
# Ventas trimestrales por region. Es el MISMO dato que presentaremos de dos
# formas distintas.

# %%
ventas = pd.DataFrame({
    "region": ["GDL", "CDMX", "MTY", "QRO"],
    "ventas": [280000, 180000, 320000, 95000],   # en pesos (MXN)
    "periodo": ["2026-Q1"] * 4,
})
print(ventas)

# %% [markdown]
# ## 1. Datos para HUMANOS: grafica + narrativa
#
# Un humano entiende "de un vistazo" con una grafica y una frase. La imagen
# informa mucho a la persona... pero muy poco a una maquina.

# %%
# Grafica de barras (para el humano)
plt.figure(figsize=(5, 3))
plt.bar(ventas["region"], ventas["ventas"],
        color=["#0094A2", "#FE730C", "#FEB200", "#532587"])
plt.ylabel("ventas (MXN)")
plt.title("Ventas por region (2026-Q1)")
plt.tight_layout()
plt.savefig(FIGURAS / "ventas_humano.png", dpi=130)
plt.close()
print("Figura guardada: figuras/ventas_humano.png")

# %%
# Resumen narrativo (para el humano): generamos la frase a partir del dato
lider = ventas.loc[ventas["ventas"].idxmax()]
total = int(ventas["ventas"].sum())
narrativa = (f"En 2026-Q1, la region lider fue {lider['region']} con "
             f"{int(lider['ventas']):,} MXN. El total vendido fue {total:,} MXN.")
print(narrativa)

# %% [markdown]
# ## 2. Datos para MAQUINAS: JSON + diccionario de datos
#
# Una maquina necesita los valores exactos, tipados y con su significado. No le
# sirve la imagen: necesita estructura, unidades y metadatos (riqueza semantica).

# %%
# Exportamos los registros como JSON estructurado
registros = ventas.to_dict(orient="records")
(DATOS / "ventas.json").write_text(json.dumps(registros, ensure_ascii=True, indent=2))
print("JSON para maquina:")
print(json.dumps(registros, ensure_ascii=True, indent=2))

# %%
# Diccionario de datos (la "capa semantica": que es cada campo)
diccionario = {
    "region": {"tipo": "str", "descripcion": "Clave de la region de ventas"},
    "ventas": {"tipo": "int", "unidad": "MXN", "descripcion": "Ventas del periodo"},
    "periodo": {"tipo": "str", "formato": "AAAA-Qn", "descripcion": "Trimestre"},
}
(DATOS / "ventas_schema.json").write_text(
    json.dumps(diccionario, ensure_ascii=True, indent=2))
print("Diccionario de datos (metadatos):")
print(json.dumps(diccionario, ensure_ascii=True, indent=2))

# %% [markdown]
# ## 3. Herramientas con contrato (lo que consume un agente)
#
# Una herramienta util para un agente declara su contrato: que recibe, que
# devuelve y que significa. Asi el agente la usa de forma confiable.

# %%
# Indexamos por region para las consultas
TABLA = ventas.set_index("region")

def consultar_ventas(region: str) -> dict:
    """Devuelve las ventas de una region.
    Entrada: region (clave, str). Salida: {region, ventas:int(MXN), periodo}.
    """
    fila = TABLA.loc[region]
    return {"region": region, "ventas": int(fila["ventas"]),
            "periodo": fila["periodo"]}

def top_regiones(n: int) -> list:
    """Devuelve las n regiones con mas ventas (lista de dicts ordenada)."""
    top = ventas.sort_values("ventas", ascending=False).head(n)
    return top[["region", "ventas"]].to_dict(orient="records")

def total_ventas() -> dict:
    """Devuelve el total de ventas de todas las regiones."""
    return {"total": int(ventas["ventas"].sum()), "unidad": "MXN"}

print("consultar_ventas('MTY') ->", consultar_ventas("MTY"))
print("top_regiones(2)        ->", top_regiones(2))
print("total_ventas()         ->", total_ventas())

# %% [markdown]
# ## 4. Mini-agente por reglas (percibir -> pensar -> actuar)
#
# Sin un LLM real, un agente sencillo puede: **percibir** la pregunta, **pensar**
# que herramienta usar (aqui por palabras clave) y **actuar** ejecutandola. Es la
# misma idea que un agente LLM, pero con reglas en vez de un modelo.

# %%
# Registro de herramientas disponibles para el agente
HERRAMIENTAS = {
    "consultar_ventas": consultar_ventas,
    "top_regiones": top_regiones,
    "total_ventas": total_ventas,
}

def mini_agente(pregunta: str) -> dict:
    # PERCIBIR: normalizamos la pregunta
    p = pregunta.lower()
    # PENSAR: elegimos la herramienta segun palabras clave
    if "total" in p:
        herramienta, args = "total_ventas", ()
    elif "top" in p or "mejores" in p:
        n = 2  # por defecto
        for token in p.split():
            if token.isdigit():
                n = int(token)
        herramienta, args = "top_regiones", (n,)
    else:
        # buscamos una region conocida en la pregunta
        region = next((r for r in TABLA.index if r.lower() in p), "MTY")
        herramienta, args = "consultar_ventas", (region,)
    # ACTUAR: ejecutamos la herramienta elegida
    resultado = HERRAMIENTAS[herramienta](*args)
    print(f"  [pensar] uso '{herramienta}{args}'  ->  [observar] {resultado}")
    return resultado

# %%
# Probamos el mini-agente con varias preguntas
preguntas = [
    "?`Cuanto vendio MTY?",
    "Dame el top 3 de regiones",
    "?`Cual es el total de ventas?",
]
for q in preguntas:
    print("Pregunta:", q)
    mini_agente(q)

# %% [markdown]
# ## Conclusiones
#
# - El **mismo dato** se presenta distinto segun el consumidor: para el humano,
#   una grafica y una frase; para la maquina, JSON tipado con su diccionario.
# - La **visualizacion** informa al humano pero no a la maquina: el agente
#   necesita valores exactos, estructura y metadatos (capa semantica).
# - Las **herramientas con contrato** (tipos y significado claros) permiten que un
#   agente las use de forma confiable.
# - Un **agente** -- aunque sea por reglas -- percibe, piensa (elige herramienta)
#   y actua; un agente LLM hace lo mismo pero decide con un modelo de lenguaje.
