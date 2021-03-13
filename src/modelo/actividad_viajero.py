from sqlalchemy import Column, Integer, ForeignKey
from src.modelo.declarative_base import Base

class ActividadViajero(Base):
   __tablename__ = 'actividad_viajero'

   actividad = Column(Integer, ForeignKey('actividad.id'),primary_key=True)
   viajero = Column(Integer, ForeignKey('viajero.id'),primary_key=True)