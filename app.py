from flask import Flask, request, jsonify
import sqlite3
from models import Producto, Inventario
import csv
import requests

app = Flask(__name__)

# Inicialización de la base de datos
def init_db():
    with sqlite3.connect('inventario.db', timeout=10) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio REAL,
                stock INTEGER,
                precio_usd REAL
            )
        ''')
        c.execute('PRAGMA journal_mode=WAL;')  # Habilitar modo WAL
        conn.commit()

# Ruta principal
@app.route('/')
def home():
    return "Sistema de Gestión de Inventarios para Pequeñas Empresas"

# Ruta para registrar un nuevo producto (POST)
@app.route('/productos', methods=['POST'])
def registrar_producto():
    data = request.get_json()

    # Datos del producto
    nombre = data.get('nombre')
    categoria = data.get('categoria')
    precio = data.get('precio')  # Precio en ARS
    stock = data.get('stock')

    # Intentar obtener el tipo de cambio
    tipo_cambio = obtener_tipo_cambio()
    if tipo_cambio is None:
        return jsonify({"error": "No se pudo obtener el tipo de cambio. Intente más tarde."}), 500

    # Calcular precio en USD
    precio_usd = round(precio / tipo_cambio, 2)

    # Guardar en la base de datos
    with sqlite3.connect('inventario.db', timeout=10) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock, precio_usd)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, categoria, precio, stock, precio_usd))
        conn.commit()

    return jsonify({
        "message": "Producto registrado con éxito",
        "producto": {
            "nombre": nombre,
            "categoria": categoria,
            "precio (ARS)": precio,
            "precio (USD)": precio_usd,
            "stock": stock
        }
    }), 201


# Ruta para consultar todos los productos (GET)
@app.route('/productos', methods=['GET'])
def consultar_productos():
    inventario = Inventario()
    productos = inventario.listar_productos()
    return jsonify(productos), 200

# Ruta para actualizar el stock de un producto (PUT)
@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_stock(id):
    data = request.get_json()
    nuevo_stock = data.get('stock')

    # Actualizar el stock en la base de datos con timeout
    with sqlite3.connect('inventario.db', timeout=10) as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE productos
            SET stock = ?
            WHERE id = ?
        ''', (nuevo_stock, id))
        conn.commit()

    return jsonify({"message": "Stock actualizado con éxito"}), 200

# Ruta para eliminar un producto (DELETE)
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    with sqlite3.connect('inventario.db', timeout=10) as conn:
        c = conn.cursor()
        c.execute('''
            DELETE FROM productos WHERE id = ?
        ''', (id,))
        conn.commit()

    return jsonify({"message": "Producto eliminado con éxito"}), 200

# Función para obtener el tipo de cambio (API externa)
def obtener_tipo_cambio(base="ARS", destino="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{destino}"  # Base en USD
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            tipo_cambio = datos["rates"].get(base)
            if tipo_cambio:
                return tipo_cambio  # Regresa ARS/USD directamente
            else:
                print(f"No se encontró el tipo de cambio para {base}.")
                return None
        else:
            print(f"Error al acceder a la API: Código {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return None




# Ruta para generar el reporte en CSV (GET)
@app.route('/reportes', methods=['GET'])
def generar_reporte():
    inventario = Inventario()
    inventario.generar_reporte_csv()
    return jsonify({"message": "Reporte generado con éxito como 'reporte_productos.csv'"}), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    init_db()  # Inicializar la base de datos
    app.run(debug=True, port=5021)

