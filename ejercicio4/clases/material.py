from abc import ABC, abstractmethod

class Material(ABC):
    """
    Clase abstracta que define puntaje y límite por bolsa según tipo.
    Cada material implementa su propia política de puntos y límites.
    """
    
    @abstractmethod
    def puntos(self, kg: float) -> float:
        """
        Calcula los puntos otorgados por los kg de material.
        Debe retornar >= 0
        """
        pass
    
    @abstractmethod
    def max_kg_por_bolsa(self) -> float:
        """
        Retorna el límite máximo de kg permitido por bolsa.
        Debe retornar > 0
        """
        pass
    
    @abstractmethod
    def nombre_material(self) -> str:
        """Nombre descriptivo del material"""
        pass
    
    def _validar_kg(self, kg: float):
        """Validación común para todos los materiales"""
        if kg <= 0:
            raise ValueError("kg debe ser mayor a 0")


class Plastico(Material):
    """
    Material plástico: puntos altos por kg, límite de 8 kg por bolsa.
    """
    
    def puntos(self, kg: float) -> float:
        self._validar_kg(kg)
        # 15 puntos por kg de plástico
        return kg * 15.0
    
    def max_kg_por_bolsa(self) -> float:
        return 8.0
    
    def nombre_material(self) -> str:
        return "Plástico"


class Vidrio(Material):
    """
    Material vidrio: puntos menores por kg, límite bajo por seguridad (5 kg).
    """
    
    def puntos(self, kg: float) -> float:
        self._validar_kg(kg)
        # 8 puntos por kg de vidrio
        return kg * 8.0
    
    def max_kg_por_bolsa(self) -> float:
        return 5.0
    
    def nombre_material(self) -> str:
        return "Vidrio"


class PapelCarton(Material):
    """
    Material papel/cartón: puntos intermedios, considera merma del 10%.
    """
    
    def puntos(self, kg: float) -> float:
        self._validar_kg(kg)
        # 10 puntos por kg, pero con merma del 10%
        kg_efectivo = kg * 0.90  # Descuento del 10% por merma
        return kg_efectivo * 10.0
    
    def max_kg_por_bolsa(self) -> float:
        return 10.0
    
    def nombre_material(self) -> str:
        return "Papel/Cartón"