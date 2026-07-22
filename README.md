# Diplomado: Lenguaje de los Datos

Materiales del diplomado **"Lenguaje de los Datos: Gobernanza, Visualizacion,
Cultura e IA Generativa"**.

Cada clase incluye sus diapositivas, un script de practica, un notebook
ejecutable y un examen de opcion multiple, organizados en `clases/XX-tema/`.

## Clases

| # | Tema | Materiales |
|---|------|-----------|
| 01 | Motivacion: los datos en el corazon de la IA | [carpeta](clases/01-motivacion/) |
| 02 | Tipos de datos y gramatica de los datos | [carpeta](clases/02-tipos-y-gramatica/) |
| 02b | Datos para humanos vs datos para maquinas | [carpeta](clases/02b-datos-humanos-vs-maquinas/) |
| 03 | Ciclo de vida de los datos (Parte I): captura y almacenamiento | [carpeta](clases/03-ciclo-vida-i/) |
| 04 | Ciclo de vida de los datos (Parte II): seguridad, analisis y archivado | [carpeta](clases/04-ciclo-vida-ii/) |
| 05 | Cultura de datos | [carpeta](clases/05-cultura-de-datos/) |
| 06 | Gobernanza de datos | [carpeta](clases/06-gobernanza-de-datos/) |

## Estructura

```
clases/
  XX-tema/
    slides.tex       Diapositivas de la sesion
    practica.py      Script de la practica
    practica.ipynb   Notebook ejecutable
    examen.tex       Examen de opcion multiple
    datos/           Datasets utilizados
    figuras/         Graficas generadas
```

## Change Log

- Clase 06 "Gobernanza de datos": diapositivas, practica, notebook y examen.
  Pilares de la gobernanza (propiedad de los datos, calidad, seguridad y
  control de acceso, catalogo y linaje, cumplimiento normativo), casos reales
  donde fallo por falta de gobernanza (Equifax, Cambridge Analytica, Danske
  Bank, NHS National Programme for IT, Uber) y tecnicas para evaluar su
  exito (dimensiones de calidad, cobertura de stewardship, auditorias de
  acceso, modelos de madurez, costo de la mala calidad de datos). La
  practica arma un catalogo con cobertura de stewardship, mide calidad de
  datos por columna, audita un log de accesos y combina todo en un
  scorecard de madurez.
- Clase 05 "Cultura de datos": diapositivas, practica, notebook y examen.
  Gramatica de datos compartida entre personas y sistemas (con ejemplos de
  datos para humanos vs para maquinas), correlacion vs causalidad (helados y
  ahogamientos, ciguenas y natalidad, correlaciones espurias) y trampas
  estadisticas clasicas (muestra sesgada, promedio bien elegido, grafica con
  eje truncado, pictogramas enganosos, cifras semi-adjuntas). La practica
  contrasta representaciones de un mismo dato, simula variables con una causa
  comun y compara un eje honesto contra uno truncado, y la media contra la
  mediana en salarios con un valor atipico.
- Clase 02b "Datos para humanos vs datos para maquinas": diapositivas, practica,
  notebook y examen. Diferencia entre datos para consumo humano (visualizacion,
  narrativa) y para maquinas (estructura, metadatos, contratos); los marcos AI
  for Data y Data for AI; que son los agentes LLM (antecedentes y ciclo
  percibir-pensar-actuar) y los retos del acceso a datos. La practica presenta
  el mismo dato para humanos (grafica) y para maquinas (JSON + diccionario), con
  herramientas de contrato y un mini-agente por reglas.
- Clase 04 "Ciclo de vida de los datos (Parte II)": diapositivas, practica,
  notebook y examen. Etapas de acceso/seguridad (cifrado en reposo y transito,
  inyeccion SQL, minimos privilegios, amenazas de IA), de
  limpieza/analisis/visualizacion (EDA, outliers con IQR, correlacion y el
  cuarteto de Anscombe) y de archivado/eliminacion (almacenamiento frio,
  derechos ARCO, GDPR). La practica anonimiza datos personales con hashing,
  hace un EDA con deteccion de outliers, demuestra Anscombe y atiende una baja
  ARCO archivando el resto con metadatos.
- Clase 03 "Ciclo de vida de los datos (Parte I)": diapositivas, practica,
  notebook y examen. Etapas de creacion/captura (censo, encuesta, sondeo,
  sensores, datos administrativos, big data y sus 5 V) y de
  transmision/almacenamiento (regla 3-2-1, ETL, data lake vs data warehouse,
  data pipeline y orquestacion con Airflow). La practica simula la captura con
  errores, estima intervalos de confianza, arma un ETL hacia una bodega SQLite
  y compara formatos de almacenamiento.
- Clase 02 "Tipos de datos y gramatica de los datos": diapositivas, practica,
  notebook y examen. Tipos por naturaleza (cualitativo/cuantitativo,
  nominal/ordinal) y por estructura (estructurado/semi/no estructurado),
  representacion numerica de imagenes, audio, texto y grafos, gramatica tidy
  (de formato wide a tidy con pandas) y malas practicas de hoja de calculo con
  casos reales (Reinhart-Rogoff, Public Health England, nombres de genes).
- Clase 01 "Motivacion: los datos en el corazon de la IA": diapositivas,
  practica y notebook. Recorrido historico IA/ML/DL, datos vs informacion,
  limites de la programacion clasica (ajedrez, Go), taxonomia del ML y retos
  de los datos a gran escala.
- Estructura inicial del repositorio de clases.
