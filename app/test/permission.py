# permissions.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QPushButton, QMessageBox

class PermisosUsuarios(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.selected_role = None
        self.setWindowTitle("Asignar Permisos")
        self.setFixedSize(200, 150)

        layout = QVBoxLayout()

        self.viewer_radio = QRadioButton("Vizualizador")
        self.controller_radio = QRadioButton("Controlador")
        layout.addWidget(self.viewer_radio)
        layout.addWidget(self.controller_radio)

        assign_button = QPushButton("Asignar")
        assign_button.clicked.connect(self.assign_role)
        layout.addWidget(assign_button)

        self.setLayout(layout)

    def assign_role(self):
        if self.viewer_radio.isChecked():
            self.selected_role = "vizualizador"
        elif self.controller_radio.isChecked():
            self.selected_role = "controlador"
        else:
            QMessageBox.warning(self, "Error", "Seleccione un rol.")
            return

        self.accept()  # Cierra el diálogo y permite continuar en user_view.py
