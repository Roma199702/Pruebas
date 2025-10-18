class Reserva:
    def __init__(self, id_reserva, cancha, cliente, inicio, fin):
        if not cliente:
            raise ValueError("Cliente no puede estar vacío.")
        if inicio >= fin:
            raise ValueError("Inicio debe ser anterior a fin.")
        self.id_reserva = id_reserva
        self.cancha = cancha
        self.cliente = cliente
        self.inicio = inicio
        self.fin = fin
        self.estado = "creada"
        self.importe = None
        self.desglose_tarifa = []
        self.historial_eventos = []

    def registrar_evento(self, tipo, detalle="", monto=None):
        evento = {"tipo": tipo, "detalle": detalle}
        if monto is not None:
            evento["monto"] = monto
        self.historial_eventos.append(evento)

    def cotizar(self, tarifa):
        if self.estado != "creada":
            raise ValueError("Solo se puede cotizar una reserva creada.")
        resultado = tarifa.calcular_importe(self.inicio, self.fin)
        self.importe = resultado["total"]
        self.desglose_tarifa = resultado["desglose"]
        self.registrar_evento("cotizada", f"Importe {self.importe}")

    def confirmar(self, motivo, reservas_existentes):
        if self.estado not in ["creada"]:
            raise ValueError("Solo se puede confirmar una reserva creada.")
        # Validar solape
        for r in reservas_existentes:
            if r.cancha.id_cancha == self.cancha.id_cancha and r.estado != "cancelada":
                if self.inicio < r.fin and r.inicio < self.fin:
                    raise ValueError("Conflicto: reserva solapada en la misma cancha.")
        # Validar mantención
        if self.cancha.calendario.intersecta(self.inicio, self.fin):
            raise ValueError("La cancha está en mantención en ese horario.")
        self.estado = "confirmada"
        self.registrar_evento("confirmada", motivo)

    def cancelar(self, motivo, politica, horas_previas):
        if self.estado not in ["creada", "confirmada"]:
            raise ValueError("Solo se puede cancelar reservas creadas o confirmadas.")
        penal = politica.penalizacion(horas_previas, self.importe or 0)
        self.estado = "cancelada"
        self.registrar_evento("cancelada", f"{motivo} - {penal['motivo']}",["monto"])

    def marcar_no_show(self, motivo):
        if self.estado != "confirmada":
            raise ValueError("Solo reservas confirmadas pueden marcarse como no_show.")
        self.estado = "no_show"
        self.registrar_evento("no_show", motivo)