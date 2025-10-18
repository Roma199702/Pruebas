from Material import Plastico, Vidrio, PapelCarton
from Suscriptor import Suscriptor
from Retiro import Retiro
from Bono_semanal import BonoSemanal

if __name__ == "__main__":
    # Crear suscriptor
    s1 = Suscriptor("S1", "Av. Principal 123")

    # Crear materiales
    plastico = Plastico()
    vidrio = Vidrio()
    papel = PapelCarton()

    # Estrategia del sistema: "rechazo" o "particion"
    estrategia = "rechazo"

    # Registrar retiros
    r1 = Retiro("R1", s1, plastico, 5, "2025-10-14", estrategia)
    r2 = Retiro("R2", s1, vidrio, 6, "2025-10-15", estrategia)  # excede vidrio max 5kg
    r3 = Retiro("R3", s1, papel, 3, "2025-10-16", estrategia)

    # Validar retiros
    r1.validar()
    r2.validar()  # será rechazado
    r3.validar()

    # Registrar contadores semanales
    semana = "2025-W42"
    s1.retiros_validos_semana[semana] = 2  # ya hay 2 retiros validados
    bono = BonoSemanal()
    bono.aplicar_bono(s1, semana)  # si >=3, aplica bono

    # Mostrar resultados
    print("Saldo puntos:", s1.saldo_puntos)
    print("Historial eventos:")
    for ev in s1.historial_eventos:
        print(ev)

    print("\nEstado de retiros:")
    for r in [r1, r2, r3]:
        print(f"{r.id_retiro}: {r.estado}, puntos: {r.puntos_calculados}")