# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 07:20:23 2017

@author: amcastro@ugr.es

MECANICA PARA INGENIEROS. Curso 2017-2018. Grado en Ingeniería Civil

Autores: Alejandro E. Martínez Castro (amcastro@ugr.es),
         Germán Rodríguez Salido,
         Rafael Muñoz Beltrán,
         Gracia Rodríguez Jerónimo,
         Juan José Granados Romera.

Departamento de Mecánica de Estructuras e Ingeniería Hidráulica.
Universidad de Granada

Python 3.6

Ejemplo de integración de arco de una parábola (Semana 10, hilos)

Licencia de Creative Commons Reconocimiento-NoComercial 4.0 Internacional.


"""

import numpy as np

def funcion(x):
    return np.sqrt(1 + (2*x / 25)**2)

import scipy.integrate as integrate

result = integrate.quad(funcion, -15, 25)

# Integración mediante una fórmula de cuadratura
# Ver más en
# help(integrate)

print (result)

print ("Resultado de la integral: ", result[0])
print ("Estimación del error de integración: ", result[1])