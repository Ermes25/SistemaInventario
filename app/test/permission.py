from PyQt6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, QApplication
from PyQt6.QtGui import QIcon
class PermisosUsuarios(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_role = None
        self.setWindowIcon(QIcon("app/images/Backgrounds/Farma_Bienestar.png"))
        self.setWindowTitle("Permisos de usuarios")
        self.setFixedSize(200, 100)

        # Layout principal
        layout = QVBoxLayout()

        # Opciones de roles
        self.viewer_radio = QRadioButton("Vizualizador")
        self.controller_radio = QRadioButton("Controlador")
        layout.addWidget(self.viewer_radio)
        layout.addWidget(self.controller_radio)

        # Botón para asignar permisos
        self.assign_button = QPushButton("Asignar")
        self.assign_button.clicked.connect(self.assign_permissions)
        layout.addWidget(self.assign_button)

        self.setLayout(layout)

    def assign_permissions(self):
        if self.viewer_radio.isChecked():
            self.selected_role = "vizualizador"
        elif self.controller_radio.isChecked():
            self.selected_role = "controlador"
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione un rol.")
            return

        QMessageBox.information(self, "Éxito", f"Rol asignado: {self.selected_role}")
        self.accept()

import sys
def main():
    app = QApplication(sys.argv)
    # Crear la ventana del formulario de login
    login = PermisosUsuarios()
    # Mostrar la ventana
    login.show()
    # Ejecutar el bucle de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()