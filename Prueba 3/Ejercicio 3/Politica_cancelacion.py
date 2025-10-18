class PoliticaCancelacion:
    def penalizacion(self, horas_previas, importe):
        raise NotImplementedError

class CancelacionFlexible(PoliticaCancelacion):
    def penalizacion(self, horas_previas, importe):
        if horas_previas >= 24:
            return {"monto_penalizacion": 0, "motivo": "Sin penalización (aviso ≥24h)"}
        else:
            return {"monto_penalizacion": round(importe * 0.2, 2), "motivo": "Penalización 20% (<24h)"}

class CancelacionEstricta(PoliticaCancelacion):
    def penalizacion(self, horas_previas, importe):
        return {"monto_penalizacion": round(importe * 0.5, 2), "motivo": "Penalización 50% (estricta)"}