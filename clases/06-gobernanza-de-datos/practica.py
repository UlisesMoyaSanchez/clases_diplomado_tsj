# %% [markdown]
# # Clase 06 -- Gobernanza de datos
#
# Practica de cuatro ideas centrales de la gobernanza de datos:
#
# 1. **Cobertura de stewardship**: un catalogo de datos simulado y el
#    porcentaje de activos con dueno/custodio asignado.
# 2. **Calidad de datos (DAMA-DMBOK)**: un dataset con nulos, duplicados y
#    formatos inconsistentes, midiendo completitud, unicidad y consistencia.
# 3. **Auditoria de accesos**: un log de accesos simulado para detectar
#    accesos que debieron revocarse (caso Uber "God View").
# 4. **Scorecard de madurez**: combinamos las metricas anteriores en un
#    nivel de madurez (inicial/gestionado/definido/optimizado).
#
# Uso:
#     python practica.py
# Genera datasets en datos/ y graficas en figuras/.

# %%
# Imports (stdlib y externos)
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

rng = np.random.default_rng(6)

# %% [markdown]
# ## 1. Cobertura de stewardship: el catalogo de datos
#
# Un catalogo simulado con activos de datos criticos, y si cada uno tiene un
# dueno (owner) y un custodio (steward) asignados. Sin ambos, un incidente
# (como Equifax) no tiene un responsable claro que reaccione a tiempo.

# %%
# Catalogo de activos: algunos con dueno/custodio, otros sin ninguno
catalogo = pd.DataFrame({
    "activo": ["clientes", "pagos", "inventario", "logs_acceso",
               "encuestas", "modelos_ml", "reportes_financieros"],
    "dueno": ["Ventas", "Finanzas", "Operaciones", None,
              "Marketing", None, "Finanzas"],
    "custodio": ["TI", "TI", "TI", "TI",
                 None, "Ciencia de Datos", "TI"],
})
catalogo.to_csv(DATOS / "catalogo_stewardship.csv", index=False)
print("Catalogo de datos:")
print(catalogo.to_string(index=False))

# %%
# Cobertura de stewardship: % de activos con dueno Y custodio asignados
catalogo["cubierto"] = catalogo["dueno"].notna() & catalogo["custodio"].notna()
cobertura_stewardship = catalogo["cubierto"].mean() * 100
print(f"\nActivos con dueno y custodio asignados: "
      f"{catalogo['cubierto'].sum()} de {len(catalogo)}")
print(f"Cobertura de stewardship: {cobertura_stewardship:.1f} %")
print("Los activos sin cobertura completa (logs_acceso, encuestas, "
      "modelos_ml) son justamente donde un incidente tardaria mas en "
      "detectarse y resolverse, por falta de un responsable claro.")

# %% [markdown]
# ## 2. Calidad de datos (DAMA-DMBOK)
#
# Un dataset de clientes con problemas tipicos: nulos, registros duplicados
# y formatos de fecha/telefono inconsistentes. Medimos completitud, unicidad
# y consistencia por columna.

# %%
# Dataset sintetico de clientes con problemas de calidad tipicos
clientes = pd.DataFrame({
    "id_cliente": [1, 2, 3, 4, 5, 5, 6, 7],
    "nombre": ["Ana Ruiz", "Luis Perez", None, "Marta Ortiz",
               "Jose Diaz", "Jose Diaz", "Rita Soto", None],
    "telefono": ["33-1234-5678", "3312345679", "(33) 1234-5680",
                  None, "33.1234.5682", "33.1234.5682",
                  "3312345683", "33-1234-5684"],
    "fecha_alta": ["2024-01-10", "10/02/2024", "2024-03-05",
                    "05-abr-2024", "2024-05-01", "2024-05-01",
                    None, "2024-07-20"],
})
clientes.to_csv(DATOS / "clientes_calidad.csv", index=False)
print("Dataset de clientes (con problemas de calidad):")
print(clientes.to_string(index=False))

# %%
# Completitud: % de valores no nulos por columna
completitud = clientes.notna().mean() * 100
print("\nCompletitud por columna (%):")
print(completitud.round(1))

# %%
# Unicidad: % de registros unicos (sin duplicar id_cliente)
duplicados = clientes.duplicated(subset=["id_cliente"]).sum()
unicidad = (1 - duplicados / len(clientes)) * 100
print(f"\nRegistros duplicados (mismo id_cliente): {duplicados}")
print(f"Unicidad: {unicidad:.1f} %")

# %%
# Consistencia de formato: cuantos patrones distintos usa cada columna
patron_telefono = clientes["telefono"].dropna().str.replace(
    r"[\d]", "#", regex=True)
patron_fecha = clientes["fecha_alta"].dropna().str.replace(
    r"[0-9]+", "#", regex=True)
print(f"\nFormatos distintos de telefono encontrados: "
      f"{patron_telefono.nunique()} -> {sorted(patron_telefono.unique())}")
print(f"Formatos distintos de fecha encontrados: "
      f"{patron_fecha.nunique()} -> {sorted(patron_fecha.unique())}")
print("Varios formatos para el mismo campo es un sintoma de falta de "
      "consistencia: la misma informacion se ve distinta segun quien la "
      "capturo.")

# %% [markdown]
# ## 3. Auditoria de accesos: el caso "God View"
#
# Un log de accesos simulado con usuarios, roles, recursos y fecha de baja
# de la organizacion (si aplica). Buscamos accesos que debieron revocarse:
# empleados que ya no estan en la organizacion pero siguen figurando con
# acceso activo a un recurso sensible.

# %%
# Log de accesos: algunos usuarios ya dados de baja, con acceso activo
accesos = pd.DataFrame({
    "usuario": ["ana", "luis", "marta", "jose", "rita", "carlos"],
    "rol": ["soporte", "ventas", "ex_empleado", "operaciones",
            "ex_empleado", "administrador"],
    "recurso": ["ubicacion_tiempo_real", "crm", "ubicacion_tiempo_real",
                 "inventario", "logs_acceso", "ubicacion_tiempo_real"],
    "fecha_baja": [None, None, "2026-03-01", None, "2026-05-15", None],
    "acceso_activo": [True, True, True, True, True, True],
})
accesos.to_csv(DATOS / "log_accesos.csv", index=False)
print("Log de accesos:")
print(accesos.to_string(index=False))

# %%
# Accesos que debieron revocarse: dados de baja pero con acceso activo
accesos["debio_revocarse"] = accesos["fecha_baja"].notna() & accesos["acceso_activo"]
pendientes = accesos[accesos["debio_revocarse"]]
print(f"\nAccesos que debieron revocarse: {len(pendientes)} de {len(accesos)}")
print(pendientes[["usuario", "rol", "recurso", "fecha_baja"]].to_string(index=False))
print("\nEsto es exactamente el patron detras del caso Uber 'God View': "
      "acceso sin control de roles (RBAC) ni auditoria periodica de "
      "revocacion, aplicado aqui a ex-empleados con acceso a un recurso "
      "sensible (ubicacion en tiempo real).")

# %% [markdown]
# ## 4. Scorecard de madurez de gobernanza
#
# Combinamos tres metricas -cobertura de stewardship, calidad promedio y
# % de accesos correctamente revocados- en un nivel de madurez simple, con
# reglas de umbral (inicial/gestionado/definido/optimizado).

# %%
# Metrica de calidad promedio: completitud, unicidad y consistencia (0-100)
completitud_prom = completitud.mean()
consistencia_aprox = 100 - (
    (patron_telefono.nunique() - 1) + (patron_fecha.nunique() - 1)
) * 10  # cada formato extra resta 10 puntos
calidad_promedio = np.mean([completitud_prom, unicidad, consistencia_aprox])

# Metrica de acceso: % de accesos que SI se revocaron a tiempo
revocacion_correcta = (1 - accesos["debio_revocarse"].mean()) * 100

metricas = pd.DataFrame({
    "metrica": ["Cobertura de stewardship", "Calidad promedio de datos",
                "Revocacion de accesos a tiempo"],
    "valor": [cobertura_stewardship, calidad_promedio, revocacion_correcta],
})
print("Metricas del scorecard:")
print(metricas.round(1).to_string(index=False))

# %%
# Nivel de madurez con reglas de umbral simples sobre el promedio general
score_general = metricas["valor"].mean()


def nivel_madurez(score):
    if score < 40:
        return "inicial"
    if score < 65:
        return "gestionado"
    if score < 85:
        return "definido"
    return "optimizado"


nivel = nivel_madurez(score_general)
print(f"\nScore general: {score_general:.1f} / 100")
print(f"Nivel de madurez de gobernanza de datos: {nivel.upper()}")

# %%
# Graficamos el scorecard como barras horizontales
fig, ax = plt.subplots(figsize=(6.5, 3.5))
colores = ["#0094A2", "#FE730C", "#532587"]
ax.barh(metricas["metrica"], metricas["valor"], color=colores)
ax.set_xlim(0, 100)
ax.set_xlabel("Valor (%)")
ax.set_title(f"Scorecard de gobernanza de datos -- nivel: {nivel}")
fig.tight_layout()
fig.savefig(FIGURAS / "scorecard_gobernanza.png", dpi=130)
plt.close(fig)
print("Figura guardada: figuras/scorecard_gobernanza.png")

# %% [markdown]
# ## Conclusiones
#
# - **Stewardship**: sin un dueno y un custodio asignados a cada activo, un
#   incidente (como Equifax) no tiene quien responda a tiempo; en nuestro
#   catalogo, solo una fraccion de los activos tiene cobertura completa.
# - **Calidad de datos**: nulos, duplicados y formatos inconsistentes
#   (telefono, fecha) bajan la completitud, la unicidad y la consistencia
#   medibles de un dataset, sin que haga falta ningun analisis complejo para
#   detectarlos.
# - **Auditoria de accesos**: un log simple revela accesos que debieron
#   revocarse -el mismo patron que produjo el caso Uber "God View"- y que
#   una revision periodica de privilegios habria detectado.
# - **Scorecard de madurez**: ninguna metrica sola describe la gobernanza de
#   una organizacion; combinarlas en un scorecard simple ubica a la
#   organizacion en un nivel de madurez y senala donde enfocar el esfuerzo.
