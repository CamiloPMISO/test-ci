from sqlalchemy import Column, Integer, String, Boolean, Float , Date, ForeignKey
from src.modelo.declarative_base import Base

class Gasto(Base):

    __tablename__ = 'gasto'
    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    valor = Column(String)
    fecha_gasto = Column(Date)
    viajero = Column(Integer, ForeignKey('viajero.id'),nullable=False)
    actividad = Column(Integer, ForeignKey('actividad.id'),nullable=False)

    def dar_concepto(self):
        return self.concepto

    def cambiar_concepto(self,concepto):
        self.concepto = concepto

    def dar_valor(self):
        return self.valor

    def cambiar_valor(self,valor):
        self.valor = valor

    def dar_fecha_gasto(self):
        return self.fecha_gasto.strftime("%d-%m-%Y")
        
    def cambiar_fecha_gasto(self,fecha_gasto):
        self.fecha_gasto = fecha_gasto

    def dar_viajero(self):
        return self.viajero 

    def cambiar_viajero(self,id_viajero):
        self.viajero = id_viajero