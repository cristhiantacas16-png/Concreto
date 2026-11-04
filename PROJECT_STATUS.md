# PROJECT_STATUS — ConcretoLab Professional Suite

**Versión:** 2.0.0 · **Python:** 3.12 · **Última actualización:** 31/10/2026

## Estado actual
FASES 0–4 completadas; FASE 5 en curso (Etapa 1 motor PDF ✅).
Aún **no** se ha probado en Windows físico (solo entorno Linux headless).

| Fase | Estado |
|---|---|
| 0 Planificación y diseño | ✅ |
| 1 Interfaz principal (ventana, sidebar, navegación, dashboard, 4 módulos, BD) | ✅ |
| 2 Ensayos: humedad, granulometría (fino/grueso), PUSS/PUSC, peso específico+absorción (fino/grueso), cemento; gráficos SVG/PDF/PNG; guardado en BD; Reportes lee de la BD | ✅ (falta validar con datos reales del usuario) |
| 3.1 Diseño: resistencia, probetas, estadística, f'cr, aceptación | ✅ |
| 3.2 ACI 211.1 (15 etapas, memoria de cálculo, por m³ y por tanda) | ✅ (tablas con verificación parcial) |
| 3.3 Método MF (13 etapas, deslizador interactivo, granulometría combinada) | ✅ (tabla m_c: verificación parcial) |
| 3.4 Comparación ACI vs MF | ✅ |
| 4 Dosificación | ⏳ |
| 5 Reportes (LaTeX, Excel) | ⏳ |
| 6 Validación y distribución | ⏳ |

## Dependencias
PySide6>=6.7 · SQLAlchemy>=2.0 · matplotlib>=3.8 · numpy · pytest. (numpy, scipy, pandas, matplotlib, openpyxl, jinja2, pyinstaller: se instalan en su fase.)

## Ejecutar
    pip install -r requirements.txt
    python main.py
    python -m pytest app/tests -q

## Árbol de archivos (Fase 1)
    main.py                      punto de entrada
    requirements.txt
    app/core/        config.py logging_setup.py navigation.py state.py
    app/database/    models.py session.py
    app/services/    project_service.py
    app/ui/          theme.py icons.py dialogs.py main_window.py
    app/ui/widgets/  panel.py topbar.py sidebar.py statusbar.py
    app/ui/pages/    dashboard.py module_page.py
    app/tests/       conftest.py test_project_service.py test_navigation.py test_ui_smoke.py
    modules/         __init__.py (MODULE_PAGES) + {ensayos,diseno,dosificacion,reportes}/page.py
    templates/latex/ {ensayos,diseno,dosificacion,common}/   (vacías: colocar plantillas propias)
    assets/images/hero.jpg   (opcional: foto del banner; si no existe se usa arte vectorial)
    app/calculations/ validation/ charts/ exporters/   (vacías, listas para Fases 2-5)

## Decisiones técnicas
- Navegación declarativa en `app/core/navigation.py`: añadir un ensayo = una línea.
- `AppState` (señales Qt) es la fuente única del proyecto activo.
- UI no toca el ORM: usa DTO (`ProjectSummary`) de `project_service`.
- BD SQLite: `Test.inputs` (medido) y `Test.results` (calculado) separados; `Design.state` = teorico|prueba|validado.
- Todo se pinta con QPainter + iconos SVG propios (sin imágenes externas).
- Barra de título nativa de Windows (más robusta que una personalizada).
- Progreso del proyecto = conteos reales de la BD; sin datos muestra 0 % (nada simulado).
- Pendiente de verificar contra fuentes (Fase 2/3): edición vigente de NTP 400.012, ASTM C136, ACI 211.1, RNE E.060, tablas de Riva López.

## Errores/limitaciones conocidas
- Fuentes: en Windows usa Bahnschrift/Segoe UI; en otros SO cae a la fuente por defecto (solo cambia el aspecto).
- Los ítems de Ensayos/Diseño/etc. muestran un marcador "Disponible en la Fase N".
- Panel derecho del dashboard se oculta bajo 1100 px de ancho.

## Última funcionalidad comprobada
Crear/abrir proyecto → dashboard, sidebar (ubicación/altitud), progreso y actividad se actualizan; búsqueda global navega.

## Archivos nuevos (Fase 2)
    app/calculations/  replicates.py (motor) catalog.py (humedad, PUS, SG fino/grueso, cemento) granulometry.py
    app/validation/husos.py + data/husos.json   (husos configurables, con estado de verificación)
    app/charts/        style.py granulometry_chart.py replicate_chart.py render.py
    app/services/      test_service.py report_data.py (FUENTE ÚNICA para PDF/Excel)
    app/ui/widgets/chart_panel.py
    modules/ensayos/   base.py replicate_page.py granulometria_page.py pages.py
    modules/reportes/page.py (tabla consolidada + exportar gráficos)

## Cambios del lote actual
- Humedad y PUSS/PUSC separados por agregado (fino/grueso): kinds humedad_fino/grueso, pus_{suelto,compactado}_{fino,grueso}. Los registros antiguos se conservan (GROUP_OF).
- data/husos.json: 15 husos del agregado grueso transcritos de la tabla del usuario (1,2,3,357,4,467,5,56,57,6,67,7,8,89,9). Tamices mayores que el primero del huso: límite implícito 100-100 (limits_for).
- Fino: límites extendidos hasta N°200 (0–5 %, ASTM C33 / C117). Tabla gruesa ahora de 4" a N°100.
- Resistencia: app/calculations/strength.py, app/charts/strength_chart.py, modules/diseno/resistencia_page.py; pegado desde Excel (app/ui/widgets/tables.py).
- Nota: la tabla del usuario dice «37.5 mm a 9 mm» en el huso 4; se transcribió como 19 mm (3/4 in.), coherente con su columna 19 mm.

## Pendiente de verificar (honestidad técnica)
- f'cr: ecuaciones 5-1/5-2/5-3 y tabla sin antecedentes (70/84/1.10f'c+50) contrastadas con fuentes que reproducen E.060/ACI 318. Para f'c>350 ediciones antiguas usan f'c+98: confirmar la edición de E.060 del proyecto.
- Criterio de aceptación (prom. de 3 ≥ f'c; individual ≥ f'c−35 o 0.90f'c si >350) y factores de s (1.16/1.08/1.03/1.00): confirmar edición.
- Límites del fino y rango N°200 (0–5 %): fuentes secundarias; confirmar con NTP 400.037 vigente.
- Criterio de TMN configurable (granulometry.TMN_RETAINED_PCT).
- Rangos usuales (cemento 2.6–3.3, SG 2.0–3.2) = alertas, no normativos.

## Siguiente tarea (ver también FASE5_ESTADO.md: rediseño editorial hecho)
3.2 ACI 211.1: requiere las tablas (agua de mezclado vs asentamiento/TMN, aire atrapado, relación a/c vs f'cr, volumen de agregado grueso vs MF/TMN). Cargarlas en data/aci211_tablas.json desde Riva López / ACI 211.1 del usuario o contrastarlas con fuentes; leer ensayos con test_service.latest_test y f'cr del registro 'resistencia'.


## FASE 3 — Archivos nuevos / modificados
    app/calculations/  mixcommon.py (interpolación, vol. absolutos, humedad, tanda) aci211.py mf_method.py
    app/services/      design_service.py (lee ensayos guardados; guarda/lee `designs`)
    app/charts/        design_chart.py (volúmenes, curva combinada, comparación); granulometry_chart.py (+ límites hasta malla N°200)
    data/              aci211_tables.json  mf_tables.json   (editables; con estado de verificación)
    modules/diseno/    common.py aci_page.py mf_page.py comparacion_page.py pages.py  (+ resistencia_page.py del lote 3.1)
    app/ui/theme.py    estilo de QGroupBox/QCheckBox; app/services/report_data.py tolerante a estadísticas incompletas
    app/tests/         test_design.py (16 pruebas)

## Decisiones técnicas (Fase 3)
- Propiedades de materiales se LEEN de los ensayos guardados (kinds: cemento_sg, sg_*, humedad_*, granulometria_*, pus_compactado_grueso, resistencia); cada valor muestra su procedencia y es editable («ingresado manualmente»).
- f'cr se toma de `resistencia` (results["fcr"]["fcr"], kg/cm²) o se ingresa a mano. El diseño guardado queda siempre `teorico`.
- ACI: agregado grueso = (b/b₀)·PUSC; fino por volúmenes absolutos; a/c = mín(resistencia, durabilidad ingresada por el usuario; no se inventa tabla de durabilidad).
- MF: m_c por doble interpolación (bolsas × TMN); r_f = (m_g − m_c)/(m_g − m_f); agua/aire/a/c con tablas ACI (procedimiento complementario, no se confunde combinación con diseño completo). Se avisa si la combinación es imposible (m_c fuera de [m_f, m_g]).
- Comparación: no fuerza coincidencia; avisa si los diseños no usan los mismos datos de entrada.
- Límites del gráfico granulométrico se prolongan hasta el último tamiz como cota monótona (punteada, rotulada «no normativa»); no afecta el cumplimiento.

## Pendiente de verificar (Fase 3)
- aci211_tables.json: contrastada con ejemplos resueltos (193 l/m³, 1.5 % aire, a/c 0.5584 a 294 kgf/cm²); falta cotejar el resto con ACI 211.1 oficial.
- mf_tables.json: solo 8 y 9 bolsas con TMN 1" contrastadas (8.13 bolsas → 5.42). Confirmar el resto con el libro de Rivva López que usa (título y edición).
- E.060 5.3.2: edición vigente y regla f'c > 350 kg/cm² (1.10 f'c + 50 vs f'c + 98 en ediciones anteriores).
- Aún sin probar en Windows físico.

## Siguiente tarea (ver también FASE5_ESTADO.md: rediseño editorial hecho)
FASE 4 (DOSIFICACIÓN): leer `designs` (ACI/MF) → dosificación por m³, volumen de obra, tandas, calculadora de humedad/absorción, mezclas de prueba (teórico → prueba → validado). Reutilizar `app/calculations/mixcommon.py`.


## Revisión Fase 3 (f'cr con método desplegable y modo «resultados de f'c»)
Nuevo:
    app/calculations/fcr.py        métodos de f'cr (unidades nativas MPa o kg/cm²) + estadística de resultados directos
    data/fcr_tables.json           grados de control (ACI 214) y coeficientes t «1 en N»  (editable; verificación parcial)
    modules/diseno/fcr_panel.py    panel desplegable de f'cr (reutilizado en Resistencia, ACI y MF)
    modules/diseno/resistencia_directa.py   modo de ejercicios: lista de f'c → n, x̄, s, CV, promedios de 3, aceptación, f'cr
    app/charts/fcr_chart.py        histograma + normal ajustada y secuencia de ensayos
    app/tests/test_fcr.py          ejercicio de 52 resultados (f'c = 17.5 MPa) y panel
Métodos de f'cr: (1) con s — E.060/ACI 318 con factor para 15–29 ensayos; (2) sin registros (tabla); (3) por grado de control
(obra/laboratorio; s = límite superior del grado, editable); (4) f'cr = f'c + z·s por % de resultados < f'c (tabla «1 en N» o % personalizado,
z exacta); (5) manual. Los diseños ACI/MF y «Resistencia» comparten el mismo panel y guardan su configuración (`fcr_ui`).
Decisión: la memoria de cálculo muestra siempre ecuaciones, sustitución, referencia y advertencias; n < 15 → se usa la tabla y se avisa.
Pendiente: contrastar tablas de grados de control y de t con el libro de Rivva López (no hubo acceso al libro; se usó ACI 214 vía fuentes secundarias).


## FASE 4 — Dosificación (completada)
Archivos nuevos:
    app/calculations/dosage.py     humedad/absorción, aditivo, tandas/volumen de obra, ASTM C138 (rendimiento, aire), ajuste a/c constante, checklist de validación
    app/services/dosage_service.py unifica diseños y mezclas guardadas como «fuentes»
    app/services/design_service.py (+) get/list_designs, set_design_state (solo avanza), save/list/get_mix
    app/charts/dosage_chart.py     teórico vs laboratorio · plan de obra · asentamiento de pruebas
    modules/dosificacion/          common.py m3_page.py humedad_page.py tandas_page.py prueba_page.py pages.py
    app/tests/test_dosage.py       15 pruebas (cálculo, persistencia de estados, flujo completo de UI)
Etapas separadas (tabla `mixes`, campo `stage`; `designs.state`): teórico → laboratorio → prueba → validado. Ninguna pantalla sobrescribe otra etapa.
Decisiones:
- «Agua efectiva» = agua de diseño − aportes de agregados; «agua a añadir» = efectiva − agua del aditivo.
- Aditivo: dosis % de cemento; su volumen se descuenta del fino (opcional) para mantener ΣV = 1 m³.
- Mezcla de prueba (ASTM C138): Y = M/γ, R_y = Y/V_tanda, aire = (T − γ)/T; a/c real con agua libre.
- Ajuste tras prueba: Δ agua → cemento = agua/(a/c), grueso constante, fino por volúmenes absolutos; se guarda como nueva corrección (`design_override`), el diseño teórico no cambia.
- VALIDADO solo si: asentamiento en rango, γ medido, f'c prom. a 28 d ≥ f'cr, ≥ 2 probetas y confirmación del usuario. Nunca se valida con datos faltantes.
- Volumen aparente de agregados y pie³ por bolsa: aproximación con PU suelto húmedo (editable).
Pendiente / no verificado: tolerancia de aire y rendimiento (se informa la diferencia, no se impone un criterio normativo); edad de diseño fija en 28 d para validar.

## Siguiente tarea (ver también FASE5_ESTADO.md: rediseño editorial hecho)
FASE 5 (REPORTES): plantillas LaTeX (ensayos/diseño/dosificación), PDF, Excel, gráficos vectoriales y memorias de cálculo; leer de `tests`, `designs` y `mixes` (una sola fuente validada).


## FASE 5 · ETAPA 1 — Motor PDF (LaTeX) ✅
Nuevo (la interfaz NO se modificó):
    app/exporters/latex_engine.py   escape TeX, entorno Jinja2 (\VAR{} \BLOCK{}), find_engine(), compile_tex() (2 pasadas)
    app/exporters/report_context.py FUENTE ÚNICA PDF+Excel: ReportBundle (proyecto, cliente, lab, ensayos, diseños, dosificación más avanzada)
    app/exporters/pdf_report.py     generate_pdf(project_id, kind in ensayos|diseno|dosificacion|completo, out_dir=None) → registra `reports`
    templates/latex/common/main.tex.j2  portada, índice, objetivo, conclusiones, referencias, firmas
    templates/latex/{ensayos,diseno,dosificacion}/*.tex.j2   secciones (editables sin tocar el código)
    app/tests/test_pdf_report.py    3 pruebas (la de compilación se omite si no hay LaTeX)
Decisiones: pdflatex + helvet (portable MiKTeX/TeX Live); gráficos PDF vectoriales (tema claro); un gráfico fallido se omite y se registra en el log;
la dosificación teórica/laboratorio/prueba se rotula como tal (nunca «validada» sin validación); no se recalcula nada, solo se lee la BD.
Logo opcional: assets/images/logo.png|pdf. Requiere MiKTeX o TeX Live.
Pruebas: 80 pasan (65 lógica + 15 UI). Probado en Linux/TeX Live; no en Windows/MiKTeX.
## Siguiente tarea (ver también FASE5_ESTADO.md: rediseño editorial hecho)
ETAPA 2: app/exporters/excel_report.py (openpyxl: portada, datos, resultados con fórmulas, gráficos nativos) sobre report_context.build().
ETAPA 3: añadir botones en modules/reportes/page.py (sin cambiar el diseño) y pruebas de coincidencia PDF↔Excel↔BD.


## Actualización: dosificación para probetas cilíndricas y robustez MF
- Nueva pantalla `DOSIFICACIÓN > Probetas cilíndricas`, con fuentes guardadas ACI 211.1 y Módulo de fineza.
- Calcula volumen geométrico, cantidad de moldes, desperdicio editable (5 % inicial) y materiales a pesar.
- Usa agregado húmedo y `agua_to_add` (agua a añadir a la mezcladora), no el agua efectiva del diseño.
- La estimación se rotula como teórica hasta comprobar rendimiento con mezcla de prueba/ASTM C138.
- Mejoras de validación en `mf_method.py`; `mf_tables.json` se mantiene intacto por su verificación parcial documentada.
- Detalle: `MEJORAS_DOSIFICACION_PROBETAS_MF.md`.
