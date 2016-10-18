# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: Py_Stoch.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************

import numpy as np
from Py_Nangam import *
from Py_N_derivs import *

####################################
######## Stochasticizations ########
####################################

# Move the following files to server
#       MeritFuncs.py
#       sparse.py
#       G2Py.gpy

StochA = np.zeros(Number_of_Parameters)
xstar = np.zeros(Number_of_Variables)

fi = open("G2Py.gpy")
for i in np.arange(Number_of_Variables):
    xstar[i] = fi.readline()


fi.close()
del fi

Fx = F(xstar,a=StochA)
# Splits
(d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qay,Xay,CAPay,PIay,
                PIcy,positions)          = varPy2Gams(xstar,posit = True)
(e1_2a,e1_2b,e1_2c,e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9)                 = varPy2Gams(Fx)


free = freevar()

def Allgood():
    # Confirming all is good
    # x >= 0
    temp = np.where(xstar < -tol())[0]
    temp2 = np.where(1-np.array([i in free for i in temp]))[0]
    if temp2.size!=0:
        print("Error - Non Free Var negative")
    # Fx >= 0
    temp = np.where(Fx<-tol())
    if (np.any(Fx < -tol())):
        print("Error - Fx negative")
    # x^TFx = 0
    temp = np.where(
            1-np.isclose(
                Fx[
                    np.where(1-np.isclose(xstar,0,tol(),tol()))     # Where x is not zero
                ],                  # Find Fx there
                0,
                tol(),
                tol()
            )           # Check if Fx is zero there
        )[0].copy()     # These are points where Fx is not near zero, among where x is not near zero
    temp2 = np.where(1-np.isclose(xstar,0,tol(),tol()))[0][temp].copy() # These are the points where the above error happens
    if temp2.size!=0:
        print("Error - Complementarity not maintained")

Allgood()

M = MeritFuncs.minFunc()
FB = MeritFuncs.FischerBurmeister()

# This should be zero
f(xstar,Fx, free=free)


pr = 1


Gx = VecNumGrad(F, xstar)
if pr:
    print('Gx computed')
    sys.stdout.flush()
# Run the following command only in Python 3. Not otherwise
# Hx = VecNumHess(F, xstar)

Jx = VecNumRandGrad(F,xstar,StochA)
if pr:
    print('Jx computed')
    sys.stdout.flush()
# Computations
# grad of \Phi

gP = grad_Phi(xstar,Fx,F=F,dF =Gx, free=free,sparsed = 1,M=M)
if pr:
    print('gP computed')
    sys.stdout.flush()

gP =  sp.sparse.csr_matrix(gP)
gPT = sp.sparse.csr_matrix(gP.transpose())
if pr:
    print('gPT computed')
    sys.stdout.flush()

# Grad and Hess of f = 0.5*norm(\Phi)^2
Phix = Phi(xstar,Fx,free=free,M=M,a=StochA)
if pr:
    print('Phix computed')
    sys.stdout.flush()

G = grad_f(xstar,Fx,F=F,a=StochA,Phix = Phix, dF = Gx, J=gPT,free=free,M=M)
if pr:
    print('G computed')
    sys.stdout.flush()

H = hess_f(xstar,Fx,F,StochA,dF = Gx, Phix = Phix,ddF = Number_of_Variables, J = gP, Jtrans = gPT, free=free, M=M)
H = np.array(H.todense()).squeeze()
if pr:
    print('H computed')
    sys.stdout.flush()

J_Phi = jacob_Phi(xstar,Fx,F,a=StochA,dFa=Jx,free=free,M=M,sparsed=1)
if pr:
    print('J_Phi computed')
    sys.stdout.flush()

fJ = jacob_f(xstar,Fx=Fx,F=F,a=StochA,free=free,J_Phi=J_Phi,dF = gP,M=M)
if pr:
    print('fJ computed')
    sys.stdout.flush()






Hu,Hs,Hv = np.linalg.svd(H)
np.savetxt('Hu.csv', Hu)
np.savetxt('Hs.csv', Hs)
np.savetxt('Hv.csv', Hv)
T_svd = np.zeros((Number_of_Parameters,Number_of_Variables))
# 8615 is the index of largest non-zero element in the Hs array
for i in np.arange(8615):
    sys.stdout.flush()
    print i,
    T_svd += np.outer(Hu[i,:].T.dot(fJ), Hv[i,:])/Hs[i]

np.savetxt('T_svd_full.csv', T_svd)

T_svds = T_svd.copy()
for i in np.arange(8251,8615):
    sys.stdout.flush()
    print i,    
    T_svds -= np.outer(Hu[i,:].T.dot(fJ), Hv[i,:])/Hs[i]

T_svds2 = T_svds.copy()
for i in np.arange(5850,8251):
    sys.stdout.flush()
    print i,    
    T_svds2 -= np.outer(Hu[i,:].T.dot(fJ), Hv[i,:])/Hs[i]

T_svds = T_svds.T
for i in np.arange(10873,11000):
    sys.stdout.flush()
    print i,
    T_svds += np.outer(Hu[i,:].T.dot(fJ), Hv[i,:])/Hs[i]


# import shelve
# filename = 'HandJ.out'
# saveVars = ['H','fJ']
# my_shelf = shelve.open(filename,'n') # 'n' for new
# for key in saveVars:
#     try:
#         my_shelf[key] = globals()[key]
#     except TypeError:
#         #
#         # __builtins__, my_shelf, and imported modules can not be shelved.
#         #
#         print('ERROR shelving: {0}'.format(key))

# my_shelf.close()



# H2 = correct_singularity(H,force=1)
# H_chol = np.linalg.cholesky(H)
# T = np.linalg.solve(H2, fJ)
# np.savetxt('T_solve.csv', T,delimiter=',')


# filename='./shelve.out'
# my_shelf = shelve.open(filename,'n') # 'n' for new
# saveVars = ['Gx','G','H','gP','gPT','Jx','J_Phi','fJ','T','Phix','H_chol']

# for key in saveVars:
#     try:
#         my_shelf[key] = globals()[key]
#     except TypeError:
#         #
#         # __builtins__, my_shelf, and imported modules can not be shelved.
#         #
#         print('ERROR shelving: {0}'.format(key))
# my_shelf.close()


# my_shelf = shelve.open(filename)
# for key in my_shelf:
#     globals()[key]=my_shelf[key]

# my_shelf.close()





















