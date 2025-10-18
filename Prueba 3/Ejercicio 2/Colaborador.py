class Colaborador:
    def __init__(self, id_colaborador, nombre, horas_semana_max, preferencia, no_disponible=None):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if horas_semana_max <= 0:
            raise ValueError("horas_semana_max debe ser > 0.")
        if preferencia not in ("manana", "tarde", "indistinto"):
            raise ValueError("Preferencia inválida.")

        self.id_colaborador = id_colaborador
        self.nombre = nombre
        self.horas_semana_max = horas_semana_max
        self.preferencia = preferencia
        self.no_disponible = no_disponible or []
        self.historial_eventos = []
        self.turnos_asignados = []

    def registrar_evento(self, tipo, detalle):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def horas_asignadas_semana(self):
        return sum(t.franja.duracion_horas() for t in self.turnos_asignados)

    def disponible(self, dia, hora_inicio, hora_fin):
        for bloque in self.no_disponible:
            if bloque["dia"] == dia and not (hora_fin <= bloque["hora_inicio"] or hora_inicio >= bloque["hora_fin"]):
                return False
        return True

    def __str__(self):
        return f"{self.nombre} ({self.preferencia}, {self.horas_asignadas_semana()}/{self.horas_semana_max}h)"