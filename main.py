import json 
import os 

ARCH_LIBROS = "libros.json"
ARCH_PRESTAMOS = "prestamos.json"

def cargar_json(ruta):
    """carga un archivo JSON de forma  segura."""
    if not os.path.exists(ruta):
        guardar_json(ruta, [])
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
            return []

def guardar_json(ruta, datos):
    """guarda datos en formato JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)