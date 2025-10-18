from datetime import datetime
from typing import Optional, List, Dict

class Reserva:
    """
    Solicitud/ocupación de una cancha en un intervalo.
    Gestiona cotización, confirmación, cancelación y no-show.
    """
    
    def __init__(self, id_reserva: str, cancha, cliente: str, 
                 inicio: datetime, fin: datetime):
        # Validaciones
        if not id_reserva or not id_reserva.strip():
            raise ValueError("id_reserva no puede estar vacío")
        if not cliente or not cliente.strip():
            raise ValueError("cliente no puede estar vacío")
        if inicio >= fin:
            raise ValueError("inicio debe ser menor que fin")
        
        self.__id_reserva = id_reserva
        self.__cancha = cancha
        self.__cliente = cliente
        self.__inicio = inicio
        self.__fin = fin
        self.__estado = "creada"
        self.__importe: Optional[float] = None
        self.__desglose_tarifa: Optional[List[Dict]] = None
        self.__historial_eventos: List[Dict] = []
        
        self.__registrar_evento("creada", f"Reserva creada para {cliente} en {cancha.nombre}")
    
    # Getters
    @property
    def id_reserva(self) -> str:
        return self.__id_reserva
    
    @property
    def cancha(self):
        return self.__cancha
    
    @property
    def cliente(self) -> str:
        return self.__cliente
    
    @property
    def inicio(self) -> datetime:
        return self.__inicio
    
    @property
    def fin(self) -> datetime:
        return self.__fin
    
    @property
    def estado(self) -> str:
        return self.__estado
    
    @property
    def importe(self) -> Optional[float]:
        """Importe calculado (solo lectura)"""
        return self.__importe
    
    @property
    def desglose_tarifa(self) -> Optional[List[Dict]]:
        """Desglose de tramos de tarifa (solo lectura)"""
        if self.__desglose_tarifa is None:
            return None
        return self.__desglose_tarifa.copy()
    
    @property
    def historial_eventos(self) -> List[Dict]:
        return self.__historial_eventos.copy()
    
    def __registrar_evento(self, tipo: str, detalle: str, monto: Optional[float] = None):
        evento = {
            "timestamp": datetime.now(),
            "tipo": tipo,
            "detalle": detalle
        }
        if monto is not None:
            evento["monto"] = monto
        self.__historial_eventos.append(evento)
    
    def cotizar(self, tarifa):
        """
        Calcula y fija el importe usando la tarifa especificada.
        El importe queda como solo lectura.
        """
        if self.__importe is not None:
            raise ValueError("La reserva ya fue cotizada")
        
        # Calcular importe y desglose
        resultado = tarifa.calcular_importe(self.__inicio, self.__fin)
        self.__importe = resultado["total"]
        self.__desglose_tarifa = resultado["desglose"]
        
        # Obtener nombre de tarifa de forma segura
        nombre_tarifa = tarifa.__class__.__name__ if hasattr(tarifa, '__class__') else "Tarifa"
        
        self.__registrar_evento(
            "cotizada",
            f"Reserva cotizada con {nombre_tarifa}",
            self.__importe
        )
    
    def confirmar(self, motivo: str, agenda_sistema):
        """
        Confirma la reserva validando:
        - No hay solape con otras reservas de la misma cancha
        - No intersecta con mantención
        """
        if self.__estado != "creada":
            raise ValueError(f"Solo se pueden confirmar reservas en estado 'creada'. Estado actual: {self.__estado}")
        
        # Verificar si hay mantención
        if self.__cancha.calendario_mantencion.intersecta(self.__inicio, self.__fin):
            raise ValueError("La reserva intersecta con un bloque de mantención")
        
        # Verificar solape con otras reservas
        if agenda_sistema.existe_solape(self.__cancha, self.__inicio, self.__fin):
            raise ValueError(f"Existe solape con otra reserva en {self.__cancha.nombre}")
        
        self.__estado = "confirmada"
        self.__registrar_evento("confirmada", f"Reserva confirmada. Motivo: {motivo}")
    
    def cancelar(self, motivo: str, politica):
        """
        Cancela la reserva aplicando la política de cancelación.
        Calcula penalización según horas previas a la reserva.
        """
        if self.__estado not in ["creada", "confirmada"]:
            raise ValueError(f"No se puede cancelar una reserva en estado '{self.__estado}'")
        
        # Calcular horas previas
        ahora = datetime.now()
        horas_previas = (self.__inicio - ahora).total_seconds() / 3600
        
        # Si ya pasó la hora de inicio, horas_previas será negativo
        if horas_previas < 0:
            horas_previas = 0
        
        # Calcular penalización
        importe_base = self.__importe if self.__importe else 0.0
        resultado_penalizacion = politica.penalizacion(horas_previas, importe_base)
        
        self.__estado = "cancelada"
        self.__registrar_evento(
            "cancelada",
            f"Reserva cancelada. {resultado_penalizacion['motivo']}",
            resultado_penalizacion['monto_penalizacion']
        )
    
    def marcar_no_show(self, motivo: str):
        """
        Marca la reserva como no-show (inasistencia).
        Solo aplica a reservas confirmadas.
        """
        if self.__estado != "confirmada":
            raise ValueError("Solo se puede marcar no-show en reservas confirmadas")
        
        self.__estado = "no_show"
        self.__registrar_evento(
            "no_show",
            f"Cliente no se presentó. Motivo: {motivo}",
            self.__importe  # Se cobra el 100% por no-show
        )
    
    def __str__(self):
        importe_str = f"${self.__importe:,.0f}" if self.__importe else "Sin cotizar"
        return (f"Reserva #{self.__id_reserva} | Cliente: {self.__cliente} | "
                f"Cancha: {self.__cancha.nombre} | Estado: {self.__estado} | "
                f"Importe: {importe_str}")