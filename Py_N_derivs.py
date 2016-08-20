# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: P_N_derivs.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************


def VecNumGrad(F,x,a=None, epsilon = epsilon(), diff = 0, Fx = None):
    if(Fx is None):
        Fx = F(x,a)
    Fx = Fx.flatten()
    (adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,
        aCostA,aPIXP,aPIXA,aLossP,aLossA,aposit) = StochPy2Gams(a,posit = 1)
    N = x.size
    (e1_2a,e1_2b,e1_2c,
    e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,
    e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9,positions)                 = varPy2Gams(Fx,posit = True)
    Grad = sp.sparse.dok_matrix((N,N))
    for i in np.arange(N):
        dFx = Fx.copy()
        delta = np.zeros(x.shape)
        delta[i] = epsilon
        (d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,
            d5,d6,Qay,Xay,CAPay,PIay,
            PIcy)          = varPy2Gams(x + delta)
        # Conditionals
        if(i<positions[1]): #d1
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3,  LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[2]): #d2
            e1_3b = E1_3b(df+adf,PIXP+aPIXP, d2)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[3]): #d3
            e1_3a = E1_3a(df+adf,PIcy, d3)
            e1_3c = E1_3c(df+adf,PIay, d3, LossA+aLossA)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3,  LossP+aLossP)
        elif(i<positions[4]): #Qpcny
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope+aDemSlope, Qpcny)
        elif(i<positions[5]): #Xpy
            e1_2b = E1_2b(CAPpy, Qp0, Xpy)
        elif(i<positions[6]): #Qpay
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_8 = E1_8(Qay, Qpay)
        elif(i<positions[7]): #Qpy
            e1_2a = E1_2a(CAPpy, Qpy)
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3,  LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[8]):  #CAPpy
            e1_2a = E1_2a(CAPpy, Qpy)
            e1_2b = E1_2b(CAPpy, Qp0, Xpy)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3,  LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[9]): #d5
            e1_7a = E1_7a(df+adf,PIay, CostA+aCostA, d5)
            e1_7c = E1_7c(d5, d6)
        elif(i<positions[10]): #d6
            e1_7b = E1_7b(df+adf,PIXA+aPIXA, d6)
            e1_7c = E1_7c(d5, d6)
        elif(i<positions[11]): #Qay
            e1_6a = E1_6a(CAPay, Qay)
            e1_8 = E1_8(Qay, Qpay)
        elif(i<positions[12]): #Xay
            e1_6b = E1_6b(CAPay, Qa0, Xay)
        elif(i<positions[13]): #CAPay
            e1_6a = E1_6a(CAPay, Qay)
            e1_6b = E1_6b(CAPay, Qa0, Xay)
        elif(i<positions[14]): #PIay
            e1_3c = E1_3c(df+adf,PIay, d3, LossA+aLossA)
            e1_7a = E1_7a(df+adf,PIay, CostA+aCostA, d5)
        elif (i< N): #PIcy
            e1_3a = E1_3a(df+adf,PIcy, d3)
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope+aDemSlope, Qpcny)
        dFx = np.concatenate((
            e1_2a.flatten(),
            e1_2b.flatten(),
            e1_2c.flatten(),
            e1_3a.flatten(),
            e1_3b.flatten(),
            e1_3c.flatten(),
            e1_3d.flatten(),
            e1_3e.flatten(),
            e1_6a.flatten(),
            e1_6b.flatten(),
            e1_7a.flatten(),
            e1_7b.flatten(),
            e1_7c.flatten(),
            e1_8.flatten(),
            e1_9.flatten()
            ))
        Grad[i,:] = np.around((dFx -Fx)/epsilon,5)
    # VecNumGrad.counter += 1
    # print(VecNumGrad.counter)
    return Grad.transpose()

def VecNumRandGrad(F,x,a=None, epsilon = epsilon(), diff = 0, Fx = None):
    if(Fx is None):
        Fx = F(x,a)
    Fx = Fx.flatten()
    if a is None:
        a = np.zeros(Number_of_Parameters)
    (adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,
        aCostA,aPIXP,aPIXA,aLossP,aLossA,aposit) = StochPy2Gams(a,posit = 1)
    (e1_2a,e1_2b,e1_2c,
    e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,
    e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9,positions)                 = varPy2Gams(Fx,posit = True)
    Na = a.size
    Nx = x.size
    (d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,
            d5,d6,Qay,Xay,CAPay,PIay,
            PIcy)          = varPy2Gams(x)
    Grad = sp.sparse.dok_matrix((Na,Nx))
    for i in np.arange(Na):
        dFx = Fx.copy()
        delta = np.zeros(a.shape)
        delta[i] = epsilon
        (adf,aDemSlope,aDemInt,aCostP,aCostQ,aCostG,
            aCostA,aPIXP,aPIXA,aLossP,aLossA)    = StochPy2Gams(a+delta)
        # Conditionals
        if (i<aposit[1]): #adf
            e1_3a = E1_3a(df+adf, PIcy, d3)
            e1_3b = E1_3b(df+adf, PIXP, d2)
            e1_3c = E1_3c(df+adf, PIay, d3, LossA)
            e1_3d = E1_3d(df+adf, CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, LossP)
            e1_3e = E1_3e(df+adf, d2, d1, CostG, Qpy, CAPpy)
            e1_7a = E1_7a(df+adf, PIay, CostA, d5)
            e1_7b = E1_7b(df+adf, PIXA, d6)
        elif(i<aposit[2]):  # aDemSlope
            e1_9 = E1_9(PIcy, DemInt, DemSlope+aDemSlope, Qpcny)
        elif(i<aposit[3]):  # aDemInt
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope, Qpcny)
        elif(i<aposit[4]):  # aCostP
            e1_3d = E1_3d(df,CostP+aCostP, CostQ, CostG, Qpy, CAPpy, d1, d3, LossP)
        elif(i<aposit[5]):  # aCostQ
            e1_3d = E1_3d(df,CostP, CostQ+aCostQ, CostG, Qpy, CAPpy, d1, d3, LossP)
        elif(i<aposit[6]):  # aCostG
            e1_3d = E1_3d(df,CostP, CostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, LossP)
            e1_3e = E1_3e(df, d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<aposit[7]):  # aCostA
            e1_7a = E1_7a(df,PIay, CostA+aCostA, d5)
        elif(i<aposit[8]):  # aPIXP
            e1_3b = E1_3b(df,PIXP+aPIXP, d2)
        elif(i<aposit[9]):  # aPIXA
            e1_7b = E1_7b(df,PIXA+aPIXA, d6)
        elif(i<aposit[10]): # LossP
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA)
            e1_3d = E1_3d(df,CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, LossP+aLossP)
        else:               # LossA
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP, LossA+aLossA)
            e1_3c = E1_3c(df,PIay, d3, LossA+aLossA)
        dFx = np.concatenate((
            e1_2a.flatten(),
            e1_2b.flatten(),
            e1_2c.flatten(),
            e1_3a.flatten(),
            e1_3b.flatten(),
            e1_3c.flatten(),
            e1_3d.flatten(),
            e1_3e.flatten(),
            e1_6a.flatten(),
            e1_6b.flatten(),
            e1_7a.flatten(),
            e1_7b.flatten(),
            e1_7c.flatten(),
            e1_8.flatten(),
            e1_9.flatten()
            ))
        Grad[i,:] = np.around((dFx -Fx)/epsilon,5)
    return Grad.transpose()

def VecNumHess(F,x, Gx=None,a=None,eps = epsilon(),diff = 0):
    N = x.size
    return np.zeros((N,N,N))

