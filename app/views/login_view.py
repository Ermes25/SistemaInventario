import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from utils.database import Conexion 

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Conexion("localhost", "root", "", "sistemainventario")  # Conexión a la base de datos
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Sistema de inventario')
        self.setFixedSize(1366, 768)

        # Establecer imagen de fondo
        background = QLabel(self)
        background.setPixmap(QPixmap("app/images/Backgrounds/background_Dashboard.jpeg"))
        background.setScaledContents(True)
        background.setGeometry(0, 0, 1366, 768)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(200, 150, 200, 150)

        frame = QFrame(self)
        frame.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        frame_layout = QVBoxLayout(frame)

        # Icono encima de los campos de ingreso
        logo_label = QLabel(frame)
        logo_pixmap = QPixmap("app/images/logins/user_1.png")
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(logo_label)

        title_label = QLabel("Iniciar sesión", frame)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 24, QFont.Weight.Bold))
        frame_layout.addWidget(title_label)
        title_label.setStyleSheet("color: black;")

        # Entrada de nombre de usuario con icono
        username_layout = QHBoxLayout()
        username_icon = QLabel()
        username_icon.setPixmap(QPixmap("app/images/logins/user_credential.png").scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFont(QFont("Times New Roman", 16))
        self.username_input.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 150); border: 1px solid gray; border-radius: 5px; padding: 5px;")
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username_input)
        frame_layout.addLayout(username_layout)

        # Entrada de contraseña con icono
        password_layout = QHBoxLayout()
        password_icon = QLabel()
        password_icon.setPixmap(QPixmap("app/images/logins/Password.png").scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Times New Roman", 16))
        self.password_input.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 150); border: 1px solid gray; border-radius: 5px; padding: 5px;")
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password_input)
        frame_layout.addLayout(password_layout)

        # Botón de iniciar sesión
        login_button = QPushButton("Ingresar")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #fb7d51;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Times New Roman';
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #FFC700;
            }
        """)
        login_button.clicked.connect(self.handle_login)
        frame_layout.addWidget(login_button)

        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db.authenticate_user(username, password):
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
            self.open_dashboard()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

    def open_dashboard(self):
        """Abre el dashboard al hacer login correctamente."""
        from views.Dashboard import Dashboard  # Importación absoluta de la clase Dashboard
        self.Dashboard = Dashboard()  # Instanciamos la clase Dashboard
        self.Dashboard.show()  # Mostramos el Dashboard
        self.close()  # Cerramos el formulario de login

