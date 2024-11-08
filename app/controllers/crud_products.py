from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFormLayout, QDialogButtonBox, QMessageBox)
from .crud_controller import ConProducto

class CRUDProductoDialog(QDialog):
    def __init__(self, conexion, parent=None, accion="crear", producto_id=None):
        super().__init__(parent)
        
        self.con_producto = ConProducto(conexion)  # Usamos el controlador de productos
        self.accion = accion
        self.producto_id = producto_id
        
        self.setWindowTitle(f"CRUD Producto - {accion.capitalize()}")
        self.setFixedSize(600, 400)

        self.init_ui()
        
    def init_ui(self):
        """Inicializa los elementos de la interfaz del diálogo"""
        # Layout principal
        layout = QVBoxLayout(self)

        # Título
        title_label = QLabel(f"{self.accion.capitalize()} Producto")
        layout.addWidget(title_label)

        # Formulario de entrada
        form_layout = QFormLayout()

        self.nombre_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.precio_input = QLineEdit()

        form_layout.addRow("Nombre del Producto:", self.nombre_input)
        form_layout.addRow("Categoría:", self.categoria_input)
        form_layout.addRow("Precio:", self.precio_input)

        layout.addLayout(form_layout)

        # Botones
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self
        )
        self.buttons.accepted.connect(self.on_accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        # Si la acción es "editar" o "ver", cargamos los datos
        if self.accion in ["editar", "ver"]:
            self.load_product()

    def load_product(self):
        """Carga un producto existente si la acción es editar o ver"""
        if self.producto_id:
            producto = self.con_producto.get_by_id(self.producto_id)
            if producto:
                self.nombre_input.setText(producto[1])  # Nombre del producto
                self.categoria_input.setText(producto[2])  # Categoría
                self.precio_input.setText(str(producto[3]))  # Precio

    def on_accept(self):
        """Acción al presionar Ok, dependiendo de la acción (crear, editar, etc.)"""
        nombre = self.nombre_input.text().strip()
        categoria = self.categoria_input.text().strip()
        precio = self.precio_input.text().strip()

        if not nombre or not categoria or not precio:
            self.show_message("Error", "Todos los campos son obligatorios.")
            return

        if self.accion == "crear":
            self.create_product(nombre, categoria, precio)
        elif self.accion == "editar":
            self.update_product(nombre, categoria, precio)
        elif self.accion == "eliminar":
            self.delete_product()
        elif self.accion == "buscar":
            self.search_product()

    def create_product(self, nombre, categoria, precio):
        """Crea un nuevo producto"""
        try:
            self.con_producto.insert(Product(nombre, categoria, precio))
            self.show_message("Éxito", "Producto creado exitosamente.")
            self.accept()
        except Exception as e:
            self.show_message("Error", f"Error al crear producto: {str(e)}")

    def update_product(self, nombre, categoria, precio):
        """Actualiza un producto existente"""
        try:
            self.con_producto.update(Product(self.producto_id, nombre, categoria, precio))
            self.show_message("Éxito", "Producto actualizado exitosamente.")
            self.accept()
        except Exception as e:
            self.show_message("Error", f"Error al actualizar producto: {str(e)}")

    def delete_product(self):
        """Elimina un producto"""
        try:
            self.con_producto.delete(self.producto_id)
            self.show_message("Éxito", "Producto eliminado exitosamente.")
            self.accept()
        except Exception as e:
            self.show_message("Error", f"Error al eliminar producto: {str(e)}")

    def search_product(self):
        """Busca un producto por ID"""
        try:
            producto = self.con_producto.get_by_id(self.producto_id)
            if producto:
                self.show_message("Resultado", f"Producto encontrado: {producto[1]} - {producto[2]} - {producto[3]}")
            else:
                self.show_message("No encontrado", "No se encontró el producto.")
        except Exception as e:
            self.show_message("Error", f"Error al buscar producto: {str(e)}")

    def show_message(self, title, message):
        """Muestra un mensaje en un cuadro de diálogo"""
        QMessageBox.information(self, title, message)

# Clase para representar el Producto
class Product:
    def __init__(self, id=None, nombre=None, categoria=None, precio=None):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
