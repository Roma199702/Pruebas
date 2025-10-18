from Servicio import CorteCabello
from Cita import Cita, ErrorAgenda
from Agenda import Agenda

def main():
    agenda = Agenda()

    # Cita 1
    c1 = Cita("c1", "Angela", "Pedro", inicio=10)  # horario representado con número (10 = 10:00)
    c1.asignar_servicio(CorteCabello())
    agenda.agregar(c1)
    c1.confirmar("Confirmada por teléfono", agenda)
    print("Cita confirmada: ", c1)

    # Intentar solape
    c2 = Cita("c2", "Luis", "Pedro", inicio=15)
    c2.asignar_servicio(CorteCabello())
    try:
        agenda.agregar(c2)
    except ErrorAgenda as e:
        print("No se pudo agregar c2: ", e)

    # Cancelar c1
    c1.cancelar("Cliente no puede asistir")
    print("Cita cancelada: ", c1.estado)

    # Ahora se puede agregar otra en el mismo horario
    c3 = Cita("c3", "Mario", "Pedro", inicio=10)
    c3.asignar_servicio(CorteCabello())
    agenda.agregar(c3)
    print("Nueva cita agregada: ", c3)

    print("Historial c1: ", c1.historial_eventos)
    print("Citas en agenda: ", agenda.citas)

if __name__ == "__main__":
    main()