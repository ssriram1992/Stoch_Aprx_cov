* Nodes
* Sets

Set P0 Producers /
P_ALK
P_CE
P_CW
*P_CWS
P_MEX2
P_MEX5
P_U2
P_U3
P_U4
P_U5
P_U6
P_U7
P_U8
P_U9
/;
Set C0 Consumers /C1*C17/;
Set N0 Nodes /
N_ALK
N_CAE
N_CAW
N_MEX1
N_MEX2
N_MEX3
N_MEX4
N_MEX5
N_US1
N_US2
N_US3
N_US4
N_US5
N_US6
N_US7
N_US8
N_US9
/;
Alias(N0,NN0);
Alias(N0,N);
Alias(P,P0);
Alias(C,C0);

Set Y Years /2015,2020,2025,2030,2035,2040,2045,2050/;
Alias(Y,Y0);

* Decision Variables
Positive Variables
Qpcny(P,C,Y) "Quantity sent from producer p in node n to consumer c in year y",
Qpy(P,Y) "Total quantity produced by producer p in year y",
Qpay(P,N0,NN0,Y) "Quantity sent in arc a by producer p in year y",
Xpy(P,Y) "Capacity expansion by producer p in year y",
CAPpy(P,Y) "Capacity of producer p in year y",

Qay(N0,NN0,Y) "Total quantity sent in arc a in year y",
Xay(N0,NN0,Y) "Capacity expansion on a in year y",
CAPay(N0,NN0,Y) "Capacity of a in year y"
;

* Prices - Variables
Variables
PIcy(C,Y) "Price for consumer c in year y",
PIay(N0,NN0,Y) "Price for arc a in year y"
;

* Other Duals
Variables
d2(P,Y),
d3(P,N,Y) "Node equilibrium dual",
d4(P,Y) "Market Balance dual",
d6(N0,NN0,Y)
;

Positive Variables
d1(P,Y) "Cap P dual",
d5(N0,NN0,Y) "CapA dual"
;

* Parameters
Parameters
Qp0(P) "Initial Production Capacity",
Qa0(N0,NN0) "Initial Transportation Capacity",
df(Y) "Discount Factors",
PIXP(P,Y) "Cost of production expansion",
PIXA(N0,NN0,Y) "Cost of transportation expansion",

*CostP(P,Y) "Unit Cost of Production",
CostA(N,NN0,Y) "Unit Cost of Transportation",
LossA(N,NN0,Y) "Losses in pipeline transportation",
LossP(P,Y) "Losses in production"
;

Parameters
CostP(P,Y),
CostQ(P,Y),
CostG(P,Y)
;



* Nodes for Producers
Set PN(P0,N0) /
P_ALK.N_ALK
P_CE.N_CAE
P_CW.N_CAW
*P_CWS.N_CAW
P_MEX2.N_MEX2
P_MEX5.N_MEX5
P_U2.N_US2
P_U3.N_US3
P_U4.N_US4
P_U5.N_US5
P_U6.N_US6
P_U7.N_US7
P_U8.N_US8
P_U9.N_US9
/;


Set CN(C0,N0);
CN(C0,N0)$(ORD(C0)=ORD(N0))=yes;

* Arcs
Set Ao(N0,NN0)/
N_ALK.N_US8
N_CAE.N_US1
N_CAE.N_US2
N_CAE.N_US3
N_CAE.N_US4
N_CAE.N_US6
N_CAW.N_CAE
N_CAW.N_US4
N_CAW.N_US6
N_CAW.N_US8
N_CAW.N_US9
N_MEX1.N_US9
N_MEX2.N_MEX5
N_MEX2.N_US7
N_MEX4.N_MEX3
N_MEX5.N_MEX4
N_US1.N_CAE
N_US1.N_US2
N_US2.N_CAE
N_US2.N_US1
N_US2.N_US3
N_US2.N_US4
N_US2.N_US5
N_US3.N_CAE
N_US3.N_US2
N_US3.N_US4
N_US3.N_US5
N_US3.N_US6
N_US4.N_CAE
N_US4.N_US2
N_US4.N_US3
N_US4.N_US5
N_US4.N_US7
N_US4.N_US8
N_US5.N_US2
N_US5.N_US3
N_US5.N_US4
N_US5.N_US6
N_US5.N_US7
N_US6.N_CAE
N_US6.N_US3
N_US6.N_US4
N_US6.N_US5
N_US6.N_US7
N_US6.N_US8
N_US7.N_MEX2
N_US7.N_US4
N_US7.N_US5
N_US7.N_US6
N_US7.N_US8
N_US8.N_CAW
N_US8.N_MEX1
N_US8.N_US4
N_US8.N_US6
N_US8.N_US7
N_US8.N_US9
N_US9.N_CAW
N_US9.N_MEX1
N_US9.N_US3
N_US9.N_US4
N_US9.N_US5
N_US9.N_US6
N_US9.N_US8
/;



* Demand Parameters
Table
DemSlope(C,Y)
     2015    2020    2025    2030    2035    2040    2045    2050
C1   9.910   9.832   9.701   9.628   9.485   9.363   9.279   9.173
C2   9.791   9.713   8.582   9.509   9.366   9.244   9.160   9.054
C3   9.709   9.631   9.500   9.427   9.285   9.162   9.078   8.972
C4   9.662   9.583   9.452   9.380   9.237   9.115   9.031   8.925
C5   9.554   9.475   9.344   9.272   9.129   9.007   8.923   8.816
C6   9.461   9.382   9.251   9.179   5.036   8.914   8.830   8.723
C7   9.284   9.205   9.074   9.002   8.859   8.737   8.653   8.546
C8   8.554   8.475   10.344  8.272   8.129   10.007  8.923   7.816
C9   8.662   8.583   10.452  8.380   8.237   10.115  9.031   7.925
C10  9.284   9.205   9.074   9.002   8.859   8.737   8.653   8.546
C11  9.461   9.382   7.251   9.179   9.036   8.914   8.830   8.723
C12  9.662   9.583   9.452   9.380   9.237   9.115   7.031   8.925
C13  9.554   9.475   9.344   9.272   9.129   9.007   8.923   8.816
C14  9.910   9.832   9.701   9.628   9.485   9.363   11.79   9.173
C15  9.791   9.713   9.582   9.509   9.366   9.244   9.160   9.054
C16  8.554   8.475   10.344  8.272   8.129   10.007  8.923   7.816
C17  9.709   9.631   9.500   9.427   9.285   9.162   9.078   8.972
;

Table DemInt(C,Y)
     2015    2020    2025    2030    2035    2040    2045    2050
C1   99.641  97.465  102.073 101.392 98.443  101.370 97.237  96.352
C2   100.617 98.442  103.049 102.368 99.420  102.346 98.213  97.329
C3   100.792 98.616  103.224 102.542 99.594  102.520 98.387  97.503
C4   94.250  92.075  96.682  96.001  93.053  95.979  91.846  90.961
C5   102.246 100.070 104.678 103.997 101.048 103.975 99.842  98.957
C6   94.260  92.085  96.692  96.011  93.063  95.989  91.856  90.972
C7   99.073  96.897  101.505 100.824 97.875  100.801 96.668  95.784
C8   100.617 98.442  103.049 102.368 99.420  102.346 98.213  97.329
C9   100.792 98.616  103.224 102.542 99.594  102.520 98.387  97.503
C10  99.073  96.897  101.505 100.824 97.875  100.801 96.668  95.784
C11  94.250  92.075  96.682  96.001  93.053  95.979  91.846  90.961
C12  100.792 98.616  103.224 102.542 99.594  102.520 98.387  97.503
C13  100.617 98.442  103.049 102.368 99.420  102.346 98.213  97.329
C14  94.260  92.085  96.692  96.011  93.063  95.989  91.856  90.972
C15  102.246 100.070 104.678 103.997 101.048 103.975 99.842  98.957
C16  99.641  97.465  102.073 101.392 98.443  101.370 97.237  96.352
C17  100.617 98.442  103.049 102.368 99.420  102.346 98.213  97.329
;


CostP('P_ALK','2015') = 20.00;
CostP('P_CE','2015') = 20.00;
CostP('P_CW','2015') = 20.00;
*CostP('P_CWS','2015') = 20.00;
CostP('P_MEX2','2015') = 25.00;
CostP('P_MEX5','2015') = 25.00;
CostP('P_U2','2015') = 45;
CostP('P_U3','2015') = 45;
CostP('P_U4','2015') = 50;
CostP('P_U5','2015') = 45;
CostP('P_U6','2015') = 45;
CostP('P_U7','2015') = 18;
CostP('P_U8','2015') = 45;
CostP('P_U9','2015') = 50;

CostQ('P_ALK','2015') = 0.10;
CostQ('P_CE','2015') = 0.10;
CostQ('P_CW','2015') = 0.10;
*CostQ('P_CWS','2015') = 0.10;
CostQ('P_MEX2','2015') = 0.10;
CostQ('P_MEX5','2015') = 0.10;
CostQ('P_U2','2015') = 0.10;
CostQ('P_U3','2015') = 0.10;
CostQ('P_U4','2015') = 0.10;
CostQ('P_U5','2015') = 0.10;
CostQ('P_U6','2015') = 0.10;
CostQ('P_U7','2015') = 0.10;
CostQ('P_U8','2015') = 0.10;
CostQ('P_U9','2015') = 0.10;

CostG('P_ALK','2015') = 10;
CostG('P_CE','2015') = 10;
CostG('P_CW','2015') = 10;
*CostG('P_CWS','2015') = 10;
CostG('P_MEX2','2015') = 10;
CostG('P_MEX5','2015') = 10;
CostG('P_U2','2015') = 10;
CostG('P_U3','2015') = 10;
CostG('P_U4','2015') = 10;
CostG('P_U5','2015') = 10;
CostG('P_U6','2015') = 10;
CostG('P_U7','2015') = 10;
CostG('P_U8','2015') = 10;
CostG('P_U9','2015') = 10;



CostP(P,Y) = CostP(P,'2015');
CostQ(P,Y) = CostQ(P,'2015');
CostG(P,Y) = CostG(P,'2015');


CostA(N,N0,Y) = 1000000;

CostA('N_ALK' ,'N_US8', '2015')     =  60.00 ;
CostA('N_CAE' ,'N_US1', '2015')     =  20.00 ;
CostA('N_CAE' ,'N_US2', '2015')     =  20.00 ;
CostA('N_CAE' ,'N_US3', '2015')     =  20.00 ;
CostA('N_CAE' ,'N_US4', '2015')     =  20.00 ;
CostA('N_CAE' ,'N_US6', '2015')     =  20.00 ;
CostA('N_CAW' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_CAW' ,'N_US4', '2015')     =  20.00 ;
CostA('N_CAW' ,'N_US6', '2015')     =  20.00 ;
CostA('N_CAW' ,'N_US8', '2015')     =  20.00 ;
CostA('N_CAW' ,'N_US9', '2015')     =  20.00 ;
CostA('N_MEX1','N_US9', '2015')     =  20.00 ;
CostA('N_MEX2','N_MEX5', '2015')    =  20.00 ;
CostA('N_MEX2','N_US7', '2015')     =  20.00 ;
CostA('N_MEX4','N_MEX3', '2015')    =  20.00 ;
CostA('N_MEX5','N_MEX4', '2015')    =  20.00 ;
CostA('N_US1' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_US1' ,'N_US2', '2015')     =  10.00 ;
CostA('N_US2' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_US2' ,'N_US1', '2015')     =  10.00 ;
CostA('N_US2' ,'N_US3', '2015')     =  20.00 ;
CostA('N_US2' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US2' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US3' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_US3' ,'N_US2', '2015')     =  20.00 ;
CostA('N_US3' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US3' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US3' ,'N_US6', '2015')     =  20.00 ;
CostA('N_US4' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_US4' ,'N_US2', '2015')     =  20.00 ;
CostA('N_US4' ,'N_US3', '2015')     =  20.00 ;
CostA('N_US4' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US4' ,'N_US7', '2015')     =  20.00 ;
CostA('N_US4' ,'N_US8', '2015')     =  20.00 ;
CostA('N_US5' ,'N_US2', '2015')     =  20.00 ;
CostA('N_US5' ,'N_US3', '2015')     =  20.00 ;
CostA('N_US5' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US5' ,'N_US6', '2015')     =  20.00 ;
CostA('N_US5' ,'N_US7', '2015')     =  20.00 ;
CostA('N_US6' ,'N_CAE', '2015')     =  20.00 ;
CostA('N_US6' ,'N_US3', '2015')     =  20.00 ;
CostA('N_US6' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US6' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US6' ,'N_US7', '2015')     =  20.00 ;
CostA('N_US6' ,'N_US8', '2015')     =  20.00 ;
CostA('N_US7' ,'N_MEX2', '2015')    =  20.00 ;
CostA('N_US7' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US7' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US7' ,'N_US6', '2015')     =  20.00 ;
CostA('N_US7' ,'N_US8', '2015')     =  20.00 ;
CostA('N_US8' ,'N_CAW', '2015')     =  20.00 ;
CostA('N_US8' ,'N_MEX1', '2015')    =  20.00 ;
CostA('N_US8' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US8' ,'N_US6', '2015')     =  20.00 ;
CostA('N_US8' ,'N_US7', '2015')     =  20.00 ;
CostA('N_US8' ,'N_US9', '2015')     =  20.00 ;
CostA('N_US9' ,'N_CAW', '2015')     =  20.00 ;
CostA('N_US9' ,'N_MEX1', '2015')    =  20.00 ;
CostA('N_US9' ,'N_US3', '2015')     =  20.00 ;
CostA('N_US9' ,'N_US4', '2015')     =  20.00 ;
CostA('N_US9' ,'N_US5', '2015')     =  20.00 ;
CostA('N_US9' ,'N_US6', '2015')     =  20.00 ;
CostA('N_US9' ,'N_US8', '2015')     =  20.00 ;



Qa0('N_ALK' ,'N_US8')       =           0.01;
Qa0('N_CAE' ,'N_US1')       =           20.00;
Qa0('N_CAE' ,'N_US2')       =           88.00;
Qa0('N_CAE' ,'N_US3')       =           35.00;
Qa0('N_CAE' ,'N_US4')       =           1.00;
Qa0('N_CAE' ,'N_US6')       =           1.00;
Qa0('N_CAW' ,'N_CAE')       =           130.00;
Qa0('N_CAW' ,'N_US4')       =           139.00;
Qa0('N_CAW' ,'N_US6')       =           139.00;
Qa0('N_CAW' ,'N_US8')       =           156.00;
Qa0('N_CAW' ,'N_US9')       =           52.00;
Qa0('N_MEX1','N_US9')       =           17.00;
Qa0('N_MEX2','N_MEX5')      =           20.00;
Qa0('N_MEX2','N_US7')       =           24.00;
Qa0('N_MEX4','N_MEX3')      =           19.00;
Qa0('N_MEX5','N_MEX4')      =           45.00;
Qa0('N_US1' ,'N_CAE')       =           6.00;
Qa0('N_US1' ,'N_US2')       =           12.00;
Qa0('N_US2' ,'N_CAE')       =           3.00;
Qa0('N_US2' ,'N_US1')       =           85.00;
Qa0('N_US2' ,'N_US3')       =           13.00;
Qa0('N_US2' ,'N_US4')       =           13.00;
Qa0('N_US2' ,'N_US5')       =           68.00;
Qa0('N_US3' ,'N_CAE')       =           105.00;
Qa0('N_US3' ,'N_US2')       =           61.00;
Qa0('N_US3' ,'N_US4')       =           27.00;
Qa0('N_US3' ,'N_US5')       =           78.00;
Qa0('N_US3' ,'N_US6')       =           16.00;
Qa0('N_US4' ,'N_CAE')       =           2.00;
Qa0('N_US4' ,'N_US2')       =           61.00;
Qa0('N_US4' ,'N_US3')       =           360.00;
Qa0('N_US4' ,'N_US5')       =           10.00;
Qa0('N_US4' ,'N_US7')       =           25.00;
Qa0('N_US4' ,'N_US8')       =           58.00;
Qa0('N_US5' ,'N_US2')       =           241.00;
Qa0('N_US5' ,'N_US3')       =           46.00;
Qa0('N_US5' ,'N_US4')       =           262.00;
Qa0('N_US5' ,'N_US6')       =           6.00;
Qa0('N_US5' ,'N_US7')       =           11.00;
Qa0('N_US6' ,'N_CAE')       =           2.00;
Qa0('N_US6' ,'N_US3')       =           262.00;
Qa0('N_US6' ,'N_US4')       =           411.00;
Qa0('N_US6' ,'N_US5')       =           390.00;
Qa0('N_US6' ,'N_US7')       =           12.00;
Qa0('N_US6' ,'N_US8')       =           108.00;
Qa0('N_US7' ,'N_MEX2')      =           72.00;
Qa0('N_US7' ,'N_US4')       =           237.00;
Qa0('N_US7' ,'N_US5')       =           852.00;
Qa0('N_US7' ,'N_US6')       =           552.00;
Qa0('N_US7' ,'N_US8')       =           137.00;
Qa0('N_US8' ,'N_CAW')       =           2.00;
Qa0('N_US8' ,'N_MEX1')      =           7.00;
Qa0('N_US8' ,'N_US4')       =           191.00;
Qa0('N_US8' ,'N_US6')       =           209.00;
Qa0('N_US8' ,'N_US7')       =           105.00;
Qa0('N_US8' ,'N_US9')       =           306.00;
Qa0('N_US9' ,'N_CAW')       =           1.00;
Qa0('N_US9' ,'N_MEX1')      =           23.00;
Qa0('N_US9' ,'N_US3')       =           2.00;
Qa0('N_US9' ,'N_US4')       =           97.00;
Qa0('N_US9' ,'N_US5')       =           5.00;
Qa0('N_US9' ,'N_US6')       =           77.00;
Qa0('N_US9' ,'N_US8')       =           78.00;







Equations
E1_2a(P,Y)
E1_2b(P,Y)
E1_2c(P,N,Y)
E1_2d(P,Y)
E1_3a(P,C,Y)
E1_3b(P,Y)
E1_3c(P,N0,NN0,Y)
E1_3d(P,Y)
E1_3e(P,Y)
E1_6a(N0,NN0,Y)
E1_6b(N0,NN0,Y)
E1_7a(N0,NN0,Y)
E1_7b(N0,NN0,Y)
E1_7c(N0,NN0,Y)
E1_8(N0,NN0,Y)
E1_9(C,Y)
;
*
* Producer
E1_2a(P,Y).. CAPpy(P,Y)-Qpy(P,Y) =g= 0;
E1_2b(P,Y).. CAPpy(P,Y) =e= Qp0(P) + sum(Y0$(ORD(Y0) <= ORD(Y)),Xpy(P,Y0));
E1_2c(P,N,Y).. sum(C$(CN(C,N)),Qpcny(P,C,Y)) +
                sum(NN0$(Ao(N,NN0)),Qpay(P,N,NN0,Y))
            =e=
                sum(NN0$(Ao(NN0,N)),Qpay(P,NN0,N,Y)*(1-LossA(NN0,N,Y))) +
                Qpy(P,Y)$(PN(P,N))*(1-LossP(P,Y)) ;
E1_2d(P,Y).. sum(C,Qpcny(P,C,Y)) =e= Qpy(P,Y)*(1-LossP(P,Y));

E1_3a(P,C,Y).. -df(Y)*piCY(C,Y)+ sum(N$(CN(C,N)),d3(P,N,Y)) +d4(P,Y) =g= 0;
E1_3b(P,Y).. df(Y)*PIXP(P,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d2(P,Y0)) =g= 0;
E1_3c(P,N0,NN0,Y)$(Ao(N0,NN0)).. df(Y)*PIay(N0,NN0,Y) + d3(P,N0,Y) - d3(P,NN0,Y)*(1-LossA(N0,NN0,Y)) =g= 0;
E1_3d(P,Y).. df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy(P,Y) - costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon))) +
                 d1(P,Y)-(sum(N0$(PN(P,N0)),d3(P,N0,Y))+d4(P,Y))*(1-LossP(P,Y)) =g= 0;
E1_3e(P,Y).. df(Y)*(costG(P,Y)*Qpy(P,Y)/(CAPpy(P,Y)+epsilon)+costG(P,Y)*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon)))+ d2(P,Y)-d1(P,Y) =g= 0;

* Pipeline Operator
E1_6a(N0,NN0,Y)$(Ao(N0,NN0)).. CAPay(N0,NN0,Y)-Qay(N0,NN0,Y) =g= 0;
E1_6b(N0,NN0,Y)$(Ao(N0,NN0)).. CAPay(N0,NN0,Y) =e= Qa0(N0,NN0) + sum(Y0$(ORD(Y0) <= ORD(Y)),Xay(N0,NN0,Y0));

E1_7a(N0,NN0,Y)$(Ao(N0,NN0)).. -df(Y)*PIay(N0,NN0,Y) + CostA(N0,NN0,Y)+d5(N0,NN0,Y) =g= 0;
E1_7b(N0,NN0,Y)$(Ao(N0,NN0)).. df(Y)*PIXA(N0,NN0,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d6(N0,NN0,Y0)) =g= 0;
E1_7c(N0,NN0,Y)$(Ao(N0,NN0)).. d6(N0,NN0,Y)-d5(N0,NN0,Y) =g= 0;

E1_8(N0,NN0,Y)$(Ao(N0,NN0)).. Qay(N0,NN0,Y) =e= sum(P,Qpay(P,N0,NN0,Y));

* Consumer
E1_9(C,Y).. PIcy(C,Y) =e= DemInt(C,Y) - DemSlope(C,Y)*sum(P,Qpcny(P,C,Y));

Model Sim_Nangam /
E1_2a.d1,
E1_2b.d2,
E1_2c.d3,
E1_2d.d4,
E1_3a.Qpcny,
E1_3b.Xpy,
E1_3c.Qpay,
E1_3d.Qpy,
E1_3e.CAPpy,

E1_6a.d5,
E1_6b.d6,
E1_7a.Qay,
E1_7b.Xay,
E1_7c.CAPay,
E1_8.PIay,
E1_9.PIcy
/;
