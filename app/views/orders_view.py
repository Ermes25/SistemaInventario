import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFrame, QLabel)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt, QSize

class InventoryOrders(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pedidos")
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
        title_label = self.create_title("Gestión de Pedidos")
        container_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir imagen entre el título y los botones
        image_label = QLabel()
        image_pixmap = QPixmap("images/model_icons/orders_crud.png")  # Asegúrate de usar la ruta correcta
        image_label.setPixmap(image_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(image_label)

        # Layout para la primera fila de botones
        first_row = QHBoxLayout()
        first_row.setSpacing(20)

        buttons_row1 = [
            ("Agregar", "#4CAF50", "images/Crud/create.png"),
            ("Editar", "#2196F3", "images/Crud/Update.png"),
            ("Eliminar", "#F44336", "images/Crud/Delete.png"),
            ("Mostrar Todos", "#9C27B0", "images/Crud/show.png"),
        ]

        for text, color, icon_path in buttons_row1:
            button = self.create_button(text, color, icon_path)
            first_row.addWidget(button)

        # Layout para la segunda fila de botones
        second_row = QHBoxLayout()
        second_row.setSpacing(20)

        buttons_row2 = [
            ("Buscar", "#757575", "images/Crud/Search.png"),
            ("Refrescar", "#FFC107", "images/Crud/Refresh.png"),
            ("Regresar al Menú", "#757575", "images/Crud/Return.png"),
        ]

        for text, color, icon_path in buttons_row2:
            button = self.create_button(text, color, icon_path)
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

