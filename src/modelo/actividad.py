from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship
from .declarative_base import Base

class Actividad(Base):

    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    terminada = Column(Boolean,default=False)
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')
    viajeros = relationship('Viajero', secondary='actividad_viajero')


    def __init__(self,nombre):
        self.nombre = nombre


    def dar_id(self):
        return self.id

    def cambiar_id(self,id):
        self.id = id 

    def dar_nombre(self):
        return self.nombre

    def cambiar_nombre(self,nombre):
        self.nombre = nombre    

    def esta_finalizada(self):
        return self.terminada

    def terminar_activdad(self):
        self.terminada = True

    def dar_gastos(self):
        return self.gastos

    def agregar_gasto(self,gasto):
        self.gastos.append(gasto)

    def cambiar_gastos(self,gastos):
        self.gastos = gastos

    def dar_viajeros_en_actividad(self):
        return self.viajeros

    def agregar_viajero_en_actividad(self,viajero):
        self.viajeros.append(viajero)

    def cambiar_viajeros(self,viajeros):
        self.viajeros = viajeros
