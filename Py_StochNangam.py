import numpy as np
from Py_Nangam import *
# from Py_N_derivs import *

####################################
######## Stochasticizations ########
####################################

# Move the following files to server
#       MeritFuncs.py
#       sparse.py
#       G2Py.gpy

StochA = np.zeros(Number_of_Parameters)
xstar = np.zeros(Number_of_Variables)

##### Initial Point
fi = open("G2Py.gpy")
for i in np.arange(Number_of_Variables):
    xstar[i] = fi.readline()


fi.close()
del fi
### Section end


##### EValuating at initial point
Fx = F(xstar,a=StochA)
### Section end

##### Splitting the variables for just the initial point
(d1,d2,d3,Qpcny,Xpy,Qpay,Qpy,CAPpy,d5,d6,Qay,Xay,CAPay,PIay,
                PIcy,positions)          = varPy2Gams(xstar,posit = True)
(e1_2a,e1_2b,e1_2c,e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
    e1_8,e1_9)                 = varPy2Gams(Fx)

StochA = StochGams2Py()
### Section end

##### List of free variables
free = freevar()
### Section end





##### Getting the Variance Structure of the input
#Coeff of variations
vdf = 0.01*df
vDemSlope = 0*DemSlope
vDemInt = 0.*DemInt
vCostP = 0.1*CostP
vCostQ = 0.1*CostQ
vCostG = 0.1*CostG
vCostA = 0*CostA
vPIXP = 0*PIXP
vPIXA = 0*PIXA
vLossP = 0*LossP
vLossA = 0*LossA
### Section end

# #### Free var deriv
# def FreeGrad(F,x,a=None):
# 	N = free.size
# 	(e1_2a,e1_2b,e1_2c,
#     e1_3a,e1_3b,e1_3c,e1_3d,e1_3e,
#     e1_6a,e1_6b,e1_7a,e1_7b,e1_7c,
#     e1_8,e1_9,positions)                 = varPy2Gams(np.zeros(x.shape),posit = True)
# 	Grad = np.zeros((N,N))	
# 	if i < positions[2]: #d2
# 		pass
# 	elif:
# 		pass
# ### Section end


#### Simulating the random variables
def corr2cov(correl, sd):
    sd = sd.reshape(sd.size,1)
    return correl*(sd.T)*sd

# adf, aDemSlope,aDemInt,aCostP,aCostQ,aCostG,aCostA,aPIXP,aPIXA,aLossP,aLossA
def Cov_Tex1():
	corrmat = np.zeros((Years()-2,Years()-2))
	for i in np.arange(5):
	    for j in np.arange(5):
	        if i==j:
	            corrmat[i,j] = 1
	        else:
	            corrmat[i,j] = max(0,0.6 - np.abs(i-j)*0.1)
	print(corrmat)
	sd = 0.1*StochA[427+72:427+77]
	return corr2cov(corrmat, sd)

def rand_Tex1(Cov):
	randa = np.zeros(Number_of_Parameters)
	vars = np.random.multivariate_normal(np.zeros(5),Cov)
	randa[427+72:427+77] = vars
	return randa


def Cov_Tex2():
	corrmat = np.zeros(((Years()-2)*Prod(),(Years()-2)*Prod()))
	for i in np.arange(5):
	    for j in np.arange(5):
	        if i==j:
	            corrmat[i,j] = 1
	        else:
	            corrmat[i,j] = max(0,0.6 - np.abs(i-j)*0.1)
	print(corrmat)
	sd = 0.1*StochA[427+72:427+77]
	return corr2cov(corrmat, sd)

def rand_Tex1(Cov):
	randa = np.zeros(Number_of_Parameters)
	vars = np.random.multivariate_normal(np.zeros(5),Cov)
	randa[427+72:427+77] = vars
	return randa



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

def Wiener_cov(vari):
    v = np.diag(vari)
    for i in np.arange(vari.shape[0]):
        for j in np.arange(i):
            v[i,j]=v[j,i] = min(vari[i],vari[j])
    return v

StochA = StochGams2Py(df,DemSlope,DemInt,CostP,CostQ,CostG,CostA,PIXP,PIXA,LossP,LossA)

factor = 0.01
sd_ref = np.sqrt(np.array([
    0,   # 2010
    0,   # 2015
    1,   # 2020
    2,   # 2025
    3,   # 2030
    4,   # 2035
    5    # 2040
    ]))*factor

for i in np.arange(427,518,7):
    temp = 0.1   
    if i==497:
        temp = 0.5
    sd = temp*sd_ref*np.min(StochA[i:i+7])
    vartemp = Wiener_cov(sd*sd)
    C3p[i:i+7,i:i+7] = vartemp




### Section end


#### iteration
xk = xstar.copy()
# ak = StochA.copy()
step = 0.01
count = 0
Cov = C3p

for i in np.arange(25):
	count = count+1
	Fxk = F(xk,rand_Tex1(Cov))
	temp1 = np.sqrt(xk**2 + Fxk**2)
	temp1[temp1 < 1e-4] = 1
	temp2 = (temp1-xk-Fxk)*(Fxk/temp1 - 1)
	temp3 = Fxk[free]
	temp3[temp3 < 1e-4] = 0
	dk = temp2.copy()
	dk[free] = -temp3
	xk1 = xk.copy()
	xk = xk - step/count*dk
	if count%1 == 0:
		print count, np.linalg.norm(xk-xk1),Fxk[11929],xk[11929]


### Section end


















