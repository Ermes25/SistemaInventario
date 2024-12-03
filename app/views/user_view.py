import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QHeaderView, QGridLayout,QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import mysql.connector
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.user_con import CRUDUsuarios

class InventoryUsuarios(QMainWindow):
    def __init__(self):
        super().__init__()
        self.crud = CRUDUsuarios()
        self.setWindowTitle("Control de Usuarios")
        self.setFixedSize(1200, 700)
        self.setWindowIcon(QIcon("app/images/Backgrounds/Farma_Bienestar.png"))
        self.setStyleSheet("background-color: #D3D3D3;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        self.create_left_panel(left_layout)
        
        right_layout = QVBoxLayout()
        self.create_table(right_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # Cargar todos los usuarios inicialmente
        self.load_all_users()

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
        menu_button.clicked.connect(self.return_to_login)  # Conecta el botón con el método correspondiente
        top_buttons_layout.addWidget(menu_button, alignment=Qt.AlignmentFlag.AlignLeft) 
        

        # Aplicar estilo global al tooltip para mejorar su visibilidad
        app_instance = QApplication.instance()
        if app_instance:
            app_instance.setStyleSheet("""
                QToolTip {
                    background-color: #FFFFE0; /* Fondo amarillo claro */
                    color: black;            /* Texto negro */
                    border: 1px solid black; /* Borde negro */
                    font-size: 12px;         /* Tamaño de fuente */
                    padding: 5px;            /* Espaciado interno */
                    border-radius: 4px;      /* Bordes redondeados */
                }
            """)

        layout.addLayout(top_buttons_layout)

        # Agregar imagen o icono
        image_label = QLabel()
        pixmap = QPixmap("app/images/model_icons/admin.png")  # Ruta de la imagen
        image_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Crear el contador de usuarios
        self.user_count_label = QLabel("Total Usuarios: 0")
        self.user_count_label.setStyleSheet(""" 
            QLabel {
                font-size: 16px;
                color: black;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(self.user_count_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)  # Espaciador

        # Crear formulario para ingresar datos
        form_layout = QVBoxLayout()
        fields = [
            ("Nombre de Usuario:", "username"),
            ("Contraseña:", "password"),
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
                    padding: 8px;
                    font-size: 12px;
                }
            """)

            form_layout.addWidget(label)
            form_layout.addWidget(input_field)

        layout.addLayout(form_layout)

        # Campo de búsqueda y botón de búsqueda
        search_layout = QHBoxLayout()
        
        search_button = QPushButton("Buscar")
        search_button.setStyleSheet("""  
            QPushButton {
                background-color: #B3E5FC;  /* Celeste claro */
                    color: black;
                    border: none;
                    border-radius: 4px;
                    padding: 2px;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                }
            QPushButton:hover {
                    background-color: #81D4FA;  /* Celeste más oscuro */
        """)
        search_button.setFixedSize(120, 40)
        search_button.clicked.connect(self.search_user)

        self.search_field = QLineEdit()
        self.search_field.setObjectName("buscar_usuario")
        self.search_field.setPlaceholderText("Busque un Usuario")
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

        # Botones de acciones en formato "uva"
        buttons_layout = QVBoxLayout()
        top_buttons = QHBoxLayout()
        bottom_buttons = QHBoxLayout()

        button_data = [
            ("Agregar", self.add_user),
            ("Editar", self.edit_user),
            ("Eliminar", self.delete_user),
            ("Refrescar", self.refresh_users),
            ("Limpiar", self.clear_table),
            ("Permisos", self.permisos_user)
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

        headers = ["ID Usuario", "Usuario", "Contraseña"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.fill_form)
        layout.addWidget(self.table)

    def load_all_users(self):
        users = self.crud.get_all_users()  # Usar el método de la clase
        self.table.setRowCount(0)
        for row, user in enumerate(users):
            self.table.insertRow(row)
            for col, value in enumerate(user):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        self.user_count_label.setText(f"Total Usuarios: {len(users)}")

    def fill_form(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            user_id = self.table.item(selected_row, 0).text()
            user = self.crud.get_user_by_id(user_id)
            if user:
                self.findChild(QLineEdit, "username").setText(user[1])
                self.findChild(QLineEdit, "password").setText(user[2])



    def search_user(self):
        search_field = self.findChild(QLineEdit, "buscar_usuario")
        username = search_field.text().strip()

        if not username:
            print("Error: El campo de búsqueda está vacío.")
            return

        users = self.crud.search_user(username)  # Llamar al método de `CRUDUsuarios`

        if users:
            self.table.setRowCount(0)  # Limpiar la tabla antes de mostrar los resultados
            for row, user in enumerate(users):
                self.table.insertRow(row)
                for col, value in enumerate(user):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row, col, item)
        else:
            print("No se encontraron usuarios con ese nombre.")
            self.table.setRowCount(0)  # Limpiar la tabla si no hay resultados

    def add_user(self):
        # Obtener los campos de entrada
        username_field = self.findChild(QLineEdit, "username")
        password_field = self.findChild(QLineEdit, "password")
        username = username_field.text().strip()
        password = password_field.text().strip()

        # Validar que los campos no estén vacíos
        if not username or not password:
            print("Error: El nombre de usuario y la contraseña no pueden estar vacíos.")
            return

        # Intentar agregar el usuario utilizando el método de la clase CRUD
        resultado = self.crud.add_user(username, password)

        if resultado == True:
            print("Usuario agregado exitosamente.")
            self.refresh_users()  # Refrescar la tabla de usuarios
            username_field.clear()
            password_field.clear()
        elif resultado == "Usuario ya existe":
            print("Error: El usuario ya existe en la base de datos.")
        else:
            print("Error al agregar el usuario.")



    def edit_user(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            print("Error: Seleccione un usuario de la tabla para editar.")
            return

        user_id = self.table.item(selected_row, 0).text()  # Obtener ID del usuario seleccionado
        username_field = self.findChild(QLineEdit, "username")
        password_field = self.findChild(QLineEdit, "password")

        username = username_field.text().strip()
        password = password_field.text().strip()

        if not username or not password:
            print("Error: El nombre de usuario y la contraseña no pueden estar vacíos.")
            return

        if self.crud.update_user(user_id, username, password):  # Usar el método del controlador
            print("Usuario actualizado exitosamente.")
            self.refresh_users()  # Recargar la tabla con los datos actualizados
            username_field.clear()
            password_field.clear()
        else:
            print("Error al actualizar el usuario.")


    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            print("Error: Seleccione un usuario de la tabla para eliminar.")
            return

        user_id = self.table.item(selected_row, 0).text()  # Obtener el ID del usuario seleccionado

        confirmation = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al usuario con ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            if self.crud.delete_user(user_id):  # Llamar al método del controlador
                print("Usuario eliminado exitosamente.")
                self.refresh_users()  # Recargar la tabla para reflejar los cambios
            else:
                print("Error al eliminar el usuario.")

    def refresh_users(self):
        self.load_all_users()

    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
    def return_to_login(self):
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from views.login_view import LoginForm
        self.loginreturn = LoginForm()
        self.loginreturn.show()
        self.close()    
    def permisos_user(self):
        from test.permission import PermisosUsuarios
        self.permisos = PermisosUsuarios()
        self.permisos.show()