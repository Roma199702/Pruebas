"""
EJERCICIO 4: Reciclaje Domiciliario con Puntos de Incentivo
Archivo principal que demuestra el funcionamiento del sistema
"""



from datetime import datetime, timedelta
from clases.suscriptor import Suscriptor
from clases.material import Plastico, Vidrio, PapelCarton
from clases.retiro import Retiro
from clases.sistema_reciclaje import SistemaReciclaje


def imprimir_separador(titulo):
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70)


def mostrar_historial(entidad, titulo):
    """Muestra el historial de eventos"""
    print(f"\n  📋 {titulo}:")
    for evento in entidad.historial_eventos[-5:]:  # Últimos 5 eventos
        timestamp = evento['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        print(f"    [{timestamp}] {evento['tipo']}: {evento['detalle']}")


def main():
    print("\n" + "♻️"*60)
    print("  SISTEMA DE RECICLAJE DOMICILIARIO")
    print("♻️"*60 + "\n")
    
    # ========================================================================
    # 1. CREAR SISTEMA Y MATERIALES
    # ========================================================================
    imprimir_separador("1. INICIALIZACIÓN DEL SISTEMA")
    
    # Sistema con estrategia de rechazo
    sistema = SistemaReciclaje(estrategia_peso="rechazo")
    print(f"✅ {sistema}")
    
    # Crear materiales (polimorfismo)
    plastico = Plastico()
    vidrio = Vidrio()
    papel_carton = PapelCarton()
    
    print("\n📦 Materiales disponibles:")
    print(f"   • {plastico.nombre_material()}: {plastico.puntos(1):.0f} pts/kg | "
          f"Máx: {plastico.max_kg_por_bolsa()}kg/bolsa")
    print(f"   • {vidrio.nombre_material()}: {vidrio.puntos(1):.0f} pts/kg | "
          f"Máx: {vidrio.max_kg_por_bolsa()}kg/bolsa")
    print(f"   • {papel_carton.nombre_material()}: {papel_carton.puntos(1):.0f} pts/kg (con merma 10%) | "
          f"Máx: {papel_carton.max_kg_por_bolsa()}kg/bolsa")
    
    # ========================================================================
    # 2. CREAR SUSCRIPTORES
    # ========================================================================
    imprimir_separador("2. REGISTRO DE SUSCRIPTORES")
    
    suscriptor1 = Suscriptor("S001", "Av. Libertador 1234")
    suscriptor2 = Suscriptor("S002", "Calle Principal 567")
    suscriptor3 = Suscriptor("S003", "Pasaje Los Robles 89")
    
    suscriptores = [suscriptor1, suscriptor2, suscriptor3]
    
    print("✅ Suscriptores registrados:")
    for sus in suscriptores:
        print(f"   • {sus}")
    
    # ========================================================================
    # 3. REGISTRAR Y VALIDAR RETIROS
    # ========================================================================
    imprimir_separador("3. REGISTRO Y VALIDACIÓN DE RETIROS")
    
    # Retiro 1: Plástico (suscriptor1)
    retiro1 = Retiro(
        "R001",
        suscriptor1,
        datetime.now(),
        plastico,
        5.0
    )
    sistema.registrar_retiro(retiro1)
    print(f"\n✅ {retiro1}")
    
    print(f"   Validando retiro...")
    sistema.validar_retiro("R001")
    print(f"   ✅ Retiro validado. Puntos otorgados: {retiro1.puntos_calculados:.2f}")
    print(f"   {suscriptor1}")
    
    # Retiro 2: Vidrio (suscriptor1)
    retiro2 = Retiro(
        "R002",
        suscriptor1,
        datetime.now(),
        vidrio,
        3.5
    )
    sistema.registrar_retiro(retiro2)
    print(f"\n✅ {retiro2}")
    
    sistema.validar_retiro("R002")
    print(f"   ✅ Retiro validado. Puntos otorgados: {retiro2.puntos_calculados:.2f}")
    print(f"   {suscriptor1}")
    
    # Retiro 3: Papel/Cartón (suscriptor1) - Este completará 3 retiros
    retiro3 = Retiro(
        "R003",
        suscriptor1,
        datetime.now(),
        papel_carton,
        8.0
    )
    sistema.registrar_retiro(retiro3)
    print(f"\n✅ {retiro3}")
    
    print(f"   Validando retiro (debería activar bonificación semanal)...")
    sistema.validar_retiro("R003")
    print(f"   ✅ Retiro validado. Puntos otorgados: {retiro3.puntos_calculados:.2f}")
    print(f"   🎁 ¡BONIFICACIÓN SEMANAL APLICADA! (+10 puntos)")
    print(f"   {suscriptor1}")
    
    # ========================================================================
    # 4. VALIDACIÓN DE LÍMITE DE PESO (RECHAZO)
    # ========================================================================
    imprimir_separador("4. VALIDACIÓN DE LÍMITE DE PESO")
    
    print(f"\n⚠️  Estrategia del sistema: {sistema.estrategia_peso}")
    print(f"   Límite de plástico: {plastico.max_kg_por_bolsa()}kg/bolsa")
    
    # Intentar retiro que excede el límite
    retiro4 = Retiro(
        "R004",
        suscriptor2,
        datetime.now(),
        plastico,
        12.0  # Excede el límite de 8kg
    )
    sistema.registrar_retiro(retiro4)
    print(f"\n📦 Intentando validar retiro de {retiro4.kg}kg de plástico...")
    
    try:
        sistema.validar_retiro("R004")
    except ValueError as e:
        print(f"   ❌ ERROR esperado: {e}")
        # Rechazar el retiro
        sistema.rechazar_retiro("R004", "Excede peso máximo permitido")
        print(f"   ℹ️  Retiro rechazado formalmente")
    
    # ========================================================================
    # 5. SISTEMA CON ESTRATEGIA DE PARTICIÓN
    # ========================================================================
    imprimir_separador("5. ESTRATEGIA DE PARTICIÓN AUTOMÁTICA")
    
    sistema_particion = SistemaReciclaje(estrategia_peso="particion")
    print(f"✅ {sistema_particion}")
    
    suscriptor4 = Suscriptor("S004", "Av. Los Pinos 456")
    
    retiro5 = Retiro(
        "R005",
        suscriptor4,
        datetime.now(),
        plastico,
        12.0  # Excede el límite pero se permite con partición
    )
    sistema_particion.registrar_retiro(retiro5)
    
    print(f"\n📦 Validando retiro de {retiro5.kg}kg con estrategia de partición...")
    sistema_particion.validar_retiro("R005")
    print(f"   ✅ Retiro validado con partición automática")
    print(f"   Puntos otorgados: {retiro5.puntos_calculados:.2f}")
    print(f"   {suscriptor4}")
    
    mostrar_historial(retiro5, "Historial del retiro con partición")
    
    # ========================================================================
    # 6. MÚLTIPLES RETIROS Y BONIFICACIÓN
    # ========================================================================
    imprimir_separador("6. ACUMULACIÓN DE RETIROS PARA BONIFICACIÓN")
    
    print(f"\n👤 {suscriptor2}")
    print(f"   Retiros validados esta semana: {suscriptor2.retiros_validados_semana}")
    
    # Crear 3 retiros para suscriptor2
    for i in range(3):
        retiro = Retiro(
            f"R10{i+1}",
            suscriptor2,
            datetime.now(),
            vidrio if i % 2 == 0 else papel_carton,
            3.0 + i
        )
        sistema.registrar_retiro(retiro)
        sistema.validar_retiro(retiro.id_retiro)
        print(f"   ✅ Retiro R10{i+1} validado: +{retiro.puntos_calculados:.2f} puntos")
    
    print(f"\n   🎁 Estado final de {suscriptor2.id_suscriptor}:")
    print(f"   {suscriptor2}")
    print(f"   Retiros esta semana: {suscriptor2.retiros_validados_semana}")
    
    # ========================================================================
    # 7. GESTIÓN DE ESTADO DEL SUSCRIPTOR
    # ========================================================================
    imprimir_separador("7. GESTIÓN DE ESTADO")
    
    print(f"\n🔒 Inhabilitando suscriptor3...")
    suscriptor3.inhabilitar("Conducta inapropiada")
    print(f"   {suscriptor3}")
    
    # Intentar validar retiro de suscriptor inhabilitado
    retiro_bloqueado = Retiro(
        "R200",
        suscriptor3,
        datetime.now(),
        plastico,
        4.0
    )
    sistema.registrar_retiro(retiro_bloqueado)
    
    print(f"\n⚠️  Intentando validar retiro de suscriptor inhabilitado...")
    try:
        sistema.validar_retiro("R200")
    except ValueError as e:
        print(f"   ❌ ERROR esperado: {e}")
    
    # Rehabilitar
    print(f"\n🔓 Habilitando nuevamente suscriptor3...")
    suscriptor3.habilitar("Período de suspensión cumplido")
    print(f"   {suscriptor3}")
    
    # ========================================================================
    # 8. REPORTES Y ESTADÍSTICAS
    # ========================================================================
    imprimir_separador("8. REPORTES Y ESTADÍSTICAS")
    
    print(f"\n📊 {sistema}")
    
    print(f"\n📈 Retiros por estado:")
    estados = ["registrado", "validado", "rechazado"]
    for estado in estados:
        count = len(sistema.listar_por_estado(estado))
        if count > 0:
            print(f"   • {estado.capitalize()}: {count}")
    
    print(f"\n♻️  Retiros por material:")
    materiales = ["Plástico", "Vidrio", "Papel/Cartón"]
    for mat in materiales:
        retiros_mat = sistema.listar_por_material(mat)
        if retiros_mat:
            kg_total = sum(r.kg for r in retiros_mat if r.estado == "validado")
            print(f"   • {mat}: {len(retiros_mat)} retiro(s), {kg_total:.1f}kg validados")
    
    print(f"\n🏆 Ranking de suscriptores por puntos:")
    suscriptores_ordenados = sorted(
        suscriptores,
        key=lambda s: s.saldo_puntos,
        reverse=True
    )
    for i, sus in enumerate(suscriptores_ordenados, 1):
        retiros_count = len(sistema.listar_por_suscriptor(sus))
        print(f"   {i}. {sus.id_suscriptor} - {sus.saldo_puntos:.0f} puntos ({retiros_count} retiros)")
    
    print(f"\n📦 Totales del sistema:")
    print(f"   • Total kg reciclados: {sistema.calcular_total_kg_reciclados():.2f}kg")
    print(f"   • Total puntos otorgados: {sistema.calcular_total_puntos_otorgados():.2f}")
    
    # ========================================================================
    # 9. CÁLCULO POLIMÓRFICO DE PUNTOS
    # ========================================================================
    imprimir_separador("9. DEMOSTRACIÓN CAlCULOS")
    
    print("\n🔢 Comparación de puntos por 5kg de cada material:")
    materiales_demo = [plastico, vidrio, papel_carton]
    
    for material in materiales_demo:
        puntos_5kg = material.puntos(5.0)
        print(f"   • {material.nombre_material()}: {puntos_5kg:.2f} puntos")
    
    print("\n   ℹ️  Nota: Papel/Cartón considera merma del 10%")
    print(f"   Cálculo: 5kg × 0.90 × 10 pts/kg = {papel_carton.puntos(5.0):.2f} puntos")
    
    # ========================================================================
    # 10. TRAZABILIDAD Y EVENTOS
    # ========================================================================
    imprimir_separador("10. TRAZABILIDAD - HISTORIAL DE EVENTOS")
    
    mostrar_historial(suscriptor1, f"Historial de {suscriptor1.id_suscriptor}")
    mostrar_historial(retiro1, "Historial del Retiro R001")
    
    # ========================================================================
    # 11. VALIDACIONES Y CASOS DE ERROR
    # ========================================================================
    imprimir_separador("11. PRUEBAS DE VALIDACIÓN")
    
    print("\n📌 Prueba 1: Intentar crear retiro con kg <= 0")
    try:
        retiro_invalido = Retiro("R999", suscriptor1, datetime.now(), plastico, -5.0)
    except ValueError as e:
        print(f"   ❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 2: Intentar validar un retiro ya validado")
    try:
        sistema.validar_retiro("R001")  # Ya fue validado antes
    except ValueError as e:
        print(f"   ❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 3: Intentar rechazar un retiro ya validado")
    try:
        sistema.rechazar_retiro("R002", "Intento de rechazo")
    except ValueError as e:
        print(f"   ❌ ERROR esperado: {e}")
    
    print("\n📌 Prueba 4: Bonificación semanal se otorga solo una vez")
    print(f"   Suscriptor1 tiene {suscriptor1.retiros_validados_semana} retiros validados")
    print(f"   Puntos actuales: {suscriptor1.saldo_puntos:.0f}")
    
    # Crear un retiro más (el 4to)
    retiro_extra = Retiro("R300", suscriptor1, datetime.now(), plastico, 2.0)
    sistema.registrar_retiro(retiro_extra)
    puntos_antes = suscriptor1.saldo_puntos
    sistema.validar_retiro("R300")
    puntos_despues = suscriptor1.saldo_puntos
    
    incremento = puntos_despues - puntos_antes
    print(f"   Puntos después del 4to retiro: {puntos_despues:.0f}")
    print(f"   Incremento: {incremento:.2f} puntos (solo del retiro, sin bono adicional)")
    
    # ========================================================================
    # 12. SIMULACIÓN DE NUEVA SEMANA
    # ========================================================================
    imprimir_separador("12. RESETEO SEMANAL")
    
    print("\n🔄 Simulando inicio de nueva semana...")
    print(f"   Estado antes del reseteo:")
    print(f"   • Suscriptor1: {suscriptor1.retiros_validados_semana} retiros esta semana")
    print(f"   • Suscriptor2: {suscriptor2.retiros_validados_semana} retiros esta semana")
    
    sistema.resetear_semana()
    
    print(f"\n   Estado después del reseteo:")
    print(f"   • Suscriptor1: {suscriptor1.retiros_validados_semana} retiros esta semana")
    print(f"   • Suscriptor2: {suscriptor2.retiros_validados_semana} retiros esta semana")
    print(f"   ℹ️  Los puntos acumulados se mantienen, solo se resetea el contador")
    
    # ========================================================================
    # 13. RESUMEN FINAL
    # ========================================================================
    imprimir_separador("13. RESUMEN FINAL DEL SISTEMA")
    
    print(f"\n🌟 Estadísticas Generales:")
    print(f"   • Total de retiros registrados: {len(sistema.retiros)}")
    print(f"   • Retiros validados: {len(sistema.listar_por_estado('validado'))}")
    print(f"   • Retiros rechazados: {len(sistema.listar_por_estado('rechazado'))}")
    print(f"   • Total kg reciclados: {sistema.calcular_total_kg_reciclados():.2f}kg")
    print(f"   • Total puntos en circulación: {sistema.calcular_total_puntos_otorgados():.2f}")
    
    print(f"\n👥 Resumen de Suscriptores:")
    for sus in suscriptores:
        retiros_sus = sistema.listar_por_suscriptor(sus)
        validados = [r for r in retiros_sus if r.estado == "validado"]
        print(f"   • {sus.id_suscriptor}: {sus.saldo_puntos:.0f} pts | "
              f"{len(validados)} retiros validados | Estado: {sus.estado}")
    
    print(f"\n♻️  Impacto Ambiental Estimado:")
    kg_plastico = sum(r.kg for r in sistema.listar_por_material("Plástico") if r.estado == "validado")
    kg_vidrio = sum(r.kg for r in sistema.listar_por_material("Vidrio") if r.estado == "validado")
    kg_papel = sum(r.kg for r in sistema.listar_por_material("Papel/Cartón") if r.estado == "validado")
    
    print(f"   • Plástico reciclado: {kg_plastico:.2f}kg")
    print(f"   • Vidrio reciclado: {kg_vidrio:.2f}kg")
    print(f"   • Papel/Cartón reciclado: {kg_papel:.2f}kg")
    print(f"   • TOTAL: {sistema.calcular_total_kg_reciclados():.2f}kg")
    
    print("\n" + "♻️"*60)
    print("  FIN DE LA DEMOSTRACIÓN")
    print("♻️"*60 + "\n")


if __name__ == "__main__":
    main()