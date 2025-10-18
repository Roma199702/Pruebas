class BonoSemanal:
    def __init__(self, puntos_bono=10):
        self.puntos_bono = puntos_bono
        self.aplicado_por_semana = {}  # suscriptor_id -> set de semanas ya bonificadas

    def aplicar_bono(self, suscriptor, semana):
        if semana not in suscriptor.retiros_validos_semana:
            return
        if suscriptor.retiros_validos_semana[semana] >= 3:
            if suscriptor.id_suscriptor not in self.aplicado_por_semana:
                self.aplicado_por_semana[suscriptor.id_suscriptor] = set()
            if semana not in self.aplicado_por_semana[suscriptor.id_suscriptor]:
                suscriptor.agregar_puntos(self.puntos_bono, f"Bono semanal aplicado, semana {semana}")
                self.aplicado_por_semana[suscriptor.id_suscriptor].add(semana)