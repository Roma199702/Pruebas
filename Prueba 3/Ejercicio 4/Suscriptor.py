class Suscriptor:
    def __init__(self, id_suscriptor, direccion):
        self.id_suscriptor = id_suscriptor
        self.direccion = direccion
        self.saldo_puntos = 0
        self.estado = "habilitado"
        self.historial_eventos = []
        self.retiros_validos_semana = {}  # semana -> count de retiros validados

    def registrar_evento(self, tipo, detalle):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def agregar_puntos(self, puntos, detalle):
        self.saldo_puntos += puntos
        self.registrar_evento("puntos_acreditados", detalle)