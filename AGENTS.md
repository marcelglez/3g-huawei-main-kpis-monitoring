# Reglas del proyecto (Codex y Claude)

Reglas duras; los hooks las hacen cumplir. Mantener corto.

1. Rutas, columnas de sitio/fecha y nombres de KPI salen SOLO de `config/kpi_config.json`. Prohibido fijarlos en el codigo.
2. Si falta una columna o KPI: DETENERSE y reportar con mensaje claro. No inventar, rellenar, interpolar ni promediar valores.
3. `Data Input/Test File.xlsx`: solo leer nombres de hojas y encabezados (fila 1). Nunca leer ni imprimir valores de datos.
4. Duplicados sitio+fecha: se conservan todas las filas en orden, sin sumar, promediar ni descartar; se avisa por log (solo claves, nunca valores). El grafico usa la primera aparicion.
5. Trabajar solo la tarea en `state/current_task.json` y escribir solo en sus rutas permitidas. Ideas nuevas van a `backlog/`.
6. Verificar con UN comando por intento: `python -m unittest discover` (el verificador central de la fabrica lo repite y exige los archivos de la tarea; este proyecto no tiene `tools/verify.py`). Maximo 3 intentos por tarea; despues marcar `bloqueada` y reportar.
7. No editar `hooks/`, `.claude/`, `.codex/`, `state/`, `config/factory.json`, `Data Input/`, `Output/`.
8. Python 3.9: sin `X | Y` en anotaciones, sin `match`, sin `zip(strict=)` ni otras funciones de 3.10+. Sin pytest (usar `unittest`). Unica dependencia: `openpyxl`.
9. Entrega: pegar la salida de verify y la lista de archivos cambiados. Nada mas.
10. Si existe el archivo `STOP` en la raiz, no empezar trabajo nuevo.

Roles: requester (requests/), planner (plans/, tasks/), implementer (rutas de la tarea), auditor (audits/, solo lectura del codigo), reporter (logs/).
