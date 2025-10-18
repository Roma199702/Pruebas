from datetime import datetime
from typing import Optional, List, Dict
from suscriptor import Suscriptor
from material import Material

class Retiro:
    """
    Registro de material entregado para reciclaje.
    Gestiona validación, puntos y trazabilidad.
    """
    
    def __init__(self, id_retiro: str, suscriptor: Suscriptor, fecha: datetime, 
                 material: Material, kg: float):
        # Validaciones
        if not id_retiro or not id_retiro.strip():
            raise ValueError("id_retiro no puede estar vacío")
        if not isinstance(suscriptor, Suscriptor):
            raise TypeError("suscriptor debe ser una instancia de Suscriptor")
        if not isinstance(material, Material):
            raise TypeError("material debe ser una instancia de Material")
        if kg <= 0:
            raise ValueError("kg debe ser mayor a 0")
        
        self.__id_retiro = id_retiro
        self.__suscriptor = suscriptor
        self.__fecha = fecha
        self.__material = material
        self.__kg = kg
        self.__estado = "registrado"
        self.__puntos_calculados: Optional[float] = None
        self.__historial_eventos: List[Dict] = []
        
        self.__registrar_evento(
            "registrado",
            f"Retiro registrado: {kg}kg de {material.nombre_material()}"
        )
    
    @property
    def id_retiro(self) -> str:
        return self.__id_retiro
    
    @property
    def suscriptor(self) -> Suscriptor:
        return self.__suscriptor
    
    @property
    def fecha(self) -> datetime:
        return self.__fecha
    
    @property
    def material(self) -> Material:
        return self.__material
    
    @property
    def kg(self) -> float:
        return self.__kg
    
    @property
    def estado(self) -> str:
        return self.__estado
    
    @property
    def puntos_calculados(self) -> Optional[float]:
        """Puntos otorgados por el retiro (solo lectura)"""
        return self.__puntos_calculados
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    @property
    def fecha_ultimo_cambio(self) -> datetime:
        """Último timestamp del historial (solo lectura)"""
        if not self.__historial_eventos:
            return self.__fecha
        return self.__historial_eventos[-1]["timestamp"]
    
    def __registrar_evento(self, tipo: str, detalle: str):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        self.__historial_eventos.append(evento)
    
    def validar(self, estrategia_peso: str = "rechazo"):
        """
        Valida el retiro aplicando la estrategia de peso definida.
        
        Args:
            estrategia_peso: "rechazo" o "particion"
        """
        if self.__estado != "registrado":
            raise ValueError(f"Solo se pueden validar retiros en estado 'registrado'. Estado actual: {self.__estado}")
        
        # Verificar que el suscriptor esté habilitado
        if self.__suscriptor.estado != "habilitado":
            raise ValueError("El suscriptor no está habilitado")
        
        # Verificar límite de peso por bolsa
        max_kg = self.__material.max_kg_por_bolsa()
        
        if self.__kg > max_kg:
            if estrategia_peso == "rechazo":
                raise ValueError(
                    f"Excede peso máximo por bolsa ({self.__kg}kg > {max_kg}kg). "
                    f"Estrategia: rechazo"
                )
            elif estrategia_peso == "particion":
                # En este caso simplificado, validamos el retiro completo
                # pero registramos que requirió partición
                self.__registrar_evento(
                    "particion_aplicada",
                    f"Retiro dividido automáticamente (original: {self.__kg}kg, límite: {max_kg}kg)"
                )
            else:
                raise ValueError("estrategia_peso debe ser 'rechazo' o 'particion'")
        
        # Calcular puntos usando polimorfismo
        self.__puntos_calculados = self.__material.puntos(self.__kg)
        
        # Acreditar puntos al suscriptor
        self.__suscriptor.acreditar_puntos(
            self.__puntos_calculados,
            f"Retiro #{self.__id_retiro} validado"
        )
        
        # Incrementar contador de retiros de la semana
        self.__suscriptor.incrementar_retiros_semana()
        
        # Cambiar estado
        self.__estado = "validado"
        self.__registrar_evento(
            "validado",
            f"Retiro validado. Puntos otorgados: {self.__puntos_calculados:.2f}"
        )
    
    def rechazar(self, motivo: str):
        """
        Rechaza el retiro sin otorgar puntos.
        Solo se puede rechazar desde estado 'registrado'.
        """
        if self.__estado != "registrado":
            raise ValueError(f"Solo se pueden rechazar retiros en estado 'registrado'. Estado actual: {self.__estado}")
        
        self.__estado = "rechazado"
        self.__registrar_evento("rechazado", f"Retiro rechazado. Motivo: {motivo}")
    
    def __str__(self):
        puntos_str = f"{self.__puntos_calculados:.2f} pts" if self.__puntos_calculados else "Sin calcular"
        return (f"Retiro #{self.__id_retiro} | {self.__material.nombre_material()} | "
                f"{self.__kg}kg | Estado: {self.__estado} | Puntos: {puntos_str}")