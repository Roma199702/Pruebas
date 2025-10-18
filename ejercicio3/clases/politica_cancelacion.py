from abc import ABC, abstractmethod
from typing import Dict
import math

class PoliticaCancelacion(ABC):
    """
    Clase abstracta para determinar penalización al cancelar según anticipación.
    """
    
    @abstractmethod
    def penalizacion(self, horas_previas: float, importe: float) -> Dict:
        """
        Calcula la penalización por cancelación.
        
        Args:
            horas_previas: Horas de anticipación a la reserva
            importe: Importe total de la reserva
            
        Returns:
            {monto_penalizacion, motivo}
        """
        pass
    
    def _redondear(self, valor: float) -> float:
        """Redondea a 2 decimales (mitad arriba)"""
        return math.floor(valor * 100 + 0.5) / 100
    
    def _validar_parametros(self, horas_previas: float, importe: float):
        """Validaciones comunes"""
        if horas_previas < 0:
            raise ValueError("horas_previas debe ser >= 0")
        if importe < 0:
            raise ValueError("importe debe ser >= 0")


class CancelacionFlexible(PoliticaCancelacion):
    """
    Política flexible:
    - 0% de penalización si cancela con ≥ 24 horas de anticipación
    - 20% de penalización si cancela con < 24 horas
    """
    
    def penalizacion(self, horas_previas: float, importe: float) -> Dict:
        self._validar_parametros(horas_previas, importe)
        
        if horas_previas >= 24:
            return {
                "monto_penalizacion": 0.0,
                "motivo": "Cancelación con más de 24 horas de anticipación (sin penalización)"
            }
        else:
            penalizacion = self._redondear(importe * 0.20)
            return {
                "monto_penalizacion": penalizacion,
                "motivo": f"Cancelación con menos de 24 horas ({horas_previas:.1f}h) - Penalización 20%"
            }


class CancelacionEstricta(PoliticaCancelacion):
    """
    Política estricta:
    - 50% de penalización independiente de la anticipación
    """
    
    def penalizacion(self, horas_previas: float, importe: float) -> Dict:
        self._validar_parametros(horas_previas, importe)
        
        penalizacion = self._redondear(importe * 0.50)
        return {
            "monto_penalizacion": penalizacion,
            "motivo": f"Cancelación con política estricta - Penalización 50%"
        }