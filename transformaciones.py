# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:46:44 2022

@author: damian
"""

import numpy as np

def translation2Transform(traslacion):
    transformacion = np.identity(4)
    transformacion[3,0] = traslacion[0]
    transformacion[3,1] = traslacion[1]
    transformacion[3,2] = traslacion[2]

    return transformacion

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

def rotateAngleX(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    
    transform = np.identity(4)
    
    transform[1,1] = c
    transform[2,1] = s
    transform[1,2] = -s
    transform[2,2] = c
    
    return transform

def rotateAngleY(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    
    transform = np.identity(4)
    
    transform[0,0] = c
    transform[2,0] = -s
    transform[0,2] = s
    transform[2,2] = c
    
    return transform

def rotateAngleZ(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    
    transform = np.identity(4)
    
    transform[0,0] = c
    transform[1,0] = s
    transform[0,1] = -s
    transform[1,1] = c
    
    return transform

def norma2(vector):
    return np.sqrt(np.sum(vector**2))

def traslacionPlaniferio(vector):
    _traslacion = np.identity(4)
    return _traslacion
#%%
class rotatorB3dm:

    def __init__(self, transform, scaleCoordMap=1.0, scaleB3dm=1.0):
        # Distancias tomadas desde wikipedia para elipsoide WGS84
        self.semiejeMayor = 6378137.0
        self.semiejeMenor = 6356752.31424
        self.scale = scaleB3dm
        self.scaleCoord = scaleCoordMap
        # achatamiento del elipsoide
        self.f = (self.semiejeMayor-self.semiejeMenor)/self.semiejeMayor
        self.e = self.f*(2-self.f)
        self.transform = np.transpose(transform)
        self.rotationPrincipal = np.identity(4)
        self.translation = np.array([transform[3,0], transform[3,1], transform[3,2]])
        for i in range(3):
            for j in range(3):
                self.rotationPrincipal[i,j] = transform[j,i]
                
        normaXYe = norma2( np.array([self.translation[0], self.translation[1]]))
 
        self.phiEli = np.arctan2(self.translation[2], normaXYe*(1-self.f) )
        self.phiLat = np.arctan2(self.translation[2], normaXYe )
        self.theta = np.arctan2(self.translation[1], self.translation[0])

        self.cPhiLat = np.cos(self.phiLat)
        self.sPhiLat = np.sin(self.phiLat)
        
        self.cPhiEli = np.cos(self.phiEli)
        self.sPhiEli = np.sin(self.phiEli)

        self.b = self.translation[2]/np.sin(self.phiEli)
        self.a= self.b/(1-self.f)

        self.cTheta = self.translation[0]/normaXYe
        self.sTheta = self.translation[1]/normaXYe

        xN = (1-self.f)*self.cPhiEli*self.cTheta
        yN = (1-self.f)*self.cPhiEli*self.sTheta
        zN = self.sPhiEli

        # Vector perpendicular a Bs As
        self.normal = np.array([xN, yN, zN])

        norma2xyN = np.abs((1-self.f)*self.cPhiEli)

        self.cThetaN = self.cTheta
        self.sThetaN = self.sTheta
        self.cPhiN = norma2xyN/norma2(self.normal)
        self.sPhiN = self.normal[2]/norma2(self.normal)

        self.thetaN = self.theta
        self.phiN = np.arctan2(self.normal[2],norma2xyN)
           
    def getTransform(self):

        #rotaciones
        self.rotation = self.rotationPrincipal
        #ultima rotacion, rotar alrrededor de x para dejar la normal en z+
        self.rotation = np.dot(rotateX(cosAngle=self.sPhiN,sinAngle=-self.cPhiN),self.rotation)
        #rotar alrrededor de Z para dejar la normal en el plano "-YZ"
        self.rotation = np.dot(rotateZ(cosAngle=-self.sThetaN,sinAngle=-self.cThetaN),self.rotation) 
        #rotar 90° para dejar el gltf en z-UP
        self.rotation = np.dot(rotateAngleX(-np.pi/2),self.rotation) 

#        self.rotation = np.dot(rotateAngleX(-np.pi/2) , self.rotation)
#        self.rotation = np.dot(rotateAngleZ(33*np.pi/180),self.rotation)
#        self.rotation = np.dot(rotateAngleX( np.pi/2 + 49.16044838886595*np.pi/180),self.rotation)
#        self.rotation = np.dot(rotateAngleZ(- np.pi/2 + 163.11144756391306*np.pi/180),self.rotation)
#        self.rotation = np.dot(rotateAngleX(np.pi/2),self.rotation)

                       
        traslacionLongitud = self.scaleCoord * self.a * self.theta
        traslacionLatitud = self.scaleCoord * self.a * ( np.log(np.tan(np.pi/4+self.phiLat/2)) - 
                            (self.e/2) * np.log((1+self.e*np.sin(self.phiLat))/(1-self.e*np.sin(self.phiLat)) ) )
        
        _transformacion = self.rotation * self.scale
        _transformacion[3,0] = traslacionLongitud
        _transformacion[3,1] = traslacionLatitud*1.0059
        _transformacion[3,2] = self.a-self.semiejeMayor
        _transformacion[3,3] = 1.0
        
        
        return transform2str(np.transpose(_transformacion))

    def getNormal(self):
        return self.normal

def transform2str(transform):
    salida = '['
    for i in range(4):
        salida = salida + '\n'
        for j in range(4):
            salida = salida + str(transform[j, i])
            if i != 3:
                salida = salida + ', '        
            else:
                if j != 3 :
                    salida = salida + ', ' 
    salida=salida + ']'
    return salida

#%%
import sys

def translacion2Transform(traslacion):
    transformacion = np.identity(4)
    transformacion[3,0] = traslacion[0]
    transformacion[3,1] = traslacion[1]
    transformacion[3,2] = traslacion[2]
    return transformacion

traslacion = [float(i) for i in sys.argv[1:4]]
trRoot = rotatorB3dm(translacion2Transform(traslacion), 1.0, 1.1175)
print(trRoot.getTransform())
# print(trRoot.getNormal())


# print(np.dot([3171.794442, -4884.134495, 8419.26857, 1.0], rotateAngleX(np.pi/2)))