class CalendarioCancha:
    def __init__(self):
        self.mantencion = []

    def agregar(self, inicio, fin):
        if inicio >= fin:
            raise ValueError("El inicio debe ser anterior al fin.")
        if self.intersecta(inicio, fin):
            raise ValueError("El bloque de mantención se solapa con otro existente.")
        self.mantencion.append({"inicio": inicio, "fin": fin})

    def intersecta(self, inicio, fin):
        for bloque in self.mantencion:
            if inicio < bloque["fin"] and bloque["inicio"] < fin:
                return True
        return False