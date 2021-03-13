# -*- coding: utf-8 -*-

import unittest
import re
import random
from faker import Faker
from datetime import date,datetime

from src.modelo.actividad import Actividad
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from src.logica.cuentas_claras import Cuentas_claras

class Reporte_compensacion_test_case(unittest.TestCase):


    def setUp(self):

        '''Crea una colección para hacer las pruebas'''
        self.cuentas_claras = Cuentas_claras()

        '''Abre la sesión'''
        self.session = Session()

        '''Crear Faker '''
        self.data_factory = Faker()

        Faker.seed(1000)

        '''Crea las actividades'''
        # crear actividades random

        self.actividades = []

        for _ in range(1):
            actividad = Actividad(nombre=self.data_factory.unique.name())
            self.session.add(actividad)
            self.actividades.append(actividad)

        # crear viajeros random
        self.viajeros = []

        for _ in range(4):
            viajero = Viajero(self.data_factory.unique.first_name(),self.data_factory.unique.last_name())
            self.session.add(viajero)
            self.viajeros.append(viajero)

        for i in range(len(self.viajeros)):
            self.actividades[0].agregar_viajero_en_actividad(self.viajeros[i])

        # crear gastos random

        self.gastos = []
        for _ in range(8):
            gasto = Gasto(concepto=self.data_factory.unique.name(),valor=random.uniform(1, 1000),fecha_gasto= datetime.strptime(self.data_factory.date(),'%Y-%m-%d'))
            self.session.add(gasto)
            self.gastos.append(gasto)

        # se asigna aleatoriamente los gastos a los viajeros
        for i in range(len(self.gastos)):
            viajero_id = random.randrange(len(self.viajeros))
            self.viajeros[viajero_id].agregar_gasto(self.gastos[i])

        for i in range(len(self.gastos)):
            self.actividades[0].agregar_gasto(self.gastos[i])
 
        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todas las actividades'''
        actividades = self.session.query(Actividad).all()

        '''Borra todas las actividades'''
        for actividad in actividades:
            self.session.delete(actividad)

        '''Consulta todas las actividades'''
        viajeros = self.session.query(Viajero).all()

        '''Borra todas las actividades'''
        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def test_validar_matriz_diagonal(self):
        reporte = self.cuentas_claras.generar_reporte_compensacion_por_actividad(1)

        for i in range(1,len(reporte)) :
            self.assertEqual(reporte[i][i],-1)

    def test_validar_reporte(self):
        reporte_por_viajero = self.cuentas_claras.generar_reporte_por_viajeros_por_actividad(1)
        reporte = self.cuentas_claras.generar_reporte_compensacion_por_actividad(1)

        promedio = sum([viajero["Valor"] for viajero in reporte_por_viajero])/len(reporte_por_viajero)

        for viajero in reporte_por_viajero :
            valor = viajero["Valor"]
            nombre_apellido = viajero["Nombre"] + " " + viajero["Apellido"]

            ind = reporte[0].index(nombre_apellido) # camilo , pedro , 0
            if promedio > valor : # debe compensar
                acum = valor + 1 # se suma 1 por el offset del -1 
                for i in range(1,len(reporte)) :
                    acum += reporte[i][ind]
                self.assertEqual(round(promedio,5),round(acum,5))
            else : # debe ser compensado
                acum = 1 # se suma 1 por el offset del -1 
                for i in range(1,len(reporte)) :
                    acum += reporte[i][ind]
                # se revisa que el viajero no haya tenido que compensar
                self.assertEqual(0,round(acum,5))                
                for i in range(1,len(reporte)):
                    if nombre_apellido == reporte[i][0]:
                        ind_fil =  i # encontramos donde esta el viajero en las filas
                        break
                acum = valor -1
                for i in range(1,len(reporte)):
                    acum-=reporte[ind_fil][i]
                self.assertEqual(round(promedio,5),round(acum,5))

