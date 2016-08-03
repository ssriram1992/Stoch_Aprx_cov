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


* We have now solved the initial optimization problem . Let us define a few parameters to recursively update the Demand function parameters

Parameter
*ref_price_S(C,Y) "Reference Supply price",
Qcy(C,Y) "Quantity consumed by consumer in year y",
Deviation(C,Y) "Ratio of model consumption to AEO consumption",
Devmax(Y) "Maximum deviation in the year",
Elasticity(C,Y) "Elasticity of Natural Gas",
eR(C,Y) "Reciprocal of Elasticity",
tolerance "Threshold beolw which deviation wont cause change in demand curve parameters" /0.05/,
up_it "Percentage increase in supply price as a result of large deviation" /1/,
lo_it "Percentage decrease in supply price as a result of large deviation" /1/
;

*Parameter ref_price_S(C,Y);
*ref_price_S(C,Y) = Dem_Cons.m(C,Y);
*execute_load './auxi/supply_cost_iter.gdx', ref_price_S;





Table ref_price_S(C,Y)
              2010        2015        2020        2025        2030        2035        2040
N_ALK     1722.799    1804.419    1937.727    1590.691    1874.633    2053.631    2486.263
N_CAE     1874.236    2472.947    1905.136    2453.534    2682.670    1687.749    2100.427
N_CAW     2160.119    2007.795    2784.839    1968.323    2381.407    2719.403    2849.169
N_MEX1    1115.358    2077.659    2543.772    2063.714    1966.543    2158.825    2245.373
N_MEX2    1603.408    1966.207    2169.157    1965.343    2370.926    2404.182    2652.249
N_MEX3    1453.943    1573.932    2053.003    1938.505    2126.317    2207.035    2745.040
N_MEX4    1282.854    1294.157    2126.409    1795.674    2078.660    2474.391    2594.837
N_MEX5    1034.867    1225.259    1636.653    1877.897    2269.414    2301.324    2559.705
N_US1     1970.315    2356.151    2439.710    2372.083    2414.795    2788.166    2456.403
N_US2     1976.538    2270.693    2526.268    2280.879    2496.007    2455.416    2938.183
N_US3     2078.385    2565.149    2390.004    2294.159    2661.414    2742.173    2939.792
N_US4     2229.862    2251.911    2427.196    2147.751    2415.965    2385.425    2442.280
N_US5     2142.953    2474.167    2611.717    1790.052    1842.741    1956.312    2063.014
N_US6     1581.238    2475.972    2602.803    1790.052    1842.741    1956.312    2063.039
N_US7     1901.171    2369.053    2734.823    1990.092    2289.237    2560.549    2754.080
N_US8     1681.098    2289.422    2118.099    2208.929    1898.440    2263.506    2450.530
N_US9     2228.623    2077.722    2566.775    2141.327    1963.453    2263.477    2918.155
;









execute_loadpoint './auxi/supply_cost_iter.gdx';

* Elasticity number from https://www.eia.gov/analysis/studies/fuelelasticities/pdf/eia-fuelelasticities.pdf
* Note that we model elasticity as a positive number
Elasticity(C,Y) = 0.29;
eR(C,Y) = 1/elasticity(C,Y);


*Qcy(C,Y) = sum(P,Qpcny.L(P,C,Y));
*Deviation(C,Y) = Qcy(C,Y)/Consumption(C,Y);
*Display ref_price_S, Deviation;

Set iteration /i1*i10/;



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

Display Deviation,ref_price_S;
execute_unload './auxi/supply_cost_iter.gdx'
)

Display DemInt,DemSlope;


