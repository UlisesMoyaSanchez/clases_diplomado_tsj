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

### 2. Correlacion no es causalidad

- Idea central: dos variables pueden moverse juntas por azar, por una
  tercera variable oculta (variable confusora), o por causalidad inversa,
  sin que una cause a la otra. Una cultura de datos madura exige distinguir
  esto antes de tomar decisiones o publicar conclusiones.
- Ejemplos a usar:
  - Venta de helados y muertes por ahogamiento: ambas suben en verano; la
    variable oculta es la temperatura/epoca del anio, no que el helado
    cause ahogamientos.
  - Numero de cigueñas y tasa de natalidad en algunas regiones de Europa:
    correlacion historica famosa, sin relacion causal (confundida con
    ruralidad/tamano de poblacion).
  - Correlaciones espurias tipo "Spurious Correlations" de Tyler Vigen
    (p.ej. consumo de queso mozzarella per capita vs. numero de doctorados
    en ingenieria civil en EE.UU.): sirven como ejemplo comico de que con
    suficientes series de tiempo, siempre aparecen correlaciones altas sin
    ningun vinculo causal.
  - Tamano del zapato y habilidad de lectura en ninos: ambas correlacionan
    con la edad (variable confusora), no una con la otra.
  - Mencionar brevemente que para hablar de causalidad se necesitan
    diseños como experimentos controlados/aleatorizados, o metodos de
    inferencia causal, no solo observar correlacion en datos historicos.

### 3. Ejemplos del libro "Como mentir con estadisticas" (Darrell Huff)

- Contexto: libro clasico (1954) sobre como graficas y estadisticas mal
  usadas -intencional o no- distorsionan la percepcion; conecta
  directamente con cultura de datos porque exige escepticismo y
  alfabetizacion estadistica en quien consume los datos, no solo en quien
  los produce.
- Ejemplos/capitulos a retomar:
  - "La muestra con sesgo incorporado": encuestas o estudios con muestras
    no representativas (p.ej. encuestas por correo o telefonicas que solo
    llegan a cierto grupo socioeconomico) presentadas como si
    representaran a toda la poblacion.
  - "El promedio bien elegido": usar media, mediana o moda segun cual
    favorezca el argumento (ej. "salario promedio" de una empresa inflado
    por sueldos de directivos, cuando la mediana da un cuadro mas realista
    del empleado tipico).
  - "La grafica que impresiona" (gee-whiz graph): truncar el eje Y o
    exagerar la escala para que un cambio pequeno (ej. 3 %) se vea como un
    crecimiento enorme.
  - Pictogramas engañosos: usar iconos donde para representar "el doble"
    se duplica la altura Y el ancho de la figura, haciendo que el area se
    vea 4 veces mayor en vez de 2 veces.
  - "Post Hoc Rides Again" (capitulo dedicado justamente a correlacion vs
    causalidad): puede usarse como puente directo con el tema anterior.
  - "Cifras semi-adjuntas" (semi-attached figures): responder una pregunta
    distinta a la que se hizo y presentarla como si respondiera la
    original (ej. "9 de cada 10 dentistas recomiendan..." sin aclarar
    la pregunta exacta o el tamano de muestra).
  - Idea de cierre: ensenar estas trampas no para manipular, sino para que
    los alumnos las reconozcan como consumidores y las eviten como
    productores de datos -esa es la cultura de datos que se busca.

<!-- Agregar mas temas de Cultura de datos aqui: alfabetizacion de datos,
     adopcion organizacional, toma de decisiones basada en datos, etc. -->
