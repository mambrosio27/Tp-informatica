import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV generado
nombre_archivo = 'reporte_productos.csv'
df = pd.read_csv(nombre_archivo)

# Mostrar los datos del CSV
print("Datos del CSV:")
print(df)

# Análisis 1: Gráfico del stock de productos
plt.figure(figsize=(10, 6))
df.plot(kind='bar', x='Nombre', y='Stock', title='Stock de Productos')
plt.xlabel('Productos')
plt.ylabel('Cantidad en Stock')
plt.title('Stock por Producto')
plt.tight_layout()
plt.show()

# Análisis 2: Precio promedio en ARS y USD
precio_promedio_ars = df['Precio (ARS)'].mean()
precio_promedio_usd = df['Precio (USD)'].mean()

print(f"\nPrecio promedio en ARS: {precio_promedio_ars:.2f}")
print(f"Precio promedio en USD: {precio_promedio_usd:.2f}")

