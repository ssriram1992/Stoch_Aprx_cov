$ontext
*******************************************************************************
Author: Sriram Sankaranarayanan
File: Simple_Nangam.gms
Institution: Johns Hopkins University
Contact: ssankar5@jhu.edu

All rights reserved.
You are free to distribute this code for non-profit purposes
as long as this header is kept intact
*******************************************************************************
Git checked out
Features:
1. Quadratic and Golembek cost terms
2. No storage
3. Losses modelled
$offtext

* Set the folder name for data folder
$SETGLOBAL data_dir "./"

* Set the folder name for output folder
$SETGLOBAL out_dir "./"


*** SOLVING OPTIONS
* Set this as "*" to solve without the golembek term
$SETGLOBAL noGolembek ""

* Set this as "*" to presolve without golembek and then introduce Golembek
$SETGLOBAL presolve ""

* Star this for a fresh start and not use the previous soln as a starting point.
$SETGLOBAL no_init ""

$SETGLOBAL offlst "*"

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

option solvelink=5;
$INCLUDE ./data.gms

CAPpy.L(P,Y) = Qp0(P);
Qpy.L(P,Y) = CAPpy.L(P,Y)*avl;


$If exist ./auxi/loadpoint.gdx %no_init% execute_loadpoint './auxi/loadpoint.gdx' d1.L,d2.L,d3.L,d4.L,Qpcny.L,Xpy.L,Qpay.L,Qpy.L,CAPpy.L,d5.L,d6.L,Qay.L,Xay.L,CAPay.L,PIay.L,PIcy.L;
*d1.L(P,Y),d2.L(P,Y),d3.L(P,N,Y),d4.L(P,Y),Qpcny.L(P,C,Y),Xpy.L(P,Y),Qpay.L(P,N0,NN0,Y),Qpy.L(P,Y),CAPpy.L(P,Y),d5.L(N0,NN0,Y),d6.L(N0,NN0,Y),Qay.L(N0,NN0,Y),Xay.L(N0,NN0,Y),CAPay.L(N0,NN0,Y),PIay.L(N0,NN0,Y),PIcy.L(C,Y);
%no_init%

%no_init%Qpy.L(P,Y)$(Qpy.L(P,Y) > CAPpy.L(P,Y)) = CAPpy.L(P,Y);


%noGolembek%$ontext
Parameter CostG_copy(P,Y);
CostG_copy(P,Y) = CostG(P,Y);
CostG(P,Y) = 0;
$ontext
$offtext

%presolve%$ontext
Parameter CostG_copy(P,Y);
CostG_copy(P,Y) = CostG(P,Y);
CostG(P,Y) = 0;
Solve Sim_Nangam using MCP;
CostG(P,Y) = CostG_copy(P,Y);
$ontext
$offtext



option MCP=PATH;
Solve Sim_Nangam using MCP;
abort$(Sim_Nangam.solvestat > 1) "Solver status indicates that MCP did not solve correctly" ;
abort$(Sim_Nangam.modelstat > 2) "Model status indicates that MCP did not solve correctly"  ;


Parameters
f1_2a(P,Y)
f1_2b(P,Y)
f1_2c(P,N,Y)
f1_2d(P,Y)
f1_3a(P,C,Y)
f1_3b(P,Y)
f1_3c(P,N0,NN0,Y)
f1_3d(P,Y)
f1_3e(P,Y)
f1_6a(N0,NN0,Y)
f1_6b(N0,NN0,Y)
f1_7a(N0,NN0,Y)
f1_7b(N0,NN0,Y)
f1_7c(N0,NN0,Y)
f1_8(N0,NN0,Y)
f1_9(C,Y)
;


f1_2a(P,Y) = min(d1.L(P,Y), CAPpy.L(P,Y)-Qpy.L(P,Y));
f1_2b(P,Y) =  -CAPpy.L(P,Y) + Qp0(P) + sum(Y0$(ORD(Y0) <= ORD(Y)),Xpy.L(P,Y0));
f1_2c(P,N,Y) = sum(C$(CN(C,N)),Qpcny.L(P,C,Y)) +
                sum(NN0$(Ao(N,NN0)),Qpay.L(P,N,NN0,Y))
            -   sum(NN0$(Ao(NN0,N)),Qpay.L(P,NN0,N,Y)*(1-LossA(NN0,N,Y))) -
                Qpy.L(P,Y)$(PN(P,N))*(1-LossP(P,Y)) ;
f1_2d(P,Y) = sum(C,Qpcny.L(P,C,Y)) - Qpy.L(P,Y)*(1-LossP(P,Y));

f1_3a(P,C,Y) = min(Qpcny.L(P,C,Y) ,-df(Y)*piCY.L(C,Y)+ sum(N$(CN(C,N)),d3.L(P,N,Y)) +d4.L(P,Y));
f1_3b(P,Y) = min(Xpy.L(P,Y) ,df(Y)*PIXP(P,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d2.L(P,Y0)));
f1_3c(P,N0,NN0,Y)$(Ao(N0,NN0)) = min( Qpay.L(P,N0,NN0,Y),df(Y)*PIay.L(N0,NN0,Y) + d3.L(P,N0,Y) - d3.L(P,NN0,Y)*(1-LossA(N0,NN0,Y)));
f1_3d(P,Y) = min(Qpy.L(P,Y),df(Y)*(costP(P,Y) +2*costQ(P,Y)*Qpy.L(P,Y) - costG(P,Y)*(CAPpy.L(P,Y)-Qpy.L(P,Y))*log(1-Qpy.L(P,Y)/(CAPpy.L(P,Y)+epsilon))) + d1.L(P,Y)-(sum(N0$(PN(P,N0)),d3.L(P,N0,Y))+d4.L(P,Y))*(1-LossP(P,Y)));
f1_3e(P,Y) = min(CAPpy.L(P,Y),df(Y)*(costG(P,Y)*Qpy.L(P,Y)/(CAPpy.L(P,Y)+epsilon)+costG(P,Y)*log(1-Qpy.L(P,Y)/(CAPpy.L(P,Y)+epsilon)))+ d2.L(P,Y)-d1.L(P,Y));
f1_6a(N0,NN0,Y) = min( d5.L(N0,NN0,Y),CAPay.L(N0,NN0,Y)-Qay.L(N0,NN0,Y));
f1_6b(N0,NN0,Y) = CAPay.L(N0,NN0,Y) - Qa0(N0,NN0) - sum(Y0$(ORD(Y0) <= ORD(Y)),Xay.L(N0,NN0,Y0));
f1_7a(N0,NN0,Y) = min( Qay.L(N0,NN0,Y),-df(Y)*PIay.L(N0,NN0,Y) + CostA(N0,NN0,Y)+d5.L(N0,NN0,Y));
f1_7b(N0,NN0,Y) = min( Xay.L(N0,NN0,Y),df(Y)*PIXA(N0,NN0,Y) - sum(Y0$(ORD(Y0) <= ORD(Y)),d6.L(N0,NN0,Y0)));
f1_7c(N0,NN0,Y) = min( CAPay.L(N0,NN0,Y),d6.L(N0,NN0,Y)-d5.L(N0,NN0,Y));
f1_8(N0,NN0,Y) = Qay.L(N0,NN0,Y) -sum(P,Qpay.L(P,N0,NN0,Y));
f1_9(C,Y) = PIcy.L(C,Y) - DemInt(C,Y) + DemSlope(C,Y)*sum(P,Qpcny.L(P,C,Y));

*Display d1.L,d2.L,d3.L,d4.L,Qpcny.L,Xpy.L,Qpay.L,Qpy.L,CAPpy.L,d5.L,d6.L,Qay.L,Xay.L,CAPay.L,PIay.L,PIcy.L;
*Display f1_2a,f1_2b,f1_2c,f1_2d,f1_3a,f1_3b,f1_3c,f1_3d,f1_3e,f1_6a,f1_6b,f1_7a,f1_7b,f1_7c,f1_8,f1_9;



******************
* Output to files*
******************

execute_unload './auxi/loadpoint.gdx'

Parameters Qcy(C,Y) "Consumed Quantity";
Qcy(C,Y) = sum(P,Qpcny.L(P,C,Y));
Display Qcy;


file O5out /O6out.gpy/;
O5out.pw  = 32767;
put O5out;


loop((P,Y),                         put d1.L    (P,Y):12:8           / );
loop((P,Y),                         put d2.L    (P,Y):12:8           / );
loop((P,N,Y),                       put d3.L    (P,N,Y):12:8         / );
loop((P,Y),                         put d4.L    (P,Y):12:8           / );
loop((P,C,Y),                       put Qpcny.L (P,C,Y):12:8         / );
loop((P,Y),                         put Xpy.L   (P,Y):12:8           / );
loop((P,N,N0,Y)$(Ao(N,N0)),         put Qpay.L  (P,N,N0,Y):12:8      / );
loop((P,Y),                         put Qpy.L   (P,Y):12:8           / );
loop((P,Y),                         put CAPpy.L (P,Y):12:8           / );
loop((N,N0,Y)$(Ao(N,N0)),           put d5.L    (N,N0,Y):12:8        / );
loop((N,N0,Y)$(Ao(N,N0)),           put d6.L    (N,N0,Y):12:8        / );
loop((N,N0,Y)$(Ao(N,N0)),           put Qay.L   (N,N0,Y):12:8        / );
loop((N,N0,Y)$(Ao(N,N0)),           put Xay.L   (N,N0,Y):12:8        / );
loop((N,N0,Y)$(Ao(N,N0)),           put CAPay.L (N,N0,Y):12:8        / );
loop((N,N0,Y)$(Ao(N,N0)),           put PIay.L  (N,N0,Y):12:8        / );
loop((C,Y),                         put PIcy.L  (C,Y):12:8           / );



Display Qpy.L,Xpy.L;
Display Qay.L,Xay.L;

Display Qpcny.L, Qay.L,  PIcy.L;

Parameters Qpc(P,C) "Quantity from P to C", Qa(N,N0) "Arc flow", Pa(N,N0) "Price for transport", Ca(N,N0) "Cost for transport";
***2015
Qpc(P,C) = Qpcny.L(P,C,'2015');
Qa(N,N0) = Qay.L(N,N0,'2015');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2015');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2015')
Display "2015";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2020
Qpc(P,C) = Qpcny.L(P,C,'2020');
Qa(N,N0) = Qay.L(N,N0,'2020');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2020');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2020')
Display "2020";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2025
Qpc(P,C) = Qpcny.L(P,C,'2025');
Qa(N,N0) = Qay.L(N,N0,'2025');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2025');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2025')
Display "2025";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2030
Qpc(P,C) = Qpcny.L(P,C,'2030');
Qa(N,N0) = Qay.L(N,N0,'2030');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2030');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2030')
Display "2030";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2035
Qpc(P,C) = Qpcny.L(P,C,'2035');
Qa(N,N0) = Qay.L(N,N0,'2035');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2035');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2035')
Display "2035";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2040
Qpc(P,C) = Qpcny.L(P,C,'2040');
Qa(N,N0) = Qay.L(N,N0,'2040');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2040');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2040')
Display "2040";
Display Qpc,  Qa, Ca, Pa;
Display "-----";
$ontext
***2045
Qpc(P,C) = Qpcny.L(P,C,'2045');
Qa(N,N0) = Qay.L(N,N0,'2045');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2045');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2045')
Display "2045";
Display Qpc,  Qa, Ca, Pa;
Display "-----";

***2050
Qpc(P,C) = Qpcny.L(P,C,'2050');
Qa(N,N0) = Qay.L(N,N0,'2050');
Pa(N,N0)$(Qa(N,N0) gt 0) = PIay.L(N,N0,'2050');
Ca(N,N0)$(Qa(N,N0) gt 0) = CostA(N,N0,'2050')
Display "2050";
Display Qpc,  Qa, Ca, Pa;
Display "-----";



Display "*************************************";
Display "******* All Variables here **********";
Display "*************************************";

Display d1.L,d2.L,d3.L,d4.L,Qpcny.L,Xpy.L,Qpay.L,Qpy.L,CAPpy.L,d5.L,d6.L,Qay.L,Xay.L,CAPay.L,PIay.L,PIcy.L;
$offtext
Display PIcy.L;