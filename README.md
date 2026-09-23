# Bibliosena Facatativá
Aplicacion monolitica de consola para la gestion de biblioteca , inventario de prestamos, JSON, reportes y control de versiones.

### Autor
*Aprendiz: Nicole Sthephanie Alonso Mayorga*
*Programa: tecnico en programacion de software*
*Centro de formacion: Sena sede Facatativa*

# Funcionalidades principales

### gestion de libros (CRUD)
**registro de libros:* registra y busca libros, se ordenan por codigo, autor, ISBN, titulo, categoria, editorial, año y cantidad
**listado de libros:* Muestra el catalogo completo de libros detallando la cantidad total, disponibls y prestados 
**buscar libros:* consulta de un titulo especifico mediante su codigo unico 
**actualizar libro:* modifica datos bibliograficos e inventario respetando los prestamos activos

### prestamos y devoluciones 
**registrar prestamo:* descvuenta stock disponible y calcula automaticamente ID, fecha de salida y fecha limite (7 dias)
**registrar devolucion:* restaura la disponibilidad e impide devoluciones dobles de un mismo prestamo
**historial:* muestra el registro general de prestamos con fcha limite superada y dias de retraso

### Modulo de reportes 
**libros actualmente prestados:* prestamo en estado 'ACTIVO' con detalles de libro y entrega
**libros sin disponibilidad:* filtra el inventario agotado 
**historial por usuario:* consulta prestamos por documento de identidad 
**ranking de libros mas prestados:* clasificacion ordenada segun la demanda de los usuarios 
**prestamos vencidos:* identifica prestamos con fecha limite superada y dias de retraso
**auditoria de inventario:* verifica la coherencia entre prestamos activos y cantidad disponible 

### Tecnologias utilizadas 
**Lenguaje Python 3.*
**persistencia:* JSON 
**control de versiones:* Git/Github

### estructura del proyecto
bibliosena/
├── main.py 
    ├── libros.json 
    ├── prestamos.json 
    ├── README.md 
    └── .gitignore

