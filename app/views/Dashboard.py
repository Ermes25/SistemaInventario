import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QFont, QPalette, QBrush, QImage
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QSize

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(1200, 700)  # Tamaño mínimo
        self.setWindowIcon(QIcon("images/Backgrounds/Farma_Bienestar.png"))  # Icono de la ventana

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # Cambio a layout horizontal

        # Layout izquierdo para fecha/hora
        left_layout = QVBoxLayout()
        
        # Fecha y hora
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Digital-7", 22))
        self.time_label.setStyleSheet("""
            QLabel {
                color: black;
                background: transparent;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        left_layout.addWidget(self.time_label)
        left_layout.addStretch()  # Espacio flexible
        main_layout.addLayout(left_layout, stretch=2)

        # Layout derecho para botones
        right_layout = QVBoxLayout()
        right_layout.setSpacing(30)  # Aumentar el espacio entre botones

        # Añadir un espaciador flexible encima de los botones para moverlos hacia abajo
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        items = [
            ("Productos", "images/model_icons/dashproducts.png", self.products_open),
            ("Proveedores", "images/model_icons/dashsuppliers.png", self.suppliers_open),
            ("Pedidos", "images/model_icons/dashorders.png", self.orders_open),  
        ]

        for text, icon_path, slot in items:
            item_layout = QHBoxLayout()  # Layout horizontal para cada botón
            
            # Label del texto
            text_label = QLabel(text)
            text_label.setFont(QFont("Arial", 20))
            text_label.setStyleSheet("color: #333; background: transparent;")
            
            # Botón con icono
            button = QPushButton()
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(80, 80))  # Tamaño del icono
            button.clicked.connect(slot)
            button.setFixedSize(80, 80)  # Botón más grande
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(33, 150, 243, 0.8);  /* Azul semitransparente */
                    border: none;
                    border-radius: 40px;  /* Ajustado al tamaño */
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(33, 150, 243, 0.9);
                }
                QPushButton:pressed {
                    background-color: rgba(33, 150, 243, 1.0);
                }
            """)

            item_layout.addWidget(button)
            item_layout.addWidget(text_label)
            right_layout.addLayout(item_layout)

        # Añadir un espaciador flexible debajo de los botones
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Ajustar alineación del layout principal
        main_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(right_layout)


        # Timer para actualizar fecha y hora
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()  # Actualizar inmediatamente

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
        current_time = QTime.currentTime().toString("hh:mm")
        current_date = QDate.currentDate().toString("dd-MM-yyyy")
        self.time_label.setText(f"{current_date} {current_time}")

    def resizeEvent(self, event):
        # Asegurar que la imagen de fondo se ajuste al tamaño de la ventana
        background = QImage("images/Backgrounds/Background.jpg").scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)
        super().resizeEvent(event)

