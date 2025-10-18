class Evento:
    def __init__(self, tipo, detalle):
        self.tipo = tipo
        self.detalle = detalle

    def __repr__(self):
        return f"[{self.tipo}] {self.detalle}"