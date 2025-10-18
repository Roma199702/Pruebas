from Cancha import Cancha
from Reserva import Reserva
from Tarifa import TarifaDiurna, TarifaNocturna, TarifaFinDeSemana
from Politica_cancelacion import CancelacionFlexible, CancelacionEstricta

if __name__ == "__main__":
    cancha1 = Cancha("C1", "Cancha Central")
    cancha1.bloquear_mantencion("2025-10-20 10:00", "2025-10-20 12:00")

    # Crear reservas
    r1 = Reserva("R1", cancha1, "Juan Pérez", "2025-10-20 09:00", "2025-10-20 10:00")
    r1.cotizar(TarifaDiurna())
    r1.confirmar("Reserva confirmada", [])

    r2 = Reserva("R2", cancha1, "Ana Gómez", "2025-10-20 11:00", "2025-10-20 12:30")
    try:
        r2.confirmar("Intento de reserva", [r1])
    except Exception as e:
        print("Error:", e)

    # Cancelación con política flexible
    r1.cancelar("Cliente no puede asistir", CancelacionFlexible(), 10)

    print("\n=== Historial Reserva 1 ===")
    for ev in r1.historial_eventos:
        print(ev)

    print("\n=== Historial Cancha ===")
    for ev in cancha1.historial_eventos:
        print(ev)