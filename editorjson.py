# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:47:36 2022

@author: damian
"""

import numpy as np
import transformaciones as tr


traslacion = np.array([2739735.055245, -4476943.731842, -3611192.317842])

transformacion = np.identity(4)
transformacion[3,0] = traslacion[0]
transformacion[3,1] = traslacion[1]
transformacion[3,2] = traslacion[2]

#%%<  
# =============================================================================
# Calcular matices de rotacion para orientatr los B3DM
# =============================================================================
trRoot = tr.rotatorB3dm(transformacion,1.0002, 0.1)
print(trRoot.getTransform())

#%%
# print(
#     tr.transform2str(
#         np.transpose(
#             np.dot(
#                 tr.rotateAngleX((-34.8-90)*np.pi/180),
#                 np.dot(
#                     tr.rotateAngleZ((-90+58.5)*np.pi/180),
#                     tr.rotateAngleX(np.pi/2)
#                 )
#             )
#         )
#     )
# )