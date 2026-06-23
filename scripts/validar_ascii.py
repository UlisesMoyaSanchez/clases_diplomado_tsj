#!/usr/bin/env python3
"""Hook PostToolUse: valida que los archivos .tex y .py sean ASCII-only.

Claude Code invoca este script tras cada Write/Edit y le pasa por stdin un
JSON con la informacion de la herramienta. Si el archivo modificado termina
en .tex o .py y contiene caracteres no-ASCII, el script sale con codigo 2 y
escribe en stderr las lineas ofensivas; Claude Code muestra ese mensaje como
retroalimentacion para que se corrija (regla ASCII-only del flujo de clase).

Cualquier otro archivo, o un .tex/.py limpio, sale con codigo 0 (sin ruido).
"""
import json
import sys


# Solo vigilamos los fuentes que deben ser ASCII puro.
EXTENSIONES_VIGILADAS = (".tex", ".py")


def ruta_archivo(payload):
    """Extrae el file_path del JSON del hook (Write y Edit lo traen igual)."""
    tool_input = payload.get("tool_input", {})
    return tool_input.get("file_path", "")


def lineas_no_ascii(texto):
    """Devuelve [(num_linea, contenido)] de las lineas con bytes no-ASCII."""
    problemas = []
    for i, linea in enumerate(texto.splitlines(), start=1):
        if any(ord(c) > 127 for c in linea):
            problemas.append((i, linea))
    return problemas


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Sin payload valido no hay nada que validar.
        return 0

    ruta = ruta_archivo(payload)
    if not ruta.endswith(EXTENSIONES_VIGILADAS):
        return 0

    try:
        with open(ruta, "r", encoding="utf-8") as fh:
            contenido = fh.read()
    except OSError:
        return 0

    problemas = lineas_no_ascii(contenido)
    if not problemas:
        return 0

    print(
        f"ASCII-only: {ruta} contiene {len(problemas)} linea(s) con "
        "caracteres no-ASCII. Reemplazalos por comandos LaTeX "
        r"(\'a, \~n, \c{c}) o ASCII equivalente:",
        file=sys.stderr,
    )
    for num, linea in problemas[:20]:
        print(f"  L{num}: {linea}", file=sys.stderr)
    if len(problemas) > 20:
        print(f"  ... y {len(problemas) - 20} mas", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
