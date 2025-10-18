class Franja:
    """
    Bloque horario a cubrir en un día específico.
    Calcula automáticamente su duración en horas.
    """
    
    def __init__(self, dia: str, hora_inicio: str, hora_fin: str):
        # Validaciones
        if not dia or not dia.strip():
            raise ValueError("dia no puede estar vacío")
        if hora_inicio >= hora_fin:
            raise ValueError("hora_inicio debe ser menor que hora_fin")
        
        self.__dia = dia
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
    
    @property
    def dia(self) -> str:
        return self.__dia
    
    @property
    def hora_inicio(self) -> str:
        return self.__hora_inicio
    
    @property
    def hora_fin(self) -> str:
        return self.__hora_fin
    
    @property
    def duracion_horas(self) -> float:
        """Calcula la duración en horas (solo lectura)"""
        # Parsear horas y minutos
        h_inicio, m_inicio = map(int, self.__hora_inicio.split(':'))
        h_fin, m_fin = map(int, self.__hora_fin.split(':'))
        
        # Calcular diferencia en minutos
        minutos_inicio = h_inicio * 60 + m_inicio
        minutos_fin = h_fin * 60 + m_fin
        diferencia_minutos = minutos_fin - minutos_inicio
        
        # Convertir a horas
        return diferencia_minutos / 60.0
    
    def obtener_momento_dia(self) -> str:
        """Determina si es mañana o tarde según la hora de inicio"""
        hora = int(self.__hora_inicio.split(':')[0])
        if hora < 14:
            return "manana"
        else:
            return "tarde"
    
    def __str__(self):
        return f"{self.__dia} {self.__hora_inicio}-{self.__hora_fin} ({self.duracion_horas:.1f}h)"
    
    def __eq__(self, other):
        if not isinstance(other, Franja):
            return False
        return (self.__dia == other.__dia and 
                self.__hora_inicio == other.__hora_inicio and
                self.__hora_fin == other.__hora_fin)
    
    def __hash__(self):
        return hash((self.__dia, self.__hora_inicio, self.__hora_fin))