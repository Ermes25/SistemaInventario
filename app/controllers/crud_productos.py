import sys
import mysql.connector
from mysql.connector import Error
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QComboBox, QDateEdit, QMessageBox
from PyQt6.QtCore import Qt, QDate

# Clase para la conexión a la base de datos
class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def execute_query(self, query, params=None):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return []

# Clase para manejar operaciones CRUD sobre los productos
class ProductosController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # Crear producto
    def crear_producto(self, nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio):
        query = """
            INSERT INTO productos (nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db_connection.execute_query(query, (nombre_producto, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio))

    # Obtener todos los productos
    def mostrar_productos(self):
        query = "SELECT * FROM productos"
        return self.db_connection.execute_query(query)

    # Buscar producto por ID
    def buscar_producto_por_id(self, producto_id):
        query = "SELECT * FROM productos WHERE id_producto = %s"
        return self.db_connection.execute_query(query, (producto_id,))

    # Editar producto
    def editar_producto(self, producto_id, nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio):
        query = """
            UPDATE productos
            SET nombre_producto = %s, categoria = %s, fecha_ingreso = %s, fecha_vencimiento = %s, cantidad = %s, precio = %s
            WHERE id_producto = %s
        """
        self.db_connection.execute_query(query, (nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio, producto_id))

    # Eliminar producto
    def eliminar_producto(self, producto_id):
        query = "DELETE FROM productos WHERE id_producto = %s"
        self.db_connection.execute_query(query, (producto_id,))
    # Refrescar la base de datos (usando DatabaseRefresher)
    def refrescar_base_datos(self):
        """
        Refresca la base de datos y muestra un mensaje en caso de éxito o error.
        """
        if self.refresher.refresh():
            print("La base de datos se ha refrescado exitosamente.")
        else:
            print("No se pudo refrescar la base de datos.")
# Clase para crear un producto
class CrearProducto(QWidget):
    def __init__(self, productos_controller):
        super().__init__()
        self.productos_controller = productos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Crear Producto")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Campo para nombre del producto
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre del Producto")
        layout.addWidget(self.nombre_input)

        # ComboBox para la categoría
        self.categoria_input = QComboBox(self)
        self.categoria_input.addItems(["Electrónica", "Ropa", "Alimentos", "Otros"])
        layout.addWidget(self.categoria_input)

        # Fecha de ingreso
        self.fecha_ingreso_input = QDateEdit(self)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_ingreso_input)

        # Fecha de vencimiento
        self.fecha_vencimiento_input = QDateEdit(self)
        self.fecha_vencimiento_input.setDate(QDate.currentDate().addYears(1))
        layout.addWidget(self.fecha_vencimiento_input)

        # Campo para cantidad
        self.cantidad_input = QLineEdit(self)
        self.cantidad_input.setPlaceholderText("Cantidad")
        layout.addWidget(self.cantidad_input)

        # Campo para precio
        self.precio_input = QLineEdit(self)
        self.precio_input.setPlaceholderText("Precio")
        layout.addWidget(self.precio_input)

        # Botón para crear producto
        self.btn_crear = QPushButton("Crear Producto", self)
        self.btn_crear.clicked.connect(self.crear_producto)
        layout.addWidget(self.btn_crear)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        layout.addWidget(self.btn_regresar)

        # Configurar el layout
        self.setLayout(layout)

    def crear_producto(self):
        nombre = self.nombre_input.text()
        categoria = self.categoria_input.currentText()
        fecha_ingreso = self.fecha_ingreso_input.date().toString("yyyy-MM-dd")
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString("yyyy")
        cantidad = self.cantidad_input.text()
        precio = self.precio_input.text()

        # Validar los campos
        if not nombre or not cantidad or not precio:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        try:
            self.productos_controller.crear_producto(nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio)
            QMessageBox.information(self, "Producto Creado", "El producto se ha creado exitosamente.")
            self.close()
            self.__init__(self.productos_controller)  # Recargar la ventana
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear el producto: {e}")
# Clase para mostrar productos
class VerProductos(QWidget):
    def __init__(self, productos_controller):
        super().__init__()
        self.productos_controller = productos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ver Productos")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Tabla para mostrar productos
        self.tabla_productos = QTableWidget(self)
        self.tabla_productos.setColumnCount(7)
        self.tabla_productos.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Categoría", "Fecha Ingreso", "Fecha Vencimiento", "Cantidad", "Precio"]
        )
        self.tabla_productos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla_productos)

        # Botón para cargar productos
        self.btn_cargar = QPushButton("Cargar Productos", self)
        self.btn_cargar.clicked.connect(self.cargar_productos)
        layout.addWidget(self.btn_cargar)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        layout.addWidget(self.btn_regresar)

        # Configurar layout
        self.setLayout(layout)

        # Cargar productos al abrir la ventana
        self.cargar_productos()

    def cargar_productos(self):
        productos = self.productos_controller.mostrar_productos()
        self.tabla_productos.setRowCount(len(productos))
        for row, producto in enumerate(productos):
            for col, dato in enumerate(producto):
                self.tabla_productos.setItem(row, col, QTableWidgetItem(str(dato)))
# Clase para buscar un producto por ID
class BuscarProductoPorID(QWidget):
    def __init__(self, productos_controller):
        super().__init__()
        self.productos_controller = productos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Buscar Producto por ID")
        self.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        # Campo para ingresar el ID del producto
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Ingrese el ID del producto")
        layout.addWidget(self.id_input)

        # Botón para buscar el producto
        self.btn_buscar = QPushButton("Buscar Producto")
        self.btn_buscar.clicked.connect(self.buscar_producto)
        layout.addWidget(self.btn_buscar)

        # Crear la tabla para mostrar los detalles
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(self.btn_regresar)

        # Configurar el layout
        self.setLayout(layout)

    def buscar_producto(self):
        producto_id = self.id_input.text()
        if not producto_id:
            QMessageBox.warning(self, "ID vacío", "Por favor ingresa un ID válido.")
            return

        try:
            producto = self.productos_controller.buscar_producto_por_id(producto_id)
            if not producto:
                QMessageBox.warning(self, "Producto no encontrado", f"No se encontró un producto con ID {producto_id}.")
                return

            # Mostrar los resultados en la tabla
            self.table.setRowCount(1)
            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels([
                "Nombre", "Categoría", "Fecha Ingreso", 
                "Fecha Vencimiento", "Cantidad", "Precio"
            ])

            for col, value in enumerate(producto[0][1:]):  # Omite el ID
                self.table.setItem(0, col, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar el producto: {e}")

    def regresar(self):
        self.close()

# Clase para eliminar un producto
class EliminarProducto(QWidget):
    def __init__(self, productos_controller):
        super().__init__()
        self.productos_controller = productos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eliminar Producto")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        # Campo para ID del producto
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID del Producto")
        layout.addWidget(self.id_input)

        # Botón para eliminar producto
        self.btn_eliminar = QPushButton("Eliminar Producto", self)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        layout.addWidget(self.btn_eliminar)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        layout.addWidget(self.btn_regresar)

        # Configurar layout
        self.setLayout(layout)

    def eliminar_producto(self):
        producto_id = self.id_input.text()

        if not producto_id:
            QMessageBox.warning(self, "Campo Vacío", "Por favor, ingrese el ID del producto.")
            return

        try:
            self.productos_controller.eliminar_producto(producto_id)
            QMessageBox.information(self, "Producto Eliminado", "El producto se ha eliminado exitosamente.")
            self.close()
            self.__init__(self.productos_controller)  # Recargar la ventana
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el producto: {e}")
        

class EditarProducto(QWidget):
    def __init__(self, productos_controller):
        super().__init__()
        self.productos_controller = productos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Producto")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Campo para ID del producto
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID del Producto")
        layout.addWidget(self.id_input)

        # Campo para nombre del producto
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nuevo Nombre del Producto")
        layout.addWidget(self.nombre_input)

        # ComboBox para la categoría
        self.categoria_input = QComboBox(self)
        self.categoria_input.addItems(["Electrónica", "Ropa", "Alimentos", "Otros"])
        layout.addWidget(self.categoria_input)

        # Fecha de ingreso
        self.fecha_ingreso_input = QDateEdit(self)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        layout.addWidget(self.fecha_ingreso_input)

        # Fecha de vencimiento
        self.fecha_vencimiento_input = QDateEdit(self)
        self.fecha_vencimiento_input.setDate(QDate.currentDate().addYears(1))
        layout.addWidget(self.fecha_vencimiento_input)

        # Campo para cantidad
        self.cantidad_input = QLineEdit(self)
        self.cantidad_input.setPlaceholderText("Nueva Cantidad")
        layout.addWidget(self.cantidad_input)

        # Campo para precio
        self.precio_input = QLineEdit(self)
        self.precio_input.setPlaceholderText("Nuevo Precio")
        layout.addWidget(self.precio_input)

        # Botón para editar producto
        self.btn_editar = QPushButton("Editar Producto", self)
        self.btn_editar.clicked.connect(self.editar_producto)
        layout.addWidget(self.btn_editar)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        layout.addWidget(self.btn_regresar)

        # Configurar layout
        self.setLayout(layout)

    def editar_producto(self):
        producto_id = self.id_input.text()
        nombre = self.nombre_input.text()
        categoria = self.categoria_input.currentText()
        fecha_ingreso = self.fecha_ingreso_input.date().toString("yyyy-MM-dd")
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString("yyyy")
        cantidad = self.cantidad_input.text()
        precio = self.precio_input.text()

        # Validar los campos
        if not producto_id or not nombre or not cantidad or not precio:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        try:
            self.productos_controller.editar_producto(producto_id, nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio)
            QMessageBox.information(self, "Producto Editado", "El producto se ha editado exitosamente.")
            self.close()
            self.__init__(self.productos_controller)  # Recargar la ventana
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar el producto: {e}")
class DatabaseRefresher:
    def __init__(self, db_connection):
        """
        Inicializa el refrescador con una conexión a la base de datos.
        """
        self.db_connection = db_connection

    def refresh(self):
        """
        Refresca la base de datos realizando una operación de consulta.
        """
        try:
            cursor = self.db_connection.cursor()
            # Ejecutar una consulta simple para simular el refresco
            cursor.execute("SELECT 1")  # Ajusta la consulta según lo necesario
            resultado = cursor.fetchone()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al refrescar la base de datos: {e}")
            return False
# Función principal
"""
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'sistemainventario'
    }
    db = DatabaseConnection(**db_config)
    productos_controller = ProductosController(db)

    app = QApplication(sys.argv)

    ventana = VerProductos(productos_controller)
    ventana.show()

    sys.exit(app.exec())


"""