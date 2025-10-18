"""
EJERCICIO 3: Canchas Vecinales
Archivo principal que demuestra el funcionamiento del sistema
"""



from datetime import datetime, timedelta
from clases.cancha import Cancha
from clases.tarifa import TarifaDiurna, TarifaNocturna, TarifaFinDeSemana, TarifaMixta
from clases.politica_cancelacion import CancelacionFlexible, CancelacionEstricta
from clases.reserva import Reserva
from clases.agenda_sistema import AgendaSistema


def imprimir_separador(titulo):
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)


def mostrar_desglose(reserva):
    """Muestra el desglose detallado de tarifas"""
    try:
        if reserva.desglose_tarifa:
            print(f"\n  💰 Desglose de tarifas para Reserva #{reserva.id_reserva}:")
            for tramo in reserva.desglose_tarifa:
                inicio = tramo['desde'].strftime('%H:%M')
                fin = tramo['hasta'].strftime('%H:%M')
                print(f"    • {inicio}-{fin} ({tramo['minutos']} min) - "
                      f"{tramo['tipo_tarifa']}: ${tramo['subtotal']:,.0f}")
            print(f"    TOTAL: ${reserva.importe:,.0f}")
    except Exception as e:
        print(f"    ⚠️  No se pudo mostrar desglose: {e}")


def main():
    print("\n" + "⚽"*35)
    print("  SISTEMA DE RESERVAS - CANCHAS VECINALES")
    print("⚽"*35)
    
    # ========================================================================
    # 1. CREAR CANCHAS Y CALENDARIO
    # ========================================================================
    imprimir_separador("1. CREACIÓN DE CANCHAS")
    
    cancha1 = Cancha("CA001", "Cancha de Fútbol A")
    cancha2 = Cancha("CA002", "Cancha de Fútbol B")
    cancha3 = Cancha("CA003", "Cancha de Tenis")
    
    print("✅ Canchas creadas:")
    print(f"   • {cancha1}")
    print(f"   • {cancha2}")
    print(f"   • {cancha3}")
    
    # ========================================================================
    # 2. BLOQUEAR MANTENCIÓN
    # ========================================================================
    imprimir_separador("2. CALENDARIO DE MANTENCIÓN")
    
    # Bloquear mantención en Cancha A
    mantencion_inicio = datetime.now() + timedelta(days=2, hours=10)
    mantencion_fin = datetime.now() + timedelta(days=2, hours=12)
    
    cancha1.bloquear_mantencion(mantencion_inicio, mantencion_fin)
    
    print(f"🔧 Mantención bloqueada en {cancha1.nombre}:")
    print(f"   {mantencion_inicio.strftime('%Y-%m-%d %H:%M')} - {mantencion_fin.strftime('%H:%M')}")
    print(f"   Total de bloques: {cancha1.cantidad_bloques_mantencion()}")
    
    # ========================================================================
    # 3. CREAR AGENDA DEL SISTEMA
    # ========================================================================
    imprimir_separador("3. INICIALIZACIÓN DEL SISTEMA")
    
    agenda = AgendaSistema()
    print(f"✅ {agenda}")
    
    # ========================================================================
    # 4. TARIFAS Y COTIZACIÓN
    # ========================================================================
    imprimir_separador("4. SISTEMA DE TARIFAS (Polimorfismo)")
    
    tarifa_diurna = TarifaDiurna(10000)
    tarifa_nocturna = TarifaNocturna(15000)
    tarifa_finde = TarifaFinDeSemana(20000)
    tarifa_mixta = TarifaMixta()
    
    print("📊 Tarifas disponibles:")
    print(f"   • Diurna (08:00-19:59): ${tarifa_diurna.valor_hora:,.0f}/hora")
    print(f"   • Nocturna (20:00-07:59): ${tarifa_nocturna.valor_hora:,.0f}/hora")
    print(f"   • Fin de Semana: ${tarifa_finde.valor_hora:,.0f}/hora")
    print(f"   • Mixta: Selección automática con prioridad")
    
    # ========================================================================
    # 5. CREAR Y COTIZAR RESERVAS
    # ========================================================================
    imprimir_separador("5. CREACIÓN Y COTIZACIÓN DE RESERVAS")
    
    print("\n📝 Reserva 1: Diurna (2 horas)")
    r1_inicio = datetime.now() + timedelta(days=1, hours=10)
    r1_fin = r1_inicio + timedelta(hours=2)
    
    reserva1 = Reserva("R001", cancha1, "Juan Pérez", r1_inicio, r1_fin)
    print(f"✅ {reserva1}")
    print(f"   Cotizando con tarifa diurna...")
    
    reserva1.cotizar(tarifa_diurna)
    print(f"   Importe: ${reserva1.importe:,.0f}")
    mostrar_desglose(reserva1)
    
    print("\n📝 Reserva 2: Mixta con cruce de horario (19:00-20:30)")
    r2_inicio = datetime.now() + timedelta(days=1, hours=19)
    r2_fin = r2_inicio + timedelta(hours=1, minutes=30)
    
    reserva2 = Reserva("R002", cancha2, "María López", r2_inicio, r2_fin)
    print(f"✅ {reserva2}")
    print(f"   Cotizando con tarifa mixta...")
    
    reserva2.cotizar(tarifa_mixta)
    print(f"   Importe: ${reserva2.importe:,.0f}")
    mostrar_desglose(reserva2)
    
    print("\n📝 Reserva 3: Fin de semana (2 horas)")
    dias_hasta_sabado = (5 - datetime.now().weekday()) % 7
    if dias_hasta_sabado == 0:
        dias_hasta_sabado = 7
    
    r3_inicio = datetime.now() + timedelta(days=dias_hasta_sabado, hours=14)
    r3_fin = r3_inicio + timedelta(hours=2)
    
    reserva3 = Reserva("R003", cancha1, "Carlos Díaz", r3_inicio, r3_fin)
    print(f"✅ {reserva3}")
    print(f"   Cotizando con tarifa de fin de semana...")
    
    reserva3.cotizar(tarifa_finde)
    print(f"   Importe: ${reserva3.importe:,.0f}")
    mostrar_desglose(reserva3)
    
    # ========================================================================
    # 6. AGREGAR A LA AGENDA Y CONFIRMAR
    # ========================================================================
    imprimir_separador("6. CONFIRMACIÓN DE RESERVAS")
    
    agenda.agregar(reserva1)
    agenda.agregar(reserva2)
    agenda.agregar(reserva3)
    
    print(f"✅ {agenda}")
    
    print(f"\n📝 Confirmando Reserva #R001...")
    try:
        reserva1.confirmar("Cliente pagó señal del 50%", agenda)
        print(f"   ✅ Reserva confirmada exitosamente")
        print(f"   Estado: {reserva1.estado}")
    except ValueError as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n📝 Confirmando Reserva #R002...")
    try:
        reserva2.confirmar("Confirmación telefónica", agenda)
        print(f"   ✅ Reserva confirmada exitosamente")
        print(f"   Estado: {reserva2.estado}")
    except ValueError as e:
        print(f"   ❌ Error: {e}")
    
    # ========================================================================
    # 7. INTENTAR RESERVA EN MANTENCIÓN
    # ========================================================================
    imprimir_separador("7. VALIDACIÓN DE MANTENCIÓN")
    
    print(f"🔧 Mantención programada en {cancha1.nombre}:")
    print(f"   {mantencion_inicio.strftime('%Y-%m-%d %H:%M')} - {mantencion_fin.strftime('%H:%M')}")
    
    r4_inicio = mantencion_inicio - timedelta(minutes=30)
    r4_fin = mantencion_inicio + timedelta(minutes=30)
    
    reserva4 = Reserva("R004", cancha1, "Ana García", r4_inicio, r4_fin)
    print(f"\n⚠️  Intentando confirmar reserva que intersecta mantención...")
    print(f"   Reserva: {r4_inicio.strftime('%d/%m %H:%M')}-{r4_fin.strftime('%H:%M')}")
    
    try:
        reserva4.cotizar(tarifa_diurna)
        agenda.agregar(reserva4)
        reserva4.confirmar("Intento de confirmación", agenda)
        print(f"   ⚠️  ADVERTENCIA: No debería confirmar")
    except ValueError as e:
        print(f"   ✅ Reserva rechazada correctamente")
        print(f"   Motivo: {e}")
    
    # ========================================================================
    # 8. VALIDACIÓN DE SOLAPES
    # ========================================================================
    imprimir_separador("8. VALIDACIÓN DE SOLAPES")
    
    r5_inicio = r1_inicio + timedelta(minutes=30)
    r5_fin = r5_inicio + timedelta(hours=1)
    
    reserva5 = Reserva("R005", cancha1, "Pedro Soto", r5_inicio, r5_fin)
    
    print(f"\n⚠️  Intentando confirmar reserva que se solapa...")
    print(f"   Reserva existente R001: {r1_inicio.strftime('%H:%M')}-{r1_fin.strftime('%H:%M')}")
    print(f"   Nueva reserva R005: {r5_inicio.strftime('%H:%M')}-{r5_fin.strftime('%H:%M')}")
    
    try:
        reserva5.cotizar(tarifa_diurna)
        agenda.agregar(reserva5)
        reserva5.confirmar("Intento de confirmación", agenda)
        print(f"   ⚠️  ADVERTENCIA: No debería confirmar")
    except ValueError as e:
        print(f"   ✅ Reserva rechazada correctamente")
        print(f"   Motivo: {e}")
    
    # ========================================================================
    # 9. POLÍTICAS DE CANCELACIÓN
    # ========================================================================
    imprimir_separador("9. POLÍTICAS DE CANCELACIÓN")
    
    politica_flexible = CancelacionFlexible()
    politica_estricta = CancelacionEstricta()
    
    print("📋 Políticas disponibles:")
    print("   • Flexible: 0% si >24h, 20% si <24h")
    print("   • Estricta: 50% siempre")
    
    # Política Flexible
    r6_inicio = datetime.now() + timedelta(days=5, hours=15)
    r6_fin = r6_inicio + timedelta(hours=1)
    
    reserva6 = Reserva("R006", cancha3, "Laura Vega", r6_inicio, r6_fin)
    reserva6.cotizar(tarifa_diurna)
    agenda.agregar(reserva6)
    
    try:
        reserva6.confirmar("Reserva para cancelar", agenda)
        print("✅ Reserva confirmada exitosamente")
    except ValueError as e:
        print(f"❌ Error esperado: {e}")

    
    print(f"\n💳 Cancelando Reserva #R006 con política flexible...")
    print(f"   Importe original: ${reserva6.importe:,.0f}")
    horas_anticipacion = (r6_inicio - datetime.now()).total_seconds() / 3600
    print(f"   Anticipación: {horas_anticipacion:.1f} horas")
    
    reserva6.cancelar("Cliente canceló por viaje", politica_flexible)
    ultimo_evento = reserva6.historial_eventos[-1]
    print(f"   ✅ Cancelación procesada")
    print(f"   Penalización: ${ultimo_evento.get('monto', 0):,.0f}")
    
    # Política Estricta
    r7_inicio = datetime.now() + timedelta(days=3, hours=18)
    r7_fin = r7_inicio + timedelta(hours=2)
    
    reserva7 = Reserva("R007", cancha2, "Roberto Silva", r7_inicio, r7_fin)
    reserva7.cotizar(tarifa_nocturna)
    agenda.agregar(reserva7)
    
    try:
        reserva7.confirmar("Reserva para cancelar", agenda)
        print("✅ Reserva confirmada exitosamente")
    except ValueError as e:
        print(f"❌ Error esperado: {e}")

    
    print(f"\n💳 Cancelando Reserva #R007 con política estricta...")
    print(f"   Importe original: ${reserva7.importe:,.0f}")
    
    reserva7.cancelar("Cliente canceló", politica_estricta)
    ultimo_evento = reserva7.historial_eventos[-1]
    print(f"   ✅ Cancelación procesada")
    print(f"   Penalización: ${ultimo_evento.get('monto', 0):,.0f}")
    
    # ========================================================================
    # 10. NO-SHOW
    # ========================================================================
    imprimir_separador("10. GESTIÓN DE NO-SHOW")
    
    print(f"\n⚠️  Marcando Reserva #R003 como no-show...")
    print(f"   Cliente: {reserva3.cliente}")
    print(f"   Importe: ${reserva3.importe:,.0f}")
    
    try:
        reserva3.marcar_no_show("Cliente no se presentó a la hora acordada")
        ultimo_evento = reserva3.historial_eventos[-1]
        print(f"✅ {ultimo_evento['detalle']}")
        print(f"Cargo por no-show: $ {ultimo_evento.get('monto', 0):,.0f}")
    except ValueError as e:
        print(f"❌ Error esperado: {e}")

    
    ultimo_evento = reserva3.historial_eventos[-1]
    print(f"   ✅ No-show registrado")
    print(f"   Cargo aplicado: ${ultimo_evento.get('monto', 0):,.0f}")
    print(f"   Estado final: {reserva3.estado}")
    
    # ========================================================================
    # 11. REPORTES Y ESTADÍSTICAS
    # ========================================================================
    imprimir_separador("11. REPORTES Y ESTADÍSTICAS")
    
    print(f"\n📊 {agenda}")
    
    print(f"\n📈 Reservas por estado:")
    estados = ["creada", "confirmada", "cancelada", "no_show"]
    for estado in estados:
        count = len(agenda.listar_por_estado(estado))
        if count > 0:
            print(f"   • {estado.capitalize()}: {count}")
    
    print(f"\n🏟️  Reservas por cancha:")
    for cancha in [cancha1, cancha2, cancha3]:
        reservas_cancha = agenda.listar_por_cancha(cancha)
        if reservas_cancha:
            print(f"   • {cancha.nombre}: {len(reservas_cancha)} reserva(s)")
    
    print(f"\n💰 Ingresos totales (confirmadas):")
    reservas_confirmadas = agenda.listar_por_estado("confirmada")
    total_ingresos = sum(r.importe for r in reservas_confirmadas if r.importe)
    print(f"   ${total_ingresos:,.0f}")
    
    # ========================================================================
    # 12. TRAZABILIDAD
    # ========================================================================
    imprimir_separador("12. TRAZABILIDAD - HISTORIAL DE EVENTOS")
    
    print(f"\n📋 Historial de Reserva #R001:")
    for evento in reserva1.historial_eventos:
        timestamp = evento['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        monto = f" | Monto: ${evento['monto']:,.0f}" if 'monto' in evento else ""
        print(f"   [{timestamp}] {evento['tipo']}: {evento['detalle']}{monto}")
    
    print(f"\n📋 Historial de Reserva #R006 (con cancelación):")
    for evento in reserva6.historial_eventos:
        timestamp = evento['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        monto = f" | Monto: ${evento['monto']:,.0f}" if 'monto' in evento else ""
        print(f"   [{timestamp}] {evento['tipo']}: {evento['detalle']}{monto}")
    
    print("\n" + "⚽"*35)
    print("  FIN DE LA DEMOSTRACIÓN")
    print("⚽"*35 + "\n")


if __name__ == "__main__":
    main()