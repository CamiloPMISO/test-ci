# -*- coding: utf-8 -*-

import unittest
from faker import Faker

from src.modelo.actividad import Actividad
from src.modelo.declarative_base import Session
from src.logica.cuentas_claras import Cuentas_claras

class Listar_actividades_test_case(unittest.TestCase):

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

        for _ in range(3):
            actividad = Actividad(nombre=self.data_factory.text())
            self.session.add(actividad)
            self.actividades.append(actividad)
        
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

        self.session.commit()
        self.session.close()

    def test_listar_actividades_caso_vacio(self):
        self.tearDown()
        actividades = self.cuentas_claras.listar_actividades()
        self.assertIsNone(actividades)

    def test_validar_numero_actividades(self):
        actividades = self.cuentas_claras.listar_actividades()
        self.assertEqual(len(actividades),3)

        for actividad in actividades:
            self.assertIsInstance(actividad,str)

    def test_validar_orden_actividades(self):
        actividades = self.cuentas_claras.listar_actividades()

        actividades_ordena = []

        for actividad in self.actividades :
            actividades_ordena.append(actividad.dar_nombre())

        for i, actividad in enumerate(sorted(actividades_ordena)):
            self.assertEqual(actividad,actividades[i])
        

