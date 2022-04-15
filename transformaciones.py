# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:46:44 2022

@author: damian
"""

import math
import numpy as np
#%%

def rotateZ(cosAngle, sinAngle):
    _rotation = np.identity(4)

    _rotation[0, 0] = cosAngle
    _rotation[0, 1] = -sinAngle
    _rotation[1, 0] = sinAngle
    _rotation[1, 1] = cosAngle

    return _rotation

def rotateX(cosAngle, sinAngle):
    _rotation = np.identity(4)

    _rotation[1, 1] = cosAngle
    _rotation[1, 2] = -sinAngle
    _rotation[2, 1] = sinAngle
    _rotation[2, 2] = cosAngle

    return _rotation


#%%
def norma2(vector):
    return np.sqrt(np.sum(vector**2))

def traslacionPlaniferio(vector):
    _traslacion = np.identity(4)
    return _traslacion

def transformacionEsferaXUp2PlanisferioZUP(transformacionGeneral):
    rotacionGral = np.identity(4)
    traslacion = np.array([transformacionGeneral[3,0], transformacionGeneral[3,1], transformacionGeneral[3,2]])
    for i in range(2):
        for j in range(3):
            rotacionGral[i,j]=transformacionGeneral[i,j]
        
    #rotaciones 
    rotacion = np.dot(rotateZ(cosAngle=-sThetaN,sinAngle=cThetaN),rotacion)
    rotacion = np.dot(rotateX(cosAngle=sPhiN,sinAngle=-cPhiN),rotacion)
        
    anguloLatitud = math.asin(sPhi)
    anguloLongitud = math.asin(sTheta)

    traslacionLatitud = semiejeMenor * anguloLatitud
    traslacionLongitud = semiejeMayor * anguloLongitud
    
    #Cambiar a sistema Z-up, "Y" norte, "X" oeste
    
    _transformacion = np.transpose(rotacion)
    _transformacion[3,0] = traslacionLongitud
    _transformacion[3,1] = traslacionLatitud
    _transformacion[3,2] = 1
    
    return _transformacion

#%%
#wgs84
semiejeMayor = 6378137.0
semiejeMenor = 6356752.31424

traslacion = np.array([2739735.055245, -4476943.731842, -3611192.317842])

transformacion = np.identity(4)
transformacion[3,0] = traslacion[0]
transformacion[3,1] = traslacion[1]
transformacion[3,2] = traslacion[2]



#%%
##Angulos
vE = traslacion
xyE = np.array([vE[0], vE[1]]) 
cTheta = vE[0]/norma2(xyE)
sTheta = vE[1]/norma2(xyE)
cPhi = norma2(xyE)/norma2(vE)
sPhi = vE[2]/norma2(vE)

xN = (semiejeMenor/semiejeMayor)*cPhi*cTheta
yN = (semiejeMenor/semiejeMayor)*cPhi*sTheta
zN = (semiejeMayor/semiejeMenor)*sPhi

normal = np.array([xN, yN, zN])

norma2Nxy = math.abs((semiejeMenor/semiejeMayor)*cPhi)

cThetaN = cTheta
sThetaN = sTheta
cPhiN = norma2Nxy/norma2(normal)
sPhiN = normal[2]/norma2(normal)


#%%
# =============================================================================
# Calcular matices de rotacion para orientatr los B3DM
# =============================================================================
trans = transformacionEsferaXUp2PlanisferioZUP(transformacion)

print(trans)