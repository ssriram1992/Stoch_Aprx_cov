$ontext
*******************************************************************************
Author: Sriram Sankaranarayanan
File: Demand_calib.gms
Institution: Johns Hopkins University
Contact: ssankar5@jhu.edu

All rights reserved.
You are free to distribute this code for non-profit purposes
as long as this header is kept intact
*******************************************************************************
$offtext

*Make Sure to run Supply_price.gms before running this. Also after running it, rename ./auxi/supply_cost_init.gdx to ./auxi/supply_cost_iter.gdx.

$SETGLOBAL offlst "*"

option solvelink = 2;

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


$INCLUDE ./data.gms
$INCLUDE ./calib_data.gms
$INCLUDE ./manual_calib.gms

$SETGLOBAL use_prev ""

*$If exists

* Getting the initial Supply price matrix
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


$If exist ./auxi/supply_cost_init.gdx execute_loadpoint './auxi/supply_cost_init.gdx'
*Solve supply_price_init using NLP minimizing obj;
*execute_unload './auxi/supply_cost_init.gdx';

* We have now solved the initial optimization problem . Let us define a few parameters to recursively update the Demand function parameters

Parameter
*ref_price_S(C,Y) "Reference Supply price",
Qcy(C,Y) "Quantity consumed by consumer in year y",
Deviation(C,Y) "Ratio of model consumption to AEO consumption",
Devmax(Y) "Maximum deviation in the year",
Elasticity(C,Y) "Elasticity of Natural Gas",
eR(C,Y) "Reciprocal of Elasticity",
tolerance "Threshold beolw which deviation wont cause change in demand curve parameters" /0.005/,
up_it "Percentage increase in supply price as a result of large deviation" /0.1/,
lo_it "Percentage decrease in supply price as a result of large deviation" /0.1/
;

Parameter ref_price_S(C,Y);
*ref_price_S(C,Y) = Dem_Cons.m(C,Y);
*execute_load './auxi/supply_cost_iter.gdx', ref_price_S;




execute_loadpoint './auxi/supply_cost_iter.gdx';

* Elasticity number from https://www.eia.gov/analysis/studies/fuelelasticities/pdf/eia-fuelelasticities.pdf
* Note that we model elasticity as a positive number
Elasticity(C,Y) = 0.29;
eR(C,Y) = 1/elasticity(C,Y);


*Qcy(C,Y) = sum(P,Qpcny.L(P,C,Y));
*Deviation(C,Y) = Qcy(C,Y)/Consumption(C,Y);
*Display ref_price_S, Deviation;

Set iteration /i1*i10/;

ref_price_S(C,Y) = DemInt(C,Y)/(1+eR(C,Y));

Loop(iteration,

*CostG(P,Y) = 0;
* Updating the demand curve
DemInt(C,Y) = ref_price_S(C,Y) * (1 + eR(C,Y));
DemSlope(C,Y) = eR(C,Y)*ref_price_S(C,Y)/Consumption(C,Y);
Display DemInt,DemSlope;

* Solving the MCP model
option MCP=PATH;
Solve Sim_Nangam using MCP;
abort$(Sim_Nangam.solvestat > 1) "Solver status indicates that MCP did not solve correctly" ;
abort$(Sim_Nangam.modelstat > 2) "Model status indicates that MCP did not solve correctly"  ;


* Updating the supply price
Qcy(C,Y) = sum(P,Qpcny.L(P,C,Y));

Deviation(C,Y) = Qcy(C,Y)/Consumption(C,Y);
Devmax(Y) = smax(C,Deviation(C,Y));
Devmax(Y)$(Devmax(Y)<2) = 2;
Devmax(Y) = smax(Y0,Devmax(Y0));

ref_price_S(C,Y)$(Deviation(C,Y) > 1+tolerance) = ref_price_S(C,Y)*(1-lo_it*(Deviation(C,Y))/Devmax(Y));
ref_price_S(C,Y)$(Deviation(C,Y) < 1-tolerance) = ref_price_S(C,Y)*(1+up_it*(Deviation(C,Y))/Devmax(Y))/df(Y);
ref_price_S(C,Y)$(Deviation(C,Y) < 0.7) = ref_price_S(C,Y)*(1+up_it);
ref_price_S(C,Y)$(Deviation(C,Y) < 0.2) = ref_price_S(C,Y)*(1+0.5+up_it);
ref_price_S(C,Y)$(Deviation(C,Y) > 1.3) = ref_price_S(C,Y)*(1-lo_it);

Display Deviation,Qpy.L,Qcy;
execute_unload './auxi/supply_cost_iter.gdx'
)

Display '***********';
Display '***Final***'
Display '***********';

Display DemInt,DemSlope;


