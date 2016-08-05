* Nodes
* Sets

Set P0 Producers /
P_ALK
P_CE
P_CW
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
N_ALK      587.640     927.568     957.472     705.952     677.364     813.059    1093.579
N_CAE       44.740      55.853      51.289      43.181      37.128      35.452      39.951
N_CAW       22.766      24.270      20.580      13.968      13.974      13.032      21.451
N_MEX1     412.835     573.533     257.251     152.355     135.118     107.779     123.308
N_MEX2      80.368      92.288      78.358      50.302      49.635      44.115      68.282
N_MEX3     213.362     135.306     144.504     127.365      98.297     105.552     110.907
N_MEX4     206.920     173.503     191.928     172.249     128.703     142.762     170.294
N_MEX5      56.103      70.815      69.458      65.893      61.183      58.957      98.859
N_US1       71.968      71.838      76.707      56.691      58.211      54.491      92.256
N_US2       21.545      22.828      25.928      20.806      24.591      18.398      21.426
N_US3       20.454      29.787      27.424      22.943      26.772      19.211      24.047
N_US4       16.414      23.400      24.185      18.049      21.212      22.095      20.431
N_US5       43.582      52.029      55.920      40.486      40.941      41.615      44.302
N_US6       37.762      50.127      48.892      37.412      39.204      37.492      42.809
N_US7       11.422      13.946      14.473      10.460      11.888      10.081      11.541
N_US8       37.828      50.189      55.326      37.230      37.254      35.828      46.650
N_US9       20.435      15.637      16.255      33.969      34.486      35.878      19.522
;

Table DemInt(C,Y)
              2010        2015        2020        2025        2030        2035        2040
N_ALK     5260.904    8304.141    8571.865    6320.109    6064.169    7278.993    9790.377
N_CAE     5742.035    7984.687    7940.178    7329.964    6541.520    6494.517    7589.799
N_CAW     5582.383    8047.817    8032.551    6034.117    6519.107    6279.892   10558.330
N_MEX1    5730.318    8219.812    8595.022    5980.642    6642.658    6301.067    8354.195
N_MEX2    5770.511    8638.337    8584.933    6024.302    6493.210    6252.546   10422.902
N_MEX3    5482.722    6224.279    8228.130    7625.213    6892.996    8280.008    9622.874
N_MEX4    5381.252    6034.147    8086.187    7472.622    6745.686    8259.725   10779.658
N_MEX5    5286.827    5986.282    8025.519    7393.420    6583.171    6343.725   10637.086
N_US1     5977.904    8807.461    8714.732    6121.790    6613.388    6435.328   10791.791
N_US2     5692.167    8176.636    8156.528    6221.096    7888.909    6379.773    7607.755
N_US3     5956.511    8264.041    8157.659    6890.320    8371.940    6337.309    7611.429
N_US4     5749.338    8110.575    8612.012    6478.208    7653.783    7972.552    7507.630
N_US5     5844.117    7988.324    7981.211    6128.768    6507.264    6344.904    7616.303
N_US6     5933.253    7993.706    7956.347    6128.768    6507.264    6344.904    7616.387
N_US7     5749.639    8004.029    7839.229    6025.006    7206.689    6216.265    7489.034
N_US8     5754.215    8566.830    8899.230    6029.226    6481.576    6233.385    8626.587
N_US9     5746.509    8219.548    9081.388    6461.168    6633.403    6242.151    7551.251
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

CostQ(P,'2010') = 0.1;
CostG(P,'2010') = 10;



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

Qa0(N0,NN0) = Qa0(N0,NN0)*2;

LossP(P,Y) = 0.0;
Qp0(P) = 2000;

LossA(N0,NN0,Y)$(Ao(N0,NN0)) = 0.0;

PIXP(P,Y) = 2;
PIXA(N0,NN0,'2010')$(Ao(N0,NN0)) = 4;

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


Scalar epsilon /0.01/;


Equations
E1_2a(P,Y)
E1_2b(P,Y)
E1_2c(P,N,Y)
*E1_2d(P,Y)
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
*E1_2d(P,Y).. sum(C,Qpcny(P,C,Y)) =e= Qpy(P,Y)*(1-LossP(P,Y));

*E1_3a(P,C,Y).. -df(Y)*piCY(C,Y)+ sum(N$(CN(C,N)),d3(P,N,Y)) +d4(P,Y) =g= 0;
E1_3a(P,C,Y).. -df(Y)*piCY(C,Y)+ sum(N$(CN(C,N)),d3(P,N,Y))  =g= 0;
E1_3b(P,Y).. df(Y)*PIXP(P,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d2(P,Y0)) =g= 0;
E1_3c(P,N0,NN0,Y)$(Ao(N0,NN0)).. df(Y)*PIay(N0,NN0,Y) + d3(P,N0,Y) - d3(P,NN0,Y)*(1-LossA(N0,NN0,Y)) =g= 0;
*E1_3d(P,Y).. df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy(P,Y) - costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon))) +
*                 d1(P,Y)-(sum(N0$(PN(P,N0)),d3(P,N0,Y))+d4(P,Y))*(1-LossP(P,Y)) =g= 0;
E1_3d(P,Y).. df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy(P,Y) - costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1-Qpy(P,Y)/(CAPpy(P,Y)+epsilon))) +
                 d1(P,Y)-sum(N0$(PN(P,N0)),d3(P,N0,Y))*(1-LossP(P,Y))=g= 0;
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