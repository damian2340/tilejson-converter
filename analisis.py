# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 01:08:52 2022

@author: damian
"""
import numpy as np
import transformaciones as tr


#%%
#wgs84
semiejeMayor = 6378137.0
semiejeMenor = 6356752.31424

f = (semiejeMayor-semiejeMenor)/semiejeMayor


traslacion = np.array([2739735.055245, -4476943.731842, -3611192.317842])

transformacion = np.identity(4)
transformacion[3,0] = traslacion[0]
transformacion[3,1] = traslacion[1]
transformacion[3,2] = traslacion[2]



#%%
##Angulos
xyE = np.array([traslacion[0], traslacion[1]]) 
normaXYe = tr.norma2(xyE)
norma2XYZe = tr.norma2(traslacion)

phi = np.arctan2(traslacion[2],(normaXYe*(1-f)))
cPhi = np.cos(phi)
sPhi = np.sin(phi)

b = traslacion[2]/np.sin(phi)
a= b/(1-f)

cTheta = traslacion[0]/normaXYe
sTheta = traslacion[1]/normaXYe

xN = (1-f)*cPhi*cTheta
yN = (1-f)*cPhi*sTheta
zN = sPhi/(1-f)

normal = np.array([xN, yN, zN])

norma2Nxy = np.abs((1-f)*cPhi)

cThetaN = cTheta
sThetaN = sTheta
cPhiN = norma2Nxy/tr.norma2(normal)
sPhiN = normal[2]/tr.norma2(normal)

theta = np.arctan2(traslacion[1],traslacion[0])
thetaN = theta
phi = np.arcsin(sPhi)
phiN = np.arcsin(sPhiN)
print("En wgs z-up tenemos:")
print("La latitud del root \"phi\" es:", phi*180/np.pi)
print("La longitud del root \"theta\" es:", theta*180/np.pi)
print("la direccion en longitud de la normal es: ", thetaN*180/np.pi)
print("la direccion en latitud de la normal es: ", phiN*180/np.pi)
print("El semieje mayor de la tierra es de ", a/1000, "km")
print("El semieje menor de la tierra es de ", b/1000, "km")
print("la diferencia entre el semieje mayor encontrado y el wgs84 es", semiejeMayor-a)
print("la diferencia entre el semieje menor encontrado y el wgs84 es", semiejeMenor-b)
