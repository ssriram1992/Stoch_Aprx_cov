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
    return 13

def Cons():
    return 17

def Node():
    return 17

def Years():
    return 7

def infinity():
    return 1e9

# Data in ProdNode.GMS

ProdNode = np.array([
    1,
    2,
    3,
    5,
    8,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    ])-1
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
    [587.640,     927.568,     957.472,     705.952,     677.364,     813.059,    1093.579],
    [ 44.740,      55.853,      51.289,      43.181,      37.128,      35.452,      39.951],
    [ 22.766,      24.270,      20.580,      13.968,      13.974,      13.032,      21.451],
    [412.835,     573.533,     257.251,     152.355,     135.118,     107.779,     123.308],
    [ 80.368,      92.288,      78.358,      50.302,      49.635,      44.115,      68.282],
    [213.362,     135.306,     144.504,     127.365,      98.297,     105.552,     110.907],
    [206.920,     173.503,     191.928,     172.249,     128.703,     142.762,     170.294],
    [ 56.103,      70.815,      69.458,      65.893,      61.183,      58.957,      98.859],
    [ 71.968,      71.838,      76.707,      56.691,      58.211,      54.491,      92.256],
    [ 21.545,      22.828,      25.928,      20.806,      24.591,      18.398,      21.426],
    [ 20.454,      29.787,      27.424,      22.943,      26.772,      19.211,      24.047],
    [ 16.414,      23.400,      24.185,      18.049,      21.212,      22.095,      20.431],
    [ 43.582,      52.029,      55.920,      40.486,      40.941,      41.615,      44.302],
    [ 37.762,      50.127,      48.892,      37.412,      39.204,      37.492,      42.809],
    [ 11.422,      13.946,      14.473,      10.460,      11.888,      10.081,      11.541],
    [ 37.828,      50.189,      55.326,      37.230,      37.254,      35.828,      46.650],
    [ 20.435,      15.637,      16.255,      33.969,      34.486,      35.878,      19.522],
    ])

DemInt = np.array([
    [5260.904,    8304.141,    8571.865,    6320.109,    6064.169,    7278.993,    9790.377],
    [5742.035,    7984.687,    7940.178,    7329.964,    6541.520,    6494.517,    7589.799],
    [5582.383,    8047.817,    8032.551,    6034.117,    6519.107,    6279.892,   10558.330],
    [5730.318,    8219.812,    8595.022,    5980.642,    6642.658,    6301.067,    8354.195],
    [5770.511,    8638.337,    8584.933,    6024.302,    6493.210,    6252.546,   10422.902],
    [5482.722,    6224.279,    8228.130,    7625.213,    6892.996,    8280.008,    9622.874],
    [5381.252,    6034.147,    8086.187,    7472.622,    6745.686,    8259.725,   10779.658],
    [5286.827,    5986.282,    8025.519,    7393.420,    6583.171,    6343.725,   10637.086],
    [5977.904,    8807.461,    8714.732,    6121.790,    6613.388,    6435.328,   10791.791],
    [5692.167,    8176.636,    8156.528,    6221.096,    7888.909,    6379.773,    7607.755],
    [5956.511,    8264.041,    8157.659,    6890.320,    8371.940,    6337.309,    7611.429],
    [5749.338,    8110.575,    8612.012,    6478.208,    7653.783,    7972.552,    7507.630],
    [5844.117,    7988.324,    7981.211,    6128.768,    6507.264,    6344.904,    7616.303],
    [5933.253,    7993.706,    7956.347,    6128.768,    6507.264,    6344.904,    7616.387],
    [5749.639,    8004.029,    7839.229,    6025.006,    7206.689,    6216.265,    7489.034],
    [5754.215,    8566.830,    8899.230,    6029.226,    6481.576,    6233.385,    8626.587],
    [5746.509,    8219.548,    9081.388,    6461.168,    6633.403,    6242.151,    7551.251],
    ])

CostP = np.zeros((Prod(),Years()))
CostP[:,0]=np.array([20,20,20,25,25,45,45,50,45,45,18,45,50])
for i in np.arange(1,Years()):
    CostP[:,i]=CostP[:,i-1].copy()

CostQ = np.zeros((Prod(),Years()))+0.1
CostG = np.zeros((Prod(),Years()))+10

CostA = np.zeros((Arcs.size(),Years()))
CostA[:,0] = np.array([60.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,10.00,20.00,10.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,20.00,
                       20.00,20.00,20.00])
                       
Qa0 = np.array([0.01,20.00,88.00,35.00,1.00,1.00,130.00,139.00,139.00,156.00,
                52.00,17.00,20.00,24.00,19.00,45.00,6.00,12.00,3.00,85.00,
                13.00,13.00,68.00,105.00,61.00,27.00,78.00,16.00,2.00,61.00,
                360.00,10.00,25.00,58.00,241.00,46.00,262.00,6.00,11.00,2.00,
                262.00,411.00,390.00,12.00,108.00,72.00,237.00,852.00,552.00,137.00,
                2.00,7.00,191.00,209.00,105.00,306.00,1.00,23.00,2.00,97.00,
                5.00,77.00,78.00])*2

LossP = np.zeros((Prod(),Years()))+0.0
Qp0 = np.zeros(Prod()) + 2000

LossA = np.zeros((Arcs.size(),Years()))

PIXP = np.zeros((Prod(),Years())) + 2
PIXA = np.zeros((Arcs.size(),Years())) + 4

df = np.ones(Years())

# Inflation
for i in np.arange(Years()-1):
    PIXP[:,i+1] = PIXP[:,i] + 0.5
    PIXA[:,i+1] = PIXA[:,i] + 0.3
    CostA[:,i+1] = CostA[:,i]
    df[i+1] = df[i]*0.95
    
CostP = CostP*1.1

gol_eps = 0.01
avl = 0.7

Number_of_Variables = Years()*(Prod()*5 + Prod()*(Node()+Cons()+Arcs.size()) + Arcs.size()*6 + Cons())
Number_of_Parameters = Years()*(2*Cons()+5*Prod()+3*Arcs.size()+1)
del(i)


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
    count = count + Prod()*Node()*Years()
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
        return (d1, d2, d3, Qpcny, Xpy, Qpay, Qpy, CAPpy, d5, d6, Qay, Xay, CAPay, PIay, PIcy,positions)
    else:
        return (d1, d2, d3, Qpcny, Xpy, Qpay, Qpy, CAPpy, d5, d6, Qay, Xay, CAPay, PIay, PIcy)

def varGams2py(d1,d2,d3,Qpcny,Qpsny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qsny,Xsy,CAPsy,PIsy,d7,d8,Qay,Xay,CAPay,PIay,PIcy):
    x = np.concatenate((
            d1.flatten(),d2.flatten(),d3.flatten(),
            Qpcny.flatten(),Xpy.flatten(),Qpay.flatten(),Qpy.flatten(),CAPpy.flatten(),
            d5.flatten(),d6.flatten(),
            Qay.flatten(),Xay.flatten(),CAPay.flatten(),PIay.flatten(),
            PIcy.flatten()
        ))
    return x

def StochGams2Py(df = df,
    DemSlope = DemSlope,DemInt = DemInt,
    CostP = CostP,CostQ = CostQ,CostG = CostG,CostA = CostA,
    PIXP = PIXP,PIXA = PIXA,
    LossP = LossP,LossA = LossA):
    return np.concatenate((
            df.flatten(),
            DemSlope.flatten(),DemInt.flatten(),
            CostP.flatten(),CostQ.flatten(),CostG.flatten(),CostA.flatten(),
            PIXP.flatten(),PIXA.flatten(),
            LossP.flatten(),LossA.flatten())
        )

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
    (d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,
            d5,d6,Qay,Xay,CAPay,PIay,
            PIcy)                            = varPy2Gams(x)
    if np.any(a is None):
        a = np.zeros(Number_of_Parameters)
    (adf, aDemSlope, aDemInt, aCostP, aCostQ, aCostG, aCostA, aPIXP, aPIXA, aLossP, aLossA) = StochPy2Gams(a)
    e1_2a   =   E1_2a(CAPpy, Qpy)
    e1_2b   =   E1_2b(CAPpy, Qp0, Xpy)
    e1_2c   =   E1_2c(Qpcny, Qpay, Qpy, LossP+aLossP, LossA+aLossA)
    e1_3a   =   E1_3a(df+adf, PIcy, d3)
    e1_3b   =   E1_3b(df+adf,PIXP+aPIXP, d2)
    e1_3c   =   E1_3c(df+adf,PIay, d3, LossA+aLossA)
    e1_3d   =   E1_3d(df+adf,CostP+aCostP, CostQ+aCostQ, CostG+aCostG, Qpy, CAPpy, d1, d3, LossP+aLossP)
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


def freevar():
    ff  = np.concatenate((
            # Producer
            np.zeros((Prod(),Years())).flatten(),                    #E1_2a
            np.ones((Prod(),Years())).flatten(),                     #E1_2b
            np.ones((Prod(),Node(),Years())).flatten(),              #E1_2c
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

####################################
######## Model Definitions #########
####################################

def E1_2a(CAPpy,Qpy): #Dual d1(P,Y)
    return avl*CAPpy-Qpy

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

def E1_3a(df, PIcy,d3): #Dual Qpcny(P,C,Y)
    t1 = np.zeros((Prod(),Cons(),Years()))
    t1[:,:,:] = -PIcy
    t2 = d3[:,ConsNode,:]
    return df*t1+t2

def E1_3b(df,PIXP,d2): #Dual Xpy(P,Y)
    return (df*PIXP - np.cumsum(d2,axis = 1))

def E1_3c(df,PIay,d3,LossA): # Dual Qpay(P,A,Y)
    t1 = np.zeros((Prod(),Arcs.size(),Years()))
    t1[:,:,:] = PIay
    t2 = np.zeros((Prod(),Arcs.size(),Years()))
    for i in np.arange(Arcs.size()):
        t2[:,i,:] = d3[:,Arcs.positions[i,0],:] - d3[:,Arcs.positions[i,1],:]*(1-LossA[i,:])
    return (df*t1 + t2)

def E1_3d(df,CostP, CostQ, CostG, Qpy, CAPpy, d1, d3, LossP): #Dual Qpy(P,Y)
    t2 = 2*CostQ*Qpy
    t3 = CostG*(CAPpy-Qpy)*np.log(1-(Qpy/(CAPpy+gol_eps)))
    t5 = np.zeros((Prod(),Years()))
    for i in np.arange(Prod()):
        t5[i,:] = d3[i,ProdNode[i],:]
    return df*(CostP +t2 -t3) +d1 -(t5)*(1-LossP)

def E1_3e(df,d2,d1,CostG,Qpy,CAPpy):  #Dual CAPpy(P,Y)
    temp = Qpy/(CAPpy+gol_eps)
    t1 = CostG*temp
    t2 = CostG*np.log(1-temp)
    return df*(t1+t2)+avl*d2-d1

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
########### Calibration ############
####################################

cPfac = np.array([
    [25.61,  47.52,   49.59,   20.85,   22.89,   23.08,   27.23],
    [24.47,  35.19,   31.04,   17.15,   34.99,   30.37,   44.90],
    [0.083,  0.200,   0.474,   0.472,   0.594,   0.404,   0.398],
    [24.71,  36.49,   39.29,   20.37,   21.89,   17.98,   22.65],
    [1.986,  1.927,   6.688,   2.926,   3.256,   2.705,   2.823],
    [1.002,  0.822,   0.724,   0.594,   0.573,   0.429,   0.545],
    [12.36,  21.62,   23.08,   12.61,   13.65,   8.709,   11.73],
    [10.71,  16.83,   14.87,   10.77,   8.818,   6.385,   10.50],
    [12.30,  23.50,   20.91,   9.496,   10.13,   8.003,   10.65],
    [17.50,  23.51,   23.53,   13.88,   14.93,   13.73,   16.62],
    [0.039,  0.067,   0.056,   0.034,   0.036,   0.041,   0.052],
    [0.422,  0.530,   0.320,   0.220,   0.237,   0.193,   0.266],
    [15.50,  25.48,   24.49,   14.52,   14.79,   11.96,   13.69],
    ])


CostP = CostP*cPfac/df
CostQ = CostQ*cPfac/df

CostG[:,0] = CostG[:,0]*0.7

# P_CE
CostG[1,:] = CostG[1,:]*5.76/df/df
CostG[1,0] = CostG[1,0]*0.9

# P_CW
CostG[2,0] = CostG[2,0]*0.81*0.85
CostG[2,1] = CostG[2,1]*0.95
CostG[2,5] = CostG[2,5]*0.9
CostG[2,:] = CostG[2,:]/2.2

# P_MEX2
CostG[3,0] = CostG[3,0]*0.4
CostG[3,1] = CostG[3,1]*1.5

# P_MEX5
CostG[4,0] = CostG[4,0]*1.17

# P_US2
CostG[5,0] = CostG[5,0]*0.7
CostG[5,1] = CostG[5,1]*0.7
CostG[5,2] = CostG[5,2]*0.7
CostG[5,3] = CostG[5,3]*0.5
CostG[5,4] = CostG[5,4]*0.5
CostG[5,5] = CostG[5,5]*0.45
CostG[5,6] = CostG[5,6]*0.5

# P_US3
CostG[6,0] = CostG[6,0]/0.95
CostG[6,3] = CostG[6,3]*0.75
CostG[6,:] = CostG[6,:]*0.85*df

# P_US4
CostG[7,0] = CostG[7,0]*0.7/0.95
CostG[7,3] = CostG[7,3]*0.75

# P_US5
CostG[8,0] = CostG[8,0]*0.9
CostG[8,:] = CostG[8,:]*0.7

# P_US6
CostG[9,0] = CostG[9,0]*0.15
CostG[9,1] = CostG[9,1]*1.2
CostG[9,2] = CostG[9,2]*1.05

# P_US7
CostG[10,0] = CostG[10,0]*0.92
CostG[10,1] = CostG[10,1]*1.25
CostG[10,2] = CostG[10,2]*1.2
CostG[10,3] = CostG[10,3]*0.75
CostG[10,4] = CostG[10,4]*0.8
CostG[10,5] = CostG[10,5]*0.75
CostG[10,6] = CostG[10,6]*0.82
CostG[10,:] = CostG[10,:]/4.8

# P_US8
CostG[11,0] = CostG[11,0]*0.95
CostG[11,1] = CostG[11,1]*1.05
CostG[11,2] = CostG[11,2]*1
CostG[11,3] = CostG[11,3]*0.65
CostG[11,4] = CostG[11,4]*0.7
CostG[11,5] = CostG[11,5]*0.6
CostG[11,6] = CostG[11,6]*0.75
CostG[11,:] = CostG[11,:]/3

# P_US9
CostG[12,:] = CostG[12,:]*1.1
CostG[12,0] = CostG[12,0]*0.1

# Tariffs
CostA[np.where(Arcs.positions[:,1]==13)[0],:] = CostA[np.where(Arcs.positions[:,1]==13)[0],:]*4








