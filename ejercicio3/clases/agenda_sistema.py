from datetime import datetime
from typing import List

class AgendaSistema:
    """
    Gestor central de reservas de canchas.
    Garantiza unicidad de IDs y previene solapes.
    """
    
    def __init__(self):
        self.__reservas: List = []
    
    @property
    def reservas(self) -> List:
        """Retorna una copia de la lista de reservas"""
        return self.__reservas.copy()
    
    def agregar(self, reserva):
        """
        Agrega una reserva validando:
        - ID único
        - Sin solapamiento (si ya está cotizada/confirmada)
        """
        # Validar unicidad de ID
        if any(r.id_reserva == reserva.id_reserva for r in self.__reservas):
            raise ValueError(f"Ya existe una reserva con id {reserva.id_reserva}")
        
        self.__reservas.append(reserva)
    
    def existe_solape(self, cancha, inicio: datetime, fin: datetime) -> bool:
        """
        Verifica si existe solapamiento temporal para una cancha.
        Solo considera reservas NO canceladas y NO no_show.
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        for reserva in self.__reservas:
            # Solo verificar reservas de la misma cancha
            if reserva.cancha.id_cancha != cancha.id_cancha:
                continue
            
            # Ignorar reservas canceladas o no_show
            if reserva.estado in ["cancelada", "no_show"]:
                continue
            
            # Verificar intersección temporal
            # A_inicio < B_fin AND B_inicio < A_fin
            if inicio < reserva.fin and reserva.inicio < fin:
                return True
        
        return False
    
    def buscar_por_id(self, id_reserva: str):
        """Busca una reserva por su ID"""
        for reserva in self.__reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        raise ValueError(f"No se encontró reserva con id {id_reserva}")
    
    def listar_por_cancha(self, cancha) -> List:
        """Lista todas las reservas de una cancha"""
        return [r for r in self.__reservas if r.cancha.id_cancha == cancha.id_cancha]
    
    def listar_por_estado(self, estado: str) -> List:
        """Lista todas las reservas con un estado específico"""
        return [r for r in self.__reservas if r.estado == estado]
    
    def listar_por_cliente(self, cliente: str) -> List:
        """Lista todas las reservas de un cliente"""
        return [r for r in self.__reservas if r.cliente.lower() == cliente.lower()]
    
    def __str__(self):
        return f"Agenda del Sistema con {len(self.__reservas)} reserva(s)"