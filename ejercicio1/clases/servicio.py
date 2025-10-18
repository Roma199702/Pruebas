from abc import ABC, abstractmethod

class Servicio(ABC):
    """
    Clase abstracta que define el contrato para los servicios de peluquería.
    Cada servicio concreto debe implementar duracion_min()
    """
    
    @abstractmethod
    def duracion_min(self) -> int:
        """
        Retorna la duración mínima del servicio en minutos.
        Debe ser > 0
        """
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__} ({self.duracion_min()} min)"


class CorteCabello(Servicio):
    """
    Servicio de corte de cabello con duración de 30 minutos
    """
    
    def duracion_min(self) -> int:
        return 30


class Coloracion(Servicio):
    """
    Servicio de coloración con duración de 90 minutos
    """
    
    def duracion_min(self) -> int:
        return 90