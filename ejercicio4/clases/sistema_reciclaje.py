from datetime import datetime, timedelta
from typing import List
from suscriptor import Suscriptor
from retiro import Retiro

class SistemaReciclaje:
    """
    Gestor principal del sistema de reciclaje domiciliario.
    Coordina retiros, bonificaciones y validaciones.
    """
    
    def __init__(self, estrategia_peso: str = "rechazo"):
        """
        Args:
            estrategia_peso: "rechazo" o "particion" (se aplica en todo el sistema)
        """
        if estrategia_peso not in ["rechazo", "particion"]:
            raise ValueError("estrategia_peso debe ser 'rechazo' o 'particion'")
        
        self.__retiros: List[Retiro] = []
        self.__estrategia_peso = estrategia_peso
        self.__bonos_aplicados_semana = set()  # Set de id_suscriptor que ya recibieron bono esta semana
    
    @property
    def retiros(self) -> List[Retiro]:
        """Retorna una copia de la lista de retiros"""
        return self.__retiros.copy()
    
    @property
    def estrategia_peso(self) -> str:
        """Estrategia de peso aplicada en el sistema"""
        return self.__estrategia_peso
    
    def registrar_retiro(self, retiro: Retiro):
        """
        Registra un nuevo retiro en el sistema.
        """
        if not isinstance(retiro, Retiro):
            raise TypeError("retiro debe ser una instancia de Retiro")
        
        # Validar unicidad de ID
        if any(r.id_retiro == retiro.id_retiro for r in self.__retiros):
            raise ValueError(f"Ya existe un retiro con id {retiro.id_retiro}")
        
        self.__retiros.append(retiro)
    
    def validar_retiro(self, id_retiro: str):
        """
        Valida un retiro y aplica bonificación semanal si corresponde.
        """
        # Buscar el retiro
        retiro = self.buscar_por_id(id_retiro)
        
        # Validar usando la estrategia del sistema
        retiro.validar(self.__estrategia_peso)
        
        # Verificar si aplica bonificación semanal
        self.__verificar_y_aplicar_bono_semanal(retiro.suscriptor)
    
    def __verificar_y_aplicar_bono_semanal(self, suscriptor: Suscriptor):
        """
        Verifica si el suscriptor califica para bonificación semanal.
        Otorga +10 puntos si tiene >= 3 retiros validados en la semana.
        """
        # Si ya recibió el bono esta semana, no aplicar de nuevo
        if suscriptor.id_suscriptor in self.__bonos_aplicados_semana:
            return
        
        # Contar retiros validados del suscriptor en la semana actual
        if suscriptor.retiros_validados_semana >= 3:
            # Otorgar bonificación
            suscriptor.acreditar_puntos(10.0, "Bonificación semanal (≥3 retiros)")
            
            # Marcar que ya recibió el bono
            self.__bonos_aplicados_semana.add(suscriptor.id_suscriptor)
    
    def rechazar_retiro(self, id_retiro: str, motivo: str):
        """
        Rechaza un retiro.
        """
        retiro = self.buscar_por_id(id_retiro)
        retiro.rechazar(motivo)
    
    def buscar_por_id(self, id_retiro: str) -> Retiro:
        """Busca un retiro por su ID"""
        for retiro in self.__retiros:
            if retiro.id_retiro == id_retiro:
                return retiro
        raise ValueError(f"No se encontró retiro con id {id_retiro}")
    
    def listar_por_suscriptor(self, suscriptor: Suscriptor) -> List[Retiro]:
        """Lista todos los retiros de un suscriptor"""
        return [r for r in self.__retiros if r.suscriptor.id_suscriptor == suscriptor.id_suscriptor]
    
    def listar_por_estado(self, estado: str) -> List[Retiro]:
        """Lista todos los retiros con un estado específico"""
        return [r for r in self.__retiros if r.estado == estado]
    
    def listar_por_material(self, nombre_material: str) -> List[Retiro]:
        """Lista todos los retiros de un tipo de material"""
        return [r for r in self.__retiros if r.material.nombre_material().lower() == nombre_material.lower()]
    
    def obtener_retiros_semana(self, suscriptor: Suscriptor) -> List[Retiro]:
        """
        Retorna los retiros validados del suscriptor en la semana actual.
        Semana se define como los últimos 7 días desde hoy.
        """
        hace_7_dias = datetime.now() - timedelta(days=7)
        retiros_suscriptor = self.listar_por_suscriptor(suscriptor)
        
        return [
            r for r in retiros_suscriptor 
            if r.estado == "validado" and r.fecha >= hace_7_dias
        ]
    
    def resetear_semana(self):
        """
        Resetea contadores semanales (al iniciar nueva semana).
        Debe ejecutarse manualmente cada semana.
        """
        self.__bonos_aplicados_semana.clear()
        
        # Resetear contadores de todos los suscriptores únicos
        suscriptores_unicos = set()
        for retiro in self.__retiros:
            suscriptores_unicos.add(retiro.suscriptor)
        
        for suscriptor in suscriptores_unicos:
            suscriptor.resetear_contador_semanal()
    
    def calcular_total_kg_reciclados(self) -> float:
        """Calcula el total de kg reciclados (solo retiros validados)"""
        return sum(r.kg for r in self.__retiros if r.estado == "validado")
    
    def calcular_total_puntos_otorgados(self) -> float:
        """Calcula el total de puntos otorgados en el sistema"""
        return sum(
            r.puntos_calculados for r in self.__retiros 
            if r.estado == "validado" and r.puntos_calculados is not None
        )
    
    def __str__(self):
        return (f"Sistema de Reciclaje | {len(self.__retiros)} retiro(s) | "
                f"Estrategia de peso: {self.__estrategia_peso}")