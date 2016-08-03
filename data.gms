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
Set C0 Consumers /
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

Set Y Years /2010, 2015,2020,2025,2030,2035,2040/;
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
              2010        2015        2020        2025        2030        2035        2040
N_ALK      856.007     896.561     962.798     790.366     931.448    1020.387    1235.349
N_CAE       64.960      76.948      54.741      64.294      67.730      54.146      49.181
N_CAW       39.187      26.934      31.738      20.267      22.706      25.103      25.749
N_MEX1     537.897     644.855     338.673     233.857     177.937     164.259     147.423
N_MEX2      99.335      93.440      88.071      72.997      80.619      75.455      77.290
N_MEX3     251.687     152.197     160.383     144.031     134.881     125.152     140.732
N_MEX4     219.426     165.527     224.508     184.121     176.416     190.243     182.346
N_MEX5      48.850      64.475      63.008      74.448      93.820      95.140     105.821
N_US1      105.516      85.487      95.524      97.713      94.548     105.018      93.409
N_US2       33.278      28.200      35.722      33.932      34.609      31.498      36.809
N_US3       31.747      41.128      35.740      33.980      37.859      36.977      41.314
N_US4       28.319      28.900      30.320      26.617      29.784      29.408      29.565
N_US5       71.087      71.682      81.398      52.600      51.573      57.077      53.379
N_US6       44.766      69.065      71.147      48.607      49.384      51.421      51.580
N_US7       16.800      18.361      22.460      15.369      16.798      18.471      18.879
N_US8       49.160      59.663      58.576      60.674      48.538      57.872      58.947
N_US9       35.253      17.583      20.437      50.077      45.406      57.871      33.559
;

Table DemInt(C,Y)
              2010        2015        2020        2025        2030        2035        2040
N_ALK     7663.485    8026.553    8619.544    7075.832    8338.885    9135.117   11059.584
N_CAE     8337.119   11000.350    8474.570   10913.996   11933.256    9919.214    9343.279
N_CAW     9608.805    8931.226   12387.732    8755.644   10593.155   12096.655   12673.890
N_MEX1    7466.232    9242.000   11315.400    9179.969    8747.726    9603.049    9988.039
N_MEX2    7132.401    8746.231    9649.009    8742.388   10546.533   10694.465   11797.935
N_MEX3    6467.540    7001.284    9132.324    8623.005    9458.445    9817.501   12210.695
N_MEX4    5706.488    5756.767    9458.854    7987.653    9246.453   11006.774   11542.551
N_MEX5    4603.374    5450.290    7280.284    8353.404   10094.980   10236.924   11386.274
N_US1     8764.505   10480.810   10852.503   10551.680   10741.674   12402.532   10926.758
N_US2     8792.186   10100.669   11237.537   10145.979   11102.928   10922.368   13069.849
N_US3     9245.230   11410.490   10631.397   10205.052   11838.704   12197.942   13077.006
N_US4     9919.041   10017.121   10796.837    9553.789   10746.879   10611.028   10863.935
N_US5     9532.446   11005.777   11617.638    7962.645    8197.020    8702.215    9176.855
N_US6     7033.783   11013.806   11577.986    7962.645    8197.020    8702.215    9176.967
N_US7     8456.933   10538.201   12165.247    8852.478   10183.158   11390.028   12250.908
N_US8     7477.988   10183.981    9421.889    9825.926    8444.785   10068.699   10900.633
N_US9     9913.530    9242.281   11417.723    9525.213    8733.981   10068.570   12980.758
;


CostP('P_ALK','2010') = 20.00;
CostP('P_CE','2010') = 20.00;
CostP('P_CW','2010') = 20.00;
*CostP('P_CWS','2010') = 20.00;
CostP('P_MEX2','2010') = 25.00;
CostP('P_MEX5','2010') = 25.00;
CostP('P_U2','2010') = 45;
CostP('P_U3','2010') = 45;
CostP('P_U4','2010') = 50;
CostP('P_U5','2010') = 45;
CostP('P_U6','2010') = 45;
CostP('P_U7','2010') = 18;
CostP('P_U8','2010') = 45;
CostP('P_U9','2010') = 50;

CostQ('P_ALK','2010') = 0.10;
CostQ('P_CE','2010') = 0.10;
CostQ('P_CW','2010') = 0.10;
*CostQ('P_CWS','2010') = 0.10;
CostQ('P_MEX2','2010') = 0.10;
CostQ('P_MEX5','2010') = 0.10;
CostQ('P_U2','2010') = 0.10;
CostQ('P_U3','2010') = 0.10;
CostQ('P_U4','2010') = 0.10;
CostQ('P_U5','2010') = 0.10;
CostQ('P_U6','2010') = 0.10;
CostQ('P_U7','2010') = 0.10;
CostQ('P_U8','2010') = 0.10;
CostQ('P_U9','2010') = 0.10;

CostG('P_ALK','2010') = 10;
CostG('P_CE','2010') = 10;
CostG('P_CW','2010') = 10;
*CostG('P_CWS','2010') = 10;
CostG('P_MEX2','2010') = 10;
CostG('P_MEX5','2010') = 10;
CostG('P_U2','2010') = 10;
CostG('P_U3','2010') = 10;
CostG('P_U4','2010') = 10;
CostG('P_U5','2010') = 10;
CostG('P_U6','2010') = 10;
CostG('P_U7','2010') = 10;
CostG('P_U8','2010') = 10;
CostG('P_U9','2010') = 10;



CostP(P,Y) = CostP(P,'2010');
CostQ(P,Y) = CostQ(P,'2010');
CostG(P,Y) = CostG(P,'2010');


CostA(N,N0,Y) = 1000000;

CostA('N_ALK' ,'N_US8', '2010')     =  60.00 ;
CostA('N_CAE' ,'N_US1', '2010')     =  20.00 ;
CostA('N_CAE' ,'N_US2', '2010')     =  20.00 ;
CostA('N_CAE' ,'N_US3', '2010')     =  20.00 ;
CostA('N_CAE' ,'N_US4', '2010')     =  20.00 ;
CostA('N_CAE' ,'N_US6', '2010')     =  20.00 ;
CostA('N_CAW' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_CAW' ,'N_US4', '2010')     =  20.00 ;
CostA('N_CAW' ,'N_US6', '2010')     =  20.00 ;
CostA('N_CAW' ,'N_US8', '2010')     =  20.00 ;
CostA('N_CAW' ,'N_US9', '2010')     =  20.00 ;
CostA('N_MEX1','N_US9', '2010')     =  20.00 ;
CostA('N_MEX2','N_MEX5', '2010')    =  20.00 ;
CostA('N_MEX2','N_US7', '2010')     =  20.00 ;
CostA('N_MEX4','N_MEX3', '2010')    =  20.00 ;
CostA('N_MEX5','N_MEX4', '2010')    =  20.00 ;
CostA('N_US1' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_US1' ,'N_US2', '2010')     =  10.00 ;
CostA('N_US2' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_US2' ,'N_US1', '2010')     =  10.00 ;
CostA('N_US2' ,'N_US3', '2010')     =  20.00 ;
CostA('N_US2' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US2' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US3' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_US3' ,'N_US2', '2010')     =  20.00 ;
CostA('N_US3' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US3' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US3' ,'N_US6', '2010')     =  20.00 ;
CostA('N_US4' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_US4' ,'N_US2', '2010')     =  20.00 ;
CostA('N_US4' ,'N_US3', '2010')     =  20.00 ;
CostA('N_US4' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US4' ,'N_US7', '2010')     =  20.00 ;
CostA('N_US4' ,'N_US8', '2010')     =  20.00 ;
CostA('N_US5' ,'N_US2', '2010')     =  20.00 ;
CostA('N_US5' ,'N_US3', '2010')     =  20.00 ;
CostA('N_US5' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US5' ,'N_US6', '2010')     =  20.00 ;
CostA('N_US5' ,'N_US7', '2010')     =  20.00 ;
CostA('N_US6' ,'N_CAE', '2010')     =  20.00 ;
CostA('N_US6' ,'N_US3', '2010')     =  20.00 ;
CostA('N_US6' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US6' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US6' ,'N_US7', '2010')     =  20.00 ;
CostA('N_US6' ,'N_US8', '2010')     =  20.00 ;
CostA('N_US7' ,'N_MEX2', '2010')    =  20.00 ;
CostA('N_US7' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US7' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US7' ,'N_US6', '2010')     =  20.00 ;
CostA('N_US7' ,'N_US8', '2010')     =  20.00 ;
CostA('N_US8' ,'N_CAW', '2010')     =  20.00 ;
CostA('N_US8' ,'N_MEX1', '2010')    =  20.00 ;
CostA('N_US8' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US8' ,'N_US6', '2010')     =  20.00 ;
CostA('N_US8' ,'N_US7', '2010')     =  20.00 ;
CostA('N_US8' ,'N_US9', '2010')     =  20.00 ;
CostA('N_US9' ,'N_CAW', '2010')     =  20.00 ;
CostA('N_US9' ,'N_MEX1', '2010')    =  20.00 ;
CostA('N_US9' ,'N_US3', '2010')     =  20.00 ;
CostA('N_US9' ,'N_US4', '2010')     =  20.00 ;
CostA('N_US9' ,'N_US5', '2010')     =  20.00 ;
CostA('N_US9' ,'N_US6', '2010')     =  20.00 ;
CostA('N_US9' ,'N_US8', '2010')     =  20.00 ;



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


LossP(P,Y) = 0.05;
Qp0(P) = 2000;

LossA(N0,NN0,Y)$(Ao(N0,NN0)) = 0.05;

PIXP(P,Y) = 2;
PIXA(N0,NN0,'2010')$(Ao(N0,NN0)) = 3;

df('2010') = 1.000;

* Inflation in production and storage expansion
Loop(Y,
    PIXP(P,Y+1)=PIXP(P,Y)+0.5;
    PIXA(N0,NN0,Y+1)$(Ao(N0,NN0))=PIXA(N0,NN0,Y)$(Ao(N0,NN0))+0.3;
    CostA(N0,NN0,Y+1)$(Ao(N0,NN0)) = CostA(N0,NN0,Y)$(Ao(N0,NN0));
    df(Y+1) = df(Y)*0.95;
*    DemInt(C,Y+1) = DemInt(C,Y)*1.1;
    CostP(P,Y) = CostP(P,Y)*1.1;
    );


CAPpy.L(P,Y) = Qp0(P)      ;
Qpy.L(P,Y) = CAPpy.L(P,Y)/2 ;

Scalar epsilon /0.01/;


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

scalar avl /0.7/;

* Producer
E1_2a(P,Y).. avl*CAPpy(P,Y)-Qpy(P,Y) =g= 0;
E1_2b(P,Y).. CAPpy(P,Y) =e= Qp0(P) + sum(Y0$(ORD(Y0) <= ORD(Y)),Xpy(P,Y0));
E1_2c(P,N,Y).. sum(C$(CN(C,N)),Qpcny(P,C,Y)) +
                sum(NN0$(Ao(N,NN0)),Qpay(P,N,NN0,Y))
            =e=
                sum(NN0$(Ao(NN0,N)),Qpay(P,NN0,N,Y)*(1-LossA(NN0,N,Y))) +
                Qpy(P,Y)$(PN(P,N))*(1-LossP(P,Y)) ;
E1_2d(P,Y).. sum(C,Qpcny(P,C,Y)) =e= Qpy(P,Y)*(1-LossP(P,Y));

*E1_3a(P,C,Y).. -df(Y)*piCY(C,Y)+ sum(N$(CN(C,N)),d3(P,N,Y)) +d4(P,Y) =g= 0;
E1_3a(P,C,Y).. -df(Y)*piCY(C,Y)+ sum(N$(CN(C,N)),d3(P,N,Y))  =g= 0;
E1_3b(P,Y).. df(Y)*PIXP(P,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d2(P,Y0)) =g= 0;
E1_3c(P,N0,NN0,Y)$(Ao(N0,NN0)).. df(Y)*PIay(N0,NN0,Y) + d3(P,N0,Y) - d3(P,NN0,Y)*(1-LossA(N0,NN0,Y)) =g= 0;
*E1_3d(P,Y).. df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy(P,Y) - costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon))) +
*                 d1(P,Y)-(sum(N0$(PN(P,N0)),d3(P,N0,Y))+d4(P,Y))*(1-LossP(P,Y)) =g= 0;
E1_3d(P,Y).. df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy(P,Y) - costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon))) +
                 d1(P,Y)-(sum(N0$(PN(P,N0)),d3(P,N0,Y)))=g= 0;
E1_3e(P,Y).. df(Y)*(costG(P,Y)*Qpy(P,Y)/(CAPpy(P,Y)+epsilon)+costG(P,Y)*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon)))+ avl*d2(P,Y)-d1(P,Y) =g= 0;

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
*E1_2d.d4,
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

*DemInt(C,Y) = DemInt(C,Y)*5;