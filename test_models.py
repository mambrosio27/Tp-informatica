from models import Producto, Inventario

# Inicializa la base de datos para pruebas
def test_inventario():
    # Crear un producto
    producto = Producto(nombre="Camiseta", categoria="Ropa", precio=7000, stock=20)

    # Guardar el producto en la base de datos
    producto.guardar_en_db()
    print("Producto guardado en la base de datos")

    # Crear un inventario
    inventario = Inventario()

    # Listar productos del inventario
    productos = inventario.listar_productos()
    print("Productos registrados en el inventario:")
    for p in productos:
        print(p)

    # Generar reporte CSV
    inventario.generar_reporte_csv()
    print("Reporte CSV generado como 'reporte_productos.csv'.")

# Ejecutar las pruebas
if __name__ == "__main__":
    test_inventario()
