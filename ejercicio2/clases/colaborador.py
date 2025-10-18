from datetime import datetime
from typing import List, Dict

class Colaborador:
    """
    Persona elegible para cubrir franjas del plan semanal.
    Gestiona preferencias, disponibilidad y límites de horas.
    """
    
    def __init__(self, id_colaborador: str, nombre: str, horas_semana_max: int, 
                 preferencia: str):
        # Validaciones
        if not id_colaborador or not id_colaborador.strip():
            raise ValueError("id_colaborador no puede estar vacío")
        if not nombre or not nombre.strip():
            raise ValueError("nombre no puede estar vacío")
        if horas_semana_max <= 0:
            raise ValueError("horas_semana_max debe ser mayor a 0")
        if preferencia not in ["manana", "tarde", "indistinto"]:
            raise ValueError("preferencia debe ser 'manana', 'tarde' o 'indistinto'")
        
        self.__id_colaborador = id_colaborador
        self.__nombre = nombre
        self.__horas_semana_max = horas_semana_max
        self.__preferencia = preferencia
        self.__no_disponible: List[Dict] = []
        self.__historial_eventos: List[Dict] = []
        self.__horas_asignadas_semana = 0.0
        
        self.__registrar_evento("creado", f"Colaborador {nombre} creado")
    
    # Getters
    @property
    def id_colaborador(self) -> str:
        return self.__id_colaborador
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def horas_semana_max(self) -> int:
        return self.__horas_semana_max
    
    @property
    def preferencia(self) -> str:
        return self.__preferencia
    
    @property
    def no_disponible(self) -> List[Dict]:
        return self.__no_disponible.copy()
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    @property
    def horas_asignadas_semana(self) -> float:
        """Suma de horas asignadas en el plan vigente (solo lectura)"""
        return self.__horas_asignadas_semana
    
    # Métodos privados
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    # Métodos públicos
    def agregar_no_disponible(self, dia: str, hora_inicio: str, hora_fin: str):
        """Agrega un intervalo de no disponibilidad"""
        if hora_inicio >= hora_fin:
            raise ValueError("hora_inicio debe ser menor que hora_fin")
        
        intervalo = {
            "dia": dia,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
        self.__no_disponible.append(intervalo)
        self.__registrar_evento(
            "no_disponible_agregado",
            f"No disponible: {dia} {hora_inicio}-{hora_fin}"
        )
    
    def esta_disponible(self, dia: str, hora_inicio: str, hora_fin: str) -> bool:
        """Verifica si el colaborador está disponible en el intervalo dado"""
        for intervalo in self.__no_disponible:
            if intervalo["dia"] == dia:
                # Verificar intersección
                if hora_inicio < intervalo["hora_fin"] and intervalo["hora_inicio"] < hora_fin:
                    return False
        return True
    
    def puede_asumir_horas(self, horas: float) -> bool:
        """Verifica si puede asumir más horas sin exceder el límite"""
        return (self.__horas_asignadas_semana + horas) <= self.__horas_semana_max
    
    def asignar_horas(self, horas: float):
        """Incrementa las horas asignadas (uso interno del sistema)"""
        if not self.puede_asumir_horas(horas):
            raise ValueError(
                f"Excedería límite semanal ({self.__horas_asignadas_semana + horas} > {self.__horas_semana_max})"
            )
        self.__horas_asignadas_semana += horas
    
    def resetear_horas_semana(self):
        """Resetea el contador de horas (al iniciar nueva semana)"""
        self.__horas_asignadas_semana = 0.0
        self.__registrar_evento("horas_reseteadas", "Contador de horas semanal reseteado")
    
    def __str__(self):
        return (f"Colaborador {self.__nombre} | Preferencia: {self.__preferencia} | "
                f"Horas: {self.__horas_asignadas_semana}/{self.__horas_semana_max}")