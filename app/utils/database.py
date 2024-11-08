import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None
        self.connect()

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.cnx.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.cnx = None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            print("Conexión cerrada.")

    def execute_query(self, query, params=None):
        """Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE)."""
        if self.cnx is None:
            print("No hay conexión a la base de datos.")
            return
        cursor = self.cnx.cursor()
        try:
            cursor.execute(query, params)
            self.cnx.commit()
            print("Consulta ejecutada con éxito.")
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()

    def execute_read_query(self, query, params=None):
        """Ejecuta una consulta de lectura (SELECT)."""
        if self.cnx is None:
            print("No hay conexión a la base de datos.")
            return []
        cursor = self.cnx.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al ejecutar la consulta de lectura: {e}")
            return []
        finally:
            cursor.close()

    def authenticate_user(self, username, password):
        """Verifica si las credenciales son correctas en la base de datos."""
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        params = (username, password)
        result = self.execute_read_query(query, params)
        return len(result) > 0  # Si hay resultados, las credenciales son correctas
