from Turno_asignado import TurnoAsignado

class PlanSemanal:
    def __init__(self, semana, franjas):
        self.semana = semana
        self.franjas = franjas
        self.turnos_asignados = []
        self.historial_eventos = []

    def registrar_evento(self, tipo, detalle):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def generar_plan(self, politica, colaboradores):
        turnos_generados = politica.asignar(self.semana, colaboradores, self.franjas)
        for t in turnos_generados:
            nuevo_turno = TurnoAsignado(t["franja"], t["responsable"], t["forzado"])
            self.turnos_asignados.append(nuevo_turno)
            t["responsable"].turnos_asignados.append(nuevo_turno)
        self.registrar_evento("plan_generado", f"Plan semanal generado ({len(self.turnos_asignados)} turnos).")

    def cobertura_porcentaje(self):
        total = len(self.franjas)
        cubiertas = len(self.turnos_asignados)
        return round((cubiertas / total) * 100, 2) if total > 0 else 0

    def valido(self):
        for t in self.turnos_asignados:
            if t.responsable.horas_asignadas_semana() > t.responsable.horas_semana_max:
                return False
        return len(self.turnos_asignados) == len(self.franjas)

    def mostrar_resumen(self):
        print("=== PLAN SEMANAL ===")
        for t in self.turnos_asignados:
            print(t)
        print(f"\nCobertura: {self.cobertura_porcentaje()}%")
        print(f"Plan válido: {'Sí' if self.valido() else 'No'}")