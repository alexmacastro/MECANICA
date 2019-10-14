# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 07:14:27 2017

@author: alex

MECÁNICA PARA INGENIEROS

Autor: Alejandro E. Martínez Castro (amcastro@ugr.es)
"""

#==============================================================================
# Ejemplo de cálculo mediante un script (Python 3.6)
#==============================================================================

import numpy as np

a = np.array([1,2,-1])
b = np.array([-2,1,3])
c = np.cross(a,b)

print ("El producto vectorial es",c) 

modulo_a = np.linalg.norm(a)
modulo_b = np.linalg.norm(b)
pescalar = a.dot(b)
coseno = pescalar / (modulo_a * modulo_b)
alfa = np.arccos(coseno)
print ("Ángulo, en radianes",alfa)
print ("Ángulo, en grados",np.degrees(alfa)) 
