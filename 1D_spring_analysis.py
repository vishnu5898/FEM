# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 20:15:52 2021

@author: Vishnu
"""

import numpy as np
from spring import *


elements, nodelist, n = get_inputs() # Getting all the required inputs for assembly
count = 0
k = []
K = np.zeros((n,n))
stiffness_list = []

# Spring element is being created and global matrix is being assembled in
# while loop

while(count<len(elements)):
    k.append(SpringElement(elements[count]))
    stiffness_list.append(k[count].K)
    K = k[count].assemble(K,nodelist[count][0],nodelist[count][1])
    count += 1
    
# Boundary conditions are asked from user
    
fixed_node_list,force_lists,force_node_lists = get_boundary_conditions()

# Solving the problem

A = solve_no_dis(K,fixed_node_list,force_lists,force_node_lists)

# Displacement matrix and force matrix are return in the form of tuple




# Post processing

print("Global stiffness matrix :\n", K, "\n")
print("Displacement matrix :\n", A[0], "\n")
print("Force matrix :\n", A[1], "\n")

f = force_list(stiffness_list,A[0],nodelist)
count = 1
print("Element forces :\n")
for i in f:
    print(count," :\n\n",i,"\n")
    count += 1