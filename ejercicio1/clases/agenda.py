from datetime import datetime
from typing import List
from .cita import Cita

class Agenda:
    """
    Contenedor y árbitro de citas.
    Garantiza unicidad de IDs y previene solapamientos por profesional.
    """
    
    def __init__(self):
        self.__citas: List[Cita] = []
    
    @property
    def citas(self) -> List[Cita]:
        """Retorna una copia de la lista de citas"""
        return self.__citas.copy()
    
    def agregar(self, cita: Cita):
        """
        Agrega una cita a la agenda validando:
        - ID único
        - Sin solapamiento con otras citas del mismo profesional
        """
        for existente in self.__citas:
            if existente.id_cita == cita.id_cita:
                print(f"❌ No se puede modificar el horario: ya existe una cita con ID {cita.id_cita}")
                return
        if self.existe_solape(cita.profesional, cita.inicio, cita.fin):
            print(f"❌ No se puede agregar la cita: hay solape con otra cita de {cita.profesional}")
            return
        self.__citas.append(cita)
    
    def existe_solape(self, profesional: str, inicio: datetime, fin: datetime) -> bool:
        """
        Verifica si existe solapamiento temporal para un profesional.
        
        Regla de intersección:
        Dos intervalos [A_inicio, A_fin) y [B_inicio, B_fin) se solapan si:
        A_inicio < B_fin AND B_inicio < A_fin
        
        Solo considera citas NO canceladas.
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        for cita in self.__citas:
            # Solo verificar citas del mismo profesional
            if cita.profesional != profesional:
                continue
            
            # Ignorar citas canceladas
            if cita.estado == "cancelada":
                continue
            
            # Ignorar citas sin servicio asignado (no tienen fin)
            if cita.fin is None:
                continue
            
            # Verificar intersección temporal
            # A_inicio < B_fin AND B_inicio < A_fin
            if inicio < cita.fin and cita.inicio < fin:
                return True
        
        return False
    
    def buscar_por_id(self, id_cita: str) -> Cita:
        """Busca una cita por su ID"""
        for cita in self.__citas:
            if cita.id_cita == id_cita:
                return cita
        raise ValueError(f"No se encontró cita con id {id_cita}")
    
    def listar_por_profesional(self, profesional: str) -> List[Cita]:
        """Lista todas las citas de un profesional"""
        return [c for c in self.__citas if c.profesional == profesional]
    
    def listar_por_estado(self, estado: str) -> List[Cita]:
        """Lista todas las citas con un estado específico"""
        return [c for c in self.__citas if c.estado == estado]
    
    def __str__(self):
        return f"Agenda con {len(self.__citas)} cita(s) registrada(s)"