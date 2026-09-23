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

def listar_libros(libros):
    """RF02: Muestra la lista de libros registrada."""
    print("\n--- LISTADO DE LIBROS ---")
    if not libros:
        print("No hay libros registrados en el sistema.")
        return
    for l in libros:
        prestados = l["cantidad_total"] - l["cantidad_disponible"]
        print(f"[{l['codigo']}] {l['titulo']} - Autor: {l['autor']} | "
              f"Total: {l['cantidad_total']} | Disponibles: {l['cantidad_disponible']} | Prestados: {prestados}")

def consultar_libro_por_codigo(libros):
    """RF03: Busca un libro por su código."""
    print("\n--- BUSCAR LIBRO ---")
    codigo = input("Ingrese el código del libro a buscar: ")
    libro = buscar_libro(libros, codigo)
    if libro:
        prestados = libro["cantidad_total"] - libro["cantidad_disponible"]
        print(f"\nCódigo: {libro['codigo']}\nISBN: {libro['isbn']}\nTítulo: {libro['titulo']}\n"
              f"Autor: {libro['autor']}\nCategoría: {libro['categoria']}\nEditorial: {libro['editorial']}\n"
              f"Año: {libro['anio']}\nTotal: {libro['cantidad_total']}\nDisponibles: {libro['cantidad_disponible']}\n"
              f"Prestados: {prestados}")
    else:
        print("Error: Libro no encontrado.")

def actualizar_libro(libros, prestamos):
    """RF04: Actualiza información del libro ajustando límites según préstamos activos."""
    print("\n--- ACTUALIZAR LIBRO ---")
    codigo = input("Código del libro a actualizar: ")
    libro = buscar_libro(libros, codigo)
    if not libro:
        print("Error: Libro no encontrado.")
        return

    prestamos_activos = sum(1 for p in prestamos if p["codigo_libro"] == libro["codigo"] and p["estado"] == "ACTIVO")

    print(f"Modificando: {libro['titulo']}")
    nuevo_titulo = input(f"Título [{libro['titulo']}]: ").strip() or libro['titulo']
    nuevo_autor = input(f"Autor [{libro['autor']}]: ").strip() or libro['autor']
    nueva_categoria = input(f"Categoría [{libro['categoria']}]: ").strip() or libro['categoria']
    nueva_editorial = input(f"Editorial [{libro['editorial']}]: ").strip() or libro['editorial']

    try:
        nuevo_total_str = input(f"Cantidad total [{libro['cantidad_total']}]: ").strip()
        nuevo_total = int(nuevo_total_str) if nuevo_total_str else libro['cantidad_total']
        if nuevo_total < prestamos_activos:
            print(f"Error: La cantidad no puede ser inferior a los préstamos activos ({prestamos_activos}).")
            return
    except ValueError:
        print("Error: Valor numérico inválido.")
        return

    diferencia = nuevo_total - libro['cantidad_total']
    libro['titulo'] = nuevo_titulo
    libro['autor'] = nuevo_autor
    libro['categoria'] = nueva_categoria
    libro['editorial'] = nueva_editorial
    libro['cantidad_total'] = nuevo_total
    libro['cantidad_disponible'] += diferencia

    guardar_json(ARCH_LIBROS, libros)
    print("✓ Libro actualizado correctamente.")

def eliminar_libro(libros, prestamos):
    """RF05: Elimina un libro si no posee préstamos activos."""
    print("\n--- ELIMINAR LIBRO ---")
    codigo = input("Código del libro a eliminar: ")
    libro = buscar_libro(libros, codigo)
    if not libro:
        print("Error: Libro no encontrado.")
        return

    tiene_activos = any(p["codigo_libro"] == libro["codigo"] and p["estado"] == "ACTIVO" for p in prestamos)
    if tiene_activos:
        print("Error: No se puede eliminar un libro con préstamos activos.")
        return

    libros.remove(libro)
    guardar_json(ARCH_LIBROS, libros)
    print("✓ Libro eliminado del catálogo.")

from datetime import datetime, timedelta

def generar_id_prestamo(prestamos):
    """Genera un ID incremental para cada préstamo."""
    if not prestamos:
        return 1
    return max(p["id_prestamo"] for p in prestamos) + 1

def registrar_prestamo(libros, prestamos):
    """RF06, RF07, RF08: Registra préstamos de libros."""
    print("\n--- REGISTRAR PRÉSTAMO ---")
    codigo = input("Código del libro: ")
    libro = buscar_libro(libros, codigo)

    if not libro:
        print("Error: El libro no existe.")
        return
    if libro["cantidad_disponible"] <= 0:
        print("Error: No hay ejemplares disponibles para préstamo.")
        return

    doc = input("Documento del usuario: ").strip()
    nombre = input("Nombre completo del usuario: ").strip()
    if not doc or not nombre:
        print("Error: Documento y nombre son datos obligatorios.")
        return

    hoy = datetime.now()
    fecha_p = hoy.strftime("%Y-%m-%d")
    fecha_l = (hoy + timedelta(days=7)).strftime("%Y-%m-%d")

    nuevo_prestamo = {
        "id_prestamo": generar_id_prestamo(prestamos),
        "codigo_libro": libro["codigo"],
        "documento_usuario": doc,
        "nombre_usuario": nombre,
        "fecha_prestamo": fecha_p,
        "fecha_limite": fecha_l,
        "fecha_devolucion": None,
        "estado": "ACTIVO"
    }

    libro["cantidad_disponible"] -= 1
    prestamos.append(nuevo_prestamo)

    guardar_json(ARCH_LIBROS, libros)
    guardar_json(ARCH_PRESTAMOS, prestamos)
    print(f"✓ Préstamo registrado (ID: {nuevo_prestamo['id_prestamo']}). Devolver antes de: {fecha_l}")

def consultar_prestamos(prestamos):
    """RF11: Lista el historial general de préstamos."""
    print("\n--- HISTORIAL DE PRÉSTAMOS ---")
    if not prestamos:
        print("Sin préstamos registrados.")
        return
    for p in prestamos:
        print(f"ID: {p['id_prestamo']} | Libro: {p['codigo_libro']} | Usuario: {p['nombre_usuario']} ({p['documento_usuario']}) | Estado: {p['estado']}")

def registrar_devolucion(libros, prestamos):
    """RF09, RF10: Registra la devolución de un libro prestado."""
    print("\n--- REGISTRAR DEVOLUCIÓN ---")
    try:
        id_p = int(input("Ingrese el ID del préstamo: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    prestamo = next((p for p in prestamos if p["id_prestamo"] == id_p), None)
    if not prestamo:
        print("Error: Préstamo no encontrado.")
        return

    if prestamo["estado"] == "DEVUELTO":
        print("Error: Este préstamo ya fue devuelto con anterioridad.")
        return

    libro = buscar_libro(libros, prestamo["codigo_libro"])
    
    prestamo["estado"] = "DEVUELTO"
    prestamo["fecha_devolucion"] = datetime.now().strftime("%Y-%m-%d")

    if libro:
        libro["cantidad_disponible"] += 1

    guardar_json(ARCH_LIBROS, libros)
    guardar_json(ARCH_PRESTAMOS, prestamos)
    print("✓ Devolución registrada correctamente.")

    