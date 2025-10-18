class Retiro:
    def __init__(self, id_retiro, suscriptor, material, kg, fecha, estrategia="rechazo"):
        if kg <= 0:
            raise ValueError("Kg debe ser > 0")
        self.id_retiro = id_retiro
        self.suscriptor = suscriptor
        self.material = material
        self.kg = kg
        self.fecha = fecha  # string tipo 'YYYY-MM-DD'
        self.estado = "registrado"
        self.puntos_calculados = 0
        self.historial_eventos = []
        self.estrategia = estrategia

    def registrar_evento(self, tipo, detalle):
        self.historial_eventos.append({"tipo": tipo, "detalle": detalle})

    def validar(self):
        if self.estado != "registrado":
            raise ValueError("Solo se puede validar un retiro registrado")

        max_kg = self.material.max_kg_por_bolsa()
        if self.kg > max_kg:
            if self.estrategia == "rechazo":
                self.rechazar(f"Excede peso máximo por bolsa ({max_kg} kg)")
                return
            elif self.estrategia == "particion":
                # Partición automática: dividir en retiros de max_kg
                num_bolsas = int(self.kg // max_kg)
                resto = self.kg % max_kg
                for i in range(num_bolsas):
                    sub_retiro = Retiro(f"{self.id_retiro}_part{i+1}", self.suscriptor,
                                        self.material, max_kg, self.fecha, self.estrategia)
                    sub_retiro.validar()
                if resto > 0:
                    sub_retiro = Retiro(f"{self.id_retiro}_partR", self.suscriptor,
                                        self.material, resto, self.fecha, self.estrategia)
                    sub_retiro.validar()
                self.registrar_evento("particionado", f"{self.kg} kg dividido en sub-retiros")
                return

        # Acreditar puntos
        puntos = self.material.puntos(self.kg)
        self.puntos_calculados = puntos
        self.suscriptor.agregar_puntos(puntos, f"Retiro {self.id_retiro} validado")
        self.estado = "validado"
        self.registrar_evento("validado", f"Retiro validado: {self.kg} kg -> {puntos} puntos")

    def rechazar(self, motivo):
        if self.estado != "registrado":
            raise ValueError("Solo se puede rechazar un retiro registrado")
        self.estado = "rechazado"
        self.registrar_evento("rechazado", motivo)