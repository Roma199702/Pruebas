from Calendario_cancha import CalendarioCancha

class Cancha:
    def __init__(self, id_cancha, nombre):
        self.id_cancha = id_cancha
        self.nombre = nombre
        self.calendario = CalendarioCancha()
        self.historial_eventos = []

    def registrar_evento(self, tipo, detalle=""):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def bloquear_mantencion(self, inicio, fin):
        self.calendario.agregar(inicio, fin)
        self.registrar_evento("mantencion_bloqueada", f"{inicio} - {fin}")

    def desbloquear_mantencion(self, inicio, fin):
        self.calendario.mantencion = [
            b for b in self.calendario.mantencion
            if not (b["inicio"] == inicio and b["fin"] == fin)
        ]
        self.registrar_evento("mantencion_desbloqueada", f"{inicio} - {fin}")