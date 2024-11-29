import sqlite3
import csv

# Clase Producto
class Producto:
    def __init__(self, nombre, categoria, precio, stock):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    def guardar_en_db(self):
        """Guarda el producto en la base de datos."""
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        ''', (self.nombre, self.categoria, self.precio, self.stock))
        conn.commit()
        conn.close()

    def actualizar_stock(self, nuevo_stock):
        """Actualiza el stock del producto."""
        self.stock = nuevo_stock
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('''
            UPDATE productos
            SET stock = ?
            WHERE nombre = ?
        ''', (self.stock, self.nombre))
        conn.commit()
        conn.close()

    def detalles(self):
        """Devuelve los detalles del producto como diccionario."""
        return {
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        """Agrega un producto al inventario y lo guarda en la base de datos."""
        self.productos.append(producto)
        producto.guardar_en_db()

    def listar_productos(self):
        """Devuelve todos los productos del inventario."""
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('SELECT nombre, categoria, precio, stock FROM productos')
        productos_db = c.fetchall()
        conn.close()
        return [{"nombre": p[0], "categoria": p[1], "precio": p[2], "stock": p[3]} for p in productos_db]

    def generar_reporte_csv(self):
        """Genera un archivo CSV con los productos."""
        conn = sqlite3.connect('inventario.db')
        c = conn.cursor()
        c.execute('SELECT nombre, categoria, precio, stock FROM productos')
        productos_db = c.fetchall()
        conn.close()

        with open('reporte_productos.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Categoría", "Precio", "Stock"])
            writer.writerows(productos_db)
