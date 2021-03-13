# -*- coding: utf-8 -*-

import unittest
import random
from faker import Faker
from datetime import datetime

from src.modelo.viajero import Viajero
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.gasto import Gasto
from src.modelo.actividad import Actividad
from src.modelo.declarative_base import Session
from src.logica.cuentas_claras import Cuentas_claras

class Listar_actividades_test_case(unittest.TestCase):

    def setUp(self):
        '''Crea una colección para hacer las pruebas'''
        self.cuentas_claras = Cuentas_claras()

        '''Abre la sesión'''
        self.session = Session()

        self.data_factory = Faker()

        Faker.seed(1000)

        # crear actividades random

        self.actividades = []

        for _ in range(2):
            actividad = Actividad(nombre=self.data_factory.text())
            self.session.add(actividad)
            self.actividades.append(actividad)
        
        # crear viajeros random
        self.viajeros = []

        for _ in range(2):
            viajero = Viajero(self.data_factory.unique.first_name(),self.data_factory.unique.last_name())
            self.session.add(viajero)
            self.viajeros.append(viajero)

        self.actividades[1].agregar_viajero_en_actividad(self.viajeros[0])
        self.actividades[1].agregar_viajero_en_actividad(self.viajeros[1])

        # crear gastos random

        self.gastos = []
        for _ in range(2):
            gasto = Gasto(concepto=self.data_factory.text(),valor=random.uniform(1, 1000),fecha_gasto= datetime.strptime(self.data_factory.date(),'%Y-%m-%d'))
            self.session.add(gasto)
            self.gastos.append(gasto)

        self.viajeros[0].agregar_gasto(self.gastos[0])
        self.viajeros[0].agregar_gasto(self.gastos[1])

        self.actividades[1].agregar_gasto(self.gastos[0])
        self.actividades[1].agregar_gasto(self.gastos[1])

        self.session.commit()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todas las actividades'''
        actividades = self.session.query(Actividad).all()

        '''Borra todas las actividades'''
        for actividad in actividades:
            self.session.delete(actividad)

        '''Consulta todos los viajeros'''
        viajeros = self.session.query(Viajero).all()

        '''Borra todos los viajeros'''
        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def test_actividad_sin_gastos(self):
        "Validar si la actividad no tiene ningún gasto devuelve una lista vacía"
        reporte_por_viajero = self.cuentas_claras.generar_reporte_por_viajeros_por_actividad(1)
        self.assertIsInstance(reporte_por_viajero,list)
        self.assertEqual(len(reporte_por_viajero),0)

    def test_viajero_sin_gasto(self):
        "Validar si un viajero de una actividad no tiene gastos, debe aparecer en la lista con gasto 0"
        reporte_por_viajero = self.cuentas_claras.generar_reporte_por_viajeros_por_actividad(2)
        nombre_apellido = self.viajeros[1].dar_nombre() + " " + self.viajeros[1].dar_apellido()
        temp_reporte = {  viajero['Nombre'] + " " + viajero['Apellido'] : viajero['Valor']  
                          for viajero in reporte_por_viajero }

        self.assertIn(nombre_apellido,temp_reporte)
        self.assertEqual(temp_reporte[nombre_apellido],0)

    def test_suma_valores(self):
        "Validar que la suma total de los gatos de los viajeros es igual a la suma total de los gastos de la actividad"
        reporte_por_viajero = self.cuentas_claras.generar_reporte_por_viajeros_por_actividad(2)
        gasto_total = 0
        gastos = self.actividades[1].dar_gastos()
        for gasto in gastos :
            gasto_total += float(gasto.dar_valor())

        gasto_total_reporte = 0
        for viajero in reporte_por_viajero :
            gasto_total_reporte += float(viajero['Valor'])

        self.assertEqual(gasto_total,gasto_total_reporte)
        
        

