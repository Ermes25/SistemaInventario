import sys
from PyQt6.QtWidgets import QApplication
from views.login_view import LoginForm

def main():
    app = QApplication(sys.argv)
    login_window = LoginForm()  # Creamos la ventana del login
    login_window.show()  # Mostramos la ventana del login
    sys.exit(app.exec())  # Iniciamos el ciclo de eventos de la aplicación

if __name__ == "__main__":
    main()
