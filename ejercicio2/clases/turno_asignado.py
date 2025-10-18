from datetime import datetime
from typing import List, Dict
from .franja import Franja
from .colaborador import Colaborador

class TurnoAsignado:
    """
    Representa la asignación de un colaborador a una franja específica.
    Registra si la asignación fue forzada (contra preferencia).
    """
    
    def __init__(self, franja: Franja, responsable: Colaborador, marcado_forzado: bool = False):
        # Validaciones
        if not isinstance(franja, Franja):
            raise TypeError("franja debe ser una instancia de Franja")
        if not isinstance(responsable, Colaborador):
            raise TypeError("responsable debe ser una instancia de Colaborador")
        
        self.__franja = franja
        self.__responsable = responsable
        self.__marcado_forzado = marcado_forzado
        self.__historial_eventos: List[Dict] = []
        
        # Registrar evento de asignación
        tipo_asignacion = "asignado_forzado" if marcado_forzado else "asignado"
        detalle = f"{responsable.nombre} asignado a {franja}"
        if marcado_forzado:
            detalle += " (FORZADO - contra preferencia)"
        
        self.__registrar_evento(tipo_asignacion, detalle)
    
    @property
    def franja(self) -> Franja:
        return self.__franja
    
    @property
    def responsable(self) -> Colaborador:
        return self.__responsable
    
    @property
    def marcado_forzado(self) -> bool:
        return self.__marcado_forzado
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    @property
    def duracion_horas(self) -> float:
        """Duración tomada de la franja (solo lectura)"""
        return self.__franja.duracion_horas
    
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    def reasignar(self, nuevo_responsable: Colaborador, motivo: str, forzado: bool = False):
        """Cambia el responsable del turno"""
        if not isinstance(nuevo_responsable, Colaborador):
            raise TypeError("nuevo_responsable debe ser una instancia de Colaborador")
        
        antiguo = self.__responsable.nombre
        self.__responsable = nuevo_responsable
        self.__marcado_forzado = forzado
        
        detalle = f"Reasignado de {antiguo} a {nuevo_responsable.nombre}. Motivo: {motivo}"
        if forzado:
            detalle += " (FORZADO)"
        
        self.__registrar_evento("reasignado", detalle)
    
    def __str__(self):
        forzado_str = " ⚠️ FORZADO" if self.__marcado_forzado else ""
        return f"{self.__franja} → {self.__responsable.nombre}{forzado_str}"