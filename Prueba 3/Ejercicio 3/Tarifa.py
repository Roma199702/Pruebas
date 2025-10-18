class Tarifa:
    def calcular_importe(self, inicio, fin):
        raise NotImplementedError

class TarifaDiurna(Tarifa):
    def calcular_importe(self, inicio, fin):
        return {"total": 10000, "desglose": [{"tipo": "diurna", "minutos": 60, "subtotal": 10000}]}

class TarifaNocturna(Tarifa):
    def calcular_importe(self, inicio, fin):
        return {"total": 15000, "desglose": [{"tipo": "nocturna", "minutos": 60, "subtotal": 15000}]}

class TarifaFinDeSemana(Tarifa):
    def calcular_importe(self, inicio, fin):
        return {"total": 20000, "desglose": [{"tipo": "findesemana", "minutos": 60, "subtotal": 20000}]}