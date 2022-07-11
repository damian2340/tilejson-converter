# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:46:44 2022

@author: damian
"""

import numpy as np



def deg2Rad(angle):
    return angle * np.pi / 180.0

def translation_2_transform(translation):
    transform = np.identity(4)

    transform[3, 0] = translation[0]
    transform[3, 1] = translation[1]
    transform[3, 2] = translation[2]
    return transform

def rotate_eje_z(cos_angle, sin_angle):
    _rotation = np.identity(3)

    _rotation[0, 0] = cos_angle
    _rotation[0, 1] = -sin_angle
    _rotation[1, 0] = sin_angle
    _rotation[1, 1] = cos_angle
    return _rotation

def rotate_eje_y(cos_angle, sin_angle):
    _rotation = np.identity(3)
    _rotation[0, 0] = cos_angle
    _rotation[2, 0] = -sin_angle
    _rotation[0, 2] = sin_angle
    _rotation[2, 2] = cos_angle
    return _rotation

def rotate_eje_x(cos_angle, sin_angle):
    _rotation = np.identity(3)

    _rotation[1, 1] = cos_angle
    _rotation[1, 2] = -sin_angle
    _rotation[2, 1] = sin_angle
    _rotation[2, 2] = cos_angle
    return _rotation

def rotate_angle_eje_x(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    transform = np.identity(3)

    transform[1, 1] = c
    transform[2, 1] = s
    transform[1, 2] = -s
    transform[2, 2] = c
    return transform

def rotate_angle_eje_y(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    transform = np.identity(3)

    transform[0, 0] = c
    transform[2, 0] = -s
    transform[0, 2] = s
    transform[2, 2] = c
    return transform

def rotate_angle_eje_z(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    transform = np.identity(3)

    transform[0, 0] = c
    transform[1, 0] = s
    transform[0, 1] = -s
    transform[1, 1] = c
    return transform

def norma2(vector):
    return np.linalg.norm(vector, 2)

def transform_2_str(transform):
    salida = '['
    for i in range(4):
        salida = salida + '\n'
        for j in range(4):
            salida = salida + str(transform[i, j])
            if i != 3:
                salida = salida + ', '
            else:
                if j != 3:
                    salida = salida + ', '
    salida = salida + '\n]'
    return salida

def bounding_2_str(bounding):
    salida = '['
    for i in range(12):
        salida = salida + str(bounding[i])
        if i != 11:
            salida = salida + ', '
    salida = salida + ']'
    return salida

def latLon_2_web_mercator(theta, phi):
    semiejeMayor = 6378137.0
    semiejeMenor = 6356752.31424

    f = (semiejeMayor-semiejeMenor)/semiejeMayor
    e = np.sqrt(f*(2-f))

    x = semiejeMayor * theta
    y = semiejeMayor * (np.log(np.tan(np.pi/4 + phi/2)) - (e/2)
                        * np.log((1 + e * np.sin(phi)) / (1 - e * np.sin(phi))))
    return [x, y]

# %% Clase rotador

class Rotator_b3dm: 
    def __init__(self, transform = np.ones([4,4]), scale_b3dm=1.0):
        # calculo de escalares
        self.semieje_mayor = 6378137.0
        self.semieje_menor = 6356752.31424
        self.scale = scale_b3dm
        self.f = (self.semieje_mayor-self.semieje_menor)/self.semieje_mayor
        self.e = np.sqrt(self.f*(2-self.f))
        # Vector despazamiento. Se usa para obtener la direccion y con esta la rotacion
        self.translation_original = np.array(
            [transform[3, 0], transform[3, 1], transform[3, 2]]).reshape(3, 1)

        # Se extrae la rotacion de la transformacion
        self.rotation_original = self.__transf_2_rot(transform)
        # Norma 2 de la proyección del vector desplazamiento sobre el plano XY
        norma_xy = norma2(
            np.array([self.translation_original[0, 0], self.translation_original[1, 0]]))
        # Obtención de la latitud y longitud del punto final de la traslación
        self.phi_lat = np.arctan2(self.translation_original[2, 0], norma_xy)
        self.theta = np.arctan2(
            self.translation_original[1, 0], self.translation_original[0, 0])

        # Angulo de la parmetrización del elipsoide,0
        self.phi_eli = np.arctan2(
            self.translation_original[2, 0], norma_xy*(1-self.f))

        self.c_phi_lat = np.cos(self.phi_lat)
        self.s_phi_lat = np.sin(self.phi_lat)

        self.c_phi_eli = np.cos(self.phi_eli)
        self.s_phi_eli = np.sin(self.phi_eli)

        # Aca se calcula los semiejes suponiendo que el desplazamiento es a la superficie del planeta
        self.b = self.translation_original[2, 0]/np.sin(self.phi_eli)
        self.a = self.b/(1-self.f)

        self.c_theta = self.translation_original[0, 0]/norma_xy
        self.s_theta = self.translation_original[1, 0]/norma_xy

        # Obtencion del vector normal a la superficie del planete en las coordenadas
        x_n = (1-self.f)*self.c_phi_eli*self.c_theta
        y_n = (1-self.f)*self.c_phi_eli*self.s_theta
        z_n = self.s_phi_eli

        self.normal = np.array([x_n, y_n, z_n]).reshape(3, 1)
        self.normal = self.normal/np.linalg.norm(self.normal, 2)

        norma2_xy_n = np.abs((1-self.f)*self.c_phi_eli)

        self.c_theta_n = self.c_theta
        self.s_theta_n = self.s_theta
        self.c_phi_n = norma2_xy_n/norma2(self.normal)
        self.s_phi_n = self.normal[2, 0]/norma2(self.normal)

        self.theta_n = self.theta
        self.phi_n = np.arctan2(self.normal[2, 0], norma2_xy_n)

    def get_normal(self):
        return self.normal/norma2(self.normal)

    def get_versor_n2X(self):
        return np.array([self.s_theta_n, -self.c_theta_n, 0])

    def get_versor_n2Y(self):
        return np.array([-(self.c_theta_n*self.s_phi_n), -(self.s_theta_n*self.s_phi_n), self.c_phi_n])

    def get_versor_n2Z(self):
        return np.array([self.c_theta_t * self.c_phi_t, self.s_theta_n * self.c_phi_n, self.s_phi_n])

    def get_transform(self):
        # rotar 90° para dejar el gltf en z-UP
        rotation = self.get_rotation()
        # rotation = np.dot( rotation, rotate_angle_eje_x(np.pi/2))
        rotation = rotation * self.scale
        trans = self.get_translacion_mercator()
        _transformacion = np.append(
            rotation.transpose(), trans.transpose(), axis=0).transpose()
        _transformacion = np.append(
            _transformacion, [np.array([0, 0, 0, 1])], axis=0).transpose()

        return _transformacion

    def get_children_transform(self, children_transf_org):
        rot_children_org = self.__transf_2_rot(children_transf_org)

        translation_org = np.array(
            [children_transf_org[3, 0], children_transf_org[3, 1], children_transf_org[3, 2]]).reshape(3, 1)

        rot_children = rot_children_org


        translation_children = translation_org

        children_transform = np.append(rot_children.transpose(
        ), translation_children.transpose(), axis=0).transpose()
        children_transform = np.append(
            children_transform, [np.array([0, 0, 0, 1])], axis=0).transpose()

        return children_transform


    def get_rotation(self):
        # rotaciones
        self.rotation = self.rotation_original
        # rotar alrrededor de Z para dejar la normal en el plano "-YZ"
        self.rotation = np.dot(
            rotate_eje_z(cos_angle=-self.s_theta_n, sin_angle=self.c_theta_n), self.rotation)
        # ultima rotacion, rotar alrrededor de x para dejar la normal en z+
        self.rotation = np.dot(
            rotate_eje_x(cos_angle=self.s_phi_n, sin_angle=self.c_phi_n), self.rotation)
        return self.rotation

    def get_translacion_mercator(self):
        traslacionLongitud = self.semieje_mayor * self.theta
        traslacionLatitud = self.semieje_mayor * (
            np.log(np.tan((np.pi/4) + (self.phi_n/2))) -
            (self.e/2) * np.log((1 + self.e * np.sin(self.phi_n)) /
                                (1 - self.e * np.sin(self.phi_n)))
        )
        traslacionLatitud -= 16000
        self.translation_original_mercator = np.array(
            [traslacionLongitud, traslacionLatitud, self.a-self.semieje_mayor]).reshape(3, 1)
        return self.translation_original_mercator

    def __transf_2_rot(self, transform):
        rotation = np.identity(3)
        for i in range(3):
            for j in range(3):
                rotation[i, j] = transform[j, i]
        return rotation

    def get_bounding(self, bv):
        ##elimino las rotasiones de los vectores d etamaña/direccion
        
        rotador_bv = rotate_eje_z(cos_angle = -self.s_theta_n , sin_angle = self.c_theta_n )
        rotador_bv = np.dot(rotate_eje_x(cos_angle = self.s_phi_n , sin_angle = self.c_phi_n ), rotador_bv )

        
        [vector_centro, vector_i, vector_j, vector_k] = self.get_bounding_vectors(bv)
        
        # vector_centro_r = np.dot(rotador_bv, vector_centro )
        # vector_i_r = np.array([ norma2(vector_i), 0, 0]).reshape(3,1)
        # vector_j_r = np.array([ 0, -norma2(vector_k), 0]).reshape(3,1)
        # vector_k_r = np.array([   0, 0, norma2(vector_j)]).reshape(3,1)
    
        #return np.concatenate((vector_centro_r, vector_i_r, vector_j_r, vector_k_r ), axis = None)
        return np.concatenate((vector_centro, vector_i, vector_j, vector_k ), axis = None)
        
    def get_bounding_vectors(self, bv):
        vector_centro = np.array(bv[0:3]).reshape(3, 1)
        vector_i = np.array(bv[3:6]).reshape(3, 1)
        vector_j = np.array(bv[6:9]).reshape(3, 1)
        vector_k = np.array(bv[9:12]).reshape(3, 1)
        
        return [vector_centro,vector_i, vector_j, vector_k]
    
    #simula la rotacion completa del root
    def get_rot_completa_bounding(self, bv):
        rotacion = rotate_angle_eje_x(np.pi/2)
        rotacion  = np.dot(self.get_rotation(), rotacion)
        
        [vector_centro, vector_i, vector_j, vector_k] = self.get_bounding_vectors(bv)
        
        vector_centro_r = np.dot(rotacion, vector_centro )
        vector_i_r = np.dot(rotacion, vector_i)
        vector_j_r = np.dot(rotacion, vector_j)
        vector_k_r = np.dot(rotacion, vector_k)
        
        return [vector_centro_r, vector_i_r, vector_j_r, vector_k_r]
    
