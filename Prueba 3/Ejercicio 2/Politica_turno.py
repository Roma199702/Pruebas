class PoliticaTurno:
    def asignar(self, semana, colaboradores, franjas):
        raise NotImplementedError("Debe implementarse en subclases.")


class TurnoFijo(PoliticaTurno):
    def asignar(self, semana, colaboradores, franjas):
        turnos = []
        i = 0
        for franja in franjas:
            titular = colaboradores[i % len(colaboradores)]
            if not titular.disponible(franja.dia, franja.hora_inicio, franja.hora_fin):
                # Buscar suplente disponible
                for suplente in colaboradores:
                    if suplente.disponible(franja.dia, franja.hora_inicio, franja.hora_fin):
                        turnos.append({"franja": franja, "responsable": suplente, "forzado": True})
                        break
            else:
                turnos.append({"franja": franja, "responsable": titular, "forzado": False})
            i += 1
        return turnos


class TurnoRotativo(PoliticaTurno):
    def asignar(self, semana, colaboradores, franjas):
        turnos = []
        ultima_apertura = None
        idx = 0
        for franja in franjas:
            col = colaboradores[idx % len(colaboradores)]

            # Regla: quien abre un día no puede abrir el siguiente
            if ultima_apertura == col.nombre:
                idx += 1
                col = colaboradores[idx % len(colaboradores)]

            turnos.append({"franja": franja, "responsable": col, "forzado": False})
            ultima_apertura = col.nombre
            idx += 1
        return turnos


class TurnoFlexible(PoliticaTurno):
    def asignar(self, semana, colaboradores, franjas):
        turnos = []
        for franja in franjas:
            asignado = None
            for col in colaboradores:
                if not col.disponible(franja.dia, franja.hora_inicio, franja.hora_fin):
                    continue
                if col.horas_asignadas_semana() + franja.duracion_horas() > col.horas_semana_max:
                    continue

                preferencia_ok = (
                    col.preferencia == "indistinto"
                    or (col.preferencia == "manana" and franja.hora_inicio < 12)
                    or (col.preferencia == "tarde" and franja.hora_inicio >= 12)
                )

                turnos.append({
                    "franja": franja,
                    "responsable": col,
                    "forzado": not preferencia_ok
                })
                asignado = col
                break

            if not asignado:
                raise ValueError(f"No se pudo asignar la franja {franja.dia} {franja.hora_inicio}-{franja.hora_fin}")
        return turnos