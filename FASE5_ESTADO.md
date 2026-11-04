# FASE 5 — Estado (Reportes PDF/Excel)

## Etapa 1 · Motor PDF (LaTeX) ✅
Ver PROJECT_STATUS.md. `generate_pdf(project_id, kind)` en `app/exporters/pdf_report.py`.

## Etapa 1b · Rediseño editorial de los informes ✅
Referencia de estilo: PDF adjunto (`Info_1.pdf`; el texto lo nombraba `Info_2.pdf`): bandas rosadas con título rojo, viñetas cuadradas, tablas con cabecera roja, memoria y anexos.
Copia de seguridad previa: `_backup_fase5/` (plantillas v1, pdf_report.py, report_context.py).

**Nuevos**
- `templates/latex/common/estilo.tex.j2` (tipografía Palatino + Helvetica, microtype, colores, títulos, tablas, cajas)
- `templates/latex/common/portada.tex.j2` (portada TikZ), `macros.tex.j2` (tabla, kvtabla, figura, memoria), `anexo_fotos.tex.j2`
- `app/exporters/report_views.py` (vistas por ensayo: replicados, granulometría, resistencia; diseño; dosificación; resumen)
- `app/exporters/report_photos.py` (anexo fotográfico)
**Modificados**: `main.tex.j2`, `ensayos/ensayos.tex.j2`, `diseno/diseno.tex.j2`, `dosificacion/dosificacion.tex.j2`, `app/exporters/pdf_report.py`,
`app/exporters/latex_engine.py` (filtros th/bf, global NR), `app/services/report_data.py` (+performed_on, notes; solo añade campos), `app/tests/test_pdf_report.py` (8 pruebas).
**Interfaz gráfica: sin cambios.**

**Contenido por informe**: portada, índice, introducción/objetivo, datos del proyecto, resumen de resultados, por ensayo (ficha, procedimiento y alcance,
identificación de muestra, datos, resultados, comparación con límites, gráfico, memoria de cálculo en 6 pasos, interpretación, alertas), diseño (parámetros,
materiales, balance de volúmenes, corrección por humedad, memoria), dosificación (por m³, humedad, bolsa, etapa rotulada), conclusiones, observaciones, referencias, firmas, anexo fotográfico.

**Anexo fotográfico**: coloque las fotos en `<carpeta de usuario>/photos/<código de proyecto>/` (jpg/png/webp…); opcional `fotos.json` con
`{"archivo.jpg": {"caption": "...", "note": "..."}}`. Sin fotos: 4 espacios reservados rotulados «sin evidencia»; nunca se usan imágenes ilustrativas como evidencia.

**Pruebas**: 8 en test_pdf_report.py + test_persistence_reports pasan; suite previa (80) pasó antes del rediseño y no se tocó código de cálculo ni UI.
PDF de prueba con datos reales (humedad, SG, PUSC, granulometría, diseño ACI): 27 páginas, sin errores de compilación; revisado visualmente (portada, tablas, memoria, gráficos, anexo).

**Errores encontrados y corregidos**: `\th` reservado de LaTeX; macros pegadas a texto; `\rowcolor` en celdas intermedias; `tcolorbox breakable`; cabeceras desalineadas (l vs X);
tablas más anchas que la página (numspec); memoria partida entre páginas; viñetas dobles en diagnóstico; numeración «Figura/Fotografía».
**Pendiente**: probar en Windows/MiKTeX; "Observaciones" y firma podrían ajustarse si queda espacio; gráficos de ensayos con datos incompletos se omiten (log).
Fuera de este bloque: Etapa 2 (Excel) y Etapa 3 (botones en Reportes).


## Etapa 1c · Informe técnico estilo «TF.pdf» (ficha de ensayo) ✅
Referencia: `TF.pdf` (informe técnico de suelos). Se conservan los colores rojo/dorado/plateado/gris oscuro. Copia previa: `_backup_fase5/latex_v2/`.
**Estructura del informe**: bloque institucional en cada página (logo | obra | «Página» / laboratorio | n.°), memorando (INFORME N°, A, De, Fecha, Asunto, Obra),
1 Trabajos de campo y laboratorio (ubicación, listado de ensayos por tipo, tabla resumen), 2 Evaluación de resultados (descripción, cumplimiento de huso),
diseño de mezcla, dosificación, conclusiones/recomendaciones, observaciones, referencias, firmas; divisor «MUESTREO Y ENSAYOS» + una **ficha por ensayo**
(condiciones ambientales y equipamiento, datos del ensayo, datos experimentales, resultados, caja de resultados, gráfico, memoria de cálculo en rejilla, interpretación);
divisor «PANEL FOTOGRÁFICO» (6 fotos/página, 2 columnas, leyenda numerada). Tablas en rejilla con numeración «Tabla N» y notas; sin portada ni índice (informe corto).
**Gráficos** (`app/charts/report_charts.py`, solo informes; la UI no cambia): PDF vectorial, fuentes incrustadas, tamaño de página, líneas 1.4–1.9 pt, rejilla mayor/menor,
doble eje de tamices (mm y designación), zona de cumplimiento, límites, puntos fuera de límites, leyenda fuera del área; réplicas: puntos + promedio ± s + rango orientativo.
**Nuevos/modificados**: `templates/latex/common/{estilo,main,memo,macros,campo_lab,anexo_fotos}.tex.j2` (+ portada.tex.j2 ya no se usa), `ensayos/ensayos.tex.j2`, `diseno/diseno.tex.j2`,
`dosificacion/dosificacion.tex.j2`, `app/exporters/{report_views,report_photos,pdf_report}.py`, `app/charts/report_charts.py`, `app/tests/test_pdf_report.py` (9 pruebas).
Datos que ConcretoLab no registra (ambiente, códigos de equipos, coordenadas, procedencia) aparecen como «no registrado»; no se inventan.
**Errores corregidos**: macro del encabezado dentro de multirow, `\th` reservado, `breakable` sin librería, nombre `items` reservado en Jinja, leyendas separadas de su tabla (ahora dentro del longtable),
`\needspace` tras longtable (páginas medio vacías), fotos más altas que la página (página en blanco).
**Pendiente**: probar en Windows/MiKTeX; logo propio en `assets/images/logo.png|pdf`; fichas de ensayos de suelos (Proctor, CBR, límites) no existen en el catálogo de ConcretoLab.

## Corrección adicional · Granulometría e identificación del informe (04-11-2026)
- TM (tamaño máximo) ahora se presenta en pulgadas y entre paréntesis en mm, tanto en los indicadores de granulometría como en el resumen y ficha PDF. TMN conserva su reporte separado; para agregado fino se indica «No aplica».
- La ficha de granulometría incorpora TM y TMN en identificación/memoria de cálculo. El resumen del informe ordena explícitamente agregado fino antes de agregado grueso, de modo que ambos registros guardados se incluyan.
- La ventana Proyectos incorpora campos opcionales esenciales para la portada: cliente, laboratorio, dirección, acreditación, responsable, profesión, CIP e institución. Permite guardar estos datos para el proyecto activo y los vincula al registro de proyecto; no se inventan datos faltantes.
- Verificación: compileall correcto; 20 pruebas focalizadas aprobadas; prueba de persistencia de perfil e inclusión/orden de granulometría fino+grueso aprobada. La prueba de GUI/PDF completa queda pendiente en Windows con PySide6/MiKTeX; en este entorno PySide6 no está instalado.
