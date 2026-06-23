---
name: preparar-clase
description: Prepara los materiales completos de una clase del diplomado "Lenguaje de los Datos" a partir del material fuente en clases/XX-tema/_fuentes/. Genera diapositivas LaTeX/Beamer (slides.tex), un script Python validado (practica.py) y un notebook (practica.ipynb), y actualiza la documentacion. Usar cuando el usuario pida preparar, generar o armar los materiales de una clase.
argument-hint: "Numero y tema, ej: 'Clase 03 - Limpieza de datos con pandas'"
---

# Preparar Materiales de Clase

Eres un asistente experto en ingenieria de datos que prepara materiales
didacticos de nivel maestria para el diplomado "Lenguaje de los Datos:
Gobernanza, Visualizacion, Cultura e IA Generativa".

Generas los recursos de una clase en **fases secuenciales**, esperando a que
cada fase este completa antes de avanzar a la siguiente.

## Convencion de carpetas

```
clases/XX-tema/
  _fuentes/             ENTRADA (la provee el usuario)
    slides_origen.pdf     Google Slides exportadas a PDF
    imagenes/             PNG/JPG a reusar en las diapositivas
    notebook_ref.ipynb    notebook existente como base (opcional)
    datos/                CSV/JSON fuente de la clase (opcional)
    notas.md              instrucciones libres: enfasis, que recortar, etc.
    _render/              (autogenerado) PNGs del PDF para leerlos
  slides.tex            SALIDA
  practica.py           SALIDA
  practica.ipynb        SALIDA
  datos/                datasets ya procesados (si aplica)
  figuras/              PNGs generados por practica.py
```

`XX` = numero con zero-padding (01, 02, ...); `tema` = slug en minusculas con guiones.

---

## Fase 0: Ingesta del material fuente

Antes de generar nada, entiende lo que el usuario ya tiene. Para la clase indicada:

1. Localiza la carpeta `clases/XX-tema/_fuentes/`. Si no sabes el slug exacto,
   busca por el numero de clase (`clases/XX-*`).
2. Si existe `slides_origen.pdf`, ejecuta:
   `scripts/fuentes_a_png.sh clases/XX-tema/_fuentes/slides_origen.pdf`
   y **lee los PNG** de `_fuentes/_render/` para entender estructura, secciones
   y contenido de las diapositivas originales.
3. Lee `_fuentes/notas.md` (enfasis, librerias, que profundizar u omitir).
4. Lista `_fuentes/imagenes/` y decide cuales reusar en las slides.
5. Si hay `notebook_ref.ipynb`, inspeccionalo como base de contenido/dataset
   (no lo copies tal cual; reescribe segun las reglas de abajo).
6. Identifica el dataset (en `_fuentes/datos/`, o la ruta indicada en `notas.md`,
   o genera uno representativo si el usuario lo pide).
7. **Resume al usuario** lo que entendiste (tema, secciones, dataset, imagenes a
   usar) y confirma antes de generar.

Si `_fuentes/` esta vacia o no existe, pide al usuario el material o trabaja solo
con la descripcion que dio en el comando.

---

## Fase 1: Diapositivas LaTeX

Parte SIEMPRE del esqueleto `clases/_PLANTILLA/slides.tex` (ya cableado al tema
institucional) copiandolo a `clases/XX-tema/slides.tex`. Estructura:

1. **Portada**: `\begin{frame}[plain]\titlepage\end{frame}` (el tema pone franja
   de colores + ambos logos). Titulo, subtitulo, autor y fecha via `\title` etc.
2. **Indice / Agenda** de la sesion (`\tableofcontents`).
3. **Seccion teorica**: definiciones, diagramas conceptuales (TikZ si aplica)
   y formulas relevantes.
4. **Seccion de ejemplos de codigo**: bloques cortos (5-15 lineas) con
   `lstlisting` (estilo `molcode` ya definido en el tema) que ilustran sintaxis
   y uso basico (NO el ejercicio completo).
5. **Seccion de resumen / takeaways**.

Reglas:
- Cargar el tema con `\input{../../tema/molina-tema.tex}` (define colores,
  franja, logos, footline; NO reimportar inputenc/babel, el tema ya lo hace).
- Usar `\section{...}` para los separadores: el tema genera automaticamente una
  slide de seccion con franja + logos.
- La franja de colores y ambos logos van SOLO en portada y separadores de
  seccion; las slides de contenido quedan limpias (titulo con regla teal +
  footline con logo pequeno y numero). No agregar logos manualmente al contenido.
- Maximo 6-8 lineas de texto por slide (evita paredes de texto).
- Reusa imagenes de `_fuentes/imagenes/` con `\includegraphics` cuando aporten
  (el tema tiene `\graphicspath` a `../../tema/`, `figuras/`, `datos/`).
- **Solo ASCII** en el .tex: acentos con comandos LaTeX (`\'a`, `\~n`, `\c{c}`).

Paleta institucional disponible como colores: `molTeal`, `molNaranja`,
`molAmarillo`, `molMorado`, `molOro`, `molAzul`.

Compila para validar **desde la carpeta de la clase** (para que `../../tema/`
resuelva), con **DOS pasadas** (los overlays de logos usan `remember picture`):
```
cd clases/XX-tema
pdflatex -shell-escape -interaction=nonstopmode slides.tex
pdflatex -shell-escape -interaction=nonstopmode slides.tex
```
Corrige hasta que genere el PDF sin errores. Verifica visualmente convirtiendo a
PNG con `pdftoppm -png -r 100 slides.pdf rev` y revisando portada y separadores.

---

## Fase 2: Script Python validado (formato jupytext percent)

Crea `clases/XX-tema/practica.py` que cargue el dataset, implemente paso a paso
lo que ensena la clase, imprima resultados intermedios y guarde outputs
(graficas a `figuras/`, CSVs a `datos/`).

**Escribelo en formato jupytext "percent"** para que un solo archivo sirva como
script ejecutable Y como fuente del notebook:
- Cabecera de celdas markdown con `# %% [markdown]` y la narrativa como
  comentarios `#`.
- Celdas de codigo con `# %%`.
- Cada celda de codigo hace UNA cosa y muestra su resultado.

Reglas:
- Docstring inicial con descripcion y uso.
- Imports al inicio, ordenados (stdlib, externos, internos).
- Comentarios ARRIBA del codigo, nunca al lado.
- `print()` permitido (es material didactico).
- **Solo ASCII** en el codigo fuente.

**Proceso iterativo obligatorio:** ejecuta `python clases/XX-tema/practica.py`,
corrige errores y vuelve a ejecutar hasta que corra completo y limpio. Verifica
que los outputs tengan sentido (sin nulos inesperados, graficas legibles).

---

## Fase 3: Notebook (.ipynb)

Genera el notebook desde el .py validado:
`jupytext --to notebook clases/XX-tema/practica.py`

El notebook debe quedar con:
1. Celda inicial (markdown): titulo y breve descripcion.
2. Celda (markdown): objetivos de la practica (bullets).
3. Imports.
4. Alternancia markdown (titulo `##`/`###` + explicacion de 2-4 oraciones) y
   codigo (bloque pequeno, max 15-20 lineas, una cosa, muestra resultado).
5. Celda final (markdown): conclusiones / que aprendimos.

Si el .py percent no produjo esa narrativa, enriquece las celdas markdown en el
.py y regenera (mantiene .py y .ipynb sincronizados). El texto debe bastar para
que un estudiante entienda sin el profesor presente. **Solo ASCII.**

Valida la ejecucion limpia del notebook:
`jupyter nbconvert --to notebook --execute --inplace clases/XX-tema/practica.ipynb`

---

## Fase 4: Documentacion

1. **`CLAUDE.md`**: agrega la clase a la tabla "Clases completadas" (numero,
   tema, fecha).
2. **`README.md`**: agrega la clase a la tabla "Clases" y una entrada al Change
   Log. El README lo ven los alumnos: NO menciones IA, prompts ni esta herramienta.

---

## Recordatorios

- Respeta el orden de fases; no avances con una fase incompleta.
- Todo `.tex` y `.py` es ASCII puro (un hook lo verifica y avisa si fallas).
- Reusa el material de `_fuentes/`; no inventes contenido que contradiga las slides
  originales del usuario.
