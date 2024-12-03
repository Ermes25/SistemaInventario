class proveedores_Modelos:
    def __init__(self,
                 nombre_proveedor ,
                 numero_proveedor ,
                 email ,
                 id_proveedores = None):
        
        self.nombre_proveedor = nombre_proveedor
        self.numero_proveedor = numero_proveedor
        self.email = email
        self.id_proveedores = id_proveedores

    def __str__(self):
        return self.nombre_proveedor
    def contacto(self):
        return self.numero_proveedor,self.email
        