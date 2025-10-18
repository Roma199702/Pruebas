class Franja:
    def __init__(self, dia, hora_inicio, hora_fin):
        if hora_fin <= hora_inicio:
            raise ValueError("hora_fin debe ser mayor que hora_inicio.")
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def duracion_horas(self):
        return self.hora_fin - self.hora_inicio

    def __str__(self):
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin}"