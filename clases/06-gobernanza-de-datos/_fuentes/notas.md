# Notas - Clase 06: Gobernanza de datos

Instrucciones libres para el skill `preparar-clase`. Se ira completando con
mas temas antes de correr `/preparar-clase Clase 06 - Gobernanza de datos`.

## Temas a cubrir

### 1. Que es gobernanza de datos (marco conceptual breve)

- Definicion: el conjunto de politicas, roles, procesos y estandares que
  garantizan que los datos de una organizacion sean confiables, seguros,
  consistentes y usables -quien puede acceder, quien es dueno, que calidad
  deben cumplir, y como se auditan.
- Pilares clave a mencionar: propiedad de los datos (data ownership/data
  stewardship), calidad de datos, seguridad y control de acceso, catalogo y
  linaje (metadata/lineage), cumplimiento normativo (GDPR, LFPDPPP en
  Mexico), ciclo de vida (conecta con Clases 03-04).

### 2. Casos de uso donde fallo la gobernanza de datos

- **Equifax (2017)**: brecha que expuso datos de 147 millones de personas;
  fallo de gobernanza en la asignacion de responsabilidad de parchar una
  vulnerabilidad conocida (nadie tenia claro quien era el dueno de esa
  responsabilidad) -ejemplo de falta de ownership y de proceso de gestion
  de vulnerabilidades.
- **Cambridge Analytica / Facebook (2018)**: datos de ~87 millones de
  usuarios recolectados y reutilizados fuera del consentimiento original
  por falta de controles sobre como terceros (apps) accedian y reusaban
  datos -fallo de gobernanza de consentimiento y de acceso de terceros.
- **Danske Bank - escandalo de lavado de dinero en su sucursal de Estonia
  (2007-2015)**: ~200 mil millones de euros en transacciones sospechosas
  no detectadas por falta de gobernanza/integracion de datos entre
  sistemas de monitoreo AML y falta de estandares comunes -ejemplo de como
  la fragmentacion de datos sin gobernanza central oculta senales de
  riesgo.
- **NHS National Programme for IT, Reino Unido (2002-2011)**: programa de
  ~12 mil millones de libras cancelado en gran parte por falta de
  estandares de datos compartidos entre hospitales y falta de gobernanza
  unificada del programa -ejemplo de gobernanza a nivel de politica
  publica.
- **Uber "God View" (2014-2016)**: empleados con acceso sin restriccion a
  ubicacion en tiempo real de cualquier usuario, usado para rastrear a
  periodistas y parejas sentimentales -fallo de gobernanza de acceso
  (ausencia de control de acceso basado en roles y de auditoria de uso).
- Cierre de la seccion: en todos los casos el problema no fue "falta de
  tecnologia" sino falta de reglas claras sobre quien es dueno, quien
  puede acceder, y como se audita -el nucleo de la gobernanza de datos.

### 3. Tecnicas para evaluar el exito de la gobernanza de datos

- **Dimensiones de calidad de datos** (marco DAMA-DMBOK): completitud,
  exactitud, consistencia, oportunidad (timeliness), unicidad -medibles
  como % de registros que cumplen cada dimension.
- **Cobertura de stewardship**: % de activos/tablas de datos criticos con
  un dueno (data owner) y un custodio (data steward) formalmente asignado.
- **Cobertura de linaje y catalogo**: % de datasets documentados en un
  catalogo de datos con su origen, transformaciones y significado (data
  dictionary).
- **Metricas de incidentes**: numero de incidentes de seguridad/calidad de
  datos por periodo, tiempo medio de deteccion (MTTD) y de remediacion
  (MTTR).
- **Auditorias de control de acceso**: revisiones periodicas de
  privilegios (principio de minimo privilegio), % de accesos revocados a
  tiempo al cambiar de rol o salir de la organizacion.
- **Cumplimiento normativo**: resultados de auditorias regulatorias (GDPR,
  LFPDPPP), multas evitadas, certificaciones (ISO/IEC 38505, ISO 8000).
- **Modelos de madurez de gobernanza de datos**: por ejemplo DCAM (Data
  Management Capability Assessment Model) o el modelo de madurez de
  Gartner, que ubican a la organizacion en niveles (inicial, gestionado,
  definido, optimizado) mediante un cuestionario/scorecard.
- **Costo de la mala calidad de datos (COPQ - cost of poor quality)**:
  estimar cuanto cuesta a la organizacion la mala calidad (retrabajos,
  decisiones erroneas) como metrica indirecta de exito al reducirse en el
  tiempo.
- Cierre: ninguna tecnica sola basta; se recomienda un scorecard que
  combine unas cuantas metricas de cada categoria y se revise
  periodicamente (trimestral/anual).

<!-- Agregar mas temas de Gobernanza de datos aqui si aplica. -->
