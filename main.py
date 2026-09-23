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

def buscar_libro(libros, codigo):
    """Busca y retorna un libro por su código."""
    for libro in libros:
        if libro["codigo"].strip().upper() == codigo.strip().upper():
            return libro
    return None

def registrar_libro(libros):
    """RF01: Registra un nuevo libro en el sistema."""
    print("\n--- REGISTRAR LIBRO ---")
    codigo = input("Código del libro (ej: L001): ").strip().upper()
    if not codigo:
        print("Error: El código es obligatorio.")
        return
    if buscar_libro(libros, codigo):
        print("Error: El código ya se encuentra registrado.")
        return

    isbn = input("ISBN: ").strip()
    if not isbn or any(l["isbn"] == isbn for l in libros):
        print("Error: El ISBN es obligatorio y debe ser único.")
        return

    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    categoria = input("Categoría: ").strip()
    editorial = input("Editorial: ").strip()

    if not titulo or not autor or not categoria:
        print("Error: Título, autor y categoría son obligatorios.")
        return

    try:
        anio = int(input("Año de publicación: "))
        cantidad_total = int(input("Cantidad total: "))
        if cantidad_total <= 0:
            print("Error: La cantidad debe ser mayor a cero.")
            return
    except ValueError:
        print("Error: El año y la cantidad deben ser valores numéricos enteros.")
        return

    nuevo_libro = {
        "codigo": codigo,
        "isbn": isbn,
        "titulo": titulo,
        "autor": autor,
        "categoria": categoria,
        "editorial": editorial,
        "anio": anio,
        "cantidad_total": cantidad_total,
        "cantidad_disponible": cantidad_total
    }
    libros.append(nuevo_libro)
    guardar_json(ARCH_LIBROS, libros)
    print("✓ Libro registrado con éxito.")