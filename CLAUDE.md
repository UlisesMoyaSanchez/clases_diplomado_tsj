# CLAUDE.md

Guia para Claude Code en este repositorio. El proyecto produce los materiales del
diplomado "Lenguaje de los Datos: Gobernanza, Visualizacion, Cultura e IA Generativa".

## Como preparar una clase

Comando: `/preparar-clase Clase XX - <tema>`

El skill esta en `.claude/skills/preparar-clase/SKILL.md` y orquesta 4 fases:
0. Ingesta del material fuente, 1. slides.tex (Beamer), 2. practica.py validado,
3. practica.ipynb, 4. documentacion.

## Convencion de carpetas

```
clases/XX-tema/
  _fuentes/            ENTRADA que provee el usuario:
    slides_origen.pdf    Google Slides exportadas a PDF
    imagenes/            PNG/JPG a reusar
    notebook_ref.ipynb   notebook existente como base (opcional)
    datos/               CSV/JSON fuente (opcional)
    notas.md             instrucciones libres
    _render/             (autogenerado) PNGs del PDF
  slides.tex           SALIDA
  practica.py          SALIDA (formato jupytext percent)
  practica.ipynb       SALIDA
  datos/  figuras/     datasets procesados y graficas generadas
```

`XX` = numero con zero-padding; `tema` = slug en minusculas con guiones.

## Tema visual institucional

Las diapositivas usan el tema compartido en `tema/`:
- `tema/molina-tema.tex`: tema Beamer (paleta, franja de colores con TikZ, logos,
  portada, separadores de seccion, footline). Se carga con
  `\input{../../tema/molina-tema.tex}` desde `clases/XX-tema/slides.tex`.
- `tema/logo_mario_molina.png` y `tema/logo_TSJ.png` (este ultimo es el renombre
  de `logos/logo_TSJpng`, que venia sin extension valida).

Paleta (muestreada del master): teal `#0094A2`, naranja `#FE730C`, amarillo
`#FEB200`, morado `#532587`. Disponibles como `molTeal`, `molNaranja`,
`molAmarillo`, `molMorado`, `molOro`, `molAzul`.

Franja + logos van solo en portada (`\titlepage`) y separadores (`\section{}`);
el contenido queda limpio. **Compilar SIEMPRE desde `clases/XX-tema/`** (rutas
`../../tema/`) y con **DOS pasadas** de pdflatex (overlays `remember picture`).

## Reglas clave

- Los `.tex` y `.py` deben ser **ASCII puro**. Un hook PostToolUse
  (`scripts/validar_ascii.py`, registrado en `.claude/settings.json`) avisa si no.
- `practica.py` se escribe en formato **jupytext percent** (`# %%`, `# %% [markdown]`)
  para que el mismo archivo se ejecute y genere el notebook sincronizado.
- El `README.md` lo ven los alumnos: NO mencionar IA, prompts ni herramientas.
- Spanish de babel requiere `texlive-lang-spanish`. El tema cae a english si no
  esta instalado. Para activarlo: `sudo apt-get install texlive-lang-spanish`.

## Scripts auxiliares

- `scripts/fuentes_a_png.sh <pdf>` : convierte el PDF de slides a PNG en `_fuentes/_render/`.
- `scripts/validar_ascii.py` : hook de validacion ASCII (no se invoca a mano).

## Prerrequisitos del entorno

LaTeX (pdflatex + beamer + pygmentize para minted), Python con pandas, matplotlib,
jupytext y nbconvert. Conversion de PDF con pdftoppm.

## Comandos de validacion

```
pdflatex -shell-escape -interaction=nonstopmode slides.tex
python clases/XX-tema/practica.py
jupytext --to notebook clases/XX-tema/practica.py
jupyter nbconvert --to notebook --execute --inplace clases/XX-tema/practica.ipynb
```

## Clases completadas

| # | Tema | Fecha |
|---|------|-------|
| 01 | Motivacion: los datos en el corazon de la IA | 2026-06-22 |
