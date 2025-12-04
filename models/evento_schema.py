from datetime import date
from pydantic import Field, BaseModel

class Evento (BaseModel):

    nombre: str = Field(default="Desconocido", description="Nombre del evento")
    tipo: str = Field(default="Desconocido", description="Tipo del evento")
    agrupacion: str = Field(default="Desconocida", description="Agrupación a la que pertenece el evento")
    detalle_tipo_rotacion: str = Field(default="Desconocido", description="Tipo de rotación de la ubicación del evento")
    frecuencia: str = Field(default="Desconocida", description="Frecuencia con la que se realiza el evento")
    tema: str = Field(default="Desconocido", description="Temática del evento")
    fecha_inicio: date = Field(default=date(2025, 1, 1), description="Fecha completa en la que inicia el evento")
    fecha_fin: date = Field(default=date(2025, 1, 1), description="Fecha completa en la que finaliza el evento")
    sede: str = Field(default="Desconocida", description="Sede en la que se realiza el evento")
    categoria: str = Field(default="Desconocida", description="Categoría a la que pertenece el evento")
    entidad_organizadora: str = Field(default="Desconocida", description="Entidad que organiza el evento")