#!/usr/bin/env bash
# fuentes_a_png.sh
# Convierte el PDF de slides de origen (exportado de Google Slides) en
# imagenes PNG, una por pagina, para que Claude pueda "ver" las diapositivas.
#
# Uso:
#   scripts/fuentes_a_png.sh clases/01-tema/_fuentes/slides_origen.pdf
#
# Salida: clases/01-tema/_fuentes/_render/slide-01.png, slide-02.png, ...
set -euo pipefail

PDF="${1:-}"
if [[ -z "$PDF" ]]; then
  echo "Uso: $0 <ruta-al-pdf>" >&2
  exit 1
fi
if [[ ! -f "$PDF" ]]; then
  echo "No existe el PDF: $PDF" >&2
  exit 1
fi

DIR="$(dirname "$PDF")"
OUT="$DIR/_render"
mkdir -p "$OUT"

# -r 110: resolucion legible sin generar archivos enormes.
# -png: formato de salida. El prefijo genera slide-01.png, slide-02.png, ...
pdftoppm -png -r 110 "$PDF" "$OUT/slide"

N="$(ls -1 "$OUT"/slide-*.png 2>/dev/null | wc -l)"
echo "OK: $N PNG generados en $OUT"
