import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtCore import Qt
from utils.database import Conexion  # Importamos la clase de conexión a la base de datos

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Farma Bienestar - Login')
        self.setFixedSize(1366, 768)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Login frame
        frame = QFrame(self)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(240, 240, 240, 0.95);
                border-radius: 10px;
            }
        """)
        frame.setFixedSize(320, 380)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(25, 25, 25, 25)

        # Logo
        logo_label = QLabel(frame)
        logo_pixmap = QPixmap("app/images/logins/user_icon.png")
        logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(logo_label)

        # Login text
        title_label = QLabel("Login", frame)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20))
        title_label.setStyleSheet("color: #333333;")
        frame_layout.addWidget(title_label)

        # Username input with icon
        username_container = QHBoxLayout()
        username_icon = QLabel()
        username_icon.setPixmap(QPixmap("app/images/logins/usr.png").scaled(20, 20))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFont(QFont("Arial", 11))
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
        """)
        username_container.addWidget(username_icon)
        username_container.addWidget(self.username_input)
        frame_layout.addLayout(username_container)

        # Password input with icon
        password_container = QHBoxLayout()
        password_icon = QLabel()
        password_icon.setPixmap(QPixmap("app/images/logins/pwd.png").scaled(20, 20))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 11))
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
                color: black;
            }
        """)
        password_container.addWidget(password_icon)
        password_container.addWidget(self.password_input)
        frame_layout.addLayout(password_container)

        # Login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;
                color: #333333;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Arial';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFC000;
            }
        """)
        login_button.clicked.connect(self.on_login_clicked)  # Conectar la acción de login
        frame_layout.addWidget(login_button)

        # Add stretch to push everything up
        frame_layout.addStretch()

        # Center the frame on the window
        frame.move((self.width() - frame.width()) // 2, (self.height() - frame.height()) // 2)

        self.setLayout(main_layout)

    def on_login_clicked(self):
        """Conectar el botón de login con el controlador."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Crear una instancia de la clase Conexion para conectar a la base de datos
        db = Conexion('localhost', 'root', '', 'sistemainventario')

        # Verificar las credenciales del usuario
        result = db.authenticate_user(username, password)

        if result == "usuario":
            # Si el resultado es "usuario", abrir la ventana de usuarios
            self.open_users_window()
        elif result == "dashboard":
            # Si el resultado es "dashboard", abrir el dashboard
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
            self.open_dashboard()  # Si las credenciales son correctas, abrir el dashboard
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

        db.close()  # Cerrar la conexión a la base de datos después de la validación

    def open_users_window(self):
        """Abre la ventana de usuarios al hacer login como admin."""
        from app.views.user_view import InventoryUsuarios # Asegúrate de tener esta vista creada
        self.usuarios_window = InventoryUsuarios()  # Instanciamos la clase de la ventana de usuarios
        self.usuarios_window.show()  # Mostramos la ventana de usuarios
        self.close()  # Cerramos el formulario de login

    def open_dashboard(self):
        """Abre el dashboard al hacer login correctamente."""
        from views.Dashboard import Dashboard  # Importación absoluta de la clase Dashboard
        self.Dashboard = Dashboard()  # Instanciamos la clase Dashboard
        self.Dashboard.show()  # Mostramos el Dashboard
        self.close()  # Cerramos el formulario de login

    def paintEvent(self, event):
        """Evento de pintura para cambiar el fondo de la ventana"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.lightGray)
