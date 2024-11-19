import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QTimer, QTime, QDate

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setFixedSize(1366, 768)
        self.setStyleSheet("background-color: lightgray;")  # Fondo gris claro

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar todo el contenido

        # Label "Bienvenido"
        welcome_label = QLabel("FARMA BIENESTAR")
        welcome_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: black;")
        layout.addWidget(welcome_label)

        # Layout para los iconos y botones
        icons_buttons_layout = QHBoxLayout()
        icons_buttons_layout.setSpacing(50)  # Espaciado entre cada columna
        icons_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar las columnas

        items = [
            ("Productos", "app/images/model_icons/dashproducts.png", self.products_open),
            ("Proveedores", "app/images/model_icons/dashsuppliers.png", self.suppliers_open),
            ("Pedidos", "app/images/model_icons/dashorders.png", self.orders_open)
        ]

        for text, icon_path, slot in items:
            item_layout = QVBoxLayout()
            item_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Icono
            icon_label = QLabel()
            icon_label.setPixmap(QIcon(icon_path).pixmap(100, 100))  # Tamaño del icono fijo
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_layout.addWidget(icon_label)

            # Botón
            button = QPushButton(text)
            button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFFF99;  /* Amarillo claro */
                    color: black;
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #FFD700;  /* Más oscuro al pasar el cursor */
                }
                QPushButton:pressed {
                    background-color: #FF6347;  /* Resaltado cuando se hace clic */
                }
            """)
            button.setFixedSize(200, 50)  # Tamaño fijo para todos los botones
            button.clicked.connect(slot)
            item_layout.addWidget(button)

            # Asegurarse de que el botón esté alineado correctamente
            item_layout.setContentsMargins(0, 10, 0, 0)  # Márgenes entre el icono y el botón

            icons_buttons_layout.addLayout(item_layout)

        layout.addLayout(icons_buttons_layout)

        # Layout para la fecha y hora (en una fila)
        self.time_label = QLabel(self)
        self.time_label.setFont(QFont("Digital-7", 18))  # Fuente digital
        self.time_label.setStyleSheet("color: black;")  # Color negro para los números
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_label.setText("Fecha y hora cargando...")  # Mensaje inicial

        # Ajustar la posición y tamaño del QLabel para la fecha y hora
        self.time_label.setGeometry(1050, 10, 300, 30)  # Ajustar el tamaño para que se vea completo

        # Actualización de fecha y hora en tiempo real
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Actualizar cada segundo

    def products_open(self):
        from views.productos_view import InventoryProducts
        self.ventanaproducto = InventoryProducts()
        self.ventanaproducto.show()
        self.close()
    def suppliers_open(self):
        from views.suppliers_view import InventoryProveedores
        self.ventanaproveedor = InventoryProveedores()
        self.ventanaproveedor.show()
        self.close()
    def orders_open(self):
        from views.orders_view import InventoryOrders
        self.ventanapedido = InventoryOrders()
        self.ventanapedido.show()
        self.close()

    def update_time(self):
        # Obtener la fecha y hora actual
        current_time = QTime.currentTime().toString("hh:mm")  # Hora
        current_date = QDate.currentDate().toString("dd-MM-yyyy")  # Fecha
        self.time_label.setText(f"{current_date} {current_time}")  # Mostrar fecha y hora en una sola línea

