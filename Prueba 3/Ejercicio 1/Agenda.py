from Cita import Cita, Estado, ErrorAgenda

class Agenda:
    def __init__(self):
        self.citas = []

    def agregar(self, cita: Cita):
        # id único
        for c in self.citas:
            if c.id_cita == cita.id_cita:
                raise ErrorAgenda(f"Ya existe una cita con id {cita.id_cita}")
        # validar solape si tiene duración
        if cita.duracion_min is not None:
            if self.existe_solape(cita.profesional, cita.inicio, cita.duracion_min):
                raise ErrorAgenda("Solape con otra cita del mismo profesional")

        self.citas.append(cita)

    def existe_solape(self, profesional, inicio, duracion_min, exclude_id=None):
        fin = inicio + duracion_min
        for otra in self.citas:
            if otra.id_cita == exclude_id:
                continue
            if otra.profesional != profesional:
                continue
            if otra.estado == Estado.CANCELADA or otra.duracion_min is None:
                continue

            otra_inicio = otra.inicio
            otra_fin = otra_inicio + otra.duracion_min

            # regla de solapamiento
            if inicio < otra_fin and otra_inicio < fin:
                return True
        return False

    def __repr__(self):
        return f"Agenda({self.citas})"