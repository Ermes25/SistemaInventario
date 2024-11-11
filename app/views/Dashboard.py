import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QMessageBox)
from PyQt6.QtGui import QPainter, QColor, QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = QPixmap("app/images/Backgrounds/Inventory_Background.jpg")

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw the background image, scaled to fit while maintaining aspect ratio
        scaled_background = self.background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        # Calculate position to center the image
        x = (self.width() - scaled_background.width()) // 2
        y = (self.height() - scaled_background.height()) // 2
        
        painter.drawPixmap(x, y, scaled_background)

class IconButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(250, 100)
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet(""" 
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #ddd;
                border-radius: 10px;
                text-align: center;
                padding-left: 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(64, 64))

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setFixedSize(1366, 768)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create gradient background
        gradient_widget = GradientWidget()
        main_layout.addWidget(gradient_widget)
        
        # Create main frame
        self.main_frame = QFrame(gradient_widget)
        self.main_frame.setStyleSheet("""background-color: white; 
                                      border-radius: 20px;
                                      background-image: url(app/images/Backgrounds/background_Dashboard.jpeg);""")
        self.main_frame.setFixedSize(800, 600)
        self.main_frame.move(283, 84)  # Center the frame

        # Create layout for main frame
        frame_layout = QHBoxLayout(self.main_frame)

        # Create left side layout
        left_layout = QVBoxLayout()
        
        # Add header
        header_label = QLabel("Bienvenidos")
        header_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        left_layout.addWidget(header_label)
        
        # Add stretcher to push "Salir" button to bottom
        left_layout.addStretch()
        
        # Add "Salir" button
        exit_button = QPushButton("Salir")
        exit_button.setFixedSize(100, 40)
        exit_button.setStyleSheet(""" 
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        exit_button.clicked.connect(self.close)
        left_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add left layout to frame layout
        frame_layout.addLayout(left_layout)

        # Add stretcher between left side and buttons
        frame_layout.addStretch()

        # Create right side layout for buttons
        right_layout = QVBoxLayout()
        
        # Create icon buttons
        buttons_data = [
            ("Productos", "app/images/model_icons/products_dashboard.png", self.products_open),
            ("Pedidos", "app/images/model_icons/orders_dashboard.png", self.orders_open),
            ("Proveedores", "app/images/model_icons/suppliers_dashboard.png", self.suppliers_open)
        ]
        for text, icon_path, slot in buttons_data:
            button = IconButton(text, icon_path)
            button.clicked.connect(slot)
            right_layout.addWidget(button)

        # Add right layout to frame layout
        frame_layout.addLayout(right_layout)

    def products_open(self):
        from views.productos_view import InventoryProducts
        self.InventoryProducts = InventoryProducts()
        self.InventoryProducts.show()
        self.close()
        
    def orders_open(self):
        from views.orders_view import InventoryOrders
        self.InventoryOrdes = InventoryOrders()
        self.InventoryOrdes.show()
        self.close()

    def suppliers_open(self):
        from views.suppliers_view import InventorySuppliers
        self.InventorySuppliers = InventorySuppliers()
        self.InventorySuppliers.show()
        self.close()
