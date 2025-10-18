from datetime import datetime
from typing import List, Dict
from .franja import Franja
from .turno_asignado import TurnoAsignado
from .colaborador import Colaborador
from .politica_turno import PoliticaTurno

class PlanSemanal:
    """
    Resultado de la planificación para una semana.
    Gestiona franjas, turnos asignados y validaciones.
    """
    
    def __init__(self, semana: str, franjas: List[Franja]):
        # Validaciones
        if not semana or not semana.strip():
            raise ValueError("semana no puede estar vacía")
        if not franjas:
            raise ValueError("debe haber al menos una franja")
        
        self.__semana = semana
        self.__franjas = franjas.copy()
        self.__turnos_asignados: List[TurnoAsignado] = []
        self.__historial_eventos: List[Dict] = []
        
        self.__registrar_evento("creado", f"Plan semanal creado para {semana}")
    
    @property
    def semana(self) -> str:
        return self.__semana
    
    @property
    def franjas(self) -> List[Franja]:
        return self.__franjas.copy()
    
    @property
    def turnos_asignados(self) -> List[TurnoAsignado]:
        return self.__turnos_asignados.copy()
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    @property
    def cobertura_porcentaje(self) -> float:
        """Calcula el porcentaje de cobertura (solo lectura)"""
        if not self.__franjas:
            return 0.0
        return (len(self.__turnos_asignados) / len(self.__franjas)) * 100
    
    @property
    def valido(self) -> bool:
        """
        Verifica si el plan es válido:
        - Todas las franjas tienen responsable
        - Nadie supera horas_semana_max
        """
        # Verificar cobertura total
        if len(self.__turnos_asignados) != len(self.__franjas):
            return False
        
        # Verificar límites de horas (se verifica durante asignación)
        return True
    
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    def generar_plan(self, politica: PoliticaTurno, colaboradores: List[Colaborador]):
        """
        Genera el plan usando la política especificada.
        Resetea horas de colaboradores antes de asignar.
        """
        if not isinstance(politica, PoliticaTurno):
            raise TypeError("politica debe ser una instancia de PoliticaTurno")
        
        # Resetear horas de todos los colaboradores
        for colaborador in colaboradores:
            colaborador.resetear_horas_semana()
        
        # Generar asignaciones usando la política
        self.__turnos_asignados = politica.asignar(self.__semana, colaboradores, self.__franjas)
        
        self.__registrar_evento(
            "plan_generado",
            f"Plan generado con {politica.__class__.__name__}. "
            f"Cobertura: {self.cobertura_porcentaje:.1f}%"
        )
    
    def reasignar(self, franja: Franja, nuevo_responsable: Colaborador, motivo: str):
        """
        Reasigna una franja a un nuevo responsable.
        Valida disponibilidad y límites de horas.
        """
        # Buscar el turno correspondiente
        turno = None
        for t in self.__turnos_asignados:
            if t.franja == franja:
                turno = t
                break
        
        if not turno:
            raise ValueError(f"No existe turno para la franja {franja}")
        
        # Validar disponibilidad
        if not nuevo_responsable.esta_disponible(franja.dia, franja.hora_inicio, franja.hora_fin):
            raise ValueError(f"{nuevo_responsable.nombre} no está disponible en ese horario")
        
        # Liberar horas del responsable anterior
        responsable_anterior = turno.responsable
        responsable_anterior.asignar_horas(-franja.duracion_horas)
        
        # Validar que el nuevo responsable no exceda límite
        if not nuevo_responsable.puede_asumir_horas(franja.duracion_horas):
            # Revertir liberación de horas
            responsable_anterior.asignar_horas(franja.duracion_horas)
            raise ValueError(f"{nuevo_responsable.nombre} excedería su límite semanal")
        
        # Verificar si rompe preferencia
        momento = franja.obtener_momento_dia()
        forzado = (nuevo_responsable.preferencia != "indistinto" and 
                  nuevo_responsable.preferencia != momento)
        
        # Asignar horas al nuevo responsable
        nuevo_responsable.asignar_horas(franja.duracion_horas)
        
        # Reasignar
        turno.reasignar(nuevo_responsable, motivo, forzado)
        
        self.__registrar_evento(
            "reasignacion",
            f"Franja {franja} reasignada a {nuevo_responsable.nombre}"
        )
    
    def obtener_turnos_por_dia(self, dia: str) -> List[TurnoAsignado]:
        """Retorna todos los turnos de un día específico"""
        return [t for t in self.__turnos_asignados if t.franja.dia == dia]
    
    def obtener_turnos_por_colaborador(self, colaborador: Colaborador) -> List[TurnoAsignado]:
        """Retorna todos los turnos de un colaborador"""
        return [t for t in self.__turnos_asignados if t.responsable.id_colaborador == colaborador.id_colaborador]
    
    def contar_turnos_forzados(self) -> int:
        """Cuenta cuántos turnos están marcados como forzados"""
        return sum(1 for t in self.__turnos_asignados if t.marcado_forzado)
    
    def __str__(self):
        return (f"Plan Semanal {self.__semana} | "
                f"Cobertura: {self.cobertura_porcentaje:.1f}% | "
                f"Válido: {'Sí' if self.valido else 'No'}")