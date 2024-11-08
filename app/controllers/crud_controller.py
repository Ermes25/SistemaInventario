import mysql.connector
from utils.database import Conexion

class ConProducto:
    def __init__(self, conexion):
        self.conexion = conexion
    def obtener_conexion():
        return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistemainventario"
    )

    def insert(self, datos_producto):
        try:
            cursor = self.conexion.cursor()
            query = """
                INSERT INTO productos (nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos_producto["nombre_producto"],
                datos_producto["categoria"],
                datos_producto["fecha_ingreso"],
                datos_producto["fecha_vencimiento"],
                datos_producto["cantidad"],
                datos_producto["precio"],
            )
            cursor.execute(query, valores)
            self.conexion.commit()
            cursor.close()  # Asegúrate de cerrar el cursor después
        except Exception as e:
            raise Exception(f"Error al insertar el producto: {e}")

    def update(self, producto):
        try:
            cursor = self.conexion.cursor()
            # Actualizamos todos los campos relevantes
            query = """
                UPDATE productos
                SET nombre_producto=%s, categoria=%s, fecha_vencimiento=%s, cantidad=%s, precio=%s
                WHERE id_producto=%s
            """
            cursor.execute(query, (producto.nombre, producto.categoria, producto.fecha_vencimiento, producto.cantidad, producto.precio, producto.id))
            self.conexion.commit()
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            self.conexion.rollback()  # Revertir si ocurre un error

    def delete(self, producto_id):
        try:
            cursor = self.conexion.cursor()
            query = "DELETE FROM productos WHERE id_producto=%s"
            cursor.execute(query, (producto_id,))
            self.conexion.commit()
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            self.conexion.rollback()  # Revertir si ocurre un error

    def get_all(self):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT * FROM productos"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todos los productos: {e}")
            return []

    def get_by_id(self, producto_id):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT * FROM productos WHERE id_producto=%s"
            cursor.execute(query, (producto_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener producto por ID: {e}")
            return None

class ConPedido:
    def __init__(self, conexion):
        self.conexion = conexion

    def get_all(self):
        """Obtener todos los pedidos."""
        query = 'SELECT * FROM pedidos'
        return self.conexion.execute_read_query(query, ())

    def get_by_id(self, id_pedido):
        """Obtener un pedido por su ID."""
        query = 'SELECT * FROM pedidos WHERE id_pedido = %s'
        return self.conexion.execute_read_query(query, (id_pedido,))

    def insert(self, pedido):
        """Insertar un nuevo pedido."""
        query = 'INSERT INTO pedidos (nombre_cliente, id_producto, id_proveedor, cantidad_pedido) VALUES (%s, %s, %s, %s)'
        return self.conexion.execute_query(query, (
            pedido.nombre_cliente,
            pedido.id_producto,
            pedido.id_proveedor,
            pedido.cantidad_pedido
        ))

    def update(self, pedido):
        """Actualizar un pedido existente."""
        query = 'UPDATE pedidos SET nombre_cliente = %s, id_producto = %s, id_proveedor = %s, cantidad_pedido = %s WHERE id_pedido = %s'
        return self.conexion.execute_query(query, (
            pedido.nombre_cliente,
            pedido.id_producto,
            pedido.id_proveedor,
            pedido.cantidad_pedido,
            pedido.id_pedido
        ))

    def delete(self, id_pedido):
        """Eliminar un pedido por su ID."""
        query = 'DELETE FROM pedidos WHERE id_pedido = %s'
        return self.conexion.execute_query(query, (id_pedido,))
