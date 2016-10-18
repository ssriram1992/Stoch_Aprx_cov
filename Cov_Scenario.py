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

Hu = np.genfromtxt('Hu_Sep5.csv')
Hv = np.genfromtxt('Hv_Sep5.csv')
Hs = np.genfromtxt('Hs_Sep5.csv')


np.set_printoptions(precision=3,linewidth = 100,formatter = {'all':lambda x: '%10.2f' % x})

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
Tt = T_svds.copy()
Tt = np.delete(Tt,useless,0)


# Shape of Tt should be (3171,2023) only. ie (variables,parameters) and not other way around

T_small = np.concatenate((np.array([np.sum(
    Tt[np.array([ np.arange(i*Cons()*Years(),i*Cons()*Years()+Years()) for i in np.arange(Prod())])+j*Years(),:],axis = 0
    ) for j in np.arange(Cons())]).reshape(Cons()*Years(),Number_of_Parameters),Tt[Prod()*Cons()*Years():,:]),axis=0)
# T_small[118,:] = T_small[118,:]/10


small_x = np.concatenate((np.array([np.sum(
    cx[np.array([ np.arange(i*Cons()*Years(),i*Cons()*Years()+Years()) for i in np.arange(Prod())])+j*Years()],axis = 0
    ) for j in np.arange(Cons())]).flatten(),cx[Prod()*Cons()*Years():]))




def corr2cov(correl, sd):
    sd = sd.reshape(sd.size,1)
    return correl*(sd.T)*sd

def Wiener_cov(vari):
    v = np.diag(vari)
    for i in np.arange(vari.shape[0]):
        for j in np.arange(i):
            v[i,j]=v[j,i] = min(vari[i],vari[j])
    return v


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
sd = np.sqrt(np.array([
    0,        # 2010
    0,        # 2015
    0.0025,     # 2020
    0.0050,   # 2025
    0.0075,   # 2030
    0.0100,   # 2035
    0.0125    # 2040
    ]))*np.min(StochA[c_pos+70:c_pos+77])






# vartemp = np.diag(sd)
# corrmat = np.zeros(vartemp.shape)
# for i in np.arange(7):
#     for j in np.arange(7):
#         if i==j:
#             corrmat[i,j] = 1
#         else:
#             corrmat[i,j] = max(0,0.6 - np.abs(i-j)*0.1)

# vartemp = corr2cov(corrmat,sd)
vartemp = Wiener_cov(sd*sd)
C2p[c_pos+70:c_pos+77,c_pos+70:c_pos+77] = vartemp
C2v = T_small.dot(C2p).dot(T_small.T)
v_Qpy = C2v[210:301,210:301]
v_Qcy = C2v[0:119,0:119]
v_Qay = C2v[301:742,301:742]
v_PIcy = C2v[1624:,1624:]


# Variances
np.sqrt(np.diag(v_Qcy).reshape(Cons(),Years()))
np.concatenate((np.arange(Arcs.size()).reshape(Arcs.size(),1),np.sqrt(np.diag(v_Qay).reshape(Arcs.size(),Years()))[:,2:]),axis=1)

np.concatenate((np.arange(Arcs.size()).reshape(Arcs.size(),1),Qay[:,2:]),axis=1)

np.sqrt(np.diag(v_Qpy).reshape(Prod(),Years()))
np.sqrt(np.diag(v_PIcy).reshape(Cons(),Years()))



# Covariances
c_Qpy_Pi = np.zeros((Prod(),Years()-2,Years()-2))
for i in np.arange(Prod()):
    temp = i*Years()
    c_Qpy_Pi[i,:,:] = v_Qpy[temp:temp+Years(),temp:temp+Years()][2:,2:]

temp = np.arange(Prod())*Years()
c_Qpy_Yi = np.zeros((Years(),Prod(),Prod()))
for i in np.arange(2,Years()):    
    c_Qpy_Yi[i,:,:] = v_Qpy[temp+i,:][:,temp+i] 

np.savetxt('c_Qpy_Yi_c1.csv', c_Qpy_Yi[2:,:,:].reshape(5*13,13))














import matplotlib.pyplot as plt

Prods = ['Alaska','E Can','W Can','Mex 2', 'Mex 5', 'Mid Atlantic','S. Atlantic','E.N. Central','E.S. Central','W.N. Central','W.S. Central','Mountain','Pacific']

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
sd_I = np.sqrt(np.array([
        0,        # 2010
        0,        # 2015
        1,     # 2020
        2,     # 2025
        3,     # 2030
        4,     # 2035
        5      # 2040
    ]))

factor = 0.1 

temp = np.zeros((5,5))
for i in np.arange(5):
    for j in np.arange(5):
        temp[i,j] = np.sqrt((i+1)*(j+1))


sd_D = sd_I*factor

# sd = (np.repeat(sd, 5,0)*DemInt[3:8,:]).flatten()

C3p[126+7*7 : 126+8*7, 126+7*7:126+8*7] = Wiener_cov(sd_I*sd_I)
C3p[7+7*7 : 7+8*7, 7+7*7:7+8*7] = Wiener_cov(sd_D*sd_D)
C3p[7+7*7+2 : 7+8*7, 126+7*7+2:126+8*7] = temp*factor
C3p[126+7*7+2 : 126+8*7, 7+7*7+2:7+8*7] = temp*factor


C3v = T_small.dot(C3p).dot(T_small.T)

v_Qpy = C3v[210:301,210:301]
v_Qcy = C3v[0:119,0:119]
v_Qay = C3v[301:742,301:742]
v_PIcy = C3v[1624:,1624:]

np.sqrt(np.diag(v_Qcy).reshape(Cons(),Years()))
np.concatenate((np.arange(Arcs.size()).reshape(Arcs.size(),1),np.sqrt(np.diag(v_Qay).reshape(Arcs.size(),Years()))[:,2:]),axis=1)

np.concatenate((np.arange(Arcs.size()).reshape(Arcs.size(),1),Qay[:,2:]),axis=1)

np.sqrt(np.diag(v_Qpy).reshape(Prod(),Years()))
np.sqrt(np.diag(v_PIcy).reshape(Cons(),Years()))




##### Sensitivity
B1 = T_small**2
B2 = np.sum(B1,axis = 0)
B3 = np.sqrt(B2)*StochA/100

