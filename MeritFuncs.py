# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: MeritFuncs.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************

# This is exclusively for class definitions
import numpy as np
import warnings
class MeritFunc(object):
    """Class for deriving various Merit Functions"""
    def __init__(self):
        pass
    def __str__(self):
        return("MeritFunc base class")
    def phi(self,a,b):
        raise NotImplementedError(self.__str__() + " Function Not Yet Implemented")
    def dphi(self,x,F, dF = None, k=-1):
        raise NotImplementedError(self.__str__() + " Derivative Not Yet Implemented")
    def ddphi(self,x,F ,dF = None, ddF = None, k = -1):
        raise NotImplementedError("Second Derivative Not Yet Implemented")
    def dphia(self,x,F,dFa):
        raise NotImplementedError("Uncertainty derivative Not Yet Implemented")

class FischerBurmeister(MeritFunc):
    """FischerBurmeister Merit Function"""
    def __init__(self):
        super(FischerBurmeister, self).__init__()
    def __str__(self):
        return("sqrt(a**2 + b**2) - a -b")
    def phi(self,a,b):
        a = np.array(a)
        b = np.array(b)
        return (np.sqrt(a**2 + b**2) - a -b)
    # dphi is not vectorized
    def dphi(self,x,F ,dF = None, k=-1,sparsed=0):
        N=dF.shape
        ans = np.zeros(N)
        if x==0 and F==0:
            return 0
            # raise ValueError("Fischer Burmeister is not differentiable at (0,0)")
        temp = np.sqrt(x**2+F**2)
        ans = F*dF/temp - dF
        if sparsed:
            ans[0,k] += x/temp-1
        else:
            ans[k] += x/temp-1
        return(ans)
    def ddphi(self,x,F ,dF = None, ddF = None, k = -1,sparsed=0):
        N = ddF.shape[0]
        if x==0 and F==0:
            return np.zeros((N,N))
            # raise ValueError("Fischer Burmeister is not differentiable at (0,0)")
        # Recurrent expressions
        t0 = np.sqrt(x**2+F**2)
        t1 = np.zeros(N)
        t1[k] = x/t0
        t2 = F/t0 * dF
        t3 = -dF
        t3[k]-=1
        D1 = np.zeros((N,N))
        D1[k,:] = -(t1+t2)/(t0**2)
        D1[k,k] += 1/t0
        D2 = np.zeros((N,N))
        D2 = ddF*F/t0
        temp = (t0*dF - F*(t1+t2))/(t0**2)
        D2 += np.outer(dF,temp)
        D3 = ddF
        return(D1+D2+D3)
    def dphia(self,x,F,dFa):
        temp= np.sqrt(x**2+F**2)
        return((F/temp-1) *dFa)

class minFunc(MeritFunc):
    """min(a,b) merit function"""
    def __init__(self):
        super(minFunc, self).__init__()
    def __str__(self):
        return ("min(a,b)")
    def phi(self,a,b):
        a = np.array(a)
        b = np.array(b)
        return (np.minimum(a,b))
    def temp(self):
        print("srir")
    # dphi is not vectorized
    def dphi(self,x,F ,dF = None, k=-1,sparsed = 0):
        if np.isclose(x,F):
           ans = np.zeros( dF.shape)
           if sparsed:
                ans[0,k] = 1
           else:
                ans[k] = 1
           ans+=dF
           return ans/2
        if x<F:
            ans = np.zeros( dF.shape)
            if sparsed:
                ans[0,k] = 1
            else:
                ans[k] = 1
        if x>F:
            ans = dF
        return ans
    def ddphi(self,x,F ,dF = None, ddF = None, k = -1):
        if x==F:
             # warnings.warn("min(a,b) is not differentiable when a=b. Problem at index ")
             ans = np.zeros(ddF.shape)
        if x<F:
            ans = np.zeros(ddF.shape)
        if x>F:
            ans = ddF
        return ans
    def dphia(self,x,F,dFa):
        return((F>x)*dFa)



# temp = FischerBurmeister()
# temp.dphi(1,2,np.array([3,4,2,4,2,5]),3)
# temp = minFunc()
# temp.dphi(1,2,np.array([3,4,2,4,2,5]),3)
# temp.dphi(12,2,np.array([3,4,2,4,2,5]),3)
# temp.dphi(2,2,np.array([3,4,2,4,2,5]),3)