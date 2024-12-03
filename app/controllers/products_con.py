import mysql.connector


class ProductCRUD:
    def __init__(self, host="localhost", user="root", password="", database="sistemainventario"):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }

    def load_all_products(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_producto, nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio 
                FROM productos;
            """)
            products = cursor.fetchall()
            connection.close()
            return products
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def add_product(self, nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                INSERT INTO productos (nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio))
            connection.commit()
            connection.close()
            print("Producto agregado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def edit_product(self, product_id, nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                UPDATE productos 
                SET nombre_producto = %s, categoria = %s, fecha_ingreso = %s, fecha_vencimiento = %s, cantidad = %s, precio = %s
                WHERE id_producto = %s;
            """
            cursor.execute(query, (nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio, product_id))
            connection.commit()
            connection.close()
            print(f"Producto con ID {product_id} actualizado.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_product(self, product_id):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = %s;", (product_id,))
            connection.commit()
            connection.close()
            print(f"Producto con ID {product_id} eliminado.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def search_product(self, search_text):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                SELECT id_producto, nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio
                FROM productos
                WHERE id_producto LIKE %s OR nombre_producto LIKE %s OR categoria LIKE %s OR cantidad LIKE %s OR precio LIKE %s;
            """
            like_text = f"%{search_text}%"
            cursor.execute(query, (like_text, like_text, like_text, like_text, like_text))
            products = cursor.fetchall()
            connection.close()
            return products
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
