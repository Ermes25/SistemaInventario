from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QDialog
from PyQt6.QtGui import QPixmap, QFont, QIcon  # Asegúrate de importar estos módulos
from PyQt6.QtCore import Qt, QSize
from controllers.crud_products import CRUDProductoDialog  
from utils.database import Conexion
from controllers.crud_controller import ConProducto

class Inventoryproducts(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conexion = Conexion(host="localhost", user="root", password="", database="sistemainventario")
        self.setWindowTitle("Gestión de Productos")
        self.setFixedSize(1366, 768)  # Dimensiones para laptop

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
        image_pixmap = QPixmap("app/images/model_icons/productos_crud.png")  # Asegúrate de usar la ruta correcta
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(image_label)

        # Layout para la primera fila de botones
        first_row = QHBoxLayout()
        first_row.setSpacing(20)

        buttons_row1 = [
            ("Agregar", "#4CAF50", "app/images/Crud/create.png"),
            ("Editar", "#2196F3", "app/images/Crud/Update.png"),
            ("Eliminar", "#F44336", "app/images/Crud/Delete.png"),
            ("Mostrar Todos", "#9C27B0", "app/images/Crud/show.png"),
        ]

        for text, color, icon_path in buttons_row1:
            button = self.create_button(text, color, icon_path)
            if text == "Agregar":
                button.clicked.connect(self.add_product)  # Llama al método de agregar producto
            elif text == "Editar":
                button.clicked.connect(self.edit_product)  # Llama al método de editar producto
            elif text == "Eliminar":
                button.clicked.connect(self.delete_product)  # Llama al método de eliminar producto
            first_row.addWidget(button)

        # Layout para la segunda fila de botones
        second_row = QHBoxLayout()
        second_row.setSpacing(20)

        buttons_row2 = [
            ("Buscar", "#757575", "app/images/Crud/Search.png"),
            ("Refrescar", "#FFC107", "app/images/Crud/Refresh.png"),
            ("Regresar al Menú", "#757575", "app/images/Crud/Return.png"),
        ]

        for text, color, icon_path in buttons_row2:
            button = self.create_button(text, color, icon_path)
            if text == "Buscar":
                button.clicked.connect(self.search_product)  # Llama al método de buscar producto
            second_row.addWidget(button)

        # Añadir las filas al contenedor
        container_layout.addLayout(first_row)
        container_layout.addLayout(second_row)

        # Añadir el marco contenedor al diseño principal
        self.main_layout.addWidget(self.container_frame)

    def add_product(self):
        """Abrir el diálogo de 'Agregar Producto'"""
        conexion = Conexion(host="localhost", user="root", password="", database="sistemainventario")
        dialog = CRUDProductoDialog(conexion, accion="crear")
        dialog.exec()  # Abre el diálogo y espera la acción del usuario

    def edit_product(self):
        """Abrir el diálogo de 'Editar Producto'"""
        # Aquí se debería obtener el ID del producto que se quiere editar
        producto_id = 1  # Ejemplo, esto debe ser dinámico
        conexion = Conexion(host="localhost", user="root", password="", database="sistemainventario")
        dialog = CRUDProductoDialog(conexion, accion="editar", producto_id=producto_id)
        dialog.exec()  # Abre el diálogo y espera la acción del usuario

    def delete_product(self):
        """Abrir el diálogo de 'Eliminar Producto'"""
        # Aquí se debería obtener el ID del producto que se quiere eliminar
        producto_id = 1  # Ejemplo, esto debe ser dinámico
        conexion = Conexion(host="localhost", user="root", password="", database="sistemainventario")
        dialog = CRUDProductoDialog(conexion, accion="eliminar", producto_id=producto_id)
        dialog.exec()  # Abre el diálogo y espera la acción del usuario

    def search_product(self):
        """Abrir el diálogo de 'Buscar Producto'"""
        # Aquí se debería obtener el ID del producto que se quiere buscar
        producto_id = 1  # Ejemplo, esto debe ser dinámico
        conexion = Conexion(host="localhost", user="root", password="", database="sistemainventario")
        dialog = CRUDProductoDialog(conexion, accion="buscar", producto_id=producto_id)
        dialog.exec()  # Abre el diálogo y espera la acción del usuario

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
