"""
EJERCICIO 1: Agenda de Peluquería y Barbería
Archivo principal que demuestra el funcionamiento del sistema
"""

from datetime import datetime, timedelta
from clases.servicio import CorteCabello, Coloracion
from clases.cita import Cita
from clases.agenda import Agenda

def imprimir_separador(titulo):
    """Helper para imprimir secciones"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)


def mostrar_historial(cita: Cita):
    """Muestra el historial de eventos de una cita"""
    print(f"\n  📋 Historial de eventos de Cita #{cita.id_cita}:")
    for evento in cita.historial_eventos:
        timestamp = evento['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        print(f"    [{timestamp}] {evento['tipo']}: {evento['detalle']}")


def main():
    print("\n" + "🌟"*35)
    print("  SISTEMA DE AGENDA - PELUQUERÍA Y BARBERÍA")
    print("🌟"*35)
    
    # ========================================================================
    # 1. CREAR AGENDA
    # ========================================================================
    imprimir_separador("1. CREACIÓN DE LA AGENDA")
    agenda = Agenda()
    print(f"✅ {agenda}")
    
    # ========================================================================
    # 2. CREAR SERVICIOS 
    # ========================================================================
    imprimir_separador("2. SERVICIOS DISPONIBLES (Polimorfismo)")
    corte = CorteCabello()
    coloracion = Coloracion()
    
    print(f"✅ Servicio creado: {corte}")
    print(f"✅ Servicio creado: {coloracion}")
    
    # ========================================================================
    # 3. CREAR CITAS
    # ========================================================================
    imprimir_separador("3. CREACIÓN DE CITAS")
    
    # Cita 1: Juan con María (Corte)
    cita1 = Cita(
        id_cita="C001",
        cliente="Juan Pérez",
        profesional="María González",
        inicio=datetime.now() + timedelta(days=1, hours=9)
    )
    print(f"✅ Cita creada: {cita1}")
    
    # Cita 2: Ana con María (Coloración)
    cita2 = Cita(
        id_cita="C002",
        cliente="Ana Martínez",
        profesional="María González",
        inicio=datetime.now() + timedelta(days=1, hours=10)
    )
    print(f"✅ Cita creada: {cita2}")
    
    # Cita 3: Pedro con Carlos (Corte)
    cita3 = Cita(
        id_cita="C003",
        cliente="Pedro López",
        profesional="Carlos Ramírez",
        inicio=datetime.now() + timedelta(days=1, hours=9)
    )
    print(f"✅ Cita creada: {cita3}")
    
    # ========================================================================
    # 4. ASIGNAR SERVICIOS
    # ========================================================================
    imprimir_separador("4. ASIGNACIÓN DE SERVICIOS")
    
    cita1.asignar_servicio(corte)
    print(f"✅ Servicio asignado a Cita #C001: {corte}")
    print(f"   Inicio: {cita1.inicio.strftime('%H:%M')} | Fin: {cita1.fin.strftime('%H:%M')} | Duración: {cita1.duracion_min} min")
    
    cita2.asignar_servicio(coloracion)
    print(f"✅ Servicio asignado a Cita #C002: {coloracion}")
    print(f"   Inicio: {cita2.inicio.strftime('%H:%M')} | Fin: {cita2.fin.strftime('%H:%M')} | Duración: {cita2.duracion_min} min")
    
    cita3.asignar_servicio(corte)
    print(f"✅ Servicio asignado a Cita #C003: {corte}")
    print(f"   Inicio: {cita3.inicio.strftime('%H:%M')} | Fin: {cita3.fin.strftime('%H:%M')} | Duración: {cita3.duracion_min} min")
    
    # ========================================================================
    # 5. AGREGAR CITAS A LA AGENDA
    # ========================================================================
    imprimir_separador("5. AGREGAR CITAS A LA AGENDA")
    
    agenda.agregar(cita1)
    print(f"✅ Cita #C001 agregada a la agenda")
    
    # Intentar agregar cita2 (debería detectar solape con cita1)
    print(f"\n⚠️  Intentando agregar Cita #C002 (María González: 10:00-11:30)...")
    print(f"   La Cita #C001 ocupa: 09:00-09:30")
    hay_solape = agenda.existe_solape(cita2.profesional, cita2.inicio, cita2.fin)
    print(f" ¿Hay solape? {'Sí' if hay_solape else 'No hay solape'}")

    
    try:
        agenda.agregar(cita2)
    except ValueError as e:
        print(f"❌ No se puede modificar el horario: ya existe una cita con ID {cita2.id_cita}")
    
    # Modificar cita2 para que no haya solape
    cita2_nueva = Cita(
        id_cita="C002",
        cliente="Ana Martínez",
        profesional="María González",
        inicio=datetime.now() + timedelta(days=1, hours=10)
    )
    cita2_nueva.asignar_servicio(coloracion)
    
    print(f"\n✅ Modificando horario de Cita #C002 a 10:00-11:30")
    try:
        agenda.agregar(cita2)
        print(f"✅ Cita #C002 agregada exitosamente")
    except ValueError:
        print(f"❌ No se puede modificar el horario: ya existe una cita con ID {cita2.id_cita}")

    
    # Agregar cita3 (diferente profesional, no hay conflicto)
    agenda.agregar(cita3)
    print(f"✅ Cita #C003 agregada a la agenda (profesional diferente)")
    
    # ========================================================================
    # 6. CONFIRMAR CITAS
    # ========================================================================
    imprimir_separador("6. CONFIRMACIÓN DE CITAS")
    
    try:
        cita1.confirmar("Cliente confirmó vía WhatsApp", agenda)
        print(f"✅ Cita #C001 confirmada")
        mostrar_historial(cita1)
    except ValueError as e:
        print(f"❌ No se puede confirmar la cita: {e}")

    
    try:
        cita3.confirmar("Cliente confirmó por teléfono", agenda)
        print(f"✅ Cita #C003 confirmada")
        mostrar_historial(cita3)
    except ValueError as e:
        print(f"❌ No se puede confirmar la cita: {e}")

    # ========================================================================
    # 7. CANCELAR CITA
    # ========================================================================
    imprimir_separador("7. CANCELACIÓN DE CITAS")
    
    cita2_nueva.cancelar("Cliente canceló por enfermedad")
    print(f"✅ Cita #C002 cancelada")
    mostrar_historial(cita2_nueva)
    
    # ========================================================================
    # 8. VALIDACIONES Y CASOS DE ERROR
    # ========================================================================
    imprimir_separador("8. PRUEBAS DE VALIDACIÓN")
    
    print("\n📌 Prueba 1: Intentar confirmar una cita sin servicio asignado")
    cita_sin_servicio = Cita(
        id_cita="C004",
        cliente="Laura Sánchez",
        profesional="María González",
        inicio=datetime.now() + timedelta(days=2, hours=14)
    )
    try:
        cita_sin_servicio.confirmar("Confirmación prematura", agenda)
    except ValueError as e:
        print(f"❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 2: Intentar cancelar una cita ya cancelada")
    try:
        cita2_nueva.cancelar("Intentando cancelar de nuevo")
    except ValueError as e:
        print(f"❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 3: Intentar asignar dos servicios a la misma cita")
    try:
        cita1.asignar_servicio(coloracion)
    except ValueError as e:
        print(f"❌ ERROR esperado: {e}")
    
    # ========================================================================
    # 9. REPORTES FINALES
    # ========================================================================
    imprimir_separador("9. RESUMEN FINAL DE LA AGENDA")
    
    print(f"\n📊 {agenda}")
    print(f"\n📅 Citas por estado:")
    print(f"   • Creadas: {len(agenda.listar_por_estado('creada'))}")
    print(f"   • Confirmadas: {len(agenda.listar_por_estado('confirmada'))}")
    print(f"   • Canceladas: {len(agenda.listar_por_estado('cancelada'))}")
    
    print(f"\n👥 Citas por profesional:")
    print(f"   • María González: {len(agenda.listar_por_profesional('María González'))} cita(s)")
    print(f"   • Carlos Ramírez: {len(agenda.listar_por_profesional('Carlos Ramírez'))} cita(s)")
    
    print("\n" + "🌟"*35)
    print("  FIN DE LA DEMOSTRACIÓN")
    print("🌟"*35 + "\n")


if __name__ == "__main__":
    main()