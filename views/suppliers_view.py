import sys
import os
from PyQt6.QtGui import QIntValidator
import re 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QHeaderView
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.suppliers_con import SupplierCRUD


class InventoryProveedores(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Proveedores")
        self.setFixedSize(1200, 700)
        self.setWindowIcon(QIcon("images/Backgrounds/Farma_Bienestar.png"))
        self.setStyleSheet("background-color: #D3D3D3;")

        self.crud = SupplierCRUD()  # Crear instancia de SupplierCRUD

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.create_left_panel(left_layout)

        right_layout = QVBoxLayout()
        self.create_table(right_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # Cargar todos los proveedores inicialmente
        self.load_all_providers()
        self.setup_signals()

    def create_left_panel(self, layout):
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
        layout.addLayout(top_buttons_layout)
        # Agregar imagen
        image_label = QLabel()
        pixmap = QPixmap("images/model_icons/crud_suppliers.png")
        image_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Contador de proveedores
        self.provider_count_label = QLabel("Total Proveedores: 0")
        self.provider_count_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: black;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(self.provider_count_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Crear formulario para datos
        form_layout = QVBoxLayout()
        fields = [
            ("Nombre Proveedor:", "nombre_proveedor"),
            ("Número Telefonico:", "numero_proveedor"),
            ("Email:", "email"),
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
            if field_name == "numero_proveedor":
                input_field.setMaxLength(8)  # Máximo 8 caracteres
                input_field.setValidator(QIntValidator(0, 99999999))
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #BDBDBD;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
            """)
            form_layout.addWidget(label)
            form_layout.addWidget(input_field)
        if field_name == "numero_proveedor":
            input_field.setMaxLength(8)  # Máximo 8 caracteres
            input_field.setValidator(QIntValidator(0, 99999999))  # Solo permite números


        layout.addLayout(form_layout)

        # Campo de búsqueda
        search_layout = QHBoxLayout()
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
        search_button.clicked.connect(self.search_provider)

        self.search_field = QLineEdit()
        self.search_field.setObjectName("buscar_proveedor")
        self.search_field.setPlaceholderText("Busque un Proveedor")
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

        # Botones de acción
        buttons_layout = QVBoxLayout()
        top_buttons = QHBoxLayout()
        bottom_buttons = QHBoxLayout()

        button_data = [
            ("Agregar", self.add_provider),
            ("Editar", self.edit_provider),
            ("Eliminar", self.delete_provider),
            ("Refrescar", self.refresh_providers),
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
        headers = ["ID Proveedor", "Nombre", "Número", "Email"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.fill_inputs_from_selection)
        layout.addWidget(self.table)

    def load_all_providers(self):
        providers = self.crud.load_all_providers()
        self.table.setRowCount(0)
        for row, provider in enumerate(providers):
            self.table.insertRow(row)
            for col, value in enumerate(provider):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        self.provider_count_label.setText(f"Total Proveedores: {len(providers)}")

    def add_provider(self):
        nombre = self.findChild(QLineEdit, "nombre_proveedor").text()
        numero = self.findChild(QLineEdit, "numero_proveedor").text()
        email = self.findChild(QLineEdit, "email").text()

        # Validaciones
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Correo válido
            print("Error: El correo no es válido.")
            return
        if not numero.isdigit() or len(numero) != 8:  # Número de 8 dígitos
            print("Error: El número debe tener exactamente 8 dígitos.")
            return

        if nombre and numero and email:
            self.crud.add_provider(nombre, numero, email)
            self.load_all_providers()

    def edit_provider(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            provider_id = self.table.item(selected_row, 0).text()
            nombre = self.findChild(QLineEdit, "nombre_proveedor").text()
            numero = self.findChild(QLineEdit, "numero_proveedor").text()
            email = self.findChild(QLineEdit, "email").text()

            # Validaciones
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Correo válido
                print("Error: El correo no es válido.")
                return
            if not numero.isdigit() or len(numero) != 8:  # Número de 8 dígitos
                print("Error: El número debe tener exactamente 8 dígitos.")
                return

            if nombre and numero and email:
                self.crud.edit_provider(provider_id, nombre, numero, email)
                self.load_all_providers()

    def delete_provider(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            provider_id = self.table.item(selected_row, 0).text()
            self.crud.delete_provider(provider_id)
            self.load_all_providers()

    def search_provider(self):
        search_text = self.search_field.text()
        if search_text:
            providers = self.crud.search_provider(search_text)
            self.table.setRowCount(0)
            for row, provider in enumerate(providers):
                self.table.insertRow(row)
                for col, value in enumerate(provider):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)

    def refresh_providers(self):
        self.load_all_providers()

    def clear_table(self):
        self.table.setRowCount(0)
        self.provider_count_label.setText("Total Proveedores: 0")
        print("Tabla limpiada.")
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

    def fill_inputs_from_selection(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:  # Asegúrate de que hay una fila seleccionada
            provider_id = self.table.item(selected_row, 0).text()
            nombre = self.table.item(selected_row, 1).text()
            numero = self.table.item(selected_row, 2).text()
            email = self.table.item(selected_row, 3).text()

            # Rellenar los campos de entrada con los datos seleccionados
            self.findChild(QLineEdit, "nombre_proveedor").setText(nombre)
            self.findChild(QLineEdit, "numero_proveedor").setText(numero)
            self.findChild(QLineEdit, "email").setText(email)

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

    
    def setup_signals(self):
        """Conecta señales para validar los campos de entrada."""
        numero_input = self.findChild(QLineEdit, "numero_proveedor")
        if numero_input:  # Verificar que el objeto existe
            numero_input.textChanged.connect(self.validate_phone_number)
        else:
            print("El campo 'numero_proveedor' no fue encontrado.")

    def clear_inputs(self):
        """Limpia los campos de entrada."""
        self.findChild(QLineEdit, "nombre_proveedor").clear()
        self.findChild(QLineEdit, "numero_proveedor").clear()
        self.findChild(QLineEdit, "email").clear()
        print("Campos de entrada limpiados.")

    def validate_phone_number(self, text):
        """Valida la longitud del número de proveedor."""
        if len(text) > 8:
            self.findChild(QLineEdit, "numero_proveedor").setText(text[:8])  # Limitar a 8 dígitos
            print("El número no puede tener más de 8 dígitos.")
        elif not text.isdigit():
            print("El número debe ser solo dígitos.")