from datetime import datetime
from typing import List, Dict

class Suscriptor:
    """
    Titular del servicio de reciclaje y acumulador de puntos.
    Gestiona estado, puntos y trazabilidad.
    """
    
    def __init__(self, id_suscriptor: str, direccion: str):
        # Validaciones
        if not id_suscriptor or not id_suscriptor.strip():
            raise ValueError("id_suscriptor no puede estar vacío")
        if not direccion or not direccion.strip():
            raise ValueError("direccion no puede estar vacía")
        
        self.__id_suscriptor = id_suscriptor
        self.__direccion = direccion
        self.__saldo_puntos = 0.0
        self.__estado = "habilitado"
        self.__historial_eventos: List[Dict] = []
        self.__retiros_validados_semana_actual = 0
        
        self.__registrar_evento("creado", f"Suscriptor creado en {direccion}")
    
    @property
    def id_suscriptor(self) -> str:
        return self.__id_suscriptor
    
    @property
    def direccion(self) -> str:
        return self.__direccion
    
    @property
    def saldo_puntos(self) -> float:
        """Saldo de puntos acumulados (solo lectura)"""
        return self.__saldo_puntos
    
    @property
    def estado(self) -> str:
        return self.__estado
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    @property
    def retiros_validados_semana(self) -> int:
        """Conteo de retiros validados en la semana vigente (solo lectura)"""
        return self.__retiros_validados_semana_actual
    
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    def acreditar_puntos(self, puntos: float, concepto: str):
        """Incrementa el saldo de puntos (uso interno del sistema)"""
        if puntos < 0:
            raise ValueError("puntos debe ser >= 0")
        
        self.__saldo_puntos += puntos
        self.__registrar_evento(
            "puntos_acreditados",
            f"+{puntos:.2f} puntos. Concepto: {concepto}"
        )
    
    def incrementar_retiros_semana(self):
        """Incrementa el contador de retiros validados en la semana"""
        self.__retiros_validados_semana_actual += 1
    
    def resetear_contador_semanal(self):
        """Resetea el contador de retiros semanales (al iniciar nueva semana)"""
        self.__retiros_validados_semana_actual = 0
        self.__registrar_evento("contador_reseteado", "Contador semanal de retiros reseteado")
    
    def inhabilitar(self, motivo: str):
        """Inhabilita al suscriptor"""
        if self.__estado == "inhabilitado":
            raise ValueError("El suscriptor ya está inhabilitado")
        
        self.__estado = "inhabilitado"
        self.__registrar_evento("inhabilitado", f"Suscriptor inhabilitado. Motivo: {motivo}")
    
    def habilitar(self, motivo: str):
        """Habilita al suscriptor"""
        if self.__estado == "habilitado":
            raise ValueError("El suscriptor ya está habilitado")
        
        self.__estado = "habilitado"
        self.__registrar_evento("habilitado", f"Suscriptor habilitado. Motivo: {motivo}")
    
    def __str__(self):
        return (f"Suscriptor {self.__id_suscriptor} | {self.__direccion} | "
                f"Puntos: {self.__saldo_puntos:.0f} | Estado: {self.__estado}")