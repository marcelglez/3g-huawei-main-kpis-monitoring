"""Read paths and column names from the project configuration."""

import json
from pathlib import Path


def load_config(path):
    """Load a JSON configuration; resolve folders relative to its project root."""
    path = Path(path).resolve()
    with path.open(encoding="utf-8") as stream:
        config = json.load(stream)
    for key in ("input_dir", "output_dir", "site_column", "date_column"):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError("Configuracion invalida: " + key)
    kpis = config.get("kpis")
    if not isinstance(kpis, dict) or len(kpis) != 8:
        raise ValueError("Configuracion invalida: se requieren 8 KPIs")
    if any(not isinstance(value, str) or not value.strip() for value in kpis.values()):
        raise ValueError("Configuracion invalida: nombres de KPI")
    columns = [config["site_column"], config["date_column"]] + list(kpis.values())
    if len(set(columns)) != len(columns):
        raise ValueError("Configuracion invalida: columnas repetidas")
    for key in ("input_dir", "output_dir"):
        config[key] = path.parent.parent / config[key]
    return config
