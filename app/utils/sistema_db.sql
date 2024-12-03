-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS sistemainventario;

-- Usar la base de datos recién creada
USE sistemainventario;

-- Crear la tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(255) NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Almacena fecha y hora de ingreso automáticamente
    fecha_vencimiento YEAR,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proveedor VARCHAR(255) NOT NULL,
    numero_proveedor VARCHAR(15), 
    email VARCHAR(255) NOT NULL
);

-- Crear la tabla de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    id_proveedor INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Almacena fecha y hora del pedido automáticamente
    cantidad_pedido INT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

-- Crear la tabla de usuarios (para la autenticación)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL 
);
