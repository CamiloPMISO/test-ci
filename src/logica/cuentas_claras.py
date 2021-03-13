from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.declarative_base import Session, Base, engine


class Cuentas_claras:

    def __init__(self) :
        Base.metadata.create_all(engine)
        self.session = Session()

    def listar_actividades(self):
        actividades = self.session.query(Actividad).all()
        if len(actividades) == 0 :
            return None
        actividades = [ actividad.dar_nombre() for actividad in actividades ]    
        return sorted(actividades)

    def dar_actividad_por_id(self,id):
        actividad = self.session.query(Actividad).get(id)
        return actividad
        
    def agregar_viajero(self,nombre,apellido):

        if nombre == "" or apellido == "" :
            return None

        if not nombre.isalpha() or not apellido.isalpha() :
            return None

        viajeros = self.session.query(Viajero).filter(Viajero.nombre==nombre,Viajero.apellido==apellido).all()
        
        if len(viajeros) > 0 :
            return None

        viajero = Viajero(nombre,apellido)
        self.session.add(viajero)
        self.session.commit()
        return True 

    def agregar_actividad(self,nombre):

        if nombre == "" :
            return None

        actividades = self.session.query(Actividad).filter(Actividad.nombre==nombre).all()

        if len(actividades) > 0 :
            return None

        actividad = Actividad(nombre)
        self.session.add(actividad)
        self.session.commit()
        return True 

            
    def dar_viajero_por_id(self,id):
        viajero = self.session.query(Viajero).get(id)
        return viajero

    def listar_gastos_actividad(self,id):

        actividad = self.dar_actividad_por_id(id)        
        gastos = actividad.dar_gastos()

        gastos_final = []

        for gasto in gastos : 
            gasto_dic ={}
            gasto_dic["Concepto"]= str(gasto.dar_concepto())
            gasto_dic["Valor"]= float(gasto.dar_valor())
            gasto_dic["Fecha"]= str(gasto.dar_fecha_gasto())
            gasto_dic["Nombre"]= str(self.dar_viajero_por_id(gasto.dar_viajero()).dar_nombre())
            gasto_dic["Apellido"]= str(self.dar_viajero_por_id(gasto.dar_viajero()).dar_apellido())
            gastos_final.append(gasto_dic)
        
        return gastos_final

    def listar_pasajeros_por_actividad(self,id):

        actividad = self.dar_actividad_por_id(id)        
        viajeros = actividad.dar_viajeros_en_actividad()

        viajeros_final = []

        for viajero in viajeros : 
            nombre_apellido = viajero.dar_nombre() + " " + viajero.dar_apellido() 
            viajeros_final.append(nombre_apellido)

        return viajeros_final

    def generar_reporte_compensacion_por_actividad(self,id):

        gastos_consolidados = self.generar_reporte_por_viajeros_por_actividad(id)

        promedio = sum([viajero["Valor"] for viajero in gastos_consolidados])/len(gastos_consolidados)

        a_compensar = {}
        deben_compensar = {}

        for gasto in gastos_consolidados : 
            nombre_apellido = gasto["Nombre"] + " " + gasto["Apellido"]
            if promedio > gasto["Valor"] :
                deben_compensar[nombre_apellido] = promedio - gasto["Valor"]
            else :
                a_compensar[nombre_apellido] = gasto["Valor"] - promedio

        reporte = [[None for i in range(len(gastos_consolidados)+1)] for j in range(len(gastos_consolidados)+1)]

        reporte[0][0]= ""
        for i in range(1,len(reporte)):
            nombre_apellido = gastos_consolidados[i-1]["Nombre"] + " " + gastos_consolidados[i-1]["Apellido"]
            reporte[i][0] =   nombre_apellido
            reporte[0][i] =   nombre_apellido

        for i in range(1,len(reporte)): # debe compensar
            for j in range(1,len(reporte)) : # a compensar
                if i == j :
                    reporte[i][j] = -1 
                else :
                    viajero1 = reporte[0][j] # filas
                    viajero2 = reporte[i][0] # columnas
                    if (viajero1 in deben_compensar) and (viajero2 in a_compensar):
                        valor1 = deben_compensar[viajero1]
                        valor2 = a_compensar[viajero2]
                        if valor1 > valor2 :
                            reporte[i][j] = valor2
                            deben_compensar[viajero1]-=valor2
                            del a_compensar[viajero2]
                        elif valor2 > valor1 :
                            reporte[i][j] = valor1
                            a_compensar[viajero2]-=valor1
                            del deben_compensar[viajero1]
                        else : 
                            reporte[i][j] = valor1
                            del deben_compensar[viajero1]
                            del a_compensar[viajero2]
                    else :
                        reporte[i][j] = 0

        return reporte

    def generar_reporte_por_viajeros_por_actividad(self,id):

        viajeros = self.listar_pasajeros_por_actividad(id)
        gastos = self.listar_gastos_actividad(id)
        
        gastos_por_viajero = {}

        for nom_viajero in viajeros :
            gastos_por_viajero[nom_viajero] = 0

        for gasto in gastos :
            nombre_apellido = gasto["Nombre"]+" "+gasto["Apellido"]
            gastos_por_viajero[nombre_apellido] += gasto["Valor"] 

        gasto_consolidado = []

        for nombre_apellido, valor in gastos_por_viajero.items() :
            viajero = {}
            viajero["Nombre"] = nombre_apellido.split(" ")[0]
            viajero["Apellido"] = nombre_apellido.split(" ")[1]
            viajero["Valor"] = valor
            gasto_consolidado.append(viajero)

        return gasto_consolidado
