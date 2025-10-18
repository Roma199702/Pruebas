from abc import ABC, abstractmethod
from typing import List
from .colaborador import Colaborador
from .franja import Franja
from .turno_asignado import TurnoAsignado

class PoliticaTurno(ABC):
    """
    Clase abstracta que define el contrato para asignar turnos.
    Cada subtipo implementa una estrategia diferente.
    """
    
    @abstractmethod
    def asignar(self, semana: str, colaboradores: List[Colaborador], 
                franjas: List[Franja]) -> List[TurnoAsignado]:
        """
        Asigna responsables a todas las franjas según la política específica.
        Retorna lista de TurnoAsignado.
        """
        pass


class TurnoFijo(PoliticaTurno):
    """
    Mantiene un titular por franja. Si no puede, asigna suplente.
    Marca como forzado si rompe preferencia.
    """
    
    def __init__(self, titulares: dict):
        """
        titulares: dict con formato {(dia, hora_inicio): id_colaborador}
        Ejemplo: {("Lunes", "08:00"): "C001"}
        """
        self.__titulares = titulares
    
    def asignar(self, semana: str, colaboradores: List[Colaborador], 
                franjas: List[Franja]) -> List[TurnoAsignado]:
        turnos = []
        
        for franja in franjas:
            clave = (franja.dia, franja.hora_inicio)
            id_titular = self.__titulares.get(clave)
            
            # Buscar titular
            titular = None
            if id_titular:
                titular = next((c for c in colaboradores if c.id_colaborador == id_titular), None)
            
            asignado = False
            forzado = False
            
            # Intentar asignar al titular
            if titular:
                if self.__puede_asignar(titular, franja):
                    # Verificar si respeta preferencia
                    momento = franja.obtener_momento_dia()
                    if titular.preferencia != "indistinto" and titular.preferencia != momento:
                        forzado = True
                    
                    turno = TurnoAsignado(franja, titular, forzado)
                    titular.asignar_horas(franja.duracion_horas)
                    turnos.append(turno)
                    asignado = True
            
            # Si no se pudo asignar al titular, buscar suplente
            if not asignado:
                for colaborador in colaboradores:
                    if self.__puede_asignar(colaborador, franja):
                        momento = franja.obtener_momento_dia()
                        forzado = (colaborador.preferencia != "indistinto" and 
                                 colaborador.preferencia != momento)
                        
                        turno = TurnoAsignado(franja, colaborador, forzado)
                        colaborador.asignar_horas(franja.duracion_horas)
                        turnos.append(turno)
                        asignado = True
                        break
            
            if not asignado:
                raise ValueError(f"No se pudo asignar responsable para {franja}")
        
        return turnos
    
    def __puede_asignar(self, colaborador: Colaborador, franja: Franja) -> bool:
        """Verifica si el colaborador puede ser asignado a la franja"""
        return (colaborador.esta_disponible(franja.dia, franja.hora_inicio, franja.hora_fin) and
                colaborador.puede_asumir_horas(franja.duracion_horas))


class TurnoRotativo(PoliticaTurno):
    """
    Prohíbe que la misma persona abra dos días seguidos.
    Asume que las franjas están ordenadas cronológicamente.
    """
    
    def asignar(self, semana: str, colaboradores: List[Colaborador], 
                franjas: List[Franja]) -> List[TurnoAsignado]:
        turnos = []
        
        # Ordenar días de la semana
        dias_ordenados = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        franjas_ordenadas = sorted(franjas, key=lambda f: (dias_ordenados.index(f.dia), f.hora_inicio))
        
        # Agrupar por día y encontrar primera franja (apertura) de cada día
        aperturas_por_dia = {}
        for franja in franjas_ordenadas:
            if franja.dia not in aperturas_por_dia:
                aperturas_por_dia[franja.dia] = franja
        
        ultimo_apertura = None
        
        for franja in franjas_ordenadas:
            es_apertura = (franja == aperturas_por_dia.get(franja.dia))
            
            # Buscar colaborador disponible
            for colaborador in colaboradores:
                # Si es apertura, verificar que no sea el mismo que abrió ayer
                if es_apertura and ultimo_apertura == colaborador.id_colaborador:
                    continue
                
                if self.__puede_asignar(colaborador, franja):
                    momento = franja.obtener_momento_dia()
                    forzado = (colaborador.preferencia != "indistinto" and 
                             colaborador.preferencia != momento)
                    
                    turno = TurnoAsignado(franja, colaborador, forzado)
                    colaborador.asignar_horas(franja.duracion_horas)
                    turnos.append(turno)
                    
                    if es_apertura:
                        ultimo_apertura = colaborador.id_colaborador
                    break
        
        if len(turnos) < len(franjas):
            raise ValueError("No se pudieron asignar todos los turnos con política rotativa")
        
        return turnos
    
    def __puede_asignar(self, colaborador: Colaborador, franja: Franja) -> bool:
        return (colaborador.esta_disponible(franja.dia, franja.hora_inicio, franja.hora_fin) and
                colaborador.puede_asumir_horas(franja.duracion_horas))


class TurnoFlexible(PoliticaTurno):
    """
    Prioriza preferencia (mañana/tarde).
    Si no hay alternativa, asigna y marca como forzado.
    """
    
    def asignar(self, semana: str, colaboradores: List[Colaborador], 
                franjas: List[Franja]) -> List[TurnoAsignado]:
        turnos = []
        
        for franja in franjas:
            momento = franja.obtener_momento_dia()
            
            # Primero intentar con colaboradores que prefieren este momento
            asignado = False
            
            # Prioridad 1: Preferencia coincide
            for colaborador in colaboradores:
                if (colaborador.preferencia == momento or colaborador.preferencia == "indistinto"):
                    if self.__puede_asignar(colaborador, franja):
                        turno = TurnoAsignado(franja, colaborador, False)
                        colaborador.asignar_horas(franja.duracion_horas)
                        turnos.append(turno)
                        asignado = True
                        break
            
            # Prioridad 2: Asignar aunque no coincida preferencia (forzado)
            if not asignado:
                for colaborador in colaboradores:
                    if self.__puede_asignar(colaborador, franja):
                        turno = TurnoAsignado(franja, colaborador, True)  # Marcado como forzado
                        colaborador.asignar_horas(franja.duracion_horas)
                        turnos.append(turno)
                        asignado = True
                        break
            
            if not asignado:
                raise ValueError(f"No se pudo asignar responsable para {franja}")
        
        return turnos
    
    def __puede_asignar(self, colaborador: Colaborador, franja: Franja) -> bool:
        return (colaborador.esta_disponible(franja.dia, franja.hora_inicio, franja.hora_fin) and
                colaborador.puede_asumir_horas(franja.duracion_horas))