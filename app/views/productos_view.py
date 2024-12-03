from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView, QGridLayout, QDateEdit
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize, QDate
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.products_con import ProductCRUD
from datetime import datetime

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

            # Configurar campos específicos
            if field_name == "fecha_ingreso":
                input_field.setPlaceholderText("Formato: yyyy-mm-dd")  # Ayuda visual para la fecha
            elif field_name == "fecha_vencimiento":
                input_field.setPlaceholderText("Formato: yyyy-mm-dd")
            elif field_name == "cantidad":
                input_field.setPlaceholderText("Solo números")
            elif field_name == "precio":
                input_field.setPlaceholderText("Ejemplo: 123.45")

            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #BDBDBD;
                    border-radius: 2px;
                    padding: 2px;
                    font-size: 12px;
                    height: 30px;
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
                    border-radius: 20px;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #81D4FA;
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
        buttons_layout = QVBoxLayout()
        top_buttons = QHBoxLayout()
        bottom_buttons = QHBoxLayout()
        button_data = [
            ("Agregar", self.add_product),
            ("Editar", self.edit_product),
            ("Eliminar", self.delete_product),
            ("Refrescar", self.load_all_products),
            ("Limpiar", self.clear_inputs),
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
                top_buttons.addWidget(button)
            else:
                bottom_buttons.addWidget(button)

        buttons_layout.addLayout(top_buttons)
        buttons_layout.addLayout(bottom_buttons)
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
        headers = ["ID Producto", "Nombre", "Categoría", "Fecha Ingreso", "Fecha Vencimiento", "Cantidad", "Precio", "Fecha Límite"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Conectar el evento de selección
        self.table.itemSelectionChanged.connect(self.load_selected_product)

        layout.addWidget(self.table)

    def calculate_expiration_status(self,expiration_year):
        try:
            # Convertir el año en una fecha al 31 de diciembre de ese año
            expiration_date = datetime(int(expiration_year), 12, 31)
            # Comparar con la fecha actual
            if expiration_date < datetime.now():
                return "Expirado"
            return "S. Expirar"
        except Exception:
            return "Fecha Inválida"

    def load_all_products(self):
        products = self.crud.load_all_products()
        self.table.setRowCount(0)
        for row, product in enumerate(products):
            self.table.insertRow(row)
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

            # Calcular el estado de la fecha límite y añadirlo a la tabla
            expiration_status =self.calculate_expiration_status(product[4])  # Índice de fecha_vencimiento (YEAR)
            status_item = QTableWidgetItem(expiration_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, len(product), status_item)  # Última columna

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
        search_text = self.search_field.text().strip().lower()  # Convertir a minúsculas para comparación
        if not search_text:
            print("Ingrese un texto para buscar.")
            return
        
        products = self.crud.load_all_products()  # Cargar todos los productos
        filtered_products = []
        
        for product in products:
            # Obtener el estado de expiración
            expiration_status = self.calculate_expiration_status(product[4])  # Índice de "fecha_vencimiento"
            
            # Convertir valores relevantes a minúsculas para búsqueda insensible a mayúsculas
            product_fields = [
                str(product[0]).lower(),  # ID Producto
                str(product[1]).lower(),  # Nombre
                str(product[2]).lower(),  # Categoría
                str(product[3]).lower(),  # Fecha Ingreso
                str(product[4]).lower(),  # Fecha Vencimiento
                str(product[5]).lower(),  # Cantidad
                str(product[6]).lower(),  # Precio
                expiration_status.lower()  # Estado de expiración
            ]
            
            # Comprobar si el texto de búsqueda está en algún campo o en el estado
            if any(search_text in field for field in product_fields):
                filtered_products.append(product)
        
        # Mostrar solo los productos filtrados
        self.table.setRowCount(0)
        for row, product in enumerate(filtered_products):
            self.table.insertRow(row)
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Añadir estado de "Fecha Límite" al final
            expiration_status = self.calculate_expiration_status(product[4])
            status_item = QTableWidgetItem(expiration_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, len(product), status_item)


    def clear_table(self):
        self.table.setRowCount(0)
        self.product_count_label.setText("Total Productos: 0")
        print("Tabla limpiada.")
    def load_selected_product(self):
        # Supongamos que los datos vienen desde una fila seleccionada en la tabla
        selected_row = self.table.currentRow()
        if selected_row == -1:  # Si no hay una fila seleccionada, no hacemos nada
            return

        # Obtener valores desde la tabla
        nombre = self.table.item(selected_row, 1).text()
        categoria = self.table.item(selected_row, 2).text()
        fecha_ingreso = self.table.item(selected_row, 3).text()
        fecha_vencimiento = self.table.item(selected_row, 4).text()
        cantidad = self.table.item(selected_row, 5).text()
        precio = self.table.item(selected_row, 6).text()

        # Llenar los campos del formulario
        self.findChild(QLineEdit, "nombre_producto").setText(nombre)
        self.findChild(QLineEdit, "categoria").setText(categoria)

        # Mostrar solo la fecha sin la hora en el campo fecha_ingreso
        if fecha_ingreso:
            fecha_solo = fecha_ingreso.split(" ")[0]  # Separar fecha y hora, tomar solo la fecha
            self.findChild(QLineEdit, "fecha_ingreso").setText(fecha_solo)
        else:
            self.findChild(QLineEdit, "fecha_ingreso").clear()

        self.findChild(QLineEdit, "fecha_vencimiento").setText(fecha_vencimiento)
        self.findChild(QLineEdit, "cantidad").setText(cantidad)
        self.findChild(QLineEdit, "precio").setText(precio)
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
    def clear_inputs(self):
        """Limpia los campos de entrada especificados."""
        fields = [
            ("Nombre Producto:", "nombre_producto"),
            ("Categoría:", "categoria"),
            ("Fecha Ingreso:", "fecha_ingreso"),
            ("Fecha Vencimiento:", "fecha_vencimiento"),
            ("Cantidad:", "cantidad"),
            ("Precio:", "precio"),
        ]
        for _, field_name in fields:
            input_field = self.findChild(QLineEdit, field_name)
            if input_field:  # Verifica que el campo existe
                input_field.clear()
        print("Campos de entrada limpiados.")
