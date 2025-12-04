import numpy as np
import math as F

def cinematica(q):
    d1 = 131.22/1000
    d4 = 63.4 /1000
    d5 = 75.05/1000
    d6 = 45.6/1000
    a2 = -110.4/1000 # -
    a3= -96/1000 # -
    
    q1 = q[0]
    q2 = q[1]
    q3 = q[2]
    q4 = q[3]
    q5 = q[4]
    q6 = q[5]
    
    q1 = q1*F.pi/180
    q2 = q2*F.pi/180
    q3 = q3*F.pi/180
    q4 = q4*F.pi/180
    q5 = q5*F.pi/180
    q6 = q6*F.pi/180
    
    A1 = np.array([
    [F.cos(q1),  0,  F.sin(q1),   0],
    [F.sin(q1),  0,  -F.cos(q1),  0],
    [   0,       1,     0,       d1],
    [   0,       0,     0,        1]
    ])
    
    A2 = np.array([
    [F.cos(q2 - F.pi/2),  -F.sin(q2 - F.pi/2),     0,     a2*F.cos(q2 - F.pi/2)],
    [F.sin(q2 - F.pi/2),  F.cos(q2 - F.pi/2),      0,     a2*F.sin(q2 - F.pi/2)],
    [   0,           0,          1,          0],
    [   0,           0,          0,          1]
    ])
    
    A3 = np.array([
    [F.cos(q3),  -F.sin(q3),     0,     a3*F.cos(q3)],
    [F.sin(q3),  F.cos(q3),      0,     a3*F.sin(q3)],
    [   0,           0,          1,          0],
    [   0,           0,          0,          1]
    ])
    
    A4 = np.array([
    [F.cos(q4 - F.pi/2),  0,  F.sin(q4 - F.pi/2),   0],
    [F.sin(q4 - F.pi/2),  0,  -F.cos(q4 - F.pi/2),  0],
    [   0,       1,     0,       d4],
    [   0,       0,     0,        1]
    ])
    
    A5 = np.array([
    [F.cos(q5 + F.pi/2),  0,  -F.sin(q5 + F.pi/2),   0],
    [F.sin(q5 + F.pi/2),  0,  F.cos(q5 + F.pi/2),    0],
    [   0,      -1,     0,        d5],
    [   0,       0,     0,         1]
    ])
    
    A6 = np.array([
    [F.cos(q6),  -F.sin(q6),     0,     0],
    [F.sin(q6),  F.cos(q6),      0,     0],
    [   0,           0,          1,     d6],
    [   0,           0,          0,     1]
    ])
    
    # Tomar vector de traslación
    A12 =  A1 @ A2
    A13 = A12 @ A3
    A14 = A13 @ A4
    A15 = A14 @ A5
    A16 = A15 @ A6
    # # DEfinir el origen Oi-1
    # O6 = A16[0:3,3]
    # O5 = A15[0:3,3]
    # O4 = A14[0:3,3]
    # O3 = A13[0:3,3]
    # O2 = A12[0:3,3]
    # O1 = A1[0:3,3]
    # # Tomar la tercera columna de las matrices Zi-1
    # Z5 = A16[0:3,2]
    # Z4 = A15[0:3,1]
    # Z3 = A14[0:3,1]
    # Z2 = A13[0:3,2]
    # Z1 = A12[0:3,2]
    # Z0 = A1[0:3,1]
    
    # J1 = np.reshape(np.cross(Z0,O6), (3,1))
    # J2 = np.reshape(np.cross(Z1,(O6-O1)), (3,1))
    # J3 = np.reshape(np.cross(Z2,(O6-O2)), (3,1))
    # J4 = np.reshape(np.cross(Z3,(O6-O3)), (3,1))
    # J5 = np.reshape(np.cross(Z4,(O6-O4)), (3,1))
    # J6 = np.reshape(np.cross(Z5,(O6-O5)), (3,1))
    # Jacob = np.block([
    #     [J1,  J2,  J3,  J4, J5, J6],
    #     [np.reshape(Z0, (3,1)),  np.reshape(Z1, (3,1)),  np.reshape(Z2, (3,1)),  np.reshape(Z3, (3,1)), np.reshape(Z4, (3,1)), np.reshape(Z5, (3,1))],
    # ])
    return A16