class TurnoAsignado:
    def __init__(self, franja, responsable, marcado_forzado=False):
        self.franja = franja
        self.responsable = responsable
        self.marcado_forzado = marcado_forzado
        self.historial_eventos = []

        self.registrar_evento("asignacion", f"Turno asignado a {responsable.nombre} ({'forzado' if marcado_forzado else 'normal'})")

    def registrar_evento(self, tipo, detalle):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def duracion_horas(self):
        return self.franja.duracion_horas()

    def __str__(self):
        estado = "Forzado" if self.marcado_forzado else "Normal"
        return f"{self.franja} → {self.responsable.nombre} ({estado})"
