# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:17:47 2022

@author: damian
"""
import numpy as np
import matplotlib.pyplot as plt
import transformaciones as tr

# %% Vecetores 3D

traslacion_root = np.array([2739735.055245, -4476943.731842, -3611192.317842])
versor_tr_root = (traslacion_root /
                  np.linalg.norm(traslacion_root, 2)).reshape(3, 1)
traslacion_child_original = np.array([3171.794442, -4884.134495, 8419.26857])
versor_tr_child = (traslacion_child_original /
                   np.linalg.norm(traslacion_child_original, 2)).reshape(3, 1)


transf_root = tr.translation_2_transform(traslacion_root)
tr_root = tr.Rotator_b3dm(transf_root)

transf_child = tr_root.get_children_transform(
    tr.translation_2_transform(traslacion_child_original))

traslacion_child_final = np.array(
    [transf_child[3, 0], transf_child[3, 1], transf_child[3, 2]]).reshape(3, 1)
traslacion_child_final = np.dot(tr_root.get_rotation(), traslacion_child_final)
print("la traslacion final del children será: ", traslacion_child_final)



versor_norm_root = tr_root.get_normal()

# rotacion completa
versor_tr_child = np.dot(tr_root.get_rotation(), np.dot(
    tr.rotate_angle_eje_x(tr.deg2Rad(90)), versor_tr_child))
versor_norm_root = np.dot(tr_root.get_rotation(), np.dot(
    tr.rotate_angle_eje_x(tr.deg2Rad(90)), versor_norm_root))


x_r = [0, float(versor_tr_root[0])]
y_r = [0, float(versor_tr_root[1])]
z_r = [0, float(versor_tr_root[2])]

x_n = [0, float(versor_norm_root[0])]
y_n = [0, float(versor_norm_root[1])]
z_n = [0, float(versor_norm_root[2])]

x_c = [0, float(versor_tr_child[0])]
y_c = [0, float(versor_tr_child[1])]
z_c = [0, float(versor_tr_child[2])]

x_eje = [0, 0]
y_eje = [0, 0]
z_eje = [-1, 1]


# %% proyecciones

cT = np.dot(np.transpose(versor_tr_root), versor_tr_child)

# %% Graficar vectores 3D

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title("Verde: Normal, Azul: childdren translacion, Rojo: original", fontsize=14, fontweight="bold")
ax.set_xlabel("X")
plt.xlim(-1, 1)
ax.set_ylabel("Y")
plt.ylim(-1, 1)
ax.set_zlabel("Z")


ax.plot3D(x_r, y_r, z_r, 'red')
ax.plot3D(x_n, y_n, z_n, 'green')
ax.plot3D(x_c, y_c, z_c, 'blue')
#ax.plot3D(x_eje, y_eje, z_eje, 'grey')

plt.show()

