# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: NumStochComp.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************

# Numerical Stochastic Complementarity problem


import sys
import numpy as np
import scipy as sp
import scipy.sparse

# from stochcomp import *
import MeritFuncs

########################
# Constants definition
########################
def tol():
    return 1e-5

def epsilon():
    return 1e-5

def ignore_error():
    return False


#######################################
# Functions on the vector function F
#######################################

# A function that calculates the gradient of an R^m |-> R^n  function
# diff  = 0 for Central difference
#       = 1 for Forward difference
#       = -1 for Backward difference
def VecNumGrad(F,x,a = None,
                epsilon = epsilon(),
                diff = 0):
    N = x.size
    Fx = F(x,a)
    Grad = np.zeros((N,N))
    for i in range(N):
        delta = np.zeros(x.shape)
        delta[i] = epsilon
        if diff==0:
            Fx = F(x-delta,a)
        else:
            delta = delta * diff
            epsilon = epsilon * diff
        Grad[i,:] = (F(x+delta,a)-Fx)/epsilon
    return(Grad.T)


def VecNumHess(F,x, a=None,
                epsilon = 0.0001,
                diff=0):
    N = x.size
    Hess = np.zeros((N,N,N))
    Gx = VecNumGrad(F,x,a,epsilon)
    for i in range(N):
        delta = np.zeros(x.shape)
        delta[i] = epsilon
        if diff==0:
            Gx = VecNumGrad(F,x-delta,a,epsilon)
        else:
            delta = delta * diff
        Hess[:,i,:] = (VecNumGrad(F,x+delta,a,epsilon)-Gx)/epsilon
    return Hess

def VecNumRandGrad(F,x,a = None,
                    epsilon = 0.0001,
                    diff=0):
    A = a.size
    N = x.size
    Fx = F(x,a)
    Grad = np.zeros((A,N)) #It's transpose will be returned.
    for i in range(A):
        delta = np.zeros(a.shape)
        delta[i] = epsilon
        if diff==0:
            Fx = F(x,a-delta)
        else:
            delta = delta * diff
            epsilon = epsilon * diff
        Grad[i,:] = (F(x,a+delta)-Fx)/epsilon
    return(Grad.T)


# This is not required since this is always a zero at solution
def VecNumJacob(F, x, a = None,
                epsilon = 0.0001,
                diff = 0):
    pass


# What if Hessian is singular :(
def correct_singularity (H,eps =tol(),force = 0):
    N = H.shape[0]
    if force:
        H+=np.identity(N)*eps
    else:
        R = np.linalg.matrix_rank(H)
        if R<N:
            H += np.identity(N)*eps
    return (H)

#############################################
# Functions on applying the merit functions
#############################################

# Detect the points where F is zero and the dual is non-zero
# Case where both are zero raises error
def Detect_F_nonzero(x, Fx = None, tol = tol(), ignerr = ignore_error()):
    F_nonzero = np.where(abs(x)<tol)[0]
    if (not ignerr) and np.all(Fx!=None) and np.any(abs(Fx[F_nonzero]<tol)) :
        temp = np.where(abs(Fx[F_nonzero])<tol)
        temp2 = F_nonzero[temp]
        temp3 = str(list(temp2))
        raise ValueError("x, F both being zero can cause issues - Problem in indices "+ temp3)
    return F_nonzero

def f(x,Fx = None, F = None, a=None,free = np.array([]), M = MeritFuncs.minFunc()):
    Phix = Phi(x,Fx, F, a,free, M)
    return Phix.T.dot(Phix)*0.5

def Phi(x,Fx = None, F = None, a=None,free = np.array([]), M = MeritFuncs.minFunc()):
    if np.all(Fx == None):
        Fx = F(x,a)
    if free.size > 0:
        ind = np.array([(xx,Fxx,i) for i,xx,Fxx in zip(range(x.size),x,Fx) if not(i in free)])
        temp =  M.phi(ind[:,0],ind[:,1])
        t2 = np.array(list(temp) + list(Fx[free]))
    else:
        t2 = M.phi(x,Fx)
    return t2

def grad_Phi(x,Fx = None, F = None, a=None, free = np.array([]), dF = None, M = MeritFuncs.minFunc(),sparsed=0):
    J = np.zeros((x.size,x.size))
    if Fx == None:
        Fx = F(x,a)
    if dF == None:
        dF = VecNumGrad(F,x,a)
    ind = np.array([(xx,Fxx,int(i)) for i,xx,Fxx in zip(range(x.size),x,Fx) if not(i in free)])
    if free.size > 0:
        if sparsed:
            J[free,:] = dF.todense()[free,:]
        else:
            J[free,:] = dF[free,:]
    J = sp.sparse.dok_matrix(J)
    for xx,Fxx,i in ind:
        J[i,:] = M.dphi(xx,Fxx,dF=dF[int(i),:],k=i,sparsed = sparsed)
    return J

def grad_f(x,Fx = None, F = None, a=None, dF = None,Phix = None,J = None,free = np.array([]), M = MeritFuncs.minFunc()):
    if np.any(Phix==None):
        if np.all(Fx == None):
            Fx = F(x,a)
        Phix = Phi(x,Fx,free=free,M=M,a=a)
    if np.all(J == None):
        J = grad_Phi(x,Fx,F,a, free,dF,M).T
    return(J.dot(Phix))

def hess_f(x,Fx = None, F = None, a=None, dF = None, ddF =None, J = None, 
            Jtrans = None, Phix=None, free = np.array([]), M = MeritFuncs.minFunc(), sparsed = 0):
    if np.any(Phix==None):
        if np.all(Fx == None):
            Fx = F(x,a)
        Phix = Phi(x,Fx,free=free,M=M,a=a)
    if np.all(J == None):
        J = grad_Phi(x,Fx,F,a,free,dF,M)
    if np.any(Jtrans==None):
        Jtrans = J.T
    JtJ = Jtrans.dot(J)
    # if sparsed:
    #     sec = sp.sparse.dok_matrix(JtJ.shape)
    # else:
    #     sec = np.zeros(JtJ.shape)
    # if np.isscalar(ddF): #If it is an LCP, all elements of ddF are zero, just the length of xstar can be entered then
    #     pass
    # else:
    #     for i in free:
    #         ddPh = ddF[i].copy()
    #         sec = sec + ddPh*Phix[i]
    # unfree = np.array([i for i in np.arange(x.size) if not(i in free)])
    # if np.isscalar(ddF):
    #     temp = np.zeros((ddF,ddF))
    #     for i in unfree:
    #         if abs(Phix[i])>tol():
    #             ddPh = M.ddphi(x[i],Fx[i],J[i,:],temp,i)
    #             print i*100.0/unfree.size,'%  ',
    #             sys.stdout.flush()
    #             sec = sec + ddPh*Phix[i]
    # else:
    #     for i in unfree:
    #         if abs(Phix[i])>tol():
    #             ddPh = M.ddphi(x[i],Fx[i],J[i,:],ddF[i],i)
    #             print i*100.0/unfree.size,'%  ',
    #             sys.stdout.flush()
    #             sec = sec + ddPh*Phix[i]
    # return JtJ + sec
    return JtJ

def jacob_Phi(x,Fx = None, F = None, a=None, dFa = None, free = np.array([]), M = MeritFuncs.minFunc(),sparsed=0):
    if np.any(Fx==None):
        Fx = F(x)
    if np.all(dFa==None):
        dFa = VecNumRandGrad(F,x,a)
    N = x.shape
    A = a.shape
    ind = np.array([(xx,Fxx,int(i)) for i,xx,Fxx in zip(range(x.size),x,Fx) if not(i in free)])
    ans = np.zeros((x.size,a.size))
    if sparsed:
        if free.size>0:
            ans[free,:] = np.array(dFa[free,:].todense()).squeeze()
        for xx,Fxx,i in ind:
            ans[int(i),:] = M.dphia(xx,Fxx,np.array(dFa[int(i),:].todense()).squeeze())
    else:
        if free.size>0:
            ans[free,:] = dFa[free,:]
        for xx,Fxx,i in ind:
            ans[i,:] = M.dphia(xx,Fxx,dFa[i,:])
    return (ans)


def jacob_f(x,Fx = None, F = None, a=None, J_Phi=None, dF=None, dFa = None, free = np.array([]), M = MeritFuncs.minFunc()):
    if np.any(J_Phi==None):
        if np.any(Fx==None):
            Fx = F(x)
        J_Phi = jacob_Phi(x,Fx,F,a,dFa,free,M)  # N x A
    if np.any(dF==None):
        dF = grad_Phi(x,Fx,F=F,a=a,free=free,M=M)                  # N x N
    N = dF.shape[0]
    return dF.T.dot(J_Phi)


































