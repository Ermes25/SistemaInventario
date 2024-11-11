import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QLabel, QMessageBox)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt, QSize
import mysql.connector  # Asegúrate de tener mysql-connector instalado

# Clase para manejar la conexión a la base de datos
class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.cursor = None
        self.connect(host, user, password, database)

    def connect(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            QMessageBox.critical(None, "Error", f"Error de conexión: {e}")
            sys.exit(1)

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            QMessageBox.critical(None, "Error", f"Error al ejecutar la consulta: {e}")
            return []

class InventoryProducts(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Productos")
        self.setFixedSize(1366, 768)  # Dimensiones para laptop

        # Conexión a la base de datos al inicio
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        self.db = DatabaseConnection(**self.db_config)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal con márgenes amplios
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(100, 50, 100, 50)

        # Frame contenedor
        self.container_frame = QFrame()
        self.set_frame_style("#FFFFFF")  # Estilo inicial del marco
        container_layout = QVBoxLayout(self.container_frame)
        container_layout.setSpacing(30)

        # Título
        title_label = self.create_title("Gestión de Productos")
        container_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir imagen entre el título y los botones
        image_label = QLabel()
        image_pixmap = QPixmap("images/model_icons/productos_crud.png")  # Asegúrate de usar la ruta correcta
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(image_label)

        # Layout para la primera fila de botones
        first_row = QHBoxLayout()
        first_row.setSpacing(20)

        buttons_row1 = [
            ("Agregar", "#4CAF50", "app/images/Crud/create.png", self.crearProducto),
            ("Editar", "#2196F3", "app/images/Crud/Update.png", self.editarProducto),
            ("Eliminar", "#F44336", "app/images/Crud/Delete.png", self.eliminarProducto),
            ("Mostrar Todos", "#9C27B0", "app/images/Crud/show.png", self.mostrarProductos),
        ]

        for text, color, icon_path, action in buttons_row1:
            button = self.create_button(text, color, icon_path)
            button.clicked.connect(action)
            first_row.addWidget(button)

        # Layout para la segunda fila de botones
        second_row = QHBoxLayout()
        second_row.setSpacing(20)

        buttons_row2 = [
            ("Buscar", "#757575", "app/images/Crud/Search.png", self.buscarProducto),
            ("Refrescar", "#FFC107", "app/images/Crud/Refresh.png", self.refrescar),
            ("Regresar al Menú", "#757575", "app/images/Crud/Return.png", self.regresarMenu),
        ]

        for text, color, icon_path, action in buttons_row2:
            button = self.create_button(text, color, icon_path)
            button.clicked.connect(action)
            second_row.addWidget(button)

        # Botones para cambiar la paleta de colores (sin etiquetas)
        color_button_row = QHBoxLayout()
        color_button_row.setSpacing(20)

        color_buttons = [
            ("Rosado Claro", "#FFB6C1"),  # Color rosado claro
            ("Verde Claro", "#90EE90"),  # Color verde claro
            ("Lila Llamativo", "#8A2BE2"),  # Color lila vibrante
            ("Blanco", "#FFFFFF"),  # Botón para regresar al color blanco
        ]

        for _, color in color_buttons:
            button = QPushButton()
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    border-radius: 20px;  /* Hacer botones circulares */
                    width: 40px;  /* Tamaño pequeño */
                    height: 40px;  /* Tamaño pequeño */
                }}
            """)
            button.clicked.connect(lambda checked, c=color: self.set_frame_style(c))  # Cambiar el color del marco
            color_button_row.addWidget(button)

        # Añadir las filas al contenedor
        container_layout.addLayout(first_row)
        container_layout.addLayout(second_row)
        container_layout.addLayout(color_button_row)

        # Centrar la fila de botones de colores
        color_button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir el marco contenedor al diseño principal
        self.main_layout.addWidget(self.container_frame)

    def set_frame_style(self, color):
        """Configura el estilo del marco según el color seleccionado."""
        self.container_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color};  /* Color seleccionado */
                border-radius: 20px;
                padding: 30px;
            }}
        """)

    def create_title(self, text):
        title_label = QLabel(text)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: black;")  # Cambiar color del texto a negro
        return title_label

    def create_button(self, text, color, icon_path):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-family: Arial;  /* Asegurarse de que la fuente sea Arial */
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        button.setIcon(QIcon(icon_path))  # Usa la ruta correcta para el ícono
        button.setIconSize(QSize(24, 24))
        return button

    def darken_color(self, color):
        """Función para oscurecer el color para el efecto hover."""
        hex_color = color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(c - 30, 0) for c in rgb)  # Oscurecer el color
        return f"#{''.join(f'{c:02x}' for c in darkened_rgb)}"

    def crearProducto(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import CrearProducto
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.crearprod = CrearProducto(ProductosController)
        self.crearprod.show()
        self.close()
        
    def editarProducto(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import EditarProducto
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.ediprod = EditarProducto(ProductosController)
        self.ediprod.show()
        self.close()

    def eliminarProducto(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import EliminarProducto
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.eliprod = EliminarProducto(ProductosController)
        self.eliprod.show()
        self.close()

    def mostrarProductos(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import VerProductos
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.VerPro = VerProductos(ProductosController)
        self.VerPro.show()
        self.close()

    def buscarProducto(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import BuscarProductoPorID
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.bidprod = BuscarProductoPorID(ProductosController)
        self.bidprod.show()
        self.close()

    def refrescar(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        from app.controllers.crud_productos import DatabaseRefresher
        from app.controllers.crud_productos import ProductosController
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sistemainventario'
        }
        db = DatabaseConnection(**db_config)
        self.refresprod = DatabaseRefresher(ProductosController)
        self.refresprod.show()
        self.close()

    def regresarMenu(self):
        from Dashboard import Dashboard
        self.regresarProd = Dashboard()
        self.regresarProd.show()
        self.close()

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryProducts()
    window.show()
    sys.exit(app.exec())
