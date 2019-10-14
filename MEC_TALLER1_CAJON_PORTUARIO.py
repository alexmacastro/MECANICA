# -*- coding: utf-8 -*-
"""
MECANICA PARA INGENIEROS. Curso 2018-2019. Grado en Ingeniería Civil

+ Alejandro E. Martínez Castro (Desarrollador principal, email:amcastro@ugr.es).
+ Germán Rodríguez Salido.
+ Manuel Chiachío Ruano
+ Rafael Bravo Pareja.
+ Rafael Muñoz Beltrán. 
+ Gracia Rodríguez Jerónimo.

Departamento de Mecánica de Estructuras e Ingeniería Hidráulica.
Universidad de Granada

Python 3.6

Taller 1. Cajón Portuario. 

(Utilizar este fichero dentro de Spyder)

Licencia de Creative Commons Reconocimiento-NoComercial 4.0 Internacional.
"""

import numpy as np

np.set_printoptions(suppress=True) # Elimina números muy pequeños
np.set_printoptions(precision=6)  # Para mostrar 6 cifras decimales

#==============================================================================
# Definición de la clase "Punto3D". Coordenadas (x, y, z) de un punto en 3D
#==============================================================================


class Punto3D:
    """ Clase para representar los puntos, coordenadas x, y """
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y 
        self.z = z
    def coords(self):
        return "({0}, {1},{2})".format(self.x, self.y, self.z)

    
class Prisma: 
    """ Prisma centro, a,b,altura, densidad"""
    def __init__(self, centro = Punto3D(), a = 0, b=0, h=0, rho=0):
        self.centro = centro # Se definirá un objeto de tipo Punto3D
        self.a = a
        self.b = b
        self.h = h
        self.rho = rho
        
    def masa(self): # Peso del prisma
        return self.a * self.b * self.h * self.rho

    def Ixg (self): # Momento de inercia respecto al eje x en CG
        return 1./12 * self.masa() * (self.h**2  + self.b**2 )
    
    def Iyg (self): # Momento de inercia respecto al eje y en CG
        return 1./12 * self.masa() * (self.h**2  + self.a**2 )
    
    def Izg (self): # Momento de inercia respecto al eje z en CG
        return 1./12 * self.masa() * (self.a**2  + self.b**2 )


#==============================================================================
# Paso 1: Listas con coordenadas x,y centros de los huecos
#==============================================================================



centrox = np.linspace(0.5 + 4.4/2, 37.95-0.5-4.4/2,8)
centroy = np.linspace(0.5 + 4.4/2, 19.35-0.5-4.4/2,4)

print("Coordenadas x de centros de huecos")
print(centrox)
print()
print("Coordenadas y de centros de huecos")
print(centroy)

#==============================================================================
# Paso 2: Parámetros geométricos
#==============================================================================
hc = 0.9 # Canto de la losa
hf = 16 # Altura de fustes
hl1 = 2 # Altura de lastre en zona 1
hl2 = 3 # Altura de lastre en zona 2
rho_h = 2.5 # Densidad hormigón, en toneladas / m3
rho_l = 1.8 # Densidad del material de lastre, en toneladas / m3

#==============================================================================
# Paso 3: Generación de losa de fondo
#==============================================================================

centro_losa = Punto3D (37.95/2, 19.35/2, -hc/2)

losa = Prisma(centro_losa, 37.95, (19.35+0.35*2), hc, rho_h)

#==============================================================================
# Paso 4: Generación del prisma del cajón sin huecos
#==============================================================================
centro_cajon = Punto3D (37.95/2, 19.35/2, hf/2)

cajon = Prisma(centro_cajon, 37.95, 19.35, hf, rho_h)

#==============================================================================
# Paso 5: Masa y centro de gravedad del cajón lastrado
#==============================================================================

# Cálculo de la masa del cajón sin descontar los huecos

masa = losa.masa() + cajon.masa()

# Generación de vectores de numpy para centros de losa y cajón
# se aprovecha así la capacidad de bucles automáticos de arrays de numpy

c_losa = np.array([losa.centro.x, losa.centro.y, losa.centro.z])
c_cajon = np.array([cajon.centro.x, cajon.centro.y, cajon.centro.z])

# Generación de vector con los momentos estáticos

# En una sola línea se vectoriza para las tres componentes
mestatico = c_losa * losa.masa() + c_cajon * cajon.masa()


# Se descuentan las celdas huecas

icelda = 0
for cx in centrox:
    for cy in centroy:
        print ("Procesando celda",icelda+1)
        centro_celda = Punto3D(cx,cy,hf/2)
        celda = Prisma(centro_celda, 4.4, 4.4, hf, rho_h)
        masa -= celda.masa()
 
        c_celda = np.array([celda.centro.x, celda.centro.y, celda.centro.z])
        mestatico -= c_celda * celda.masa()
        
        icelda += 1

print ("Se añaden celdas lastradas de la izquierda, altura hl1")
# Se añaden las celdas lastradasicelda = 0
icelda = 0
for cx in centrox[0:4]:
    for cy in centroy:
        print ("Procesando celda lastrada con hl1",icelda+1)
        centro_celda_lastre = Punto3D(cx,cy,hl1/2)
        celda = Prisma(centro_celda_lastre, 4.4, 4.4, hl1, rho_l)
        masa += celda.masa()
 
        c_celda_lastre = np.array([celda.centro.x, celda.centro.y, celda.centro.z])
        mestatico += c_celda_lastre * celda.masa()
        
        icelda += 1

print ("Se añaden celdas lastradas de la derecha, altura hl2")
# Se añaden celdas de la derecha, lastradas con hl2 
icelda -=1
for cx in centrox[4:8]:
    for cy in centroy:
        print ("Procesando celda lastrada con hl2",icelda+1)
        centro_celda_lastre = Punto3D(cx,cy,hl2/2)
        celda = Prisma(centro_celda_lastre, 4.4, 4.4, hl2, rho_l)
        masa += celda.masa()
 
        c_celda_lastre = np.array([celda.centro.x, celda.centro.y, celda.centro.z])
        mestatico += c_celda_lastre * celda.masa()
        
        icelda += 1

print ("Propiedades másicas")
print ("Masa total (Toneladas) = ", masa)
centro_gravedad = mestatico / masa
print ("Centro de gravedad (m)", centro_gravedad)

cgx, cgy, cgz = (centro_gravedad[0],centro_gravedad[1],centro_gravedad[2])



#==============================================================================
# Paso 6: Tensor de inercia en el centro de gravedad
#==============================================================================

# LOSA DEL CAJÓN
#    Traslación de los momentos de inercia al centro de gravedad, por Steiner
print ("Calculando momentos de inercia del cajón en el centro de gravedad")

print ("Primero de la losa de cimentación")
Ixg = losa.Ixg() + losa.masa()*( (losa.centro.y-cgy)**2 + (losa.centro.z-cgz)**2)
Iyg = losa.Iyg() + losa.masa()*( (losa.centro.x-cgx)**2 + (losa.centro.z-cgz)**2)
Izg = losa.Izg() + losa.masa()*( (losa.centro.x-cgx)**2 + (losa.centro.y-cgy)**2)

# Traslación de los productos de inercia. 
# El prisma, respecto de su centro de gravedad, tiene nulos los productos de inercia
Pxyg = losa.masa()*( (losa.centro.y-cgy) * (losa.centro.z-cgz))
Pxzg = losa.masa()*( (losa.centro.x-cgx) * (losa.centro.z-cgz))
Pyzg = losa.masa()*( (losa.centro.x-cgx) * (losa.centro.y-cgy))

# FUSTES, SIN DESCONTAR LOS HUECOS
print ("Segundo, de los fustes, sin descontar huecos")
Ixg += cajon.Ixg() + cajon.masa()*( (cajon.centro.y-cgy)**2 + (cajon.centro.z-cgz)**2)
Iyg += cajon.Iyg() + cajon.masa()*( (cajon.centro.x-cgx)**2 + (cajon.centro.z-cgz)**2)
Izg += cajon.Izg() + cajon.masa()*( (cajon.centro.x-cgx)**2 + (cajon.centro.y-cgy)**2)

Pxyg += cajon.masa()*( (cajon.centro.y-cgy) * (cajon.centro.z-cgz))
Pxzg += cajon.masa()*( (cajon.centro.x-cgx) * (cajon.centro.z-cgz))
Pyzg += cajon.masa()*( (cajon.centro.x-cgx) * (cajon.centro.y-cgy))

# FUSTES, DESCONTANDO HUECOS
print ("Control, Ixg  ", Ixg)
print ("Tercero, descontando los huecos")

icelda = 0
for cx in centrox:
    for cy in centroy:
        print ("Procesando celda",icelda+1)
        centro_celda = Punto3D(cx,cy,hf/2)
        celda = Prisma(centro_celda, 4.4, 4.4, hf, rho_h)
        
        Ixg -= celda.Ixg() + celda.masa()*( (celda.centro.y-cgy)**2 + (celda.centro.z-cgz)**2)
        Iyg -= celda.Iyg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.z-cgz)**2)
        Izg -= celda.Izg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.y-cgy)**2)
 
        Pxyg -= celda.masa()*( (celda.centro.y-cgy) * (celda.centro.z-cgz))
        Pxzg -= celda.masa()*( (celda.centro.x-cgx) * (celda.centro.z-cgz))
        Pyzg -= celda.masa()*( (celda.centro.x-cgx) * (celda.centro.y-cgy))
        
        icelda += 1

print ("Control, Ixg  ", Ixg)
print ("Cuarto, añadiendo lastre en zona izquierda, hl1")

icelda = 0
for cx in centrox[0:4]:
    for cy in centroy:
        print ("Procesando celda lastrada con hl1",icelda+1)
        centro_celda_lastre = Punto3D(cx,cy,hl1/2)
        celda = Prisma(centro_celda_lastre, 4.4, 4.4, hl1, rho_l)
        
        Ixg += celda.Ixg() + celda.masa()*( (celda.centro.y-cgy)**2 + (celda.centro.z-cgz)**2)
        Iyg += celda.Iyg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.z-cgz)**2)
        Izg += celda.Izg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.y-cgy)**2)
 
        Pxyg += celda.masa()*( (celda.centro.y-cgy) * (celda.centro.z-cgz))
        Pxzg += celda.masa()*( (celda.centro.x-cgx) * (celda.centro.z-cgz))
        Pyzg += celda.masa()*( (celda.centro.x-cgx) * (celda.centro.y-cgy))
        
        icelda += 1

print ("Se añaden celdas lastradas de la derecha, altura hl2")
# Se añaden celdas de la derecha, lastradas con hl2 
icelda -=1
for cx in centrox[4:8]:
    for cy in centroy:
        print ("Procesando celda lastrada con hl2",icelda+1)
        centro_celda_lastre = Punto3D(cx,cy,hl2/2)
        celda = Prisma(centro_celda_lastre, 4.4, 4.4, hl2, rho_l)

        Ixg += celda.Ixg() + celda.masa()*( (celda.centro.y-cgy)**2 + (celda.centro.z-cgz)**2)
        Iyg += celda.Iyg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.z-cgz)**2)
        Izg += celda.Izg() + celda.masa()*( (celda.centro.x-cgx)**2 + (celda.centro.y-cgy)**2)
 
        Pxyg += celda.masa()*( (celda.centro.y-cgy) * (celda.centro.z-cgz))
        Pxzg += celda.masa()*( (celda.centro.x-cgx) * (celda.centro.z-cgz))
        Pyzg += celda.masa()*( (celda.centro.x-cgx) * (celda.centro.y-cgy))
        
        icelda += 1
        
print ()
print ()
print ("============================================")
print ("MASA TOTAL                                ")
print ("Masa total (Toneladas) = ", masa)
print ("Centro de gravedad (m)", centro_gravedad)
print ()
print ("============================================")
print (" TENSOR DE INERCIA EN EL CENTRO DE GRAVEDAD ")
print ("Ixg (T·m2) = ",Ixg)
print ("Iyg (T·m2) = ",Iyg)
print ("Izg (T·m2) = ",Izg)
print ("Pxyg (T·m2) = ",Pxyg)
print ("Pxzg (T·m2) = ",Pxzg)
print ("Pyzg (T·m2) = ",Pyzg)

#==============================================================================
# Paso 6: Diagonalización del tensor de inercia en G
#==============================================================================
Inercia = np.array([[Ixg, -Pxyg, -Pxzg],
                    [-Pxyg, Iyg, -Pyzg],
                    [-Pxzg, -Pyzg, Izg]])
Iprin, vect = np.linalg.eig(Inercia)
print ("========================================")
print ("Momentos principales de inercia", Iprin)

print ("Matriz de paso M(B,E) ")
print (vect)

# Ordenados de mayor a menor: 

idx = Iprin.argsort()[::-1] # de menor a mayor, cambiar -1 por 1
Iprin = Iprin[idx]
vect = vect[:,idx]

print ()
print ("Valores propios  ordenados de mayor a menor")
print (Iprin)
print ("Vectores propios ordenados (por columnas)")
print (vect)


