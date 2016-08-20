# *******************************************************************************
# Author: Sriram Sankaranarayanan
# File: Cov_Scenario.py
# Institution: Johns Hopkins University
# Contact: ssankar5@jhu.edu

# All rights reserved.
# You are free to distribute this code for non-profit purposes
# as long as this header is kept intact
# *******************************************************************************

import numpy as np
from Py_Nangam import *


T = np.genfromtxt('T_testvals.csv',delimiter=',')

useless = np.concatenate((
        np.arange(1729),
        np.arange(3367,9100),
        np.arange(9191,10164),
        np.arange(11046,11487)
        ))

def clean_x(xstar):
    cleanx = xstar.copy()
    useless = np.concatenate((
        np.arange(1729),
        np.arange(3367,9100),
        np.arange(9191,10164),
        np.arange(11046,11487)
        ))
    return np.delete(xstar, useless)

(vdf,
    vDemSlope,vDemInt,
    vCostP,vCostQ,vCostG,vCostA,
    vPIXP,vPIXA,
    vLossP,vLossA,
    vpos) = StochPy2Gams(posit=1)

fi = open("G2Py.gpy")
xstar = np.zeros(Number_of_Variables)
for i in np.arange(Number_of_Variables):
    xstar[i] = fi.readline()

fi.close()
del fi

cx = clean_x(xstar)
StochA = StochGams2Py()

Tt = T.copy()
Tt = T_svds.T.copy()
Tt = np.delete(Tt,useless,0)

# Covariance Matrix 1 with all having a coefficient of variation vari
vari = 0.1 # Std dev is 10% of the mean
(d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qay,Xay,CAPay,PIay,
                PIcy,positions)          = varPy2Gams(xstar,posit = True)

vdf         =   (vari*df)**2
vDemSlope   =   (vari*DemSlope)**2
vDemInt     =   (vari*DemInt)**2
vCostP      =   (vari*CostP)**2
vCostQ      =   (vari*CostQ)**2
vCostG      =   (vari*CostG)**2
vCostA      =   (vari*CostA)**2
vPIXP       =   (vari*PIXP)**2
vPIXA       =   (vari*PIXA)**2
vLossP      =   (vari*LossP)**2
vLossA      =   (vari*LossA)**2

C1p = np.diag(np.concatenate((
    vdf.flatten(),
    vDemSlope.flatten(),
    vDemInt.flatten(),
    vCostP.flatten(),
    vCostQ.flatten(),
    vCostG.flatten(),
    vCostA.flatten(),
    vPIXP.flatten(),
    vPIXA.flatten(),
    vLossP.flatten(),
    vLossA.flatten()
    )))

C1v = Tt.dot(C1p).dot(Tt.T)
cC1v = clean_final_covariance(C1v)
np.savetxt('cC1v.csv', cC1v,delimiter=',')

def corr2cov(correl, sd):
    sd = sd.reshape(sd.size,1)
    return correl*(sd.T)*sd


# Scenario 1: Uncertainty in Texas (US7) Production cost (linear)
# No uncertainty in 2010 and 2015.
# 5% uncertainty n 2020, 3.33% additional uncertainty in every period there on.
# Correlation of 50% between adjacent periods, 40% between alternate periods, 30% with 2 period gap and so on, floored at 0
# Initializing zeros for deterministic parameters
vdf         =   (df)*0
vDemSlope   =   (DemSlope)*0
vDemInt     =   (DemInt)*0
vCostP      =   (CostP)*0
vCostQ      =   (CostQ)*0
vCostG      =   (CostG)*0
vCostA      =   (CostA)*0
vPIXP       =   (PIXP)*0
vPIXA       =   (PIXA)*0
vLossP      =   (LossP)*0
vLossA      =   (LossA)*0
C2p = np.diag(np.concatenate((
    vdf.flatten(),
    vDemSlope.flatten(),
    vDemInt.flatten(),
    vCostP.flatten(),
    vCostQ.flatten(),
    vCostG.flatten(),
    vCostA.flatten(),
    vPIXP.flatten(),
    vPIXA.flatten(),
    vLossP.flatten(),
    vLossA.flatten()
    )))

c_pos = 427

StochA = StochGams2Py()
# CostP for Texas starts from c_pos+7*10 to c_pos + 7*11
sd = np.array([
    0,        # 2010
    0,        # 2015
    0.05,     # 2020
    0.0833,   # 2025
    0.1166,   # 2030
    0.1499,   # 2035
    0.1833    # 2040
    ])*StochA[c_pos+70:c_pos+77]


vartemp = np.diag(sd)
corrmat = np.zeros(vartemp.shape)
for i in np.arange(7):
    for j in np.arange(7):
        if i==j:
            corrmat[i,j] = 1
        else:
            corrmat[i,j] = max(0,0.6 - np.abs(i-j)*0.1)

vartemp = corr2cov(corrmat,sd)
C2p[c_pos+70:c_pos+77,c_pos+70:c_pos+77] = vartemp
C2v = Tt.dot(C2p).dot(Tt.T)
v_Qpy = C2v[1638:1729,1638:1729]
v_PIcy = C2v[3052:,3052:]
v_Flow = C2v[1729:2170,1729:2170]


# Scenario 2: Uncertainty in Mexico Demand 
# No uncertainty in 2010 and 2015.
# Production costs 10% standard deviation in Mexico, and 50% correlation between Mexican production costs in 2020
# 2% additional standard deviation every period there after

# Initializing zeros for deterministic parameters
vdf         =   (df)*0
vDemSlope   =   (DemSlope)*0
vDemInt     =   (DemInt)*0
vCostP      =   (CostP)*0
vCostQ      =   (CostQ)*0
vCostG      =   (CostG)*0
vCostA      =   (CostA)*0
vPIXP       =   (PIXP)*0
vPIXA       =   (PIXA)*0
vLossP      =   (LossP)*0
vLossA      =   (LossA)*0
C3p = np.diag(np.concatenate((
    vdf.flatten(),
    vDemSlope.flatten(),
    vDemInt.flatten(),
    vCostP.flatten(),
    vCostQ.flatten(),
    vCostG.flatten(),
    vCostA.flatten(),
    vPIXP.flatten(),
    vPIXA.flatten(),
    vLossP.flatten(),
    vLossA.flatten()
    )))

# Now calibrating the Variance for Mexico ie Nodes (3+1) to (7+1) (5 nodes * 7 years)- 35 x 35 Matrix
sd = np.array([
        0,        # 2010
        0,        # 2015
        0.01,     # 2020
        0.01,     # 2025
        0.01,     # 2030
        0.01,     # 2035
        0.01      # 2040
    ])*DemInt[7,:]

# sd = (np.repeat(sd, 5,0)*DemInt[3:8,:]).flatten()

C3p[126+7*7 : 126+8*7, 126+7*7:126+8*7] = np.diag(sd*sd)

C3v = Tt.dot(C3p).dot(Tt.T)

v_Qpy3 = C3v[1638:1729,1638:1729]
v_PIcy = C3v[3052:,3052:]
v_Flow = C3v[1729:2170,1729:2170]

np.sqrt(np.diag(v_Qpy3).reshape(13,7))

a=3
C4p =  np.diag(np.concatenate((
    vdf.flatten(),
    vDemSlope.flatten(),
    vDemInt.flatten(),
    vCostP.flatten(),
    vCostQ.flatten(),
    vCostG.flatten(),
    vCostA.flatten(),
    vPIXP.flatten(),
    vPIXA.flatten(),
    vLossP.flatten(),
    vLossA.flatten()
    )))

sd = np.array([
        0,        # 2010
        0,        # 2015
        0.01,     # 2020
        0.01,     # 2025
        0.01,     # 2030
        0.01,     # 2035
        0.01      # 2040
    ])*DemInt[a,:]

C4p[126+a*7 : 126+(a+1)*7, 126+a*7:126+(a+1)*7] = np.diag(sd*sd)
C4v = Tt.dot(C4p).dot(Tt.T)
v_Qpy4 = C3v[1638:1729,1638:1729]
np.sqrt(np.diag(v_Qpy4).reshape(13,7))


