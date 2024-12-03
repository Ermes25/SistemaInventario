import mysql.connector

class CrudPedidos:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "sistemainventario"

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"Error al conectar con la base de datos: {err}")
            return None

    def execute_query(self, query, params):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()
                connection.close()
            except mysql.connector.Error as err:
                print(f"Error al ejecutar la consulta: {err}")
        else:
            print("No se pudo conectar a la base de datos")

    def cargar_pedidos(self):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id_pedido, id_producto, id_proveedor, fecha_pedido, cantidad_pedido FROM pedidos")
                pedidos = cursor.fetchall()
                connection.close()
                return pedidos
            except mysql.connector.Error as err:
                print(f"Error al cargar pedidos: {err}")
        return []

    def cargar_productos(self):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id_producto, nombre_producto FROM productos")
                productos = cursor.fetchall()
                connection.close()
                return productos
            except mysql.connector.Error as err:
                print(f"Error al cargar productos: {err}")
        return []

    def cargar_proveedores(self):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
                proveedores = cursor.fetchall()
                connection.close()
                return proveedores
            except mysql.connector.Error as err:
                print(f"Error al cargar proveedores: {err}")
        return []

    def obtener_nombre_producto(self, id_producto):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT nombre_producto FROM productos WHERE id_producto = %s"
                cursor.execute(query, (id_producto,))
                nombre = cursor.fetchone()
                connection.close()
                return nombre[0] if nombre else None
            except mysql.connector.Error as err:
                print(f"Error al obtener nombre de producto: {err}")
        return None

    def obtener_nombre_proveedor(self, id_proveedor):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT nombre_proveedor FROM proveedores WHERE id_proveedor = %s"
                cursor.execute(query, (id_proveedor,))
                nombre = cursor.fetchone()
                connection.close()
                return nombre[0] if nombre else None
            except mysql.connector.Error as err:
                print(f"Error al obtener nombre de proveedor: {err}")
        return None

    
    def obtener_id_producto_por_nombre(self, nombre_producto):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT id_producto FROM productos WHERE nombre_producto = %s"
                cursor.execute(query, (nombre_producto,))
                result = cursor.fetchone()
                connection.close()
                return result[0] if result else None
            except mysql.connector.Error as err:
                print(f"Error al obtener ID del producto por nombre: {err}")
        return None
    def obtener_id_producto(self, nombre_producto):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT id_producto FROM productos WHERE nombre_producto = %s"
                cursor.execute(query, (nombre_producto,))
                resultado = cursor.fetchone()
                connection.close()
                if resultado:
                    return resultado[0]  # Retorna el id del producto
                return None  # Si no se encuentra el producto
            except mysql.connector.Error as err:
                print(f"Error al obtener id de producto: {err}")
        return None

    def obtener_id_proveedor_por_nombre(self, nombre_proveedor):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT id_proveedor FROM proveedores WHERE nombre_proveedor = %s"
                cursor.execute(query, (nombre_proveedor,))
                result = cursor.fetchone()
                connection.close()
                return result[0] if result else None
            except mysql.connector.Error as err:
                print(f"Error al obtener ID del proveedor por nombre: {err}")
        return None

    def obtener_id_proveedor(self, nombre_proveedor):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT id_proveedor FROM proveedores WHERE nombre_proveedor = %s"
                cursor.execute(query, (nombre_proveedor,))
                id_proveedor = cursor.fetchone()
                connection.close()
                return id_proveedor[0] if id_proveedor else None
            except mysql.connector.Error as err:
                print(f"Error al obtener ID de proveedor: {err}")
        return None

    
    def agregar_pedido(self, id_producto, id_proveedor, fecha_pedido, cantidad_pedido):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO pedidos (id_producto, id_proveedor, fecha_pedido, cantidad_pedido) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id_producto, id_proveedor, fecha_pedido, cantidad_pedido))
                connection.commit()
                connection.close()
                return True
            except mysql.connector.Error as err:
                print(f"Error al agregar pedido: {err}")
                connection.rollback()
        return False

    
    def buscar_pedidos(self, texto_busqueda):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT p.id_pedido, pr.nombre_producto, pv.nombre_proveedor, p.fecha_pedido, p.cantidad_pedido
                    FROM pedidos p
                    LEFT JOIN productos pr ON p.id_producto = pr.id_producto
                    LEFT JOIN proveedores pv ON p.id_proveedor = pv.id_proveedor
                    WHERE pr.nombre_producto LIKE %s OR pv.nombre_proveedor LIKE %s OR p.id_pedido = %s OR p.cantidad_pedido = %s
                '''
                cursor.execute(query, (texto_busqueda, texto_busqueda, texto_busqueda, texto_busqueda))
                results = cursor.fetchall()
                connection.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error en la búsqueda de pedidos: {err}")
        return []

        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT p.id_pedido, pr.nombre_producto, pv.nombre_proveedor, p.fecha_pedido, p.cantidad_pedido
                    FROM pedidos p
                    LEFT JOIN productos pr ON p.id_producto = pr.id_producto
                    LEFT JOIN proveedores pv ON p.id_proveedor = pv.id_proveedor
                    WHERE pr.nombre_producto LIKE %s OR pv.nombre_proveedor LIKE %s OR p.id_pedido LIKE %s OR p.cantidad_pedido LIKE %s
                '''
                pattern = f"%{texto_busqueda}%"
                cursor.execute(query, (pattern, pattern, pattern, pattern))
                results = cursor.fetchall()
                connection.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error al buscar pedidos: {err}")
        return []

        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    INSERT INTO pedidos (id_producto, id_proveedor, cantidad_pedido)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (id_producto, id_proveedor, cantidad_pedido))
                connection.commit()
                connection.close()
                return True
            except mysql.connector.Error as err:
                print(f"Error al agregar pedido: {err}")
        return False

    def editar_pedido(self, id_pedido, id_producto, id_proveedor, fecha_pedido, cantidad_pedido):
        query = """
            UPDATE pedidos
            SET id_producto = %s, id_proveedor = %s, fecha_pedido = %s, cantidad_pedido = %s
            WHERE id_pedido = %s
        """
        params = (id_producto, id_proveedor, fecha_pedido, cantidad_pedido, id_pedido)
        self.execute_query(query, params)

    def eliminar_pedido(self, id_pedido):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "DELETE FROM pedidos WHERE id_pedido = %s"
                cursor.execute(query, (id_pedido,))
                connection.commit()
                connection.close()
                return True
            except mysql.connector.Error as err:
                print(f"Error al eliminar pedido: {err}")
        return False

    
    def buscar_pedidos(self, texto_busqueda):
        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = '''
                    SELECT p.id_pedido, pr.nombre_producto, pv.nombre_proveedor, p.fecha_pedido, p.cantidad_pedido
                    FROM pedidos p
                    LEFT JOIN productos pr ON p.id_producto = pr.id_producto
                    LEFT JOIN proveedores pv ON p.id_proveedor = pv.id_proveedor
                    WHERE pr.nombre_producto LIKE %s OR pv.nombre_proveedor LIKE %s OR p.id_pedido = %s OR p.cantidad_pedido = %s
                '''
                cursor.execute(query, (texto_busqueda, texto_busqueda, texto_busqueda, texto_busqueda))
                results = cursor.fetchall()
                connection.close()
                return results
            except mysql.connector.Error as err:
                print(f"Error en la búsqueda de pedidos: {err}")
        return []

        connection = self.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT id_pedido, id_producto, id_proveedor, fecha_pedido, cantidad_pedido
                    FROM pedidos
                    WHERE id_pedido LIKE %s OR id_producto LIKE %s OR id_proveedor LIKE %s OR cantidad_pedido LIKE %s
                """
                pattern = f"%{texto_busqueda}%"
                cursor.execute(query, (pattern, pattern, pattern, pattern))
                resultados = cursor.fetchall()
                connection.close()
                return resultados
            except mysql.connector.Error as err:
                print(f"Error en la búsqueda de pedidos: {err}")
        return []
