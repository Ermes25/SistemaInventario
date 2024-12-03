import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtGui import QFont, QPixmap, QPainter, QImage, QIcon
from PyQt6.QtCore import Qt, QRect, QUrl
from PyQt6.QtGui import QDesktopServices
from utils.database import Conexion
import json

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sessions = []
        self.config_dir = "app/utils/allow"
        self.config_file = os.path.join(self.config_dir, "sessions_config.json")
        self.load_previous_sessions()  # Cargar usuarios anteriores al iniciar

    def initUI(self):
        self.setWindowTitle('Farma Bienestar - Login')
        self.setMinimumSize(1200, 700)  # Set minimum size for the window
        self.setWindowIcon(QIcon('images/Backgrounds/Farma_Bienestar.png'))  # Set window icon

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Login frame
        self.frame = QFrame(self)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        self.frame.setFixedSize(320, 420)
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(25, 25, 25, 25)

        # Logo
        logo_label = QLabel(self.frame)
        logo_pixmap = QPixmap("images/logins/user_icon.png")
        logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(logo_label)

        # Login text with shadow
        title_label = QLabel("LOGIN", self.frame)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("""
            color: #333333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        """)
        frame_layout.addWidget(title_label)

        # Username input with icon
        username_container = QHBoxLayout()
        username_icon = QLabel()
        username_icon.setPixmap(QPixmap("images/logins/usr.png").scaled(20, 20))
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
        password_icon.setPixmap(QPixmap("images/logins/pwd.png").scaled(20, 20))
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
        login_button = QPushButton("INICIAR SESIÓN")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #5CD6C9;
                color: white;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Arial';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4BC0B5;
            }
        """)
        login_button.clicked.connect(self.on_login_clicked)
        frame_layout.addWidget(login_button)

        # Establecer el botón como predeterminado
        login_button.setDefault(True)

        # Permitir también activar el botón con Enter/Intro
        login_button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Asegura que el botón pueda recibir el enfoque

        # Si el foco está en un campo de texto, al presionar Enter se ejecutará la acción del botón


        # Additional icon and label below login button
        bottom_container = QHBoxLayout()

        # Manual icon (unchanged position)
        bottom_icon = QLabel()
        bottom_icon_pixmap = QPixmap("images/Backgrounds/icon_exclamation_mark.png")
        bottom_icon.setPixmap(bottom_icon_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        bottom_container.addWidget(bottom_icon)
        bottom_container.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottom_icon.mousePressEvent = self.open_manual  # Event added to open manual

        frame_layout.addLayout(bottom_container)

        # Add stretch to push everything up
        frame_layout.addStretch()

        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        # Reposition the frame when the window is resized
        self.frame.move(self.width() - self.frame.width() - 50, (self.height() - self.frame.height()) // 2)
    def ensure_config_directory(self):
        """Crear el directorio de configuración si no existe."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def load_previous_sessions(self):
        """Cargar sesiones desde el archivo JSON configurado."""
        self.ensure_config_directory()  # Asegurarnos de que el directorio exista

        try:
            # Leer la configuración para obtener la ruta del archivo de sesiones
            with open(self.config_file, "r") as config_file:
                config = json.load(config_file)
                file_path = config.get("file_path", "")

            if file_path and os.path.exists(file_path):
                with open(file_path, "r") as session_file:
                    self.sessions = json.load(session_file)
            else:
                self.sessions = []

        except (FileNotFoundError, json.JSONDecodeError):
            # Si no hay configuración o está dañada, inicializar lista vacía
            self.sessions = []
    def save_session(self, username):
        """Agregar una nueva sesión al archivo de sesiones."""
        if username.lower() != "admin" and username not in self.sessions:
            self.sessions.append(username)
    def closeEvent(self, event):
        """Al cerrar el programa, guardar las sesiones en el archivo seleccionado por el usuario."""
        self.ensure_config_directory()  # Asegurarnos de que el directorio exista

        try:
            # Leer la configuración para obtener la ruta del archivo de sesiones
            with open(self.config_file, "r") as config_file:
                config = json.load(config_file)
                file_path = config.get("file_path", "")
        except (FileNotFoundError, json.JSONDecodeError):
            file_path = ""

        if not file_path:
            # Si no hay archivo configurado, pedir al usuario que seleccione la ubicación
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Seleccionar ubicación para guardar las sesiones",
                "",
                "Archivos JSON (*.json)"
            )
            if file_path:
                # Guardar la ruta del archivo en la configuración
                with open(self.config_file, "w") as config_file:
                    json.dump({"file_path": file_path}, config_file, indent=4)

        if file_path:
            # Guardar las sesiones en el archivo
            try:
                with open(file_path, "w") as session_file:
                    json.dump(self.sessions, session_file, indent=4)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar las sesiones: {str(e)}")

        # Llamar al evento de cierre predeterminado
        super().closeEvent(event)

    def on_login_clicked(self):
        """Conectar el botón de login con el controlador."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Crear una instancia de la clase Conexion para conectar a la base de datos
        db = Conexion('localhost', 'root', '', 'sistemainventario')

        # Verificar las credenciales del usuario
        result = db.authenticate_user(username, password)

        if result in ["usuario", "dashboard"]:
            self.save_session(username)  # Guardar la sesión si es válida
            if result == "usuario":
                self.open_users_window()
            else:
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                self.open_dashboard()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

        db.close()

    def open_manual(self, event):
        """Abrir archivo PDF de manual."""
        pdf_path = "app/utils/manual.pdf"
        if os.path.exists(pdf_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo: {pdf_path}")

    def open_users_window(self):
        from views.user_view import InventoryUsuarios
        self.usuarios_window = InventoryUsuarios()
        self.usuarios_window.show()
        self.close()

    def open_dashboard(self):
        from views.Dashboard import Dashboard
        self.Dashboard = Dashboard()
        self.Dashboard.show()
        self.close()

    def paintEvent(self, event):
        """Evento de pintura para establecer la imagen de fondo"""
        painter = QPainter(self)
        background = QImage("images/Backgrounds/Background.jpg")
        if not background.isNull():
            scaled_background = background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

            # Calcular las coordenadas para centrar la imagen
            x = (scaled_background.width() - self.width()) // 2
            y = (scaled_background.height() - self.height()) // 2

            # Dibujar la parte central de la imagen para llenar toda la ventana
            target_rect = self.rect()
            source_rect = QRect(x, y, self.width(), self.height())
            painter.drawImage(target_rect, scaled_background, source_rect)

