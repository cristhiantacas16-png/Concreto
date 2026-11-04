# Cambios: dosificación para probetas y robustez del módulo MF

## Dosificación para probetas cilíndricas
- Se agregó la pantalla `DOSIFICACIÓN > Probetas cilíndricas`.
- El selector reutiliza `dosage_service.sources()`: puede tomar diseños guardados ACI 211.1 o Módulo de fineza, además de mezclas de laboratorio/prueba/validadas.
- Entradas: diámetro, altura, cantidad de probetas y desperdicio (5 % por defecto, editable).
- Calcula volumen geométrico unitario, volumen neto, reserva por desperdicio y volumen total.
- Escala la dosificación corregida por m³: cemento, agregado fino húmedo, agregado grueso húmedo y agua a añadir. Si existe aditivo, también lo muestra.
- El agua se toma de `lab['water_to_add']`, no de `water_effective` ni de `water_design`, para evitar confundir el agua efectiva con la que se incorpora físicamente a la mezcladora.
- Los resultados se identifican como estimación teórica; el rendimiento real debe verificarse mediante mezcla de prueba y peso unitario fresco (ASTM C138).

## Robustez del módulo de Módulo de Fineza
- Se agregaron validaciones de entradas finitas y positivas para bolsas/m³, TMN y volumen de tanda.
- Se valida la proporción manual de fino antes de ejecutar el diseño.
- La interpolación granulométrica ahora informa claramente si faltan filas o hay aberturas/porcentajes inválidos.
- La curva combinada valida proporciones y pesos específicos antes de convertir fracciones volumétricas a masa.
- Se conservó `data/mf_tables.json` sin alterar sus valores: el propio archivo indica que su verificación es parcial y que solo se ha contrastado un punto de control. No se deben presentar las demás filas como verificadas hasta cotejarlas con la edición exacta del texto de referencia.

## Pruebas
- Se añadieron pruebas unitarias para volumen y pesadas de probetas, el uso de agua a añadir y entradas inválidas.
- Se añadió una prueba de integración de interfaz para las fuentes ACI y MF.
- `compileall` de `app` y `modules`: correcto.
- Pruebas pytest de interfaz no ejecutadas en este entorno porque no está instalada la dependencia PySide6. Deben ejecutarse en el entorno Windows de ConcretoLab.
