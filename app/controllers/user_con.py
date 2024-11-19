import mysql.connector

class CRUDUsuarios:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "sistemainventario",
        }

    def connect_db(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return None

    def get_all_users(self):
        try:
            connection = self.connect_db()
            if connection is None:
                return []

            cursor = connection.cursor()
            cursor.execute("SELECT id, username, password FROM usuarios;")
            users = cursor.fetchall()
            connection.close()
            return users
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_user_by_id(self, user_id):
        try:
            connection = self.connect_db()
            if connection is None:
                return None

            cursor = connection.cursor()
            cursor.execute("SELECT id, username, password FROM usuarios WHERE id = %s;", (user_id,))
            user = cursor.fetchone()
            connection.close()
            return user
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def add_user(self, username, password):
        try:
            connection = self.connect_db()
            if connection is None:
                return False

            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (%s, %s);",
                (username, password)
            )
            connection.commit()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    def search_user(self, search_term):
        try:
            connection = self.connect_db()
            if connection is None:
                return []

            cursor = connection.cursor()
            query = "SELECT id, username, password FROM usuarios WHERE username LIKE %s OR id LIKE %s;"
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
            users = cursor.fetchall()
            connection.close()
            return users
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def update_user(self, user_id, username, password):
        try:
            connection = self.connect_db()
            if connection is None:
                return False

            cursor = connection.cursor()
            query = "UPDATE usuarios SET username = %s, password = %s WHERE id = %s;"
            cursor.execute(query, (username, password, user_id))
            connection.commit()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    def delete_user(self, user_id):
        try:
            connection = self.connect_db()
            if connection is None:
                return False

            cursor = connection.cursor()
            query = "DELETE FROM usuarios WHERE id = %s;"
            cursor.execute(query, (user_id,))
            connection.commit()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
