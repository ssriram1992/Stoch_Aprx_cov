$ontext
*******************************************************************************
Author: Sriram Sankaranarayanan
File: Supply_price.gms
Institution: Johns Hopkins University
Contact: ssankar5@jhu.edu

All rights reserved.
You are free to distribute this code for non-profit purposes
as long as this header is kept intact
*******************************************************************************
$offtext

$SETGLOBAL offlst "*"
*option solvelink = 5;

%offlst%$ontext
$offlisting
$offsymlist
$Offsymxref
Option Solprint = off;
Option limrow = 0;
Option limcol = 0;
$inlinecom /* */
option solveopt=merge ;
$ontext
$offtext

option solvelink=2;
$INCLUDE ./data.gms
$INCLUDE ./calib_data.gms

Equations
Supply_Cost
Dem_Cons(C,Y)
;

Variable Obj;

Supply_Cost.. obj =e= sum(Y,df(Y)*(
*Production costs
    sum(P,(CostP(P,Y) + costG(P,Y))*Qpy(P,Y)
        +costQ(P,Y)*sqr(Qpy(P,Y))
        +costG(P,Y)*(CAPpy(P,Y)-Qpy(P,Y))*log(1 - Qpy(P,Y)/(CAPpy(P,Y)+epsilon)))
* Transport costs
    +sum((N0,NN0),CostA(N0,NN0,Y)*Qay(N0,NN0,Y))
* Investment costs
    +sum((P),Xpy(P,Y)*PIXP(P,Y))
    +sum((N0,NN0),Xay(N0,NN0,Y)*PIXA(N0,NN0,Y))
    ));

Dem_Cons(C,Y).. sum(P,Qpcny(P,C,Y)) =g= Consumption(C,Y);

model supply_price_init
/
Supply_Cost
Dem_Cons
E1_2a
E1_2b
E1_2c
*E1_2d
E1_6a
E1_6b
E1_8
E1_9
/;

*costG(P,Y) = 0;

$If exist ./auxi/supply_cost_init.gdx execute_loadpoint './auxi/supply_cost_init.gdx'
$INCLUDE ./manual_calib.gms
Solve supply_price_init using NLP minimizing obj;
Parameter ref_price_S(C,Y);
ref_price_S(C,Y) = Dem_Cons.m(C,Y);
Display ref_price_S;


execute_unload 'auxi/supply_cost_init.gdx'
Display Dem_Cons.m;
Display PIcy.L;
Parameter Qcy(C,Y);
Qcy(C,Y) = sum(P,Qpcny.L(P,C,Y));
Display Qcy;
Display DemInt;
Display Qpcny.L,Xpy.L,Qpay.L,Qpy.L,CAPpy.L,Qay.L,Xay.L,CAPay.L,PIcy.L;
