# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: Oligopoly6.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************

import numpy as np
import numpy.matlib
import sparse
from NumStochComp import *
import shelve

#Globals


def Prod():
    return 14

def Cons():
    return 17

def Node():
    return 17

def Years():
    return 8

def infinity():
    return 1e9

# Data in ProdNode.GMS

ProdNode = np.array([1,2,3,3,5,8,10,11,12,13,14,15,16,17])-1
ConsNode = np.arange(17)
Arcs = sparse.coo_array((Node(),Node()))
Arcs.positions = np.array([
    [0,15],
    [1,8],
    [1,9],
    [1,10],
    [1,11],
    [1,13],
    [2,1],
    [2,11],
    [2,13],
    [2,15],
    [2,16],
    [3,16],
    [4,7],
    [4,14],
    [6,5],
    [7,6],
    [8,1],
    [8,9],
    [9,1],
    [9,8],
    [9,10],
    [9,11],
    [9,12],
    [10,1],
    [10,9],
    [10,11],
    [10,12],
    [10,13],
    [11,1],
    [11,9],
    [11,10],
    [11,12],
    [11,14],
    [11,15],
    [12,9],
    [12,10],
    [12,11],
    [12,13],
    [12,14],
    [13,1],
    [13,10],
    [13,11],
    [13,12],
    [13,14],
    [13,15],
    [14,4],
    [14,11],
    [14,12],
    [14,13],
    [14,15],
    [15,2],
    [15,3],
    [15,11],
    [15,13],
    [15,14],
    [15,16],
    [16,2],
    [16,3],
    [16,10],
    [16,11],
    [16,12],
    [16,13],
    [16,15],
    ])
Arcs.values = np.ones(Arcs.positions.shape[0])


# Parameter definitions
DemSlope = np.array([
    [9.910,   9.832,   9.701,   9.628,   9.485,   9.363,   9.279,   9.173],
    [9.791,   9.713,   8.582,   9.509,   9.366,   9.244,   9.160,   9.054],
    [9.709,   9.631,   9.500,   9.427,   9.285,   9.162,   9.078,   8.972],
    [9.662,   9.583,   9.452,   9.380,   9.237,   9.115,   9.031,   8.925],
    [9.554,   9.475,   9.344,   9.272,   9.129,   9.007,   8.923,   8.816],
    [9.461,   9.382,   9.251,   9.179,   5.036,   8.914,   8.830,   8.723],
    [9.284,   9.205,   9.074,   9.002,   8.859,   8.737,   8.653,   8.546],
    [8.554,   8.475,   10.344,  8.272,   8.129,   10.007,  8.923,   7.816],
    [8.662,   8.583,   10.452,  8.380,   8.237,   10.115,  9.031,   7.925],
    [9.284,   9.205,   9.074,   9.002,   8.859,   8.737,   8.653,   8.546],
    [9.461,   9.382,   7.251,   9.179,   9.036,   8.914,   8.830,   8.723],
    [9.662,   9.583,   9.452,   9.380,   9.237,   9.115,   7.031,   8.925],
    [9.554,   9.475,   9.344,   9.272,   9.129,   9.007,   8.923,   8.816],
    [9.910,   9.832,   9.701,   9.628,   9.485,   9.363,   11.79,   9.173],
    [9.791,   9.713,   9.582,   9.509,   9.366,   9.244,   9.160,   9.054],
    [8.554,   8.475,   10.344,  8.272,   8.129,   10.007,  8.923,   7.816],
    [9.709,   9.631,   9.500,   9.427,   9.285,   9.162,   9.078,   8.972]
    ])
DemInt = np.array([
    [99.641,  97.465,  102.073, 101.392, 98.443,  101.370, 97.237,  96.352],
    [100.617, 98.442,  103.049, 102.368, 99.420,  102.346, 98.213,  97.329],
    [100.792, 98.616,  103.224, 102.542, 99.594,  102.520, 98.387,  97.503],
    [94.250,  92.075,  96.682,  96.001,  93.053,  95.979,  91.846,  90.961],
    [102.246, 100.070, 104.678, 103.997, 101.048, 103.975, 99.842,  98.957],
    [94.260,  92.085,  96.692,  96.011,  93.063,  95.989,  91.856,  90.972],
    [99.073,  96.897,  101.505, 100.824, 97.875,  100.801, 96.668,  95.784],
    [100.617, 98.442,  103.049, 102.368, 99.420,  102.346, 98.213,  97.329],
    [100.792, 98.616,  103.224, 102.542, 99.594,  102.520, 98.387,  97.503],
    [99.073,  96.897,  101.505, 100.824, 97.875,  100.801, 96.668,  95.784],
    [94.250,  92.075,  96.682,  96.001,  93.053,  95.979,  91.846,  90.961],
    [100.792, 98.616,  103.224, 102.542, 99.594,  102.520, 98.387,  97.503],
    [100.617, 98.442,  103.049, 102.368, 99.420,  102.346, 98.213,  97.329],
    [94.260,  92.085,  96.692,  96.011,  93.063,  95.989,  91.856,  90.972],
    [102.246, 100.070, 104.678, 103.997, 101.048, 103.975, 99.842,  98.957],
    [99.641,  97.465,  102.073, 101.392, 98.443,  101.370, 97.237,  96.352],
    [100.617, 98.442,  103.049, 102.368, 99.420,  102.346, 98.213,  97.329]
    ])

df = np.ones(Years())
for i in np.arange(1,Years()):
    df[i] = df[i-1]*0.95


CostP = np.zeros((Prod(),Years()))
CostP[:,0]=np.array([20,20,20,20,25,25,45,45,50,45,45,18,45,50])
for i in np.arange(1,Years()):
    CostP[:,i]=CostP[:,i-1].copy()

CostQ = np.zeros((Prod(),Years()))+0.1
CostG = np.zeros((Prod(),Years()))+10

LossP = np.zeros((Prod(),Years()))
LossA = np.zeros((Arcs.size(),Years()))

Qp0 = np.zeros(Prod()) + 100
Qa0 = np.array([0.01,20.00,88.00,35.00,1.00,1.00,130.00,139.00,139.00,156.00,
                52.00,17.00,20.00,24.00,19.00,45.00,6.00,12.00,3.00,85.00,
                13.00,13.00,68.00,105.00,61.00,27.00,78.00,16.00,2.00,61.00,3
                60.00,10.00,25.00,58.00,241.00,46.00,262.00,6.00,11.00,2.00,
                262.00,411.00,390.00,12.00,108.00,72.00,237.00,852.00,552.00,137.00,
                2.00,7.00,191.00,209.00,105.00,306.00,1.00,23.00,2.00,97.00,
                5.00,77.00,78.00])

PIXP = np.zeros((Prod(),Years())) + 2
PIXA = np.zeros((Arcs.size(),Years()))+3


CostA = np.zeros((Arcs.size(),Years()))
for i in np.arange(Arcs.size()):
     CostA[i,0] = 0.2

CostA = np.zeros((Arcs.size(),Years()))
CostA[:,0] = np.array([60.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,10.00,20.00,10.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00])

# Inflation
for i in np.arange(Years()-1):
    PIXP[:,i+1] = PIXP[:,i] + 0.5
    PIXA[:,i+1] = PIXA[:,i] + 0.3

Number_of_Variables = Years()*(Prod()*6 + Prod()*(Node()+Cons()+Arcs.size()) + Arcs.size()*6 + Cons())
Number_of_Parameters = Years()*(2*Cons()+5*Prod()+3*Arcs.size()+1)
del(i,j)


###############
## FUNCTIONS ##
###############

def varPy2Gams(x,posit = 0):
    x = x.flatten()
    temp = x.copy()
    positions = np.array([0],dtype='int16')
    count = 0
    d1      =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    d2      =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    d3      =   np.array(temp[0:Prod()*Node()*Years()]).reshape(Prod(),Node(),Years())
    temp    =   temp[Prod()*Node()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    d4      =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()*Node()
    positions = np.concatenate((positions,[count]))
    #
    Qpcny   =   np.array(temp[0:Prod()*Cons()*Years()]).reshape(Prod(),Cons(),Years())
    temp    =   temp[Prod()*Cons()*Years():]
    count = count + Prod()*Cons()*Years()
    positions = np.concatenate((positions,[count]))
    #
    Xpy     =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    Qpay    =   np.array(temp[0:Prod()*Arcs.size()*Years()]).reshape(Prod(),Arcs.size(),Years())
    temp    =   temp[Prod()*Arcs.size()*Years():]
    count = count + Prod()*Years()*Arcs.size()
    positions = np.concatenate((positions,[count]))
    #
    Qpy     =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    CAPpy   =   np.array(temp[0:Prod()*Years()]).reshape(Prod(),Years())
    temp    =   temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    # Transport
    d5      =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    d6      =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    Qay     =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    Xay     =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    CAPay   =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    PIay    =   np.array(temp[0:Arcs.size()*Years()]).reshape(Arcs.size(),Years())
    temp    =   temp[Arcs.size()*Years():]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    #Consumer
    PIcy    =   np.array(temp[0:Cons()*Years()]).reshape(Cons(),Years())
    # Return
    if(posit):
        return (d1, d2, d3, d4, Qpcny, Xpy, Qpay, Qpy, CAPpy, d5, d6, Qay, Xay, CAPay, PIay, PIcy,positions)
    else:
        return (d1, d2, d3, d4, Qpcny, Xpy, Qpay, Qpy, CAPpy, d5, d6, Qay, Xay, CAPay, PIay, PIcy)

def varGams2py(d1,d2,d3,d4,Qpcny,Qpsny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qsny,Xsy,CAPsy,PIsy,d7,d8,Qay,Xay,CAPay,PIay,PIcy):
    x = np.concatenate((
            d1.flatten(),d2.flatten(),d3.flatten(),d4.flatten(),
            Qpcny.flatten(),Xpy.flatten(),Qpay.flatten(),Qpy.flatten(),CAPpy.flatten(),
            d5.flatten(),d6.flatten(),
            Qay.flatten(),Xay.flatten(),CAPay.flatten(),PIay.flatten(),
            PIcy.flatten()
        ))
    return x


def StochPy2Gams(StochA = None,posit = 0):
    if (StochA is None):
         StochA = np.zeros(Number_of_Parameters)
    # a = a.flatten()
    temp = StochA.copy()
    positions = np.array([0],dtype='int16')
    count = 0
    #
    adf = np.array(temp[0:Years()]).reshape((Years(),))
    temp = temp[Years():]
    count = count + Years()
    positions = np.concatenate((positions,[count]))
    #
    aDemSlope = np.array(temp[0:Cons()*Years()]).reshape((Cons(),Years()))
    temp = temp[Cons()*Years():]
    count = count + Cons()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aDemInt   = np.array(temp[0:Cons()*Years()]).reshape((Cons(),Years()))
    temp = temp[Cons()*Years():]
    count = count + Cons()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aCostP    = np.array(temp[0:Years()*Prod()]).reshape((Prod(),Years()))
    temp = temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aCostQ    = np.array(temp[0:Years()*Prod()]).reshape((Prod(),Years()))
    temp = temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aCostG    = np.array(temp[0:Years()*Prod()]).reshape((Prod(),Years()))
    temp = temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aCostA    = np.array(temp[0:Years()*Arcs.size()]).reshape((Arcs.size(),Years()))
    temp = temp[Arcs.size()*Years(): ]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aPIXP     = np.array(temp[0:Years()*Prod()]).reshape((Prod(),Years()))
    temp = temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aPIXA     = np.array(temp[0:Years()*Arcs.size()]).reshape((Arcs.size(),Years()))
    temp = temp[Arcs.size()*Years(): ]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aLossP    = np.array(temp[0:Years()*Prod()]).reshape((Prod(),Years()))
    temp = temp[Prod()*Years():]
    count = count + Prod()*Years()
    positions = np.concatenate((positions,[count]))
    #
    aLossA    = np.array(temp[0:Years()*Arcs.size()]).reshape((Arcs.size(),Years()))
    temp = temp[Arcs.size()*Years(): ]
    count = count + Arcs.size()*Years()
    positions = np.concatenate((positions,[count]))
    if posit:
        return (adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,aCostA,aPIXP,aPIXA,aLossP,aLossA,positions)
    else:
        return (adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,aCostA,aPIXP,aPIXA,aLossP,aLossA)



def F(x,a=None):
    (d1,d2,d3,d4,Qpcny,Xpy,Qpay,Qpy,CAPpy,
            d5,d6,Qay,Xay,CAPay,PIay,
            PIcy)                            = varPy2Gams(x)
    if np.any(a is None):
        a = np.zeros(Number_of_Parameters)
    (adf, aDemSlope, aDemInt, aCostP, aCostQ, aCostG, aCostA, aPIXP, aPIXA, aLossP, aLossA) = StochPy2Gams(a)
    e1_2a   =   E1_2a(CAPpy, Qpy)
    e1_2b   =   E1_2b(CAPpy, Qp0, Xpy)
    e1_2c   =   E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
    e1_2d   =   E1_2d(Qpcny, Qpy,LossP+aLossP)
    e1_3a   =   E1_3a(df+adf, PIcy, d3, d4)
    e1_3b   =   E1_3b(df+adf,PIXP+aPIXP, d2)
    e1_3c   =   E1_3c(df+adf,PIay, d3, LossA+aLossA)
    e1_3d   =   E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
    e1_3e   =   E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
    e1_6a   =   E1_6a(CAPay, Qay)
    e1_6b   =   E1_6b(CAPay, Qa0, Xay)
    e1_7a   =   E1_7a(df+adf,PIay, CostA+aCostA, d5)
    e1_7b   =   E1_7b(df+adf,PIXA+aPIXA, d6)
    e1_7c   =   E1_7c(d5, d6)
    e1_8    =   E1_8(Qay, Qpay)
    e1_9    =   E1_9(PIcy, DemInt+aDemInt, DemSlope+aDemSlope, Qpcny)
    return np.concatenate((
            e1_2a.flatten(),
            e1_2b.flatten(),
            e1_2c.flatten(),
            e1_2d.flatten(),
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

def VecNumGrad(F,x,a=None, epsilon = epsilon(), diff = 0, Fx = None):
    if(Fx is None):
        Fx = F(x,a)
    Fx = Fx.flatten()
    (adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,
        aCostA,aPIXP,aPIXA,aLossP,aLossA,aposit) = StochPy2Gams(a,posit = 1)
    N = x.size
    (e1_2a,e1_2b,e1_2c,e1_2d,
    e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,
    e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9,positions)                 = varPy2Gams(Fx,posit = True)
    Grad = sp.sparse.dok_matrix((N,N))
    for i in np.arange(N):
        dFx = Fx.copy()
        delta = np.zeros(x.shape)
        delta[i] = epsilon
        (d1,d2,d3,d4,Qpcny,Xpy,Qpay,Qpy,CAPpy,
            d5,d6,Qay,Xay,CAPay,PIay,
            PIcy)          = varPy2Gams(x + delta)
        # Conditionals
        if(i<positions[1]): #d1
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[2]): #d2
            e1_3b = E1_3b(df+adf,PIXP+aPIXP, d2)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[3]): #d3
            e1_3a = E1_3a(df+adf,PIcy, d3, d4)
            e1_3c = E1_3c(df+adf,PIay, d3, LossA+aLossA)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
        elif(i<positions[4]): #d4
            e1_3a = E1_3a(df+adf,PIcy, d3, d4)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
        elif(i<positions[5]): #Qpcny
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_2d = E1_2d(Qpcny, Qpy, LossP+aLossP)
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope+aDemSlope, Qpcny)
        elif(i<positions[6]): #Xpy
            e1_2b = E1_2b(CAPpy, Qp0, Xpy)
        elif(i<positions[7]): #Qpay
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_8 = E1_8(Qay, Qpay)
        elif(i<positions[8]): #Qpy
            e1_2a = E1_2a(CAPpy, Qpy)
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
            e1_2d = E1_2d(Qpcny, Qpy, LossP+aLossP)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[9]):  #CAPpy
            e1_2a = E1_2a(CAPpy, Qpy)
            e1_2b = E1_2b(CAPpy, Qp0, Xpy)
            e1_3d = E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
            e1_3e = E1_3e(df+adf,d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<positions[10]): #d5
            e1_7a = E1_7a(df+adf,PIay, CostA+aCostA, d5)
            e1_7c = E1_7c(d5, d6)
        elif(i<positions[11]): #d6
            e1_7b = E1_7b(df+adf,PIXA+aPIXA, d6)
            e1_7c = E1_7c(d5, d6)
        elif(i<positions[12]): #Qay
            e1_6a = E1_6a(CAPay, Qay)
            e1_8 = E1_8(Qay, Qpay)
        elif(i<positions[13]): #Xay
            e1_6b = E1_6b(CAPay, Qa0, Xay)
        elif(i<positions[14]): #CAPay
            e1_6a = E1_6a(CAPay, Qay)
            e1_6b = E1_6b(CAPay, Qa0, Xay)
        elif(i<positions[15]): #PIay
            e1_3c = E1_3c(df+adf,PIay, d3, LossA+aLossA)
            e1_7a = E1_7a(df+adf,PIay, CostA+aCostA, d5)
        elif (i< N): #PIcy
            e1_3a = E1_3a(df+adf,PIcy, d3, d4)
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope+aDemSlope, Qpcny)
        dFx = np.concatenate((
            e1_2a.flatten(),
            e1_2b.flatten(),
            e1_2c.flatten(),
            e1_2d.flatten(),
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
    (e1_2a,e1_2b,e1_2c,e1_2d,
    e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,
    e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9,positions)                 = varPy2Gams(Fx,posit = True)
    Na = a.size
    Nx = x.size
    (d1,d2,d3,d4,Qpcny,Xpy,Qpay,Qpy,CAPpy,
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
            e1_3a = E1_3a(df+adf, PIcy, d3, d4)
            e1_3b = E1_3b(df+adf, PIXP, d2)
            e1_3c = E1_3c(df+adf, PIay, d3, LossA)
            e1_3d = E1_3d(df+adf, CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, d4, LossP)
            e1_3e = E1_3e(df+adf, d2, d1, CostG, Qpy, CAPpy)
            e1_7a = E1_7a(df+adf, PIay, CostA, d5)
            e1_7b = E1_7b(df+adf, PIXA, d6)
        elif(i<aposit[2]):  # aDemSlope
            e1_9 = E1_9(PIcy, DemInt, DemSlope+aDemSlope, Qpcny)
        elif(i<aposit[3]):  # aDemInt
            e1_9 = E1_9(PIcy, DemInt+aDemInt, DemSlope, Qpcny)
        elif(i<aposit[4]):  # aCostP
            e1_3d = E1_3d(df,CostP+aCostP, CostQ, CostG, Qpy, CAPpy, d1, d3, d4, LossP)
        elif(i<aposit[5]):  # aCostQ
            e1_3d = E1_3d(df,CostP, CostQ+aCostQ, CostG, Qpy, CAPpy, d1, d3, d4, LossP)
        elif(i<aposit[6]):  # aCostG
            e1_3d = E1_3d(df,CostP, CostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, d4, LossP)
            e1_3e = E1_3e(df, d2, d1, CostG+aCostG, Qpy, CAPpy)
        elif(i<aposit[7]):  # aCostA
            e1_7a = E1_7a(df,PIay, CostA+aCostA, d5)
        elif(i<aposit[8]):  # aPIXP
            e1_3b = E1_3b(df,PIXP+aPIXP, d2)
        elif(i<aposit[9]):  # aPIXA
            e1_7b = E1_7b(df,PIXA+aPIXA, d6)
        elif(i<aposit[10]): # LossP
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA)
            e1_2d = E1_2d(Qpcny, Qpy, LossP+aLossP)
            e1_3d = E1_3d(df,CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, d4, LossP+aLossP)
        else:               # LossA
            e1_2c = E1_2c(Qpcny, Qpay, Qpy, LossP, LossA+aLossA)
            e1_3c = E1_3c(df,PIay, d3, LossA+aLossA)
        dFx = np.concatenate((
            e1_2a.flatten(),
            e1_2b.flatten(),
            e1_2c.flatten(),
            e1_2d.flatten(),
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


def freevar():
    ff  = np.concatenate((
            # Producer
            np.zeros((Prod(),Years())).flatten(),                    #E1_2a
            np.ones((Prod(),Years())).flatten(),                     #E1_2b
            np.ones((Prod(),Node(),Years())).flatten(),              #E1_2c
            np.ones((Prod(),Years())).flatten(),                     #E1_2d
            np.zeros((Prod(),Cons(),Years())).flatten(),             #E1_3a
            np.zeros((Prod(),Years())).flatten(),                    #E1_3b
            np.zeros((Prod(),Arcs.size(),Years())).flatten(),        #E1_3c
            np.zeros((Prod(),Years())).flatten(),                    #E1_3d
            np.zeros((Prod(),Years())).flatten(),                    #E1_3e
            # Pipelines
            np.zeros((Arcs.size(),Years())).flatten(),               #E1_6a
            np.ones((Arcs.size(),Years())).flatten(),                #E1_6b
            np.zeros((Arcs.size(),Years())).flatten(),               #E1_7a
            np.zeros((Arcs.size(),Years())).flatten(),               #E1_7b
            np.zeros((Arcs.size(),Years())).flatten(),               #E1_7c
            np.ones((Arcs.size(),Years())).flatten(),                #E1_8
            # Consumer
            np.ones((Cons(),Years())).flatten()                      #E1_9
            ))
    return np.where(ff)[0]



#Equation definitions
def E1_2a(CAPpy,Qpy): #Dual d1(P,Y)
    return CAPpy-Qpy

def E1_2b(CAPpy, Qp0, Xpy): #Dual d2(P,Y)
    return CAPpy - np.matlib.repmat(Qp0, Years(), 1).T - np.cumsum(Xpy,1)

def E1_2c(Qpcny, Qpay,Qpy,LossP,LossA): #Dual d3(P,N,Y)
    e1_2c = np.zeros((Prod(),Node(),Years()))
    for i in np.arange(Node()):
        temp = np.where(ConsNode==i)[0]
        t1 = np.sum(Qpcny[:,temp,:],1)
        # Pipeline masses
        temp = np.where(Arcs.positions[:,0]==i)[0]
        t2 = np.sum(Qpay[:,temp,:],axis=1)
        temp = np.where(Arcs.positions[:,1]==i)[0]
        t3 = np.sum(Qpay[:,temp,:]*(1-LossA[temp,:]),axis=1)
        # Total Prod()
        temp = np.where(ProdNode==i)[0]
        t4 = np.zeros((Prod(),Years()))
        t4[temp,:] = Qpy[temp,:]
        e1_2c[:,i,:] = t1+t2-t3-t4*(1-LossP)
    return e1_2c

def E1_2d(Qpcny,Qpy,LossP): #Dual d4(P,Y)
    t1 = np.sum(Qpcny,1)
    t2 = Qpy*(1-LossP)
    return t1-t2

def E1_3a(df, PIcy,d3,d4): #Dual Qpcny(P,C,Y)
    t1 = np.zeros((Prod(),Cons(),Years()))
    t1[:,:,:] = -PIcy
    t2 = d3[:,ConsNode,:]
    t3 = np.zeros((Prod(),Cons(),Years()))
    for i in np.arange(Cons()):
        t3[:,i,:] = d4
    return df*t1+t2+t3

def E1_3b(df,PIXP,d2): #Dual Xpy(P,Y)
    return (df*PIXP - np.cumsum(d2,axis = 1))

def E1_3c(df,PIay,d3,LossA): # Dual Qpay(P,A,Y)
    t1 = np.zeros((Prod(),Arcs.size(),Years()))
    t1[:,:,:] = PIay
    t2 = np.zeros((Prod(),Arcs.size(),Years()))
    for i in np.arange(Arcs.size()):
        t2[:,i,:] = d3[:,Arcs.positions[i,0],:] - d3[:,Arcs.positions[i,1],:]*(1-LossA[i,:])
    return (df*t1 + t2)

def E1_3d(df,CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, d4, LossP): #Dual Qpy(P,Y)
    t2 = 2*CostQ*Qpy
    t3 = CostG*(CAPpy-Qpy)*np.log(1-(Qpy/(CAPpy+epsilon())))
    t5 = np.zeros((Prod(),Years()))
    for i in np.arange(Prod()):
        t5[i,:] = d3[i,ProdNode[i],:]
    return df*(CostP +t2 -t3) +d1 -(t5+d4)*(1-LossP)

def E1_3e(df,d2,d1,CostG,Qpy,CAPpy):  #Dual CAPpy(P,Y)
    temp = Qpy/(CAPpy+epsilon())
    t1 = CostG*temp
    t2 = CostG*np.log(1-temp)
    return df*(t1+t2)+d2-d1

def E1_6a(CAPay,Qay): #Dual d5(A,Y)
    return (CAPay - Qay )

def E1_6b(CAPay, Qa0, Xay): #Dual d6(A,Y)
    return (CAPay - np.repeat(Qa0.reshape((Arcs.size(),1)),Years(),axis = 1) - np.cumsum(Xay,axis = 1))

def E1_7a(df,PIay,CostA,d5): #Dual Qay(A,Y)
    return (-df*PIay + CostA + d5)

def E1_7b(df,PIXA,d6): #Dual Xay(A,Y)
    return (df*PIXA - np.cumsum(d6,axis = 1))

def E1_7c(d5,d6):  #Dual CAPay(A,Y)
    return (d6-d5)

def E1_8(Qay,Qpay): #Dual PIay(A,Y)
    return Qay - np.sum(Qpay,axis = 0)

def E1_9(PIcy, DemInt, DemSlope, Qpcny): #Dual PIcy(C,Y)
    return (PIcy - DemInt + DemSlope*(np.sum(Qpcny,axis = 0)))


####################################
######## Stochasticizations ########
####################################

# Move the following files to server
#       MeritFuncs.py
#       sparse.py
#       O6out.gpy



StochA = np.zeros(Number_of_Parameters)
xstar = np.zeros(Number_of_Variables)

fi = open("O6out.gpy")
for i in np.arange(Number_of_Variables):
    xstar[i] = fi.readline()


fi.close()
del fi

Fx = F(xstar,a=StochA)

free = freevar()

# Confirming all is good
# x >= 0
temp = np.where(xstar < -tol())[0]
temp2 = np.where(1-np.array([i in free for i in temp]))[0]
if temp2.size!=0:
    print("Error - Non Free Var negative")

# Fx >= 0
if (np.any(Fx < -tol())):
    print("Error - Fx negative")

# x^TFx = 0
temp = np.where(1-np.isclose(Fx[np.where(1-np.isclose(xstar,0))],0,1e-5,1e-5))[0].copy()
temp2 = np.where(1-np.isclose(xstar,0))[0][temp].copy()
if temp2.size!=0:
    print("Error - Complementarity not maintained")

M = minFunc()
FB = MeritFuncs.FischerBurmeister()

# This should be zero
f(xstar,Fx, free=free)

# Splits
(d1,d2,d3,d4,Qpcny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qay,Xay,CAPay,PIay,
                PIcy)          = varPy2Gams(xstar)
(e1_2a,e1_2b,e1_2c,e1_2d,e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9,positions)                 = varPy2Gams(Fx,posit = True)


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
saveVars = ['Gx','G','H','gP','gPT','Jx','J_Phi','fJ','T','Phix']

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





















