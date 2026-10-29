---
name: nueva-tarea
description: Crear una peticion para la fabrica central.
---
Actua como requester. Identifica FACTORY como la raiz que contiene esta skill.
Pide el proyecto si no es obvio, titulo, objetivo y 3-5 criterios medibles.
Haz como maximo dos rondas de preguntas; registra supuestos menores.
Ejecuta `python E:\Claude_Codex\Nueva carpeta\rf-factory/tools/run_factory.py --project <P> new-request --title "..."`.
Completa la peticion creada, incluyendo alcance, restricciones y criterios.
Fija la seccion 12 en `lista` si es ejecutable o `bloqueada` si falta informacion clave.
Termina indicando `python E:\Claude_Codex\Nueva carpeta\rf-factory/tools/run_factory.py --project <P> run`.
