## Bienvenidos 👋
este repositorio es la creacion de un:
## Sistema de Inventario
Un sistema de inventario es un conjunto de procedimientos y normas que permiten controlar y planificar los materiales y productos que utiliza. También se le conoce como control de existencias
## Herramientas
![Python](https://img.icons8.com/?size=100&id=13441&format=png&color=000000)![Mysql](https://img.icons8.com/?size=100&id=9nLaR5KFGjN0&format=png&color=000000)

# 📦 Sistema de Inventario - Manual Tecnico

## ✨ Introducción

El **Sistema de Inventario** es una herramienta diseñada para facilitar la gestión de productos, proveedores y datos relacionados. Este software permite:

- 📝 **Registrar** y **actualizar** información clave.
- 📊 **Supervisar** datos desde una plataforma centralizada.
- 🎯 **Optimizar** el manejo de inventarios y tomar decisiones empresariales informadas.

---

## 🛠️ Requisitos del Sistema

### Stacks:
- 🐍 **Lenguaje**: Python 3.10 o superior.
- 🖼️ **Framework**: PyQt6 para la interfaz gráfica.
- 🗄️ **Base de datos**: MySQL (compatible con otras bases de datos SQL).
- ⚙️ **ORM**: SQLAlchemy.

### Hardware:
- ⚡ **Procesador**: Intel i3 o superior.
- 💾 **RAM**: 4 GB mínimo.
- 📂 **Espacio en disco**: 500 MB libres.

---

## 🚀 Instalación

### Paso 1: Clonar el repositorio
https://github.com/Ermes25/system_inventary.git

### Paso 2: Configuración inicial

1. Abre el archivo de configuración del sistema, usualmente llamado `config.py` o similar.
2. Localiza la sección de **configuración de la base de datos**.
3. Edita los valores correspondientes para que coincidan con tu entorno. Por ejemplo:

python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'nombre_de_tu_base_de_datos'
}

### Paso 3: Ejecución del sistema

1. Asegúrate de que todos los requisitos estén instalados y configurados correctamente.
2. Navega al directorio donde se encuentra el archivo principal del sistema (`main.py`).
3. Ejecuta el siguiente comando para iniciar el sistema:
4. python main.py

## 📂 Estructura del Sistema

- 🔐 **Módulo de Autenticación**: Permite a los usuarios iniciar sesión y acceder al sistema de manera segura.
- 🛒 **Gestión de Productos**: Ofrece herramientas para agregar, editar y eliminar productos del inventario.
- 📇 **Gestión de Proveedores**: Administra los datos de los proveedores asociados al negocio.
- 📊 **Dashboard**: Proporciona una visión general de las métricas clave, como el total de productos y proveedores registrados.

---

## 🖱️ Uso del Sistema

### 1️⃣ Inicio de Sesión
1. Ejecuta el archivo `main.py`.
2. Ingresa tu nombre de usuario y contraseña.
3. Haz clic en **'Iniciar sesión'**.

### 2️⃣ Gestión de Productos
1. Accede al módulo de productos desde el menú principal.
2. Usa las opciones para:
   - 🆕 **Agregar productos**.
   - ✏️ **Editar productos existentes**.
   - 🗑️ **Eliminar productos** del inventario.

### 3️⃣ Gestión de Proveedores
1. Ve al módulo de proveedores desde el menú principal.
2. Administra la información de los proveedores:
   - Agrega nuevos proveedores.
   - Actualiza los datos de los existentes.

### 4️⃣ Uso del Dashboard
Consulta métricas clave como:
- 🔢 Total de productos registrados.
- 🛍️ Número de proveedores asociados.

---

## 🛠️ Resolución de Problemas

### 🐍 **Error**: `ModuleNotFoundError: No module named 'PyQt6'`
**Solución**: Instala la librería necesaria ejecutando:
```bash
pip install PyQt6
pip install PyQt6 tools
pip install mysql-connector-python
