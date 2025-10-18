from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta
from typing import Dict, List
import math

class Tarifa(ABC):
    """
    Clase abstracta para calcular importes según franja temporal.
    Implementa prorrateo por minutos y redondeo monetario.
    """
    
    def __init__(self, valor_hora: float):
        if valor_hora <= 0:
            raise ValueError("valor_hora debe ser mayor a 0")
        self._valor_hora = valor_hora
    
    @property
    def valor_hora(self) -> float:
        return self._valor_hora
    
    @abstractmethod
    def nombre_tarifa(self) -> str:
        """Nombre descriptivo de la tarifa"""
        pass
    
    def calcular_importe(self, inicio: datetime, fin: datetime) -> Dict:
        """
        Calcula el importe total con prorrateo por minutos.
        Retorna: {total, desglose[]}
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        # Calcular minutos totales
        duracion_minutos = (fin - inicio).total_seconds() / 60
        
        # Calcular importe con prorrateo
        importe_total = (duracion_minutos / 60) * self._valor_hora
        importe_total = self._redondear(importe_total)
        
        # Crear desglose simple
        desglose = [{
            "desde": inicio,
            "hasta": fin,
            "tipo_tarifa": self.nombre_tarifa(),
            "minutos": int(duracion_minutos),
            "valor_hora": self._valor_hora,
            "subtotal": importe_total
        }]
        
        return {
            "total": importe_total,
            "desglose": desglose
        }
    
    def _redondear(self, valor: float) -> float:
        """Redondea a 2 decimales (mitad arriba)"""
        return math.floor(valor * 100 + 0.5) / 100


class TarifaDiurna(Tarifa):
    """
    Tarifa diurna: 08:00 - 19:59
    """
    
    def __init__(self, valor_hora: float = 10000.0):
        super().__init__(valor_hora)
    
    def nombre_tarifa(self) -> str:
        return "Diurna"


class TarifaNocturna(Tarifa):
    """
    Tarifa nocturna: 20:00 - 07:59
    Contempla cruce de medianoche.
    """
    
    def __init__(self, valor_hora: float = 15000.0):
        super().__init__(valor_hora)
    
    def nombre_tarifa(self) -> str:
        return "Nocturna"


class TarifaFinDeSemana(Tarifa):
    """
    Tarifa de fin de semana: sábado y domingo (todo el día)
    Prioritaria sobre Diurna/Nocturna
    """
    
    def __init__(self, valor_hora: float = 20000.0):
        super().__init__(valor_hora)
    
    def nombre_tarifa(self) -> str:
        return "FinDeSemana"


class TarifaMixta(Tarifa):
    """
    Tarifa inteligente que calcula según hora del día.
    Usa prioridad: FinDeSemana > Nocturna > Diurna
    """
    
    def __init__(self):
        super().__init__(10000.0)  # Valor base
    
    def nombre_tarifa(self) -> str:
        return "Mixta"
    
    def calcular_importe(self, inicio: datetime, fin: datetime) -> Dict:
        """
        Calcula importe considerando cambios de tarifa durante el intervalo.
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        desglose = []
        total = 0.0
        
        # Procesar minuto a minuto para detectar cambios de tarifa
        actual = inicio
        while actual < fin:
            # Determinar tarifa del momento actual
            tarifa_momento = self._determinar_tarifa_momento(actual)
            tramo_inicio = actual
            
            # Avanzar mientras se mantenga la misma tarifa
            while actual < fin and self._determinar_tarifa_momento(actual) == tarifa_momento:
                actual += timedelta(minutes=1)
            
            tramo_fin = min(actual, fin)
            minutos = (tramo_fin - tramo_inicio).total_seconds() / 60
            
            # Calcular subtotal del tramo
            subtotal = (minutos / 60) * tarifa_momento
            subtotal = self._redondear(subtotal)
            
            desglose.append({
                "desde": tramo_inicio,
                "hasta": tramo_fin,
                "tipo_tarifa": self._nombre_tarifa_momento(tramo_inicio),
                "minutos": int(minutos),
                "valor_hora": tarifa_momento,
                "subtotal": subtotal
            })
            
            total += subtotal
        
        return {
            "total": self._redondear(total),
            "desglose": desglose
        }
    
    def _determinar_tarifa_momento(self, dt: datetime) -> float:
        """Determina el valor/hora según el momento"""
        # Prioridad 1: Fin de semana
        if dt.weekday() >= 5:  # Sábado o Domingo
            return 20000.0
        
        # Prioridad 2: Horario nocturno
        hora = dt.time()
        if hora >= time(20, 0) or hora < time(8, 0):
            return 15000.0
        
        # Prioridad 3: Diurno
        return 10000.0
    
    def _nombre_tarifa_momento(self, dt: datetime) -> str:
        """Retorna el nombre de la tarifa según el momento"""
        if dt.weekday() >= 5:
            return "FinDeSemana"
        hora = dt.time()
        if hora >= time(20, 0) or hora < time(8, 0):
            return "Nocturna"
        return "Diurna"