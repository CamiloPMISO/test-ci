# -*- coding: utf-8 -*-

import unittest
from faker import Faker
import random

from src.modelo.viajero import Viajero
from src.modelo.actividad_viajero import ActividadViajero
from src.modelo.gasto import Gasto
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

        # crear nombres y apellidos random invalidos

        self.nombres_invalidos= []

        for _ in range(10):
            self.nombres_invalidos.append(self.data_factory.bothify(text='#?#?##?',letters='!"#$%&/()='))

        # crear viajeros random 

        self.viajeros = []

        for _ in range(10):
            viajero = Viajero(self.data_factory.unique.first_name(),self.data_factory.unique.last_name())
            self.viajeros.append(viajero)

        self.session.close()

    def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos los viajeros'''
        viajeros = self.session.query(Viajero).all()

        '''Borra todos los viajeros'''
        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

    def test_validar_campos_nombre_apellidos_solo_alfabetico_viajero(self):
        """Validar que tanto el campo del nombre como del apellido no tengan carácteres especiales"""
        
        res1 = self.cuentas_claras.agregar_viajero(random.choice(self.nombres_invalidos),random.choice(self.nombres_invalidos))
        res2 = self.cuentas_claras.agregar_viajero(self.data_factory.unique.first_name(),random.choice(self.nombres_invalidos))
        res3 = self.cuentas_claras.agregar_viajero(random.choice(self.nombres_invalidos),self.data_factory.unique.last_name())

        self.assertIsNone(res1)
        self.assertIsNone(res2)
        self.assertIsNone(res3)
    
    def test_validar_campos_nombre_apellidos_no_nulos_viajero(self):
        """Validar que tanto el campo del nombre como del apellido no estén vacios"""
        res1 = self.cuentas_claras.agregar_viajero("","")
        res2 = self.cuentas_claras.agregar_viajero(self.data_factory.unique.first_name(),"")
        res3 = self.cuentas_claras.agregar_viajero("",self.data_factory.unique.last_name())

        self.assertIsNone(res1)
        self.assertIsNone(res2)
        self.assertIsNone(res3)

    def test_agregar_viajero_con_exito(self):
        """Validar agregar viajero con éxito"""
        rand_viajero1 = self.viajeros[0]
        rand_viajero2 = self.viajeros[1]
        res1 = self.cuentas_claras.agregar_viajero(rand_viajero1.dar_nombre(),rand_viajero1.dar_apellido())
        self.cuentas_claras.agregar_viajero(rand_viajero2.dar_nombre(),rand_viajero2.dar_apellido())
        
        viajero1 = self.session.query(Viajero).filter(Viajero.nombre==rand_viajero1.dar_nombre(),Viajero.apellido==rand_viajero1.dar_apellido()).first()
        viajero2 = self.session.query(Viajero).filter(Viajero.id == 2).first()
        
        self.assertTrue(res1)
        self.assertIsNotNone(viajero1)
        self.assertEqual(viajero1.dar_nombre(),rand_viajero1.dar_nombre())
        self.assertEqual(viajero1.dar_apellido(),rand_viajero1.dar_apellido())
        self.assertIsNotNone(viajero2)

    def test_no_agregar_viajero_duplicado(self):
        """Validar que no se agregue viajero cuando este ya exista"""
        rand_viajero3 = self.viajeros[2]
        self.cuentas_claras.agregar_viajero(rand_viajero3.dar_nombre(),rand_viajero3.dar_apellido())
        res = self.cuentas_claras.agregar_viajero(rand_viajero3.dar_nombre(),rand_viajero3.dar_apellido())
        
        self.assertIsNone(res)
        
        

