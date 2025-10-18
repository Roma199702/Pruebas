from Colaborador import Colaborador
from Franja import Franja
from Politica_turno import TurnoFlexible
from Plan_semanal import PlanSemanal

def main():
    # Crear colaboradores
    colaboradores = [
        Colaborador(1, "Ana", 20, "manana"),
        Colaborador(2, "Luis", 25, "tarde"),
        Colaborador(3, "Marta", 30, "indistinto")
    ]

    # Definir franjas de la semana
    franjas = [
        Franja("Lunes", 8, 12),
        Franja("Lunes", 14, 18),
        Franja("Martes", 8, 12),
        Franja("Martes", 14, 18),
        Franja("Miércoles", 8, 12),
        Franja("Miércoles", 14, 18)
    ]

    # Crear plan semanal
    plan = PlanSemanal("Semana 1", franjas)
    politica = TurnoFlexible()

    # Generar el plan
    plan.generar_plan(politica, colaboradores)

    # Mostrar resumen
    plan.mostrar_resumen()

if __name__ == "__main__":
    main()
