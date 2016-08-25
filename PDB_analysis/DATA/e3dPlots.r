header <- read.table("Analysis_dataSet_ProACt.txt", nrows = 1, header = FALSE, sep ="\t", stringsAsFactors = FALSE)
itcVSproACtTable<-read.table("Analysis_dataSet_ProACt.txt", skip = 2, header = FALSE, sep ="\t")
colnames(itcVSproACtTable) <- unlist(header)

itcVSproACtTable

dG<-itcVSproACtTable$DeltaG
dH<-itcVSproACtTable$deltaH
TdS<-itcVSproACtTable$TdeltaS
K<-itcVSproACtTable$Kd

HBondsNo<-itcVSproACtTable$HBondsNo

Polar_Contacts<-itcVSproACtTable$Polar_Contacts
Apolar_Contacts<-itcVSproACtTable$Apolar_Contacts

Polar_Water_Contacts<-itcVSproACtTable$Polar_Water_Contacts
Apolar_Water_Contacts<-itcVSproACtTable$Apolar_Water_Contacts

Surface_Waters<-itcVSproACtTable$Surface_Waters
Cleft_Waters<-itcVSproACtTable$Cleft_Waters
Buried_Waters<-itcVSproACtTable$Buried_Waters

library(scatterplot3d)
#####################################################################
dGvsContacts <-scatterplot3d(Polar_Contacts, Apolar_Contacts,dG, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Contacts")
fit <- lm(dG ~ Polar_Contacts + Apolar_Contacts)
dGvsContacts$plane3d(fit)
summary(fit)
> summary(fit)

Call:
lm(formula = dG ~ Polar_Contacts + Apolar_Contacts)

Residuals:
     Min       1Q   Median       3Q      Max 
-20.9006  -4.9413  -0.5788   6.4171  16.0622 

Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
(Intercept)     -3.062e+01  2.445e+00 -12.523   <2e-16 ***
Polar_Contacts  -3.418e-04  5.988e-02  -0.006   0.9955    
Apolar_Contacts -4.448e-02  1.707e-02  -2.605   0.0115 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 7.988 on 61 degrees of freedom
Multiple R-squared:  0.1046,    Adjusted R-squared:  0.07521 
F-statistic: 3.562 on 2 and 61 DF,  p-value: 0.03443


dHvsContacts <-scatterplot3d(Polar_Contacts, Apolar_Contacts,dH, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs Contacts")
fit <- lm(dH ~ Polar_Contacts+Apolar_Contacts)
dHvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dG ~ Polar_Contacts + Apolar_Contacts)

Residuals:
     Min       1Q   Median       3Q      Max 
-20.9006  -4.9413  -0.5788   6.4171  16.0622 

Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
(Intercept)     -3.062e+01  2.445e+00 -12.523   <2e-16 ***
Polar_Contacts  -3.418e-04  5.988e-02  -0.006   0.9955    
Apolar_Contacts -4.448e-02  1.707e-02  -2.605   0.0115 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 7.988 on 61 degrees of freedom
Multiple R-squared:  0.1046,    Adjusted R-squared:  0.07521 
F-statistic: 3.562 on 2 and 61 DF,  p-value: 0.03443

TdSvsContacts <-scatterplot3d(Polar_Contacts, Apolar_Contacts,TdS, pch=16, highlight.3d=TRUE, type="h", main="TdS vs Contacts")
fit <- lm(TdS ~ Polar_Contacts+Apolar_Contacts)
TdSvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = TdS ~ Polar_Contacts + Apolar_Contacts)

Residuals:
    Min      1Q  Median      3Q     Max 
-67.035 -14.490   6.895  17.442  71.973 

Coefficients:
                 Estimate Std. Error t value Pr(>|t|)    
(Intercept)     -40.64412    8.45782  -4.806 1.04e-05 ***
Polar_Contacts    1.00206    0.20716   4.837 9.31e-06 ***
Apolar_Contacts   0.41017    0.05906   6.945 2.88e-09 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 27.63 on 61 degrees of freedom
Multiple R-squared:  0.4948,    Adjusted R-squared:  0.4783 
F-statistic: 29.88 on 2 and 61 DF,  p-value: 9.005e-10

KvsContacts <-scatterplot3d(Polar_Contacts, Apolar_Contacts,K, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs Contacts")
fit <- lm(K ~ Polar_Contacts+Apolar_Contacts)
TdSvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = K ~ Polar_Contacts + Apolar_Contacts)

Residuals:
   Min     1Q Median     3Q    Max 
-66.85 -42.61 -16.74  -5.07 370.35 

Coefficients:
                Estimate Std. Error t value Pr(>|t|)   
(Intercept)      90.0516    26.6273   3.382  0.00126 **
Polar_Contacts   -0.7213     0.6522  -1.106  0.27308   
Apolar_Contacts  -0.4304     0.1859  -2.315  0.02400 * 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 87 on 61 degrees of freedom
Multiple R-squared:  0.08592,   Adjusted R-squared:  0.05595 
F-statistic: 2.867 on 2 and 61 DF,  p-value: 0.06457

#####################################################################

dGvsContacts <-scatterplot3d(Polar_Water_Contacts, Apolar_Water_Contacts,dG, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Water Contacts")
fit <- lm(dG ~ Polar_Water_Contacts+Apolar_Water_Contacts)
dGvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dG ~ Polar_Water_Contacts + Apolar_Water_Contacts)

Residuals:
     Min       1Q   Median       3Q      Max 
-16.1624  -5.2854   0.1387   5.4881  16.6194 

Coefficients:
                       Estimate Std. Error t value Pr(>|t|)    
(Intercept)           -28.39252    2.54307 -11.165 2.23e-16 ***
Polar_Water_Contacts   -0.02192    0.06739  -0.325 0.746020    
Apolar_Water_Contacts   0.14203    0.03446   4.122 0.000115 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 7.307 on 61 degrees of freedom
Multiple R-squared:  0.2507,    Adjusted R-squared:  0.2262 
F-statistic: 10.21 on 2 and 61 DF,  p-value: 0.00015

dHvsContacts <-scatterplot3d(Polar_Water_Contacts, Apolar_Water_Contacts, dH, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs Water Contacts")
fit <- lm(dH ~ Polar_Water_Contacts+Apolar_Water_Contacts)
dHvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dH ~ Polar_Water_Contacts + Apolar_Water_Contacts)

Residuals:
   Min     1Q Median     3Q    Max 
-86.62  -9.35   5.29  15.55  43.36 

Coefficients:
                      Estimate Std. Error t value Pr(>|t|)    
(Intercept)           -72.8234     9.7635  -7.459 3.76e-10 ***
Polar_Water_Contacts   -1.2035     0.2587  -4.652 1.82e-05 ***
Apolar_Water_Contacts  -0.1921     0.1323  -1.452    0.152    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 28.05 on 61 degrees of freedom
Multiple R-squared:  0.3895,    Adjusted R-squared:  0.3694 
F-statistic: 19.46 on 2 and 61 DF,  p-value: 2.912e-07

TdSvsContacts <-scatterplot3d(Polar_Water_Contacts, Apolar_Water_Contacts,TdS, pch=16, highlight.3d=TRUE, type="h", main="TdS vs Water Contacts")
fit <- lm(TdS ~ Polar_Water_Contacts+Apolar_Water_Contacts)
TdSvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = TdS ~ Polar_Water_Contacts + Apolar_Water_Contacts)

Residuals:
    Min      1Q  Median      3Q     Max 
-79.987  -8.166   5.409  17.006  54.148 

Coefficients:
                      Estimate Std. Error t value Pr(>|t|)    
(Intercept)           -44.3645    10.3241  -4.297 6.33e-05 ***
Polar_Water_Contacts   -1.1776     0.2736  -4.304 6.17e-05 ***
Apolar_Water_Contacts  -0.3334     0.1399  -2.383   0.0203 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 29.66 on 61 degrees of freedom
Multiple R-squared:  0.4179,    Adjusted R-squared:  0.3988 
F-statistic:  21.9 on 2 and 61 DF,  p-value: 6.791e-08

KvsContacts <-scatterplot3d(Polar_Water_Contacts, Apolar_Water_Contacts,K, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs Water Contacts")
fit <- lm(K ~ Polar_Water_Contacts+Apolar_Water_Contacts)
KvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = K ~ Polar_Water_Contacts + Apolar_Water_Contacts)

Residuals:
   Min     1Q Median     3Q    Max 
-85.58 -42.41 -13.32   7.02 351.12 

Coefficients:
                      Estimate Std. Error t value Pr(>|t|)    
(Intercept)           120.8101    29.1861   4.139 0.000109 ***
Polar_Water_Contacts    1.4133     0.7734   1.827 0.072518 .  
Apolar_Water_Contacts   0.6098     0.3955   1.542 0.128301    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 83.86 on 61 degrees of freedom
Multiple R-squared:  0.1507,    Adjusted R-squared:  0.1229 
F-statistic: 5.413 on 2 and 61 DF,  p-value: 0.006855


#####################################################################
header <- read.table("Analysis_dataSet.txt", nrows = 1, header = FALSE, sep ="\t", stringsAsFactors = FALSE)
itcVSfeaturesTable<-read.table("Analysis_dataSet.txt", skip = 2, header = FALSE, sep ="\t")
colnames(itcVSfeaturesTable) <- unlist(header)

itcVSfeaturesTable

dG<-itcVSfeaturesTable$DeltaG
dH<-itcVSfeaturesTable$deltaH
TdS<-itcVSfeaturesTable$TdeltaS
K<-itcVSfeaturesTable$Kd

MW<-itcVSfeaturesTable$MoleWeight
MM<-itcVSfeaturesTable$MomoisMass

AlogP<-itcVSfeaturesTable$AlogP
XlogP<-itcVSfeaturesTable$XlogP


Hacc<-itcVSfeaturesTable$H_acceptors
Hd<-itcVSfeaturesTable$H_donors
RotBonds<-itcVSfeaturesTable$FreelyRotBonds
violLepinskiRule<-itcVSfeaturesTable$RuleOf5Violations

PSA<-itcVSfeaturesTable$PolarSurfaceArea
Polarizability<-itcVSfeaturesTable$Polarizability
RefrIndex<-itcVSfeaturesTable$RefractionIndex
MolarRefractivity<-itcVSfeaturesTable$MolarRefractivity
surfTension<-itcVSfeaturesTable$Surface_Tension
Molar_Volume<-itcVSfeaturesTable$Molar_Volume

#####################################################################
dGvsContacts <-scatterplot3d(Polarizability, MW,dG, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Polar Surface Area and Molecular Weight")
fit <- lm(dG ~ Polarizability+MW)
dGvsContacts$plane3d(fit)
summary(fit)

dHvsContacts <-scatterplot3d(dH,AlogP, MoleWeight, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs AlogP and Molecular Weight")
fit <- lm(dH ~ AlogP+MoleWeight)
TdSvsContacts$plane3d(fit)
summary(fit)

TdSvsContacts <-scatterplot3d(TdS,AlogP, MoleWeight, pch=16, highlight.3d=TRUE, type="h", main="TdS vs AlogP and Molecular Weight")
fit <- lm(TdS ~ AlogP+MoleWeight)
TdSvsContacts$plane3d(fit)
summary(fit)

KvsContacts <-scatterplot3d(K,AlogP, MoleWeight, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs AlogP and Molecular Weight")
fit <- lm(K ~ AlogP+MoleWeight)
TdSvsContacts$plane3d(fit)
summary(fit)


#####################################################################
dGvsContacts <-scatterplot3d(dG,Polarizability, surfTension, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Polarizabiliry and Surface Tension")
fit <- lm(dG ~ Polarizability+Surface_Tension)
TdSvsContacts$plane3d(fit)
summary(fit)

dHvsContacts <-scatterplot3d(dH,Polarizability, Surface_Tension, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs Polarizabiliry and Surface Tension")
fit <- lm(dH ~ Polarizability+Surface_Tension)
TdSvsContacts$plane3d(fit)
summary(fit)

TdSvsContacts <-scatterplot3d(TdS,Polarizability, Surface_Tension, pch=16, highlight.3d=TRUE, type="h", main="TdS vs Polarizabiliry and Surface Tension")
fit <- lm(TdS ~ Polarizability+Surface_Tension)
TdSvsContacts$plane3d(fit)
summary(fit)

KvsContacts <-scatterplot3d(K,Polarizability, Surface_Tension, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs Polarizabiliry and Surface Tension")
fit <- lm(K ~ Polarizability+Surface_Tension)
TdSvsContacts$plane3d(fit)
summary(fit)

##################################################################
#####################################################################
dGvsContacts <-scatterplot3d(dG,MW, Molar_Volume, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Polarizabiliry and Surface Tension")
fit <- lm(dG ~ MW+Molar_Volume)
TdSvsContacts$plane3d(fit)
summary(fit)

dHvsContacts <-scatterplot3d(dH,MW, Molar_Volume, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs Polarizabiliry and Surface Tension")
fit <- lm(dH ~ MW+Molar_Volume)
TdSvsContacts$plane3d(fit)
summary(fit)

TdSvsContacts <-scatterplot3d(TdS,MW, Molar_Volume, pch=16, highlight.3d=TRUE, type="h", main="TdS vs Polarizabiliry and Surface Tension")
fit <- lm(TdS ~ MW+Molar_Volume)
TdSvsContacts$plane3d(fit)
summary(fit)

KvsContacts <-scatterplot3d(K,MW, Molar_Volume, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs Polarizabiliry and Surface Tension")
fit <- lm(K ~ MW+Molar_Volume)
TdSvsContacts$plane3d(fit)
summary(fit)

#####################################################################
library(scatterplot3d)
dGvsContacts <-scatterplot3d(RotBonds, Hd,dG, pch=16, highlight.3d=TRUE, type="h", main="Gibb's energy vs Polarizabiliry and Surface Tension")
fit <- lm(dG ~ RotBonds+Hacc)
dGvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dG ~ RotBonds + Hacc)

Residuals:
    Min      1Q  Median      3Q     Max 
-35.319  -4.302   0.439   7.096  15.625 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) -35.9077     3.1596 -11.365   <2e-16 ***
RotBonds     -0.4432     0.2400  -1.847   0.0695 .  
Hacc          0.2709     0.4936   0.549   0.5851    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 9.064 on 62 degrees of freedom
Multiple R-squared:  0.06263,   Adjusted R-squared:  0.03239 
F-statistic: 2.071 on 2 and 62 DF,  p-value: 0.1347

dHvsContacts <-scatterplot3d(RotBonds, Hd, dH, pch=16, highlight.3d=TRUE, type="h", main="Enthalpy vs Polarizabiliry and Surface Tension")
fit <- lm(dH ~ RotBonds+Hacc)
dHvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dH ~ RotBonds + Hacc)

Residuals:
    Min      1Q  Median      3Q     Max 
-96.767  -6.285   5.507  13.295  52.520 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) -28.1984     9.1326  -3.088  0.00302 ** 
RotBonds      4.7745     0.6937   6.883 3.43e-09 ***
Hacc         -3.2622     1.4267  -2.287  0.02565 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 26.2 on 62 degrees of freedom
Multiple R-squared:  0.4728,    Adjusted R-squared:  0.4558 
F-statistic:  27.8 on 2 and 62 DF,  p-value: 2.402e-09

TdSvsContacts <-scatterplot3d(RotBonds, Hacc,TdS, pch=16, highlight.3d=TRUE, type="h", main="TdS vs No of Rotating Bonds and H-bond acceptors")
fit <- lm(TdS ~ RotBonds+Hacc)
TdSvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = TdS ~ RotBonds + Hacc)

Residuals:
    Min      1Q  Median      3Q     Max 
-62.276  -6.840   4.568  12.847  45.552 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept)   7.7047     8.4990   0.907  0.36816    
RotBonds      5.2057     0.6456   8.063 3.07e-11 ***
Hacc         -3.5306     1.3277  -2.659  0.00995 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 24.38 on 62 degrees of freedom
Multiple R-squared:  0.5524,    Adjusted R-squared:  0.5379 
F-statistic: 38.25 on 2 and 62 DF,  p-value: 1.509e-11


TdSvsContacts <-scatterplot3d(RotBonds, Hd,TdS, pch=16, highlight.3d=TRUE, type="h", main="TdS vs No of Rotating Bonds and H-bond donors")
fit <- lm(dG ~ RotBonds+Hd)
TdSvsContacts$plane3d(fit)
summary(fit)
Call:
lm(formula = dG ~ RotBonds + Hd)

Residuals:
    Min      1Q  Median      3Q     Max 
-33.227  -4.687  -0.222   5.581  17.584 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) -40.1236     2.3890 -16.795  < 2e-16 ***
RotBonds     -1.0406     0.2723  -3.821  0.00031 ***
Hd            1.8058     0.5636   3.204  0.00214 ** 
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 8.416 on 62 degrees of freedom
Multiple R-squared:  0.1919,    Adjusted R-squared:  0.1658 
F-statistic:  7.36 on 2 and 62 DF,  p-value: 0.001355

Call:
lm(formula = dH ~ RotBonds + Hd)

Residuals:
     Min       1Q   Median       3Q      Max 
-106.199   -8.146    3.258   13.648   58.211 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) -53.3552     7.6314  -6.992 2.22e-09 ***
RotBonds      2.8189     0.8699   3.241  0.00192 ** 
Hd            2.4471     1.8004   1.359  0.17901    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 26.88 on 62 degrees of freedom
Multiple R-squared:  0.4449,    Adjusted R-squared:  0.427 
F-statistic: 24.85 on 2 and 62 DF,  p-value: 1.189e-08


Call:
lm(formula = TdS ~ RotBonds + Hd)

Residuals:
    Min      1Q  Median      3Q     Max 
-73.882  -6.365   4.760  12.930  56.578 

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept) -13.1628     7.2974  -1.804   0.0761 .  
RotBonds      3.8555     0.8318   4.635 1.89e-05 ***
Hd            0.6223     1.7216   0.361   0.7190    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 25.71 on 62 degrees of freedom
Multiple R-squared:  0.5024,    Adjusted R-squared:  0.4863 
F-statistic: 31.29 on 2 and 62 DF,  p-value: 4.022e-10


KvsContacts <-scatterplot3d(K,HBondsNo, Hacc, pch=16, highlight.3d=TRUE, type="h", main="Affinity vs Polarizabiliry and Surface Tension")
fit <- lm(dH ~ HBondsNo+Hacc)
TdSvsContacts$plane3d(fit)
summary(fit)

#####################################################################
