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

M = MeritFuncs.minFunc()
FB = MeritFuncs.FischerBurmeister()

# This should be zero
f(xstar,Fx, free=free)


# Gradients
Gx = VecNumGrad(F, xstar)

# Run the following command only in Python 3. Not otherwise
# Hx = VecNumHess(F, xstar)
Jx = VecNumRandGrad(F,xstar,StochA)

# Computations
# grad of \Phi
gP = grad_Phi(xstar,Fx,F=F,dF =Gx, free=free,sparsed = 1,M=M)
gP =  sp.sparse.csr_matrix(gP)
gPT = sp.sparse.csr_matrix(gP.transpose())

# Grad and Hess of f = 0.5*norm(\Phi)^2
# This is some random text

Phix = Phi(xstar,Fx,free=free,M=M,a=StochA)
G = grad_f(xstar,Fx,F=F,a=StochA,Phix = Phix, dF = Gx, J=gPT,free=free,M=M)
H = hess_f(xstar,Fx,F,StochA,dF = Gx, Phix = Phix,ddF = Number_of_Variables, J = gP, Jtrans = gPT, free=free, M=M)
H = np.array(H.todense()).squeeze()

J_Phi = jacob_Phi(xstar,Fx,F,a=StochA,dFa=Jx,free=free,M=M,sparsed=1)
fJ = jacob_f(xstar,Fx=Fx,F=F,a=StochA,free=free,J_Phi=J_Phi,dF = gP,M=M)

import shelve
filename = 'HandJ.out'
saveVars = ['H','fJ']
my_shelf = shelve.open(filename,'n') # 'n' for new
for key in saveVars:
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))

my_shelf.close()

H = correct_singularity(H,force=1)
H_chol = np.linalg.cholesky(H)
T = np.linalg.solve(H, fJ)
np.savetxt('T_testvals.csv', T,delimiter=',')


filename='./shelve.out'
my_shelf = shelve.open(filename,'n') # 'n' for new
saveVars = ['Gx','G','H','gP','gPT','Jx','J_Phi','fJ','T','Phix','H_chol']

for key in saveVars:
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()


my_shelf = shelve.open(filename)
for key in my_shelf:
    globals()[key]=my_shelf[key]

my_shelf.close()





















