# Notas - Clase 05: Cultura de datos

Instrucciones libres para el skill `preparar-clase`. Se ira completando con
mas temas antes de correr `/preparar-clase Clase 05 - Cultura de datos`.

## Temas a cubrir

### 1. Gramatica de los datos: ejemplos para humanos vs para maquinas

- Retomar la gramatica de los datos (ver Clase 02: tipos por naturaleza y
  por estructura, formato tidy) y la distincion datos-para-humanos vs
  datos-para-maquinas (ver Clase 02b) pero enmarcada como un problema de
  **cultura de datos**: para que una organizacion tome decisiones con datos,
  necesita una gramatica compartida y consistente, no solo entre personas
  sino entre personas y sistemas.
- Ejemplos a usar (mismo dato, dos representaciones):
  - Datos para humanos: una grafica o tabla resumen, lenguaje natural,
    unidades y formato legibles (fechas "22 de julio de 2026", nombres
    completos, redondeo).
  - Datos para maquinas: el mismo dato en JSON/CSV estructurado, con
    tipos explicitos, claves normalizadas, diccionario de datos o schema
    (ISO 8601 para fechas, codigos en vez de texto libre, unidades en
    metadatos).
  - Mostrar como una gramatica de datos deficiente (columnas ambiguas,
    formatos inconsistentes, mezclar texto libre con codigos) rompe tanto
    la lectura humana como el procesamiento automatico, y como eso es un
    sintoma de falta de cultura de datos en la organizacion.

<!-- Agregar mas temas de Cultura de datos aqui: alfabetizacion de datos,
     adopcion organizacional, toma de decisiones basada en datos, etc. -->
