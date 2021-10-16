# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 20:53:20 2021

@author: Vishnu
"""

import numpy as np

'''
"SpringElement(k)" is a class which generates an object with a stiffness matrix
of k for 2 node elements. This class contains a method called "assemble(G,i,j)"
where G is the global matrix which is a square matrix. i and j are the nodes of
the corresponding elements. This method returns the value of assembled global
matrix.

Example:
    k1 = SpringElement(25)
    G = np.zeros((3,3))
    G = K1.assemble(G,1,3)

'''


class SpringElement():
    
    # Initialization of stiffness matrix
    
    def __init__(self,k):
        self.K = np.array([[ k, -k],
                           [-k,  k]])
    
    def assemble(self,G,i,j):
        
        # Error detection in node assembly
        
        if(i==j or i<0 or j<0):
            print("Error in assembly")
            return 0;
        # Assembling of corresponding stiffness matrix
        
        else:
            G[i-1][i-1] += self.K[0][0] # Gii = Gii + Kii
            G[i-1][j-1] += self.K[0][1] # Gij = Gij + Kij
            G[j-1][i-1] += self.K[1][0] # Gji = Gji + Kji
            G[j-1][j-1] += self.K[1][1] # Gjj = Gjj + Kjj
            return G

'''
This method desn't work with displacement boundary condition. Fixed boundary
condition is assumed.

"solve_no_dis(K,u,F,force_node_list)" is a function to solve the displacement and force
equations using matrix manipulation. It returns the displacement matrix and
force matrix in the form of tuple (displacement,force).

"K" is the final global matrix, "u" is the fixed boundary conditions in the form
of a list with fixed node numbers, "F" is the list of forces to be applied and
"force_node_list" is the list of nodes where forces are applied in the same
order as "F"

'''

def solve_no_dis(K,u,F,force_node_list):
    n = K.shape[0] # assigning no. of nodes to n
    temp = K # temporary storage of global matrix, as K going to change
    
    # Reducing stiffness matrix
    
    count = 0 # count is added for correct deletion of rows and columns
    for j in u:
        for k in range(0,2):
            K = np.delete(K,j-1-count,axis=k) # deleting rows or columns
        count += 1
        
    reduced_K = K # reduced stiffness matrix assignment
    K = temp # restoring the global matrix to K after manipulation
    del temp
    del j,k
    
    # Assigning boundary conditions to force matrix A
    
    A = np.zeros((n,1))
    count = 0
    for j in force_node_list:
        A[j-1][0] = F[count]
        count += 1
    del j
    
    # Reducing force matrix
    
    count = 0
    temp = A
    for j in u:
        A = np.delete(A,j-1-count,axis=0)
        count += 1
    
    reduced_F = A
    A = temp
    del temp
    del j
    
    # Solving the matrix equation to get displacement matrix
    
    inverse_K = np.linalg.inv(reduced_K)
    U_reduced = np.dot(inverse_K,reduced_F)
    
    # Combining solution to form displacement matrix
    
    for j in u:
        U_reduced = np.insert(U_reduced,j-1,0,axis=0)
    U = U_reduced
    
    # Solving force equation
    
    A = np.dot(K,U)
    
    return (U,A)

'''
"force_element(element_stiffness_matrix,U,nodelist)" is a function for finding
elemental forces corresponding to 2 nodes of the element. Its input parameters
are "stiffness_matrix of element", "U" and "nodelist". Here "U" is the global
solved displacement matrix, which is in the form of numpy array. "nodelist" is
the nodes of corresponding elements and should be in list format.

The function returns solved force matrix of the given element.

Example:
    
    f = force_element(K,U,[1,2])
    
    where 1 and 2 are nodes of element

'''

def force_element(element_stiffness_matrix,U,nodelist):
    n = element_stiffness_matrix.shape[0]
    u = np.zeros((n,1))
    for i in range(0,n):
        u[i][0] = U[nodelist[i]-1][0]
    f = np.dot(element_stiffness_matrix,u)
    return f

"""
force_list(stiffness_list,U,element_nodelist) is a function similar to
force_element() function. The differe between both the function is that
force_list() takes a collection of stiffness matrices of elements as input whereas
force_element() takes only a single stiffness matrix of an element and give result.

Also "nodelist" also has difference as above respectively

Example:
    
    force_list(G,U,nodelist)
    
    Here "G" is a collection of stiffness matrices of elements and "nodelist"
    is also a collection of nodes of different elements.
    
    Both should be given as list.
    
    G = [K1,k2,k3] where K1 is a 2 x 2 matrix
    nodelist = [[1,2],[2,3],[3,4]]
    

"""

def force_list(stiffness_list,U,element_nodelist):
    f = []
    count = 0
    while(count<len(element_nodelist)):
        f.append(force_element(stiffness_list[count],U,element_nodelist[count]))
        count += 1
    return f

"""
get_inputs() is a function which does not take any parameter. This function returns
"stiffness of elements in the form of a list", "nodes of different elements in
the form of a list" and "number of nodes". We need 3 variables to get return values
from the function.

The function gets input from the user regarding stiffnessess and nodes of
different elements.
"""

def get_inputs():
    elements = [] # 2 lists are defined to store input values from user
    nodelist = []
    n_nodes = int(input("Total no. of nodes :\n"))
    n_elements = int(input("Total no. elements:\n"))
    count = 0
    while(count<n_elements):
        print("Stiffness of element", count+1, "(in SI unit):")
        elements.append(int(input()))    
        print("Nodes of element", count+1, ": (Seperate nodes by space)")
        a = input()
        a = a.split() # The input is splitted to get list of nodes as list
        a = [int(a[0]),int(a[1])]
        nodelist.append(a)
        count += 1
    return (elements,nodelist,n_nodes)

"""
get_boundary_conditions() is a function which do not take any arguments. It
gets input from the user regarding boundary conditions to be given for the problem
to be solved.

The function returns "list of fixed nodes", "forces given" and
"the nodes of given force".

They return everything in the form of list. We need 3 variables to get return
values from the function.
"""

def get_boundary_conditions():
    zero_displacement_list = [] # 3 lists are defined to store input values
    force_list = []
    force_node_list = []
    n_fixed = int(input("Total no. of fixed boundary :"))
    count = 0
    
    # while loop is given to get inputs from user repeatedly
    
    while(count<n_fixed):
        print("Enter fixed node ", count+1, ":")
        zero_displacement_list.append(int(input()))
        count += 1
    count = 0
    n_force = int(input("Total no. of force applied :\n"))
    while(count<n_force):
        print("Enter force ", count+1, "(in Newton):")
        force_list.append(int(input()))
        print("Enter node of force", count+1, ":")
        force_node_list.append(int(input()))
        count += 1
    return (zero_displacement_list,force_list,force_node_list)
    
    
    
        
