class pedidos_Modelos:
    def __init__(self,
                 id_produ,
                 id_prove,
                 nombre_cliente,
                 fecha_pedido,
                 cantidad_pedido,
                 id_pedido = None):
        self.id_produ = id_produ
        self.id_prove = id_prove
        self.nombre_cliente = nombre_cliente
        self.fecha_pedido = fecha_pedido
        self.cantidad_pedido = cantidad_pedido
        self.id_pedido = id_pedido

    def __str__(self):
        return self.id_pedido
    def cantidad_obt(self):
        return self.cantidad_pedido
    def productos_obtener(self):
        return self.id_produ
    def prove_obtener(self):
        return self.id_prove
    
        