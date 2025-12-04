from sqlalchemy import Column, Integer, String, Date, Text
from config.db_config import Base

class Evento (Base):
    __tablename__ = "evento"

    evento_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, default="Desconocido")
    tipo = Column(String(255), nullable=False, default="Desconocido")
    agrupacion = Column(String(255), nullable=False, default="Desconocido")
    detalle_tipo_rotacion = Column(String(255), nullable=False, default="Desconocido")
    frecuencia = Column(String(255), nullable=False, default="Desconocida")
    tema = Column(String(255), nullable=False, default="Otro")
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    sede = Column(Text, nullable=False, default="Desconocida")
    categoria = Column(String(255), nullable=False, default="Desconocida")
    sitio_web = Column(String(255), nullable=False, default="Desconocido")
    entidad_organizadora = Column(String(255), nullable=False, default="Desconocida")
    requiere_revision = Column(String(255), nullable=False, default=True)