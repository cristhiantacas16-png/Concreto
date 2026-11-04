# ConcretoLab · Revisión del módulo Reportes PDF

## Cambios aplicados

- REPORTES muestra únicamente la generación de PDF; se retiraron Excel y Plantillas LaTeX de ese módulo.
- Se retiró el apartado independiente de Normativa y Bibliografía del PDF y el grupo de navegación lateral solicitado. Las normas de ensayo siguen identificadas en las fichas técnicas de cada ensayo.
- Se aumentó la tipografía general a 12 pt, el interlineado y el tamaño de las tablas; se reforzaron los cuadros de resultados con borde y color de acento.
- Los gráficos del informe se insertan como PDF vectorial con tipografía TrueType embebida; no se convierten a capturas PNG para el informe.
- La tabla granulométrica incorpora la masa del fondo y presenta la masa recuperada total, haciendo coincidir la tabla con el control de masa.
- El TMN se muestra en pulgadas para agregado grueso (acompañado por equivalencia en mm). Para agregado fino se indica que el TMN no aplica.
- El resumen de cada ensayo prioriza su magnitud principal: humedad (%), peso unitario (kg/m³), peso específico seco (g/cm³), etc.
- Se identifican explícitamente los dos procedimientos de peso específico/absorción: agregado fino por picnómetro (A, B, S, C; ASTM C128) y agregado grueso por pesadas en aire/sumergida (A, B, C; ASTM C127).

## Criterio de unidades

El contenido de humedad se expresa en porcentaje (%) conforme a su definición como relación entre masa de agua y masa seca. kg/cm³ es una unidad de densidad y no corresponde a contenido de humedad. Las masas experimentales continúan expresadas en g y no se alteran.

## Validación pendiente en Windows

El código Python compila sintácticamente. La ejecución completa de la interfaz requiere PySide6 en el entorno Windows del usuario. La compilación final PDF debe verificarse allí con MiKTeX o TeX Live y los paquetes LaTeX instalados.

## Datos complementarios por ensayo y panel fotográfico
- En Reportes se incorporó **Datos por ensayo**: permite registrar condición ambiental, temperatura, humedad relativa, equipos principales y código/identificación de equipos para cada ensayo guardado. Los datos generales de cliente, laboratorio, dirección y responsable no se repiten en esta sección. Los campos sin información se imprimen como `S/N`.
- Los metadatos se guardan dentro del registro del último ensayo (`inputs._report_meta`), sin alterar entradas medidas ni resultados calculados.
- En Reportes se incorporó **Panel fotográfico**: crea/abre `photos/<código de proyecto>/`, permite añadir imágenes y asignarles una leyenda. Las leyendas se guardan en `fotos.json` y se usan en el anexo fotográfico del PDF.
