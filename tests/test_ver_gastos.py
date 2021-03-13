# -*- coding: utf-8 -*-

import unittest
import re
import random
from datetime import date,datetime
from faker import Faker

from src.modelo.actividad import Actividad
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from src.logica.cuentas_claras import Cuentas_claras

class Listar_gastos_test_case(unittest.TestCase):


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

        for _ in range(2):
            actividad = Actividad(nombre=self.data_factory.unique.name())
            self.session.add(actividad)
            self.actividades.append(actividad)


        # crear viajeros random
        self.viajeros = []

        for _ in range(2):
            viajero = Viajero(self.data_factory.unique.first_name(),self.data_factory.unique.last_name())
            self.session.add(viajero)
            self.viajeros.append(viajero)

        self.actividades[0].agregar_viajero_en_actividad(self.viajeros[0])
        self.actividades[0].agregar_viajero_en_actividad(self.viajeros[1])

        # crear gastos random

        self.gastos = []
        for _ in range(2):
            gasto = Gasto(concepto=self.data_factory.text(),valor=random.uniform(1, 1000),fecha_gasto= datetime.strptime(self.data_factory.date(),'%Y-%m-%d'))
            self.session.add(gasto)
            self.gastos.append(gasto)

        self.viajeros[0].agregar_gasto(self.gastos[0])
        self.viajeros[1].agregar_gasto(self.gastos[1])

        self.actividades[0].agregar_gasto(self.gastos[0])
        self.actividades[0].agregar_gasto(self.gastos[1])

        '''Persiste los objetos y cierra la sesión'''
        self.session.commit()
        self.session.close()

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

    def test_listar_gastos_caso_vacio(self):
        gastos = self.cuentas_claras.listar_gastos_actividad(2)
        self.assertIsInstance(gastos,list)
        self.assertEqual(len(gastos),0)

    def test_validar_contenido_gastos(self) :
        gastos = self.cuentas_claras.listar_gastos_actividad(1)
 
        for gasto in gastos :
            self.assertIn("Concepto", gasto)
            self.assertIn("Valor", gasto)
            self.assertIn("Nombre", gasto)
            self.assertIn("Fecha", gasto)
            self.assertIn("Apellido", gasto)

    def test_validar_tipo_info_gastos(self) :
        gastos = self.cuentas_claras.listar_gastos_actividad(1)
 
        for gasto in gastos :
            self.assertIsInstance(gasto["Concepto"], str)
            self.assertIsInstance(gasto["Valor"], float)
            self.assertIsInstance(gasto["Nombre"], str)
            self.assertIsInstance(gasto["Fecha"], str)
            self.assertIsInstance(gasto["Apellido"], str)

    def test_validar_formato_fecha_gastos(self) :
        gastos = self.cuentas_claras.listar_gastos_actividad(1)

        regex = re.compile(r'^([0-2][0-9]|(3)[0-1])(\-)(((0)[0-9])|((1)[0-2]))(\-)\d{4}$')
        
        for gasto in gastos :
            self.assertTrue(regex.match(gasto["Fecha"])) # se desea formato dd-mm-yyyy

