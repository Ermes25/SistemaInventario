import mysql.connector


class SupplierCRUD:
    def __init__(self, host="localhost", user="root", password="", database="sistemainventario"):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
        }

    def load_all_providers(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT id_proveedor, nombre_proveedor, numero_proveedor, email FROM proveedores;")
            providers = cursor.fetchall()
            connection.close()
            return providers
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def add_provider(self, nombre, numero, email):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                INSERT INTO proveedores (nombre_proveedor, numero_proveedor, email)
                VALUES (%s, %s, %s);
            """
            cursor.execute(query, (nombre, numero, email))
            connection.commit()
            connection.close()
            print("Proveedor agregado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def edit_provider(self, provider_id, nombre, numero, email):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                UPDATE proveedores
                SET nombre_proveedor = %s, numero_proveedor = %s, email = %s
                WHERE id_proveedor = %s;
            """
            cursor.execute(query, (nombre, numero, email, provider_id))
            connection.commit()
            connection.close()
            print("Proveedor actualizado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_provider(self, provider_id):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = "DELETE FROM proveedores WHERE id_proveedor = %s;"
            cursor.execute(query, (provider_id,))
            connection.commit()
            connection.close()
            print("Proveedor eliminado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def search_provider(self, search_text):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            query = """
                SELECT id_proveedor, nombre_proveedor, numero_proveedor, email
                FROM proveedores
                WHERE id_proveedor LIKE %s
                OR nombre_proveedor LIKE %s
                OR numero_proveedor LIKE %s
                OR email LIKE %s;
            """
            like_text = f"%{search_text}%"
            cursor.execute(query, (like_text, like_text, like_text, like_text))
            providers = cursor.fetchall()
            connection.close()
            return providers
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
