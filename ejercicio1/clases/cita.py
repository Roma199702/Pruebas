from datetime import datetime, timedelta
from typing import Optional, List, Dict
from .servicio import Servicio

class Cita:
    """
    Representa una reserva entre un cliente y un profesional.
    Maneja estados, servicios y trazabilidad de eventos.
    """
    
    def __init__(self, id_cita: str, cliente: str, profesional: str, inicio: datetime):
        # Validaciones iniciales
        if not id_cita or not id_cita.strip():
            raise ValueError("id_cita no puede estar vacío")
        if not cliente or not cliente.strip():
            raise ValueError("cliente no puede estar vacío")
        if not profesional or not profesional.strip():
            raise ValueError("profesional no puede estar vacío")
        if inicio <= datetime.now():
            raise ValueError("inicio debe ser una fecha futura")
        
        # Atributos públicos
        self.__id_cita = id_cita
        self.__cliente = cliente
        self.__profesional = profesional
        self.__inicio = inicio
        
        # Atributos privados (solo lectura)
        self.__duracion_min: Optional[int] = None
        self.__servicio: Optional[Servicio] = None
        self.__estado = "creada"
        self.__historial_eventos: List[Dict] = []
        
        # Registrar evento de creación
        self.__registrar_evento("creada", f"Cita creada para {cliente} con {profesional}")
    
    # Getters para atributos públicos
    @property
    def id_cita(self) -> str:
        return self.__id_cita
    
    @property
    def cliente(self) -> str:
        return self.__cliente
    
    @property
    def profesional(self) -> str:
        return self.__profesional
    
    @property
    def inicio(self) -> datetime:
        return self.__inicio
    
    # Getters para atributos de solo lectura
    @property
    def duracion_min(self) -> Optional[int]:
        """Duración en minutos (solo lectura)"""
        return self.__duracion_min
    
    @property
    def estado(self) -> str:
        """Estado actual de la cita (solo lectura)"""
        return self.__estado
    
    @property
    def fin(self) -> Optional[datetime]:
        """Fecha/hora de fin calculada (solo lectura)"""
        if self.__duracion_min is None:
            return None
        return self.__inicio + timedelta(minutes=self.__duracion_min)
    
    @property
    def historial_eventos(self) -> List[Dict]:
        """Historial inmutable de eventos (solo lectura)"""
        return self.__historial_eventos.copy()
    
    # Métodos privados
    def __registrar_evento(self, tipo: str, detalle: str):
        """Registra un evento en el historial"""
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    # Operaciones públicas
    def asignar_servicio(self, servicio: Servicio):
        """
        Asigna un servicio a la cita y fija la duración.
        Solo se puede asignar una vez.
        """
        if not isinstance(servicio, Servicio):
            raise TypeError("servicio debe ser una instancia de Servicio")
        
        if self.__servicio is not None:
            raise ValueError("La cita ya tiene un servicio asignado")
        
        duracion = servicio.duracion_min()
        if duracion <= 0:
            raise ValueError("La duración del servicio debe ser mayor a 0")
        
        self.__servicio = servicio
        self.__duracion_min = duracion
        self.__registrar_evento(
            "servicio_asignado",
            f"Servicio {servicio.__class__.__name__} asignado ({duracion} min)"
        )
    
    def confirmar(self, motivo: str, agenda):
        """
        Confirma la cita si cumple todas las validaciones:
        - Estado debe ser 'creada'
        - Debe tener servicio asignado
        - No debe haber solape con otras citas del mismo profesional
        """
        if self.__estado != "creada":
            raise ValueError(f"Solo se pueden confirmar citas en estado 'creada'. Estado actual: {self.__estado}")
        
        if self.__servicio is None or self.__duracion_min is None:
            raise ValueError("Debe asignar un servicio antes de confirmar")
        
        # Verificar solape con agenda
        if agenda.existe_solape(self.__profesional, self.__inicio, self.fin):
            raise ValueError(f"Existe solape con otra cita del profesional {self.__profesional}")
        
        self.__estado = "confirmada"
        self.__registrar_evento("confirmada", f"Cita confirmada. Motivo: {motivo}")
    
    def cancelar(self, motivo: str):
        """
        Cancela la cita si está en estado 'creada' o 'confirmada'
        """
        if self.__estado not in ["creada", "confirmada"]:
            raise ValueError(f"No se puede cancelar una cita en estado '{self.__estado}'")
        
        self.__estado = "cancelada"
        self.__registrar_evento("cancelada", f"Cita cancelada. Motivo: {motivo}")
    
    def __str__(self):
        fin_str = self.fin.strftime("%Y-%m-%d %H:%M") if self.fin else "Sin servicio asignado"
        return (f"Cita #{self.__id_cita} | Cliente: {self.__cliente} | "
                f"Profesional: {self.__profesional} | Estado: {self.__estado} | "
                f"Inicio: {self.__inicio.strftime('%Y-%m-%d %H:%M')} | Fin: {fin_str}")