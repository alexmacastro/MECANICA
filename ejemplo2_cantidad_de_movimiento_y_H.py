# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:44:02 2017

@author: Alejandro Martínez Castro

MECANICA PARA INGENIEROS. Curso 2017-2018. Grado en Ingeniería Civil

         Alejandro E. Martínez Castro (amcastro@ugr.es),
         Germán Rodríguez Salido,
         Rafael Muñoz Beltrán,
         Gracia Rodríguez Jerónimo,
         Juan José Granados Romera.

Departamento de Mecánica de Estructuras e Ingeniería Hidráulica.
Universidad de Granada

Python 3.6

Dinámica de sistemas de partículas
Semana 11

Licencia de Creative Commons Reconocimiento-NoComercial 4.0 Internacional.
Ejemplo cantidad movimiento y H
"""

import numpy as np

m1 = 1
m2 = 2
m3 = 3

r1 = np.array([1,2,1])
r2 = np.array([0,2,2])
r3 = np.array([1,2,3])

v1 = np.array([1,0,0])
v2 = np.array([0,2,0])
v3 = np.array([0,0,1])

masa = m1 + m2 + m3

rg = (m1*r1 + m2*r2 + m3*r3)/masa

vg = (m1*v1 + m2*v2 + m3*v3)/masa

print ("centro de masas: ",rg)
print ("velocidad G:", vg)

#==============================================================================
# Cantidad de movimiento
#==============================================================================
vecp = m1*v1 + m2 * v2 + m3*v3

print ("Cantidad de movimiento", vecp)

#==============================================================================
# Con el centro de masas
#==============================================================================

vecp2 = masa * vg

print ("Cantidad de movimiento del centro de masas", vecp2)


#==============================================================================
# Momento cinético en el origen
#==============================================================================

H0 = np.cross(r1,m1*v1) + np.cross(r2,m2*v2) + np.cross(r3,m3*v3)
print ("Momento H0", H0)

H0_g = np.cross(rg,masa*vg)

print ("H0_G", H0_g)

print ("El momento cinético no es igual al que se obtendría intuitivamente")