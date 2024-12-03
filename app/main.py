import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from views.login_view import LoginForm
from PyQt6.QtWidgets import QApplication
  

def main():
    app = QApplication(sys.argv)
    # Crear la ventana del formulario de login
    login = LoginForm()
    # Mostrar la ventana
    login.show()
    # Ejecutar el bucle de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
