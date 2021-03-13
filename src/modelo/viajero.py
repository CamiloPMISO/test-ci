from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base

class Viajero(Base):

    __tablename__ = 'viajero'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    actividades = relationship('Actividad', secondary='actividad_viajero')
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')

    def __init__(self,nombre,apellido):
        self.nombre = nombre
        self.apellido = apellido

    def dar_id(self):
        return self.id
    
    def dar_nombre(self):
        return self.nombre

    def cambiar_nombre(self,nombre):
        self.nombre = nombre

    def dar_apellido(self):
        return self.apellido

    def cambiar_apellido(self,apellido):
        self.apellido = apellido

    def dar_actividades(self):
        return self.activiades

    def cambiar_actividades(self,actividades):
        self.actividades = actividades

    def dar_gastos(self,gastos):
        return self.gastos

    def agregar_gasto(self,gasto):
        self.gastos.append(gasto)