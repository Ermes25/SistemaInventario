import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QLineEdit, QFormLayout, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal
import mysql.connector

# --- Conexión a la base de datos ---
class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

# --- Controlador de proveedores ---
class ProveedoresController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_proveedores(self):
        query = "SELECT * FROM proveedores"
        return self.db_connection.fetch_all(query)

    def obtener_proveedor_por_id(self, id_proveedor):
        query = "SELECT * FROM proveedores WHERE id_proveedor = %s"
        return self.db_connection.fetch_all(query, (id_proveedor,))

    def agregar_proveedor(self, nombre, numero, email):
        query = "INSERT INTO proveedores (nombre_proveedor, numero_proveedor, email) VALUES (%s, %s, %s)"
        self.db_connection.execute(query, (nombre, numero, email))

    def editar_proveedor(self, id_proveedor, nombre, numero, email):
        query = "UPDATE proveedores SET nombre_proveedor = %s, numero_proveedor = %s, email = %s WHERE id_proveedor = %s"
        self.db_connection.execute(query, (nombre, numero, email, id_proveedor))

    def eliminar_proveedor(self, id_proveedor):
        query = "DELETE FROM proveedores WHERE id_proveedor = %s"
        self.db_connection.execute(query, (id_proveedor,))

    def refrescar_base_de_datos(self):
        return "Base de datos refrescada correctamente."

# --- Ventanas para CRUD de Proveedores ---
class CrearProveedor(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Crear Proveedor")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.nombre_input = QLineEdit(self)
        self.numero_input = QLineEdit(self)
        self.email_input = QLineEdit(self)

        self.form_layout.addRow("Nombre:", self.nombre_input)
        self.form_layout.addRow("Número:", self.numero_input)
        self.form_layout.addRow("Correo:", self.email_input)

        layout.addLayout(self.form_layout)

        self.btn_guardar = QPushButton("Guardar", self)
        self.btn_guardar.clicked.connect(self.guardar_proveedor)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_proveedor(self):
        nombre = self.nombre_input.text()
        numero = self.numero_input.text()
        email = self.email_input.text()

        if not nombre or not numero or not email:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, rellene todos los campos.")
            return

        try:
            self.proveedores_controller.agregar_proveedor(nombre, numero, email)
            QMessageBox.information(self, "Proveedor Guardado", "Proveedor creado exitosamente.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar el proveedor: {e}")

class EditarProveedor(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.id_proveedor = None  # Al principio no tenemos un ID
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Proveedor")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Campo de búsqueda por ID
        self.id_buscar_input = QLineEdit(self)
        self.id_buscar_input.setPlaceholderText("Buscar proveedor por ID")
        self.form_layout.addRow("ID Proveedor:", self.id_buscar_input)

        self.nombre_input = QLineEdit(self)
        self.numero_input = QLineEdit(self)
        self.email_input = QLineEdit(self)

        self.form_layout.addRow("Nombre:", self.nombre_input)
        self.form_layout.addRow("Número:", self.numero_input)
        self.form_layout.addRow("Correo:", self.email_input)

        layout.addLayout(self.form_layout)

        # Botón para cargar el proveedor
        self.btn_cargar = QPushButton("Cargar Proveedor", self)
        self.btn_cargar.clicked.connect(self.cargar_proveedor)
        layout.addWidget(self.btn_cargar)

        # Botón para editar el proveedor
        self.btn_editar = QPushButton("Editar Proveedor", self)
        self.btn_editar.clicked.connect(self.editar_proveedor)
        layout.addWidget(self.btn_editar)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.close)
        layout.addWidget(self.btn_regresar)

        self.setLayout(layout)

    def cargar_proveedor(self):
        # Obtenemos el ID del proveedor desde el campo de búsqueda
        id_proveedor = self.id_buscar_input.text()

        if id_proveedor:
            proveedor = self.proveedores_controller.obtener_proveedor_por_id(id_proveedor)
            if proveedor:
                proveedor = proveedor[0]  # Tomamos el primer resultado
                self.id_proveedor = proveedor['id_proveedor']
                self.nombre_input.setText(proveedor['nombre_proveedor'])
                self.numero_input.setText(proveedor['numero_proveedor'])
                self.email_input.setText(proveedor['email'])
            else:
                QMessageBox.warning(self, "Proveedor No Encontrado", "No se encontró el proveedor con ese ID.")
        else:
            QMessageBox.warning(self, "ID Vacío", "Por favor, ingrese un ID de proveedor.")

    def editar_proveedor(self):
        # Verificar que un proveedor haya sido cargado
        if not self.id_proveedor:
            QMessageBox.warning(self, "Proveedor No Cargado", "Por favor, cargue un proveedor primero.")
            return

        # Verificar que los campos no estén vacíos
        nombre = self.nombre_input.text()
        numero = self.numero_input.text()
        email = self.email_input.text()

        if not nombre or not numero or not email:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, rellene todos los campos.")
            return

        try:
            # Guardamos los cambios en la base de datos
            self.proveedores_controller.editar_proveedor(self.id_proveedor, nombre, numero, email)
            QMessageBox.information(self, "Proveedor Editado", "Proveedor actualizado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar el proveedor: {e}")

class EliminarProveedor(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Eliminar Proveedor")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID Proveedor', 'Nombre', 'Número', 'Correo'])

        layout.addWidget(self.table)

        self.btn_eliminar = QPushButton("Eliminar", self)
        self.btn_eliminar.clicked.connect(self.eliminar_proveedor)
        layout.addWidget(self.btn_eliminar)

        self.setLayout(layout)

        self.cargar_proveedores()

    def cargar_proveedores(self):
        proveedores = self.proveedores_controller.obtener_proveedores()
        self.table.setRowCount(0)

        for proveedor in proveedores:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(proveedor['id_proveedor'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(proveedor['nombre_proveedor']))
            self.table.setItem(row_position, 2, QTableWidgetItem(proveedor['numero_proveedor']))
            self.table.setItem(row_position, 3, QTableWidgetItem(proveedor['email']))

    def eliminar_proveedor(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selección Vacía", "Selecciona un proveedor para eliminar.")
            return

        id_proveedor = self.table.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar al proveedor con ID {id_proveedor}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                self.proveedores_controller.eliminar_proveedor(id_proveedor)
                QMessageBox.information(self, "Proveedor Eliminado", "Proveedor eliminado exitosamente.")
                self.cargar_proveedores()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar el proveedor: {e}")

class RefrescarBaseDeDatos(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Refrescar Base de Datos")
        self.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        self.btn_refrescar = QPushButton("Refrescar", self)
        self.btn_refrescar.clicked.connect(self.refrescar_base_de_datos)
        layout.addWidget(self.btn_refrescar)

        self.setLayout(layout)

    def refrescar_base_de_datos(self):
        mensaje = self.proveedores_controller.refrescar_base_de_datos()
        QMessageBox.information(self, "Refrescado", mensaje)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class MostrarProveedores(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mostrar Proveedores")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        # Tabla para mostrar los proveedores
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Número", "Correo"])
        layout.addWidget(self.table)

        # Botón para cargar todos los proveedores
        self.btn_cargar = QPushButton("Cargar Todos los Proveedores", self)
        self.btn_cargar.clicked.connect(self.cargar_proveedores)
        layout.addWidget(self.btn_cargar)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.close)
        layout.addWidget(self.btn_regresar)

        self.setLayout(layout)

    def cargar_proveedores(self):
        """Cargar todos los proveedores en la tabla"""
        try:
            proveedores = self.proveedores_controller.obtener_proveedores()
            if not proveedores:
                QMessageBox.information(self, "Sin Proveedores", "No hay proveedores registrados.")
                return

            self.table.setRowCount(0)  # Limpiar la tabla antes de cargar nuevos datos

            for proveedor in proveedores:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                self.table.setItem(row_position, 0, QTableWidgetItem(str(proveedor['id_proveedor'])))
                self.table.setItem(row_position, 1, QTableWidgetItem(proveedor['nombre_proveedor']))
                self.table.setItem(row_position, 2, QTableWidgetItem(proveedor['numero_proveedor']))
                self.table.setItem(row_position, 3, QTableWidgetItem(proveedor['email']))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar proveedores: {e}")
class BuscarProveedorPorID(QWidget):
    def __init__(self, proveedores_controller):
        super().__init__()
        self.proveedores_controller = proveedores_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Buscar Proveedor por ID")
        self.setGeometry(150, 150, 400, 250)

        layout = QVBoxLayout()

        # Formulario para ingresar el ID del proveedor
        self.form_layout = QFormLayout()
        self.id_input = QLineEdit(self)
        self.form_layout.addRow("ID del Proveedor:", self.id_input)

        layout.addLayout(self.form_layout)

        # Botón para buscar proveedor
        self.btn_buscar = QPushButton("Buscar Proveedor", self)
        self.btn_buscar.clicked.connect(self.buscar_proveedor)
        layout.addWidget(self.btn_buscar)

        # Tabla para mostrar los detalles del proveedor
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Número", "Correo"])
        layout.addWidget(self.table)

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.clicked.connect(self.close)
        layout.addWidget(self.btn_regresar)

        self.setLayout(layout)

    def buscar_proveedor(self):
        """Buscar proveedor por ID y mostrar los detalles en la tabla"""
        id_proveedor = self.id_input.text()

        if not id_proveedor:
            QMessageBox.warning(self, "ID Vacío", "Por favor, ingrese un ID de proveedor.")
            return

        try:
            proveedor = self.proveedores_controller.obtener_proveedor_por_id(id_proveedor)
            if proveedor:
                proveedor = proveedor[0]  # Tomamos el primer resultado
                self.mostrar_detalles_proveedor(proveedor)
            else:
                QMessageBox.warning(self, "Proveedor No Encontrado", "No se encontró el proveedor con el ID proporcionado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar el proveedor: {e}")

    def mostrar_detalles_proveedor(self, proveedor):
        """Mostrar los detalles del proveedor en la tabla"""
        self.table.setRowCount(0)  # Limpiar la tabla antes de mostrar los nuevos datos

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(proveedor['id_proveedor'])))
        self.table.setItem(row_position, 1, QTableWidgetItem(proveedor['nombre_proveedor']))
        self.table.setItem(row_position, 2, QTableWidgetItem(proveedor['numero_proveedor']))
        self.table.setItem(row_position, 3, QTableWidgetItem(proveedor['email']))
# --- Aplicación principal ---
def main():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'sistemainventario'
    }
    db = DatabaseConnection(**db_config)
    proveedores_controller = ProveedoresController(db)

    app = QApplication(sys.argv)

    ventana = BuscarProveedorPorID(proveedores_controller)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()