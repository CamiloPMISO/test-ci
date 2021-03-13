# -*- coding: utf-8 -*-

import unittest
import re
from datetime import date
from faker import Faker
import random


from src.modelo.actividad import Actividad
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session
from src.logica.cuentas_claras import Cuentas_claras

class Crear_Actividad_test_case(unittest.TestCase):


    def setUp(self):
        '''Crea una colección para hacer las pruebas'''
        self.cuentas_claras = Cuentas_claras()

        '''Abre la sesión'''
        self.session = Session()

        self.data_factory = Faker()

        Faker.seed(1000)

        # crear actividades random 

        self.actividades = []

        for _ in range(10):
            actividad = Actividad(self.data_factory.unique.name())
            self.actividades.append(actividad)

        self.session.close()

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
        actividades = self.cuentas_claras.dar_actividad_por_id(2)
        self.assertIsNot(actividades,0)


    def test_agregar_actividad_con_exito(self):
        """Validar que se agregue actividad nueva"""
        rand_act1 = self.actividades[0]

        res1 = self.cuentas_claras.agregar_actividad(rand_act1.dar_nombre())

        actividad1 = self.session.query(Actividad).filter(Actividad.nombre==rand_act1.dar_nombre()).first()
        nombre_actividad = actividad1.dar_nombre()

        self.assertIsNotNone(actividad1)
        self.assertTrue(res1)
        self.assertEqual(nombre_actividad, rand_act1.dar_nombre())


    def test_actividad_duplicada(self):
        """Validar que no se agregue actividad cuando este ya exista"""
        rand_act1 = self.actividades[0]

        self.cuentas_claras.agregar_actividad(rand_act1.dar_nombre())

        res = self.cuentas_claras.agregar_actividad(rand_act1.dar_nombre())

        self.assertIsNone(res)
