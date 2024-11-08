class productos_Modelos:
    def __init__(self, 
                 nombre_producto,
                 categoria ,
                 fecha_ingreso ,
                 fecha_vencimiento ,
                 cantidad ,
                 precio ,
                 id_productos = None):
        
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.fecha_ingreso = fecha_ingreso
        self.fecha_vencimiento = fecha_vencimiento
        self.cantidad = cantidad
        self.precio = precio
        self.id_productos = id_productos

    def __str__(self):
        return self.nombre_producto
    def precio_obt (self):
        return self.precio
    def categoria_obt (self):
        return self.categoria
    
          