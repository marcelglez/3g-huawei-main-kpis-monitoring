# PLAN-001: 3G Huawei Main KPIs Monitoring (REQ-001)

> Nota: AGENTS.md y templates/plan.md / templates/task.md no existen en el repo; se uso el formato de plan/tarea de las instrucciones globales. Si existen en otra ruta, reformatear.

## Diseno
Paquete `kpi_monitor/` + JSON de configuracion en `config/kpi_config.json` (nada fijo en codigo: rutas, columnas de sitio/fecha/KPI, prefijo de salida).
- `config.py`: carga y valida el JSON.
- `loader.py`: crea `Data input/` y `Output/` si faltan, lee solo los `*.xlsx` de `Data input/` (ignora `~$*`), valida columnas, consolida sin alterar valores, avisa por `logging` de duplicados (sitio+fecha) sin sumarlos ni promediarlos.
- `report.py`: escribe el xlsx con `openpyxl`: hoja `Data` (datos tal cual) y hoja `Charts` con celda desplegable (validacion de datos, nativo, sin macros) con la lista de sitios, una tabla auxiliar por formulas (INDEX/MATCH por sitio+fecha; vacio -> `NA()` para que el grafico no rellene) y 8 graficos de linea, uno por KPI.
- `__main__.py`: CLI (`python -m kpi_monitor`), errores claros, codigo de salida != 0 sin generar reporte.
- `tools/verify.py`: ejecuta `python -m unittest discover` y propaga el codigo de salida.
- Dependencia nueva: `openpyxl` (unica; graficos nativos y validacion de datos; ligera). Alternativas descartadas: xlsxwriter (no lee xlsx, requeriria dos librerias); pandas (pesado para la laptop).
- Pruebas con fixtures sinteticas generadas en la prueba (`Data input/` esta en .gitignore).

## Tareas y dependencias
| Tarea | Entrega | Depende de |
|---|---|---|
| T-001 | Config JSON + loader/validacion | - |
| T-002 | Generador del reporte xlsx | T-001 |
| T-003 | CLI + verify.py + requirements + prueba extremo a extremo | T-001, T-002 |

## Criterios REQ-001 cubiertos
1 (carpetas) -> T-001; 2 (data identica) -> T-002; 3 (8 graficos + filtro) -> T-002; 4 (errores) -> T-001/T-003; 5 (verify) -> T-003.

## Riesgos
- Nombres de columna literales (guion largo, `Grp_ 3G`) pueden diferir de la muestra real: T-001 los contrasta con `Data input/Test File.xlsx` y reporta diferencias sin cambiar el JSON a ciegas.
- Las formulas no tienen valor en cache hasta abrir en Excel: las pruebas verifican estructura, no valores calculados.
