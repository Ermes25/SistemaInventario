import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox
)
from mysql.connector import Error
import mysql.connector

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
class MostrarPedidos(QWidget):
    def __init__(self, pedidos_controller):
        super().__init__()
        self.pedidos_controller = pedidos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mostrar Pedidos")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Tabla para mostrar los pedidos
        self.table_pedidos = QTableWidget(self)
        self.table_pedidos.setColumnCount(5)  # 5 columnas: ID, Producto, Proveedor, Cantidad, Fecha
        self.table_pedidos.setHorizontalHeaderLabels(['ID Pedido', 'Producto', 'Proveedor', 'Cantidad', 'Fecha'])

        layout.addWidget(self.table_pedidos)

        # Botones
        botones_layout = QHBoxLayout()

        self.btn_cargar = QPushButton("Cargar Pedidos", self)
        self.btn_cargar.clicked.connect(self.cargar_pedidos)
        botones_layout.addWidget(self.btn_cargar)

        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.regresar)
        botones_layout.addWidget(self.btn_regresar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def cargar_pedidos(self):
        """Carga los pedidos desde la base de datos en la tabla."""
        try:
            pedidos = self.pedidos_controller.obtener_pedidos()
            self.table_pedidos.setRowCount(len(pedidos))

            for row, pedido in enumerate(pedidos):
                self.table_pedidos.setItem(row, 0, QTableWidgetItem(str(pedido['id_pedido'])))
                self.table_pedidos.setItem(row, 1, QTableWidgetItem(str(pedido['producto'])))
                self.table_pedidos.setItem(row, 2, QTableWidgetItem(str(pedido['proveedor'])))
                self.table_pedidos.setItem(row, 3, QTableWidgetItem(str(pedido['cantidad_pedido'])))
                self.table_pedidos.setItem(row, 4, QTableWidgetItem(str(pedido['fecha_pedido'])))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los pedidos: {e}")

    def regresar(self):
        """Acción al presionar el botón de regresar (sin funcionalidad)."""
        pass


class EliminarPedidos(QWidget):
    def __init__(self, pedidos_controller):
        super().__init__()
        self.pedidos_controller = pedidos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eliminar Pedido")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Campo de búsqueda por ID
        search_layout = QHBoxLayout()
        self.label_buscar = QLabel("Eliminar por ID de Pedido:", self)
        self.line_edit_id = QLineEdit(self)
        self.line_edit_id.setPlaceholderText("Ingrese el ID del pedido")
        search_layout.addWidget(self.label_buscar)
        search_layout.addWidget(self.line_edit_id)

        layout.addLayout(search_layout)

        # Botones
        botones_layout = QHBoxLayout()

        self.btn_eliminar = QPushButton("Eliminar Pedido", self)
        self.btn_eliminar.clicked.connect(self.eliminar_pedido)
        botones_layout.addWidget(self.btn_eliminar)

        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.regresar)
        botones_layout.addWidget(self.btn_regresar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def eliminar_pedido(self):
        """Elimina un pedido por ID desde la base de datos."""
        id_pedido = self.line_edit_id.text()

        if not id_pedido:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingrese un ID de pedido.")
            return

        try:
            if self.pedidos_controller.eliminar_pedido(id_pedido):
                QMessageBox.information(self, "Éxito", "Pedido eliminado exitosamente.")
            else:
                QMessageBox.warning(self, "No encontrado", f"No se encontró un pedido con el ID {id_pedido}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el pedido: {e}")

    def regresar(self):
        """Acción al presionar el botón de regresar (sin funcionalidad)."""
        pass


class CrearPedidos(QWidget):
    def __init__(self, pedidos_controller):
        super().__init__()
        self.pedidos_controller = pedidos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Crear Pedido")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Formulario para crear un nuevo pedido
        self.label_producto = QLabel("Producto:", self)
        self.line_edit_producto = QLineEdit(self)
        self.label_proveedor = QLabel("Proveedor:", self)
        self.line_edit_proveedor = QLineEdit(self)
        self.label_cantidad = QLabel("Cantidad:", self)
        self.line_edit_cantidad = QLineEdit(self)
        self.label_fecha = QLabel("Fecha de Pedido:", self)
        self.line_edit_fecha = QLineEdit(self)

        layout.addWidget(self.label_producto)
        layout.addWidget(self.line_edit_producto)
        layout.addWidget(self.label_proveedor)
        layout.addWidget(self.line_edit_proveedor)
        layout.addWidget(self.label_cantidad)
        layout.addWidget(self.line_edit_cantidad)
        layout.addWidget(self.label_fecha)
        layout.addWidget(self.line_edit_fecha)

        # Botones
        botones_layout = QHBoxLayout()

        self.btn_crear = QPushButton("Crear Pedido", self)
        self.btn_crear.clicked.connect(self.crear_pedido)
        botones_layout.addWidget(self.btn_crear)

        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.regresar)
        botones_layout.addWidget(self.btn_regresar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def crear_pedido(self):
        """Crea un nuevo pedido en la base de datos."""
        producto = self.line_edit_producto.text()
        proveedor = self.line_edit_proveedor.text()
        cantidad = self.line_edit_cantidad.text()
        fecha = self.line_edit_fecha.text()

        if not producto or not proveedor or not cantidad or not fecha:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor complete todos los campos.")
            return

        try:
            if self.pedidos_controller.crear_pedido(producto, proveedor, cantidad, fecha):
                QMessageBox.information(self, "Éxito", "Pedido creado exitosamente.")
            else:
                QMessageBox.warning(self, "Error", "Hubo un problema al crear el pedido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear el pedido: {e}")

    def regresar(self):
        """Acción al presionar el botón de regresar (sin funcionalidad)."""
        pass


class BuscarPorIdPedidos(QWidget):
    def __init__(self, pedidos_controller):
        super().__init__()
        self.pedidos_controller = pedidos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Buscar Pedido por ID")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Campo de búsqueda por ID
        search_layout = QHBoxLayout()
        self.label_buscar = QLabel("Buscar por ID de Pedido:", self)
        self.line_edit_id = QLineEdit(self)
        self.line_edit_id.setPlaceholderText("Ingrese el ID del pedido")
        search_layout.addWidget(self.label_buscar)
        search_layout.addWidget(self.line_edit_id)

        layout.addLayout(search_layout)

        # Tabla para mostrar el pedido
        self.table_pedido = QTableWidget(self)
        self.table_pedido.setColumnCount(5)  # 5 columnas: ID, Producto, Proveedor, Cantidad, Fecha
        self.table_pedido.setHorizontalHeaderLabels(['ID Pedido', 'Producto', 'Proveedor', 'Cantidad', 'Fecha'])

        layout.addWidget(self.table_pedido)

        # Botones
        botones_layout = QHBoxLayout()

        self.btn_buscar = QPushButton("Buscar Pedido", self)
        self.btn_buscar.clicked.connect(self.buscar_pedido)
        botones_layout.addWidget(self.btn_buscar)

        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.regresar)
        botones_layout.addWidget(self.btn_regresar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def buscar_pedido(self):
        """Busca el pedido por ID desde la base de datos."""
        id_pedido = self.line_edit_id.text()

        if not id_pedido:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingrese un ID de pedido.")
            return

        try:
            pedido = self.pedidos_controller.obtener_pedido_por_id(id_pedido)
            if pedido:
                self.table_pedido.setRowCount(1)
                self.table_pedido.setItem(0, 0, QTableWidgetItem(str(pedido['id_pedido'])))
                self.table_pedido.setItem(0, 1, QTableWidgetItem(str(pedido['producto'])))
                self.table_pedido.setItem(0, 2, QTableWidgetItem(str(pedido['proveedor'])))
                self.table_pedido.setItem(0, 3, QTableWidgetItem(str(pedido['cantidad_pedido'])))
                self.table_pedido.setItem(0, 4, QTableWidgetItem(str(pedido['fecha_pedido'])))
            else:
                QMessageBox.warning(self, "No encontrado", f"No se encontró un pedido con el ID {id_pedido}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar el pedido: {e}")

    def regresar(self):
        """Acción al presionar el botón de regresar (sin funcionalidad)."""
        pass


class EditarPedidos(QWidget):
    def __init__(self, pedidos_controller):
        super().__init__()
        self.pedidos_controller = pedidos_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Pedido")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        # Formulario para editar un pedido
        self.label_id = QLabel("ID del Pedido:", self)
        self.line_edit_id = QLineEdit(self)
        self.label_producto = QLabel("Producto:", self)
        self.line_edit_producto = QLineEdit(self)
        self.label_proveedor = QLabel("Proveedor:", self)
        self.line_edit_proveedor = QLineEdit(self)
        self.label_cantidad = QLabel("Cantidad:", self)
        self.line_edit_cantidad = QLineEdit(self)
        self.label_fecha = QLabel("Fecha de Pedido:", self)
        self.line_edit_fecha = QLineEdit(self)

        layout.addWidget(self.label_id)
        layout.addWidget(self.line_edit_id)
        layout.addWidget(self.label_producto)
        layout.addWidget(self.line_edit_producto)
        layout.addWidget(self.label_proveedor)
        layout.addWidget(self.line_edit_proveedor)
        layout.addWidget(self.label_cantidad)
        layout.addWidget(self.line_edit_cantidad)
        layout.addWidget(self.label_fecha)
        layout.addWidget(self.line_edit_fecha)

        # Botones
        botones_layout = QHBoxLayout()

        self.btn_editar = QPushButton("Editar Pedido", self)
        self.btn_editar.clicked.connect(self.editar_pedido)
        botones_layout.addWidget(self.btn_editar)

        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.regresar)
        botones_layout.addWidget(self.btn_regresar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def editar_pedido(self):
        """Edita un pedido en la base de datos."""
        id_pedido = self.line_edit_id.text()
        producto = self.line_edit_producto.text()
        proveedor = self.line_edit_proveedor.text()
        cantidad = self.line_edit_cantidad.text()
        fecha = self.line_edit_fecha.text()

        if not id_pedido or not producto or not proveedor or not cantidad or not fecha:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor complete todos los campos.")
            return

        try:
            if self.pedidos_controller.editar_pedido(id_pedido, producto, proveedor, cantidad, fecha):
                QMessageBox.information(self, "Éxito", "Pedido editado exitosamente.")
            else:
                QMessageBox.warning(self, "Error", "Hubo un problema al editar el pedido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar el pedido: {e}")

    def regresar(self):
        """Acción al presionar el botón de regresar (sin funcionalidad)."""
        pass


class PedidosController:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def obtener_pedidos(self):
        """Obtiene todos los pedidos de la base de datos."""
        cursor = self.db_connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos")
        return cursor.fetchall()

    def eliminar_pedido(self, id_pedido):
        """Elimina un pedido por ID."""
        cursor = self.db_connector.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        self.db_connector.commit()
        return cursor.rowcount > 0

    def crear_pedido(self, producto, proveedor, cantidad, fecha):
        """Crea un nuevo pedido."""
        cursor = self.db_connector.cursor()
        cursor.execute("INSERT INTO pedidos (producto, proveedor, cantidad_pedido, fecha_pedido) VALUES (%s, %s, %s, %s)",
                       (producto, proveedor, cantidad, fecha))
        self.db_connector.commit()
        return cursor.rowcount > 0

    def obtener_pedido_por_id(self, id_pedido):
        """Obtiene un pedido por ID."""
        cursor = self.db_connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (id_pedido,))
        return cursor.fetchone()

    def editar_pedido(self, id_pedido, producto, proveedor, cantidad, fecha):
        """Edita un pedido existente."""
        cursor = self.db_connector.cursor()
        cursor.execute(
            "UPDATE pedidos SET producto = %s, proveedor = %s, cantidad_pedido = %s, fecha_pedido = %s WHERE id_pedido = %s",
            (producto, proveedor, cantidad, fecha, id_pedido)
        )
        self.db_connector.commit()
        return cursor.rowcount > 0


def main():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'sistemainventario'
    }
    db = DatabaseConnection(**db_config)
    productos_controller = PedidosController(db)

    app = QApplication(sys.argv)

    ventana = MostrarPedidos(PedidosController)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
