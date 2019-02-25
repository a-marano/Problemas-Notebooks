# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:49:18 2017

@author: Alejandro
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pandas: análisis de datos
# numpy: análisis matemático (matrices,...)

file2read = 'aforo1.csv'

# El fichero a leer no debe contener acentos ni caracteres que no se usen
# en inglés (ñ, ç, etc.)
# Si se genera el csv desde excel normalmente usará la coma (,) para separar decimales
# y el punto y coma (;) para separar columnas. Esto puede producir errores,
# lo mejor será remplazar las comas por puntos y los puntos y coma por comas
#     1º remplace , por .
#     2º remplace ; por , 

datos = pd.read_csv(file2read, sep=',', skiprows=[0], na_values=['-'])

# na_values=['-'] hace que pandas sepa que los guiones son datos faltantes.
# Ahora vamos a decirle a pandas que cuando falte un dato, rellene
# el hueco con el dato del día posterior o anterior.
# Este procedimiento genera algunos errores
#     1) produce días adicionales (30 de febrero, 31 de noviembre, etc)
#     2) cuando faltan muchos datos (caso de abril del último año) se
#        completa la tabla con datos puntuales que pueden ser muy diferentes
#        de los que realmente ocurren. Lo mejor en esos casos, es desechar
#        el año con datos faltantes.

datos = datos.fillna(method='bfill')
datos = datos.fillna(method='ffill')


# years es una lista que contiene los años hidrográficos contenidos
# en el fichero aforo1.csv
years = datos['Ao'].unique()


# en datos_anuales separamos los datos para todos los años contenidos en el 
# fichero en estudio.
datos_anuales = [datos[datos['Ao']==i] for i in years]
# Examine el elemento datos_anuales en el explorador de variables.


# nombre de los meses según aparecen en las columnas de datos.
meses = datos.columns[3:]

# los datos de cada año se convierten en una matriz de numpy para poder
# ordenarlos de mayor a menor
datos_array = []
for i in range(len(years)):
    matriz = np.array([datos_anuales[i][m] for m in meses])
    datos_array.append(matriz)
    
# Por último, los ordenamos de mayor a menor
datos_ordenados = []
for i in range(len(years)):
    datos_ordenados.append(np.sort(datos_array[i].ravel())[::-1])
    
    
# obtención de la media
# la solución fácil es hacer la suma de los años que queremos considerar
# y dividirlo por el número de años:
    
media = (datos_ordenados[0]+datos_ordenados[1]+datos_ordenados[2])/3

# Graficando los resultados
fig, ax = plt.subplots()
a = plt.plot(datos_ordenados[0])
b = plt.plot(datos_ordenados[1])
c = plt.plot(datos_ordenados[2])
d = plt.plot(datos_ordenados[3])
m = plt.plot(media,lw=4)
plt.xlabel(u'días')
plt.ylabel(u'$m^3/s$')
plt.show()
