from Evento import Evento
from Servicio import Servicio

class ErrorAgenda(Exception):
    pass


class Estado:
    CREADA = "creada"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"


class Cita:
    def __init__(self, id_cita, cliente, profesional, inicio):
        if not cliente.strip():
            raise ValueError("El cliente no puede estar vacío")
        if not profesional.strip():
            raise ValueError("El profesional no puede estar vacío")

        self.id_cita = id_cita
        self.cliente = cliente
        self.profesional = profesional
        self.inicio = inicio  # aquí puede ser número o texto
        self.duracion_min = None
        self.estado = Estado.CREADA
        self.historial_eventos = []

    def asignar_servicio(self, servicio: Servicio):
        duracion = servicio.duracion_min()
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor que 0")
        self.duracion_min = duracion
        self.historial_eventos.append(Evento("servicio_asignado", f"Duración {duracion} min"))

    def confirmar(self, motivo, agenda):
        if self.estado != Estado.CREADA:
            raise ErrorAgenda("Solo se puede confirmar si está 'creada'")
        if self.duracion_min is None:
            raise ErrorAgenda("No tiene servicio asignado")
        if agenda.existe_solape(self.profesional, self.inicio, self.duracion_min, self.id_cita):
            raise ErrorAgenda("Existe solape con otra cita no cancelada")

        self.estado = Estado.CONFIRMADA
        self.historial_eventos.append(Evento("confirmacion", motivo))

    def cancelar(self, motivo):
        if self.estado not in (Estado.CREADA, Estado.CONFIRMADA):
            raise ErrorAgenda("Solo se puede cancelar si está 'creada' o 'confirmada'")
        self.estado = Estado.CANCELADA
        self.historial_eventos.append(Evento("cancelacion", motivo))

    def fin(self):
        if self.duracion_min is None:
            return None
        return self.inicio + self.duracion_min

    def __repr__(self):
        return f"Cita({self.id_cita}, {self.cliente}, {self.profesional}, inicio={self.inicio}, dur={self.duracion_min}, estado={self.estado})"
