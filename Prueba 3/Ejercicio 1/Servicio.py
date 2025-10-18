class Servicio:
    def duracion_min(self):
        raise NotImplementedError("Debe implementarse en subclase")


class CorteCabello(Servicio):
    def duracion_min(self):
        return 30


class Coloracion(Servicio):
    def duracion_min(self):
        return 90