import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.orders_con import CrudPedidos

class InventoryOrders(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Pedidos")
        self.setFixedSize(1200, 700)
        self.setWindowIcon(QIcon("images/Backgrounds/Farma_Bienestar.png"))
        self.setStyleSheet("background-color: #D3D3D3;")

        # Instancia del CRUD
        self.crud_pedidos = CrudPedidos()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.create_left_panel(left_layout)

        right_layout = QVBoxLayout()
        self.create_table(right_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # Cargar todos los pedidos inicialmente
        self.load_all_orders()

    
    def create_search_bar(self, layout):
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
        search_button.clicked.connect(self.search_orders)
        search_layout.addWidget(search_button)
        
        # Campo de entrada de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por Producto, Proveedor, ID o Cantidad")
        self.search_input.setStyleSheet("background-color: white; color: black; padding: 5px; border: 1px solid #CCC;")
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)

    def search_orders(self):
        search_text = self.search_input.text()
        results = self.crud_pedidos.buscar_pedidos(search_text)
        self.table.setRowCount(0)
        for row, order in enumerate(results):
            self.table.insertRow(row)
            for col, value in enumerate(order):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    def create_left_panel(self, layout):
        # Layout para los botones en la parte superior
        top_buttons_layout = QHBoxLayout()

         # Botón "regresar" al dashboard
        menu_button = QPushButton("")
        menu_button.setIcon(QIcon("images/crud_views/return.png"))
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
        export_button.setIcon(QIcon("images/model_icons/csv_icon.png"))  # Cambia el icono según corresponda
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

        # Imagen del panel
        image_label = QLabel()
        pixmap = QPixmap("images/model_icons/crud_orders.png")
        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Etiqueta de total de pedidos
        self.total_label = QLabel("Total de Pedidos: 0")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        layout.addWidget(self.total_label)

        # Layout del formulario de entradas
        form_layout = QVBoxLayout()
        self.id_producto_combo = QComboBox()
        self.id_proveedor_combo = QComboBox()
        self.load_product_and_provider_names()

        self.fecha_pedido_input = QLineEdit()
        self.cantidad_pedido_input = QLineEdit()

        # Configuración de estilo para campos de entrada
        for input_field in [self.fecha_pedido_input, self.cantidad_pedido_input]:
            input_field.setStyleSheet("""
                background-color: white;
                color: black;
                padding: 5px;
                border: none;
            """)

        for combo in [self.id_producto_combo, self.id_proveedor_combo]:
            combo.setStyleSheet("""
                background-color: white;
                color: black;
                border: none;
            """)

        # Etiquetas y campos de entrada
        fields = [
            ("Producto:", self.id_producto_combo),
            ("Proveedor:", self.id_proveedor_combo),
            ("Fecha Pedido:", self.fecha_pedido_input),
            ("Cantidad:", self.cantidad_pedido_input)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: black; padding: 5px;")
            form_layout.addWidget(label)
            form_layout.addWidget(widget)

        layout.addLayout(form_layout)

        # Barra de búsqueda colocada justo debajo de los inputs
        self.create_search_bar(layout)

        # Layout de botones CRUD
        buttons_layout = QVBoxLayout()
        top_buttons = QHBoxLayout()
        bottom_buttons = QHBoxLayout()

        button_data = [
            ("Agregar", self.add_order),
            ("Editar", self.edit_order),
            ("Eliminar", self.delete_order),
            ("Refrescar", self.load_all_orders),
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
        headers = ["ID Pedido", "Producto", "Proveedor", "Fecha Pedido", "Cantidad"]  # Cambié los nombres de columna
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Aseguramos que las cabeceras sean visibles
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Conectar la selección de una fila a una función para cargar los datos en los campos
        self.table.selectionModel().selectionChanged.connect(self.load_selected_order)

        layout.addWidget(self.table)

    def load_all_orders(self):
        orders = self.crud_pedidos.cargar_pedidos()
        self.table.setRowCount(0)
        for row, order in enumerate(orders):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(order[0])))  # ID Pedido
            producto_nombre = self.crud_pedidos.obtener_nombre_producto(order[1])
            proveedor_nombre = self.crud_pedidos.obtener_nombre_proveedor(order[2])
            self.table.setItem(row, 1, QTableWidgetItem(producto_nombre))  # Nombre Producto
            self.table.setItem(row, 2, QTableWidgetItem(proveedor_nombre))  # Nombre Proveedor
            for col, value in enumerate(order[3:], start=3):  # Comenzamos desde la columna 3
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        self.total_label.setText(f"Total de Pedidos: {len(orders)}")

    def load_product_and_provider_names(self):
        productos = self.crud_pedidos.cargar_productos()
        proveedores = self.crud_pedidos.cargar_proveedores()

        self.id_producto_combo.clear()
        self.id_producto_combo.addItems([p[1] for p in productos])  # Cargar solo los nombres
        self.id_proveedor_combo.clear()
        self.id_proveedor_combo.addItems([p[1] for p in proveedores])  # Cargar solo los nombres

    def add_order(self):
        # Obtener los IDs a partir de los nombres seleccionados
        nombre_producto = self.id_producto_combo.currentText()
        nombre_proveedor = self.id_proveedor_combo.currentText()
        id_producto = self.crud_pedidos.obtener_id_producto(nombre_producto)
        id_proveedor = self.crud_pedidos.obtener_id_proveedor(nombre_proveedor)
        fecha_pedido = self.fecha_pedido_input.text()
        cantidad_pedido = self.cantidad_pedido_input.text()
        self.crud_pedidos.agregar_pedido(id_producto, id_proveedor, fecha_pedido, cantidad_pedido)
        self.load_all_orders()

    
    def load_selected_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_pedido_item = self.table.item(selected_row, 0)
            producto_item = self.table.item(selected_row, 1)
            proveedor_item = self.table.item(selected_row, 2)
            fecha_item = self.table.item(selected_row, 3)
            cantidad_item = self.table.item(selected_row, 4)

            if id_pedido_item and producto_item and proveedor_item and fecha_item and cantidad_item:
                id_pedido = id_pedido_item.text()
                nombre_producto = producto_item.text()
                nombre_proveedor = proveedor_item.text()
                fecha_pedido = fecha_item.text()
                cantidad_pedido = cantidad_item.text()

                # Fill inputs
                self.id_producto_combo.setCurrentText(nombre_producto)
                self.id_proveedor_combo.setCurrentText(nombre_proveedor)
                self.fecha_pedido_input.setText(fecha_pedido)
                self.cantidad_pedido_input.setText(cantidad_pedido)

                # Store selected ID for editing or deleting
                self.selected_order_id = id_pedido

        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_pedido_item = self.table.item(selected_row, 0)
            if id_pedido_item is not None:
                id_pedido = id_pedido_item.text()
            else:
                return

            id_producto_item = self.table.item(selected_row, 1)
            nombre_producto = id_producto_item.text() if id_producto_item is not None else ""
            id_producto = self.crud_pedidos.obtener_id_producto_por_nombre(nombre_producto)

            id_proveedor_item = self.table.item(selected_row, 2)
            nombre_proveedor = id_proveedor_item.text() if id_proveedor_item is not None else ""
            id_proveedor = self.crud_pedidos.obtener_id_proveedor_por_nombre(nombre_proveedor)

            fecha_pedido_item = self.table.item(selected_row, 3)
            fecha_pedido = fecha_pedido_item.text() if fecha_pedido_item is not None else ""

            cantidad_pedido_item = self.table.item(selected_row, 4)
            cantidad_pedido = cantidad_pedido_item.text() if cantidad_pedido_item is not None else ""

            # Rellenar los campos con los datos seleccionados
            self.id_producto_combo.setCurrentText(nombre_producto)
            self.id_proveedor_combo.setCurrentText(nombre_proveedor)
            self.fecha_pedido_input.setText(fecha_pedido)
            self.cantidad_pedido_input.setText(cantidad_pedido)

    def edit_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_pedido_item = self.table.item(selected_row, 0)
            if id_pedido_item is not None:
                id_pedido = id_pedido_item.text()

                # Obtener datos actualizados desde los campos
                nombre_producto = self.id_producto_combo.currentText()
                nombre_proveedor = self.id_proveedor_combo.currentText()
                id_producto = self.crud_pedidos.obtener_id_producto(nombre_producto)
                id_proveedor = self.crud_pedidos.obtener_id_proveedor(nombre_proveedor)
                fecha_pedido = self.fecha_pedido_input.text()
                cantidad_pedido = self.cantidad_pedido_input.text()

                # Actualizar el pedido en la base de datos
                self.crud_pedidos.editar_pedido(id_pedido, id_producto, id_proveedor, fecha_pedido, cantidad_pedido)
                self.load_all_orders()

    def delete_order(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_pedido_item = self.table.item(selected_row, 0)
            if id_pedido_item is not None:
                id_pedido = id_pedido_item.text()
                self.crud_pedidos.eliminar_pedido(id_pedido)
                self.load_all_orders()

    def clear_form(self):
        # Ocultar todas las filas del grid
        row_count = self.table.rowCount()
        for row in range(row_count):
            self.table.setRowHidden(row, True)


    def return_to_dashboard(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from views.Dashboard import Dashboard  # Importa el Dashboard
        self.dashboard = Dashboard()  # Crea una instancia del Dashboard
        self.dashboard.show()  # Muestra el Dashboard
        self.close()  # Cierra la ventana actual

    def open_help_manual(self):
        import subprocess
        import os
        pdf_path = os.path.abspath("utils/manual.pdf")  # Asegúrate de que sea una ruta válida
        try:
            if os.path.exists(pdf_path):
                subprocess.Popen([pdf_path], shell=True)  # Abre el PDF con la aplicación predeterminada
            else:
                print(f"El archivo no existe: {pdf_path}")
        except Exception as e:
            print(f"No se pudo abrir el archivo: {e}")
    
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
            ("Producto:", self.id_producto_combo),
            ("Proveedor:", self.id_proveedor_combo),
            ("Fecha Pedido:", self.fecha_pedido_input),
            ("Cantidad:", self.cantidad_pedido_input),
        ]

        for label, widget in fields:
            if isinstance(widget, QLineEdit):
                widget.clear()  # Limpiar texto en QLineEdit
            elif hasattr(widget, "setCurrentIndex"):  # Para QComboBox u otros con índices
                widget.setCurrentIndex(0)
            else:
                print(f"Widget no soportado: {label}")

        print("Campos de entrada limpiados.")




