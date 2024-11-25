from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView, QGridLayout
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.products_con import ProductCRUD


class InventoryProducts(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Productos")
        self.setFixedSize(1200, 700)
        self.setWindowIcon(QIcon("app/images/Backgrounds/Farma_Bienestar.png"))
        self.setStyleSheet("background-color: #D3D3D3;")

        self.crud = ProductCRUD()  # Instancia de ProductCRUD

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.create_left_panel(left_layout)

        right_layout = QVBoxLayout()
        self.create_table(right_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        self.load_all_products()

    def create_left_panel(self, layout):
        top_buttons_layout = QHBoxLayout()

        # Botón "regresar" al dashboard
        menu_button = QPushButton("")
        menu_button.setIcon(QIcon("app/images/crud_views/return.png"))
        menu_button.setIconSize(QSize(24, 24))
        menu_button.setFixedWidth(80)  # Botón menos ancho
        menu_button.setStyleSheet("""
            QPushButton {
                background-color: #B3E5FC;  /* Celeste claro */
                color: black;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #81D4FA;
            }
        """)
        menu_button.clicked.connect(self.return_to_dashboard)  # Conecta el botón con el método correspondiente
        top_buttons_layout.addWidget(menu_button, alignment=Qt.AlignmentFlag.AlignLeft) 
        
        # Botón para exportar registros a CSV
        export_button = QPushButton("Exportar")
        export_button.setIcon(QIcon("app/images/model_icons/csv_icon.png"))  # Cambia el icono según corresponda
        export_button.setIconSize(QSize(24, 24))
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #B3E5FC;  /* Celeste claro */
                color: black;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #81D4FA;
            }
        """)
        export_button.clicked.connect(self.export_to_csv)  # Conecta al método de exportar
        top_buttons_layout.addWidget(export_button)

        # Agregar el layout al panel izquierdo
        layout.addLayout(top_buttons_layout)
        # Agregar imagen
        image_label = QLabel()
        pixmap = QPixmap("app/images/model_icons/crud_products.png")
        image_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Contador de productos
        self.product_count_label = QLabel("Total Productos: 0")
        self.product_count_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: black;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(self.product_count_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)  # Espaciador

        # Crear formulario para datos
        form_layout = QVBoxLayout()
        fields = [
            ("Nombre Producto:", "nombre_producto"),
            ("Categoría:", "categoria"),
            ("Fecha Ingreso:", "fecha_ingreso"),
            ("Fecha Vencimiento:", "fecha_vencimiento"),
            ("Cantidad:", "cantidad"),
            ("Precio:", "precio"),
        ]

        for label_text, field_name in fields:
            label = QLabel(label_text)
            label.setStyleSheet("""
                QLabel {
                    color: black;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
            input_field = QLineEdit()
            input_field.setObjectName(field_name)
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #BDBDBD;
                    border-radius: 4px;
                    padding: 6px;  /* Ajusta el relleno interno */
                    font-size: 12px;  /* Tamaño de la fuente más legible */
                    height: 100px;  /* Asegura una altura mínima */
                }
            """)
            form_layout.addWidget(label)
            form_layout.addWidget(input_field)

        layout.addLayout(form_layout)

        # Campo de búsqueda
        search_layout = QHBoxLayout()

        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #B3E5FC;  /* Celeste claro */
                    color: black;
                    border: none;
                    border-radius: 4px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                }
            QPushButton:hover {
                    background-color: #81D4FA;  /* Celeste más oscuro */
            }
        """)
        search_button.clicked.connect(self.search_product)

        self.search_field = QLineEdit()
        self.search_field.setObjectName("buscar_producto")
        self.search_field.setPlaceholderText("Busque un Producto")
        self.search_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        search_layout.addWidget(search_button)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)

        # Botones de acciones
        buttons_layout = QGridLayout()
        button_data = [
            ("Agregar", self.add_product),
            ("Editar", self.edit_product),
            ("Eliminar", self.delete_product),
            ("Refrescar", self.load_all_products),
            ("Limpiar Tabla", self.clear_table),
        ]

        for i, (text, func) in enumerate(button_data):
            button = QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #B3E5FC;  /* Celeste claro */
                    color: black;
                    border: none;
                    border-radius: 20px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #81D4FA;
                }
            """)
            button.clicked.connect(func)
            button.setFixedSize(120, 40)
            if i < 3:
                buttons_layout.addWidget(button, 0, i)
            else:
                buttons_layout.addWidget(button, 1, i - 3)

        layout.addLayout(buttons_layout)

    def create_table(self, layout):
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #BDBDBD;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                color: black;
                padding: 5px;
                border: 1px solid #BDBDBD;
                font-weight: bold;
            }
            QTableWidget::item {
                color: black;
                padding: 5px;
            }
        """)
        headers = ["ID Producto", "Nombre", "Categoría", "Fecha Ingreso", "Fecha Vencimiento", "Cantidad", "Precio"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Conectar el evento de selección
        self.table.itemSelectionChanged.connect(self.load_selected_product)

        layout.addWidget(self.table)


    def load_all_products(self):
        products = self.crud.load_all_products()
        self.table.setRowCount(0)
        for row, product in enumerate(products):
            self.table.insertRow(row)
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        self.product_count_label.setText(f"Total Productos: {len(products)}")

    def add_product(self):
        nombre = self.findChild(QLineEdit, "nombre_producto").text()
        categoria = self.findChild(QLineEdit, "categoria").text()
        fecha_ingreso = self.findChild(QLineEdit, "fecha_ingreso").text()
        fecha_vencimiento = self.findChild(QLineEdit, "fecha_vencimiento").text()
        cantidad = self.findChild(QLineEdit, "cantidad").text()
        precio = self.findChild(QLineEdit, "precio").text()

        if not all([nombre, categoria, fecha_ingreso, fecha_vencimiento, cantidad, precio]):
            print("Complete todos los campos.")
            return
        self.crud.add_product(nombre, categoria, fecha_ingreso, fecha_vencimiento, int(cantidad), float(precio))
        self.load_all_products()

    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            print("Seleccione un producto para editar.")
            return
        product_id = self.table.item(selected_row, 0).text()
        nombre = self.findChild(QLineEdit, "nombre_producto").text()
        categoria = self.findChild(QLineEdit, "categoria").text()
        fecha_ingreso = self.findChild(QLineEdit, "fecha_ingreso").text()
        fecha_vencimiento = self.findChild(QLineEdit, "fecha_vencimiento").text()
        cantidad = self.findChild(QLineEdit, "cantidad").text()
        precio = self.findChild(QLineEdit, "precio").text()

        self.crud.edit_product(
            product_id,
            nombre or self.table.item(selected_row, 1).text(),
            categoria or self.table.item(selected_row, 2).text(),
            fecha_ingreso or self.table.item(selected_row, 3).text(),
            fecha_vencimiento or self.table.item(selected_row, 4).text(),
            int(cantidad) if cantidad else int(self.table.item(selected_row, 5).text()),
            float(precio) if precio else float(self.table.item(selected_row, 6).text())
        )
        self.load_all_products()

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            print("Seleccione un producto para eliminar.")
            return
        product_id = self.table.item(selected_row, 0).text()
        self.crud.delete_product(product_id)
        self.load_all_products()

    def search_product(self):
        search_text = self.search_field.text()
        if not search_text:
            print("Ingrese un texto para buscar.")
            return
        products = self.crud.search_product(search_text)
        self.table.setRowCount(0)
        for row, product in enumerate(products):
            self.table.insertRow(row)
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    def clear_table(self):
        self.table.setRowCount(0)
        self.product_count_label.setText("Total Productos: 0")
        print("Tabla limpiada.")
    def load_selected_product(self):
        # Obtener la fila seleccionada
        selected_row = self.table.currentRow()
        if selected_row == -1:  # Verificar si hay una fila seleccionada
            return

        # Rellenar los campos con los datos de la fila seleccionada
        self.findChild(QLineEdit, "nombre_producto").setText(self.table.item(selected_row, 1).text())
        self.findChild(QLineEdit, "categoria").setText(self.table.item(selected_row, 2).text())
        self.findChild(QLineEdit, "fecha_ingreso").setText(self.table.item(selected_row, 3).text())
        self.findChild(QLineEdit, "fecha_vencimiento").setText(self.table.item(selected_row, 4).text())
        self.findChild(QLineEdit, "cantidad").setText(self.table.item(selected_row, 5).text())
        self.findChild(QLineEdit, "precio").setText(self.table.item(selected_row, 6).text())
    def return_to_dashboard(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from views.Dashboard import Dashboard  # Importa el Dashboard
        self.dashboard = Dashboard()  # Crea una instancia del Dashboard
        self.dashboard.show()  # Muestra el Dashboard
        self.close()  # Cierra la ventana actual

    def export_to_csv(self):
        import csv
        from PyQt6.QtWidgets import QFileDialog

        # Abrir un cuadro de diálogo para seleccionar la ubicación del archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo CSV",
            "registros_productos.csv",  # Nombre sugerido por defecto
            "Archivos CSV (*.csv)"
        )

        if not file_path:  # Si el usuario cancela, no hacer nada
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Escribir los encabezados
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)

                # Escribir los datos de la tabla
                for row in range(self.table.rowCount()):
                    writer.writerow([
                        self.table.item(row, col).text() if self.table.item(row, col) else ""
                        for col in range(self.table.columnCount())
                    ])

            print(f"Registros exportados a {file_path}")
        except Exception as e:
            print(f"Error al exportar registros: {e}")
