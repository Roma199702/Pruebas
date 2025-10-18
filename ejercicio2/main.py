"""
EJERCICIO 2: Turnos para Cafetería Escolar
Archivo principal que demuestra el funcionamiento del sistema
"""

from clases.colaborador import Colaborador
from clases.franja import Franja
from clases.turno_asignado import TurnoAsignado
from clases.politica_turno import TurnoFijo, TurnoRotativo, TurnoFlexible
from clases.plan_semanal import PlanSemanal


def imprimir_separador(titulo):
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)


def mostrar_plan(plan: PlanSemanal):
    """Muestra el plan semanal de forma organizada"""
    print(f"\n📅 {plan}")
    print(f"   Turnos forzados: {plan.contar_turnos_forzados()}")
    
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for dia in dias:
        turnos_dia = plan.obtener_turnos_por_dia(dia)
        if turnos_dia:
            print(f"\n  {dia}:")
            for turno in turnos_dia:
                print(f"    • {turno}")


def mostrar_colaboradores(colaboradores):
    """Muestra el estado de todos los colaboradores"""
    print("\n👥 Estado de colaboradores:")
    for col in colaboradores:
        print(f"   {col}")


def main():
    print("\n" + "☕"*35)
    print("  SISTEMA DE TURNOS - CAFETERÍA ESCOLAR")
    print("☕"*35)
    
    # ========================================================================
    # 1. CREAR COLABORADORES
    # ========================================================================
    imprimir_separador("1. CREACIÓN DE COLABORADORES")
    
    col1 = Colaborador("C001", "María López", 20, "manana")
    col2 = Colaborador("C002", "Juan Pérez", 15, "tarde")
    col3 = Colaborador("C003", "Ana García", 25, "indistinto")
    col4 = Colaborador("C004", "Carlos Ruiz", 18, "manana")
    
    colaboradores = [col1, col2, col3, col4]
    
    print("✅ Colaboradores creados:")
    for col in colaboradores:
        print(f"   • {col}")
    
    # Agregar no disponibilidades
    col1.agregar_no_disponible("Miercoles", "14:00", "16:00")
    col2.agregar_no_disponible("Lunes", "08:00", "12:00")
    
    print("\n📝 Restricciones de disponibilidad:")
    print(f"   • María López: No disponible Miércoles 14:00-16:00")
    print(f"   • Juan Pérez: No disponible Lunes 08:00-12:00")
    
    # ========================================================================
    # 2. CREAR FRANJAS
    # ========================================================================
    imprimir_separador("2. CREACIÓN DE FRANJAS")
    
    franjas = [
        # Lunes
        Franja("Lunes", "08:00", "10:00"),
        Franja("Lunes", "10:00", "12:00"),
        Franja("Lunes", "14:00", "16:00"),
        
        # Martes
        Franja("Martes", "08:00", "10:00"),
        Franja("Martes", "10:00", "12:00"),
        Franja("Martes", "14:00", "16:00"),
        
        # Miércoles
        Franja("Miercoles", "08:00", "10:00"),
        Franja("Miercoles", "10:00", "12:00"),
        Franja("Miercoles", "14:00", "16:00"),
        
        # Jueves
        Franja("Jueves", "08:00", "10:00"),
        Franja("Jueves", "14:00", "16:00"),
        
        # Viernes
        Franja("Viernes", "08:00", "10:00"),
        Franja("Viernes", "10:00", "12:00"),
    ]
    
    print(f"✅ {len(franjas)} franjas creadas")
    total_horas = sum(f.duracion_horas for f in franjas)
    print(f"   Total de horas a cubrir: {total_horas:.1f} horas")
    
    # ========================================================================
    # 3. POLÍTICA TURNO FLEXIBLE
    # ========================================================================
    imprimir_separador("3. PLAN CON POLÍTICA FLEXIBLE")
    
    plan_flexible = PlanSemanal("Semana 1 (17-21 Oct)", franjas)
    politica_flexible = TurnoFlexible()
    
    print("\n🔄 Generando plan con TurnoFlexible...")
    print("   (Prioriza preferencias mañana/tarde)")
    
    plan_flexible.generar_plan(politica_flexible, colaboradores)
    
    mostrar_plan(plan_flexible)
    mostrar_colaboradores(colaboradores)
    
    # ========================================================================
    # 4. POLÍTICA TURNO FIJO
    # ========================================================================
    imprimir_separador("4. PLAN CON POLÍTICA FIJO")
    
    # Resetear colaboradores
    for col in colaboradores:
        col.resetear_horas_semana()
    
    # Definir titulares para algunas franjas
    titulares = {
        ("Lunes", "08:00"): "C001",      # María López
        ("Martes", "08:00"): "C001",     # María López
        ("Miercoles", "08:00"): "C004",  # Carlos Ruiz
        ("Jueves", "08:00"): "C001",     # María López
        ("Viernes", "08:00"): "C004",    # Carlos Ruiz
    }
    
    plan_fijo = PlanSemanal("Semana 1 (17-21 Oct)", franjas)
    politica_fijo = TurnoFijo(titulares)
    
    print("\n🔒 Generando plan con TurnoFijo...")
    print("   (Mantiene titulares por franja)")
    print("\n   Titulares definidos:")
    print("   • Lunes 08:00 → María López")
    print("   • Martes 08:00 → María López")
    print("   • Miércoles 08:00 → Carlos Ruiz")
    
    plan_fijo.generar_plan(politica_fijo, colaboradores)
    
    mostrar_plan(plan_fijo)
    mostrar_colaboradores(colaboradores)
    
    # ========================================================================
    # 5. POLÍTICA TURNO ROTATIVO
    # ========================================================================
    imprimir_separador("5. PLAN CON POLÍTICA ROTATIVO")
    
    # Resetear colaboradores
    for col in colaboradores:
        col.resetear_horas_semana()
    
    plan_rotativo = PlanSemanal("Semana 1 (17-21 Oct)", franjas)
    politica_rotativo = TurnoRotativo()
    
    print("\n🔄 Generando plan con TurnoRotativo...")
    print("   (Evita que la misma persona abra dos días seguidos)")
    
    plan_rotativo.generar_plan(politica_rotativo, colaboradores)
    
    mostrar_plan(plan_rotativo)
    
    # Verificar rotación de aperturas
    print("\n🔍 Verificación de rotación de aperturas:")
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for dia in dias:
        turnos_dia = plan_rotativo.obtener_turnos_por_dia(dia)
        if turnos_dia:
            primer_turno = min(turnos_dia, key=lambda t: t.franja.hora_inicio)
            print(f"   • {dia} apertura (08:00): {primer_turno.responsable.nombre}")
    
    mostrar_colaboradores(colaboradores)
    
    # ========================================================================
    # 6. REASIGNACIONES
    # ========================================================================
    imprimir_separador("6. REASIGNACIONES")
    
    print("\n📝 Reasignando turno del Lunes 10:00-12:00...")
    franja_a_reasignar = Franja("Lunes", "10:00", "12:00")
    
    print(f"   Responsable anterior: ", end="")
    for turno in plan_rotativo.turnos_asignados:
        if turno.franja == franja_a_reasignar:
            print(turno.responsable.nombre)
            break
    
    try:
        plan_rotativo.reasignar(
            franja_a_reasignar,
            col4,  # Carlos Ruiz
            "Cambio por solicitud del colaborador"
        )
        print(f"✅ Turno reasignado a Carlos Ruiz")
    except ValueError as e:
        print(f"❌ No se pudo reasignar: {e}")
    
    # ========================================================================
    # 7. VALIDACIONES Y CASOS DE ERROR
    # ========================================================================
    imprimir_separador("7. PRUEBAS DE VALIDACIÓN")
    
    print("\n📌 Prueba 1: Intentar crear colaborador con horas_semana_max inválido")
    try:
        col_invalido = Colaborador("C999", "Inválido", -5, "manana")
    except ValueError as e:
        print(f"❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 2: Intentar crear franja con hora_inicio >= hora_fin")
    try:
        franja_invalida = Franja("Lunes", "14:00", "14:00")
    except ValueError as e:
        print(f"❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 3: Verificar límite de horas semanales")
    print(f"   María López: {col1.horas_asignadas_semana}/{col1.horas_semana_max} horas")
    if col1.horas_asignadas_semana <= col1.horas_semana_max:
        print(f"   ✅ Dentro del límite permitido")
    
    # ========================================================================
    # 8. ESTADÍSTICAS FINALES
    # ========================================================================
    imprimir_separador("8. ESTADÍSTICAS COMPARATIVAS")
    
    planes = [
        ("Flexible", plan_flexible),
        ("Fijo", plan_fijo),
        ("Rotativo", plan_rotativo)
    ]
    
    print("\n📊 Comparación de políticas:\n")
    print(f"{'Política':<15} {'Cobertura':<12} {'Turnos Forzados':<20} {'Válido':<10}")
    print("-" * 57)
    
    for nombre, plan in planes:
        cobertura = f"{plan.cobertura_porcentaje:.1f}%"
        forzados = plan.contar_turnos_forzados()
        valido = "Sí" if plan.valido else "No"
        print(f"{nombre:<15} {cobertura:<12} {forzados:<20} {valido:<10}")
    
    print("\n📈 Distribución de carga por colaborador (Plan Rotativo):")
    for col in colaboradores:
        turnos = plan_rotativo.obtener_turnos_por_colaborador(col)
        print(f"   • {col.nombre}: {len(turnos)} turno(s), {col.horas_asignadas_semana:.1f} horas")
    
    # ========================================================================
    # 9. HISTORIAL DE EVENTOS
    # ========================================================================
    imprimir_separador("9. TRAZABILIDAD - HISTORIAL DE EVENTOS")
    
    print("\n📋 Historial del Plan Rotativo:")
    for evento in plan_rotativo.historial_eventos[-5:]:  # Últimos 5 eventos
        timestamp = evento['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        print(f"   [{timestamp}] {evento['tipo']}: {evento['detalle']}")
    
    print("\n" + "☕"*35)
    print("  FIN DE LA DEMOSTRACIÓN")
    print("☕"*35 + "\n")


if __name__ == "__main__":
    main()