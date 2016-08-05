Table cPfac(P,Y)
         2010  2015   2020   2025   2030   2035   2040
P_ALK    25.61 47.52  49.59  20.85  22.89  23.08  27.23
P_CE     24.47 35.19  31.04  17.15  34.99  30.37  44.90
P_CW     0.083 0.200  0.474  0.472  0.594  0.404  0.398
P_MEX2   24.71 36.49  39.29  20.37  21.89  17.98  22.65
P_MEX5   1.986 1.927  6.688  2.926  3.256  2.705  2.823
P_U2     1.002 0.822  0.724  0.594  0.573  0.429  0.545
P_U3     12.36 21.62  23.08  12.61  13.65  8.709  11.73
P_U4     10.71 16.83  14.87  10.77  8.818  6.385  10.50
P_U5     12.30 23.50  20.91  9.496  10.13  8.003  10.65
P_U6     17.50 23.51  23.53  13.88  14.93  13.73  16.62
P_U7     0.039 0.067  0.056  0.034  0.036  0.041  0.052
P_U8     0.422 0.530  0.320  0.220  0.237  0.193  0.266
P_U9     15.50 25.48  24.49  14.52  14.79  11.96  13.69
;

Display CostP;

CostP(P,Y) = CostP(P,Y)*cPfac(P,Y)/df(Y);

Display CostP;

CostQ(P,Y) = CostQ(P,Y)*cPfac(P,Y)/df(Y);

CostG(P,'2010') = CostG(P,'2010')*0.7;


CostG('P_CE',Y) = CostG('P_CE',Y)*5.76/df(Y)/df(Y);
CostG('P_CE','2010') = CostG('P_CE','2010')*0.9;

CostG('P_CW','2010') = CostG('P_CW','2010')*0.9*0.9*0.85;
CostG('P_CW','2015') = CostG('P_CW','2015')*0.95;
CostG('P_CW','2035') = CostG('P_CW','2035')*0.9;
CostG('P_CW',Y) = CostG('P_CW',Y)/2.2;


CostG('P_MEX2','2010') = CostG('P_MEX2','2010')*0.4;
CostG('P_MEX2','2015') = CostG('P_MEX2','2015')*1.5;

CostG('P_MEX5','2010') = CostG('P_MEX5','2010')*1.17;


CostG('P_U2','2010') = CostG('P_U2','2010')*0.7;
CostG('P_U2','2015') = CostG('P_U2','2015')*0.7;
CostG('P_U2','2020') = CostG('P_U2','2020')*0.7;
CostG('P_U2','2025') = CostG('P_U2','2025')*0.50;
CostG('P_U2','2030') = CostG('P_U2','2030')*0.50;
CostG('P_U2','2035') = CostG('P_U2','2035')*0.45;
CostG('P_U2','2040') = CostG('P_U2','2040')*0.50;

CostG('P_U3','2010') = CostG('P_U3','2010')*1/0.95;
CostG('P_U3','2025') = CostG('P_U3','2025')*0.75;
CostG('P_U3',Y) = CostG('P_U3',Y)*0.85*df(Y);

CostG('P_U4','2010') = CostG('P_U4','2010')*0.7/0.95;
CostG('P_U4','2025') = CostG('P_U4','2025')*0.75;

CostG('P_U5',Y) = CostG('P_U5',Y)*0.7;
CostG('P_U5','2010') = CostG('P_U5','2010')*0.9;

CostG('P_U6','2010') = CostG('P_U6','2010')*0.15;
CostG('P_U6','2015') = CostG('P_U6','2015')*1.2;
CostG('P_U6','2020') = CostG('P_U6','2020')*1.05;
*CostG('P_U6','2040') = CostG('P_U6','2040')*0.8;

CostG('P_U7','2010') = CostG('P_U7','2010')*0.92;
CostG('P_U7','2015') = CostG('P_U7','2015')*1.25;
CostG('P_U7','2020') = CostG('P_U7','2020')*1.2;
CostG('P_U7','2025') = CostG('P_U7','2025')*0.75;
CostG('P_U7','2030') = CostG('P_U7','2030')*0.8;
CostG('P_U7','2035') = CostG('P_U7','2035')*0.75;
CostG('P_U7','2040') = CostG('P_U7','2040')*0.82;
CostG('P_U7',Y) = CostG('P_U7',Y)/4.8;


CostG('P_U8','2010') = CostG('P_U8','2010')*0.95;
CostG('P_U8','2015') = CostG('P_U8','2015')*1.05;
CostG('P_U8','2020') = CostG('P_U8','2020')*1;
CostG('P_U8','2025') = CostG('P_U8','2025')*0.65;
CostG('P_U8','2030') = CostG('P_U8','2030')*0.70;
CostG('P_U8','2035') = CostG('P_U8','2035')*0.60;
CostG('P_U8','2040') = CostG('P_U8','2040')*0.75;
CostG('P_U8',Y) = CostG('P_U8',Y)/3;


CostG('P_U9','2010') = CostG('P_U9','2010')*0.1;
CostG('P_U9',Y) = CostG('P_U9',Y)*1.1;



* Tariff editing

* THe below ones to ensure that flow happens in all the pipelines

CostA('N_US8','N_US9',Y) = CostA('N_US8','N_US9',Y);
CostA(N0,'N_US6',Y) = CostA(N0,'N_US6',Y)*4;
