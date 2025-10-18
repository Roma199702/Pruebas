from datetime import datetime
from typing import List, Dict

class CalendarioCancha:
    """
    Encapsula la indisponibilidad por mantención de una cancha.
    """
    
    def __init__(self):
        self.__mantencion: List[Dict] = []
    
    @property
    def mantencion(self) -> List[Dict]:
        """Lista de intervalos de mantención (solo lectura)"""
        return self.__mantencion.copy()
    
    def obtener_bloques(self) -> List[Dict]:
        """Retorna copia de todos los bloques de mantención"""
        return self.__mantencion.copy()
    
    def cantidad_bloques(self) -> int:
        """Retorna la cantidad de bloques de mantención"""
        return len(self.__mantencion)
    
    def agregar(self, inicio: datetime, fin: datetime):
        """
        Agrega un bloque de mantención validando:
        - inicio < fin
        - No solape con bloques existentes
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        # Verificar solape con bloques existentes
        for bloque in self.__mantencion:
            if inicio < bloque["fin"] and bloque["inicio"] < fin:
                raise ValueError(
                    f"El bloque se solapa con mantención existente: "
                    f"{bloque['inicio']} - {bloque['fin']}"
                )
        
        self.__mantencion.append({"inicio": inicio, "fin": fin})
    
    def intersecta(self, inicio: datetime, fin: datetime) -> bool:
        """
        Verifica si el intervalo [inicio, fin) intersecta con algún bloque de mantención.
        """
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        for bloque in self.__mantencion:
            # Regla de intersección: A_inicio < B_fin AND B_inicio < A_fin
            if inicio < bloque["fin"] and bloque["inicio"] < fin:
                return True
        
        return False
    
    def eliminar(self, inicio: datetime, fin: datetime):
        """Elimina un bloque de mantención específico"""
        self.__mantencion = [
            b for b in self.__mantencion 
            if not (b["inicio"] == inicio and b["fin"] == fin)
        ]


class Cancha:
    """
    Recurso reservable que puede quedar indisponible por mantención.
    """
    
    def __init__(self, id_cancha: str, nombre: str):
        # Validaciones
        if not id_cancha or not id_cancha.strip():
            raise ValueError("id_cancha no puede estar vacío")
        if not nombre or not nombre.strip():
            raise ValueError("nombre no puede estar vacío")
        
        self.__id_cancha = id_cancha
        self.__nombre = nombre
        self.__calendario_mantencion = CalendarioCancha()
        self.__historial_eventos: List[Dict] = []
        
        self.__registrar_evento("creada", f"Cancha {nombre} creada")
    
    @property
    def id_cancha(self) -> str:
        return self.__id_cancha
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def calendario_mantencion(self) -> CalendarioCancha:
        """Calendario de mantención (acceso para uso del sistema)"""
        return self.__calendario_mantencion
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    def cantidad_bloques_mantencion(self) -> int:
        """Retorna la cantidad de bloques de mantención sin exponer la lista"""
        return self.__calendario_mantencion.cantidad_bloques()
    
    def obtener_bloques_mantencion(self) -> List[Dict]:
        """Retorna copia de los bloques de mantención"""
        return self.__calendario_mantencion.obtener_bloques()
    
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    def bloquear_mantencion(self, inicio: datetime, fin: datetime):
        """Agrega un intervalo de mantención al calendario"""
        self.__calendario_mantencion.agregar(inicio, fin)
        self.__registrar_evento(
            "mantencion_bloqueada",
            f"Mantención bloqueada: {inicio.strftime('%Y-%m-%d %H:%M')} - {fin.strftime('%Y-%m-%d %H:%M')}"
        )
    
    def desbloquear_mantencion(self, inicio: datetime, fin: datetime):
        """Elimina un intervalo de mantención del calendario"""
        self.__calendario_mantencion.eliminar(inicio, fin)
        self.__registrar_evento(
            "mantencion_desbloqueada",
            f"Mantención eliminada: {inicio.strftime('%Y-%m-%d %H:%M')} - {fin.strftime('%Y-%m-%d %H:%M')}"
        )
    
    def __str__(self):
        bloques = self.cantidad_bloques_mantencion()
        return f"Cancha {self.__nombre} (ID: {self.__id_cancha}) | {bloques} bloque(s) de mantención"