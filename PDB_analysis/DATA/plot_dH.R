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

#dHvsMW
test<-cor.test(MW, dH)
test$p.value 0.001131652
test$estimate 0.3949175 


test<-cor.test(MW, dH, method="spearman")
test$p.value  4.382974e-05
test$estimate 0.4841604

test<-cor.test(MW, dH, method="kendall")
test$p.value 0.0001991861
test$estimate  0.3164743 

plot(MW, dH, pch=20, col='red', xlab="Molecular Weight", ylab="Enthalpy", text(530, 30, cex=0.8, "Pearson's corr. 0.3949175 , p-val=0.001131652\nRho 0.4841604, p-val=4.382974e-05\nTau 0.0001991861, p-val=0.3164743"), main="Enthalpy Vs Molecular Weight")
abline(lm(dH~MW), col="blue")

#####################################################################

#dHvsMM
test<-cor.test(MM, dH)
test$p.value  0.00113055
test$estimate 0.3949482 

test<-cor.test(MM, dH, method="spearman")
test$p.value  4.382974e-05
test$estimate 0.4841604 

test<-cor.test(MM, dH, method="kendall")
test$p.value  0.0001991861
test$estimate 0.3164743

plot(MM, dH, pch=20, col='red', xlab="Monoisotopic Mass", ylab="Enthalpy", text(530, 30, cex=0.8, "Pearson's corr. 0.3949482, p-val=0.00113055\nRho 0.4841604, p-val=4.382974e-05\nTau 0.3164743, p-val=0.0001991861"), main="Enthalpy Vs Monoisotopic Mass")
abline(lm(dH~MM), col="blue")

#####################################################################

#dHvsAlogP
test<-cor.test(AlogP, dH)
test$p.value 0.02459779
test$estimate -0.278648 

test<-cor.test(AlogP, dH, method="spearman")
test$p.value  0.03654546
test$estimate -0.2599007

test<-cor.test(AlogP, dH, method="kendall")
test$p.value  0.03570769
test$estimate -0.2136109 

plot(AlogP, dH, pch=20, col='red', xlab="AlogP", ylab="Enthalpy", text(1.8, 30, cex=0.8, "Pearson's corr. -0.278648, p-val=0.02459779\nRho -0.2599007, p-val=0.03654546\nTau -0.2136109, p-val=0.03570769"), main="Enthalpy Vs AlogP")
abline(lm(dH~AlogP), col="blue")

#####################################################################

#dHvsXlogP
test<-cor.test(XlogP, dH)
test$p.value 0.4619061
test$estimate 0.09285814 

test<-cor.test(XlogP, dH, method="spearman")
> test$p.value
[1] 0.239244
> test$estimate  
      rho 
0.1480403    

test<-cor.test(XlogP, dH, method="kendall")
> test$p.value
[1] 0.263937
> test$estimate 
      tau 
0.1008602 

plot(XlogP, dH, pch=20, col='red', xlab="XlogP", ylab="Enthalpy", text(3, 30, cex=0.8, "Pearson's corr. 0.09285814 , p-val=0.4619061\nRho 0.1480403, p-val=0.239244\nTau 0.1008602, p-val=0.263937"), main="Enthalpy Vs XlogP")
abline(lm(dH~XlogP), col="blue")

#####################################################################

#dHvsHacc
test<-cor.test(Hacc, dH)
> test$p.value
[1] 0.03310982
> test$estimate 
      cor 
0.2646892  

test<-cor.test(Hacc, dH, method="spearman")
> test$p.value
[1] 0.00134967
> test$estimate 
      rho 
0.3893007 

test<-cor.test(Hacc, dH, method="kendall")
> test$p.value
[1] 0.005485706
> test$estimate
      tau 
0.2489552 

plot(Hacc, dH, pch=20, col='red', xlab="Hydrogen Acceptors", ylab="Enthalpy", text(19, 30, cex=0.8, "Pearson's corr. 0.2646892, p-val=0.03310982\nRho 0.3893007, p-val=0.00134967\nTau 0.2489552, p-val=0.005485706"), main="Enthalpy Vs Hydrogen Acceptors")
abline(lm(dH~Hacc), col="blue")

#####################################################################

#dHvsHd
test<-cor.test(Hd, dH)
> test$p.value
[1] 2.015326e-07
> 
> test$estimate
      cor 
0.5923611 

test<-cor.test(Hd, dH, method="spearman")
> test$p.value
[1] 2.048603e-06
> 
> test$estimate
      rho 
0.5502736 

test<-cor.test(Hd, dH, method="kendall")
> test$p.value
[1] 2.905373e-05
> 
> test$estimate
      tau 
0.3742571 

plot(Hd, dH, pch=20, col='red', xlab="Hydrogen Donors", ylab="Enthalpy", text(10, 30, cex=0.8, "Pearson's corr. 0.5923611, p-val=2.015326e-07\nRho 0.5502736, p-val=2.048603e-06\nTau 0.3742571, p-val=2.905373e-05"), main="Enthalpy Vs Hydrogen Donors")
abline(lm(dH~Hd), col="blue")
#####################################################################

#dHvsRotBonds
test<-cor.test(RotBonds, dH)
> test$p.value
[1] 3.351347e-09
> test$estimate
      cor 
0.6545007 

test<-cor.test(RotBonds, dH, method="spearman")
> test$p.value
[1] 1.65661e-08
> test$estimate
      rho 
0.6318628 

test<-cor.test(RotBonds, dH, method="kendall")
> test$p.value
[1] 1.66609e-07
> test$estimate
      tau 
0.4612656 

plot(RotBonds, dH, pch=20, col='red', xlab="Rotating Bonds", ylab="Enthalpy", text(15, 30, cex=0.8, "Pearson's corr. 0.6545007, p-val=3.351347e-09\nRho 0.6318628, p-val=1.65661e-08\nTau 0.4612656, p-val=1.66609e-07"), main="Enthalpy Vs Rotating Bonds")
abline(lm(dH~RotBonds), col="blue")

#####################################################################

#dHvsViolLepinskiRule
test<-cor.test(violLepinskiRule, dH)
> test$p.value
[1] 0.01151525
> 
> test$estimate
      cor 
0.3115951 

test<-cor.test(violLepinskiRule, dH, method="spearman")
> test$p.value
[1] 0.002334712
> 
> test$estimate
      rho 
0.3711742 

test<-cor.test(violLepinskiRule, dH, method="kendall")
> test$p.value
[1] 0.004103984
> 
> test$estimate
      tau 
0.2786604 

plot(violLepinskiRule, dH, pch=20, col='red', xlab="No of violations of 5 Rule", text(2.5, 30, cex=0.8, "Pearson's corr. 0.3115951, p-val=0.01151525\nRho 0.3711742, p-val=0.002334712\nTau 0.2786604, p-val=0.004103984"), ylab="Enthalpy", main="Enthalpy Vs No of violations of 5 Rule")
abline(lm(dH~violLepinskiRule), col="blue")

#####################################################################

#dHvsPSA
test<-cor.test(PSA, dH)
> test$p.value
[1] 0.00228934
> test$estimate 
      cor 
0.3718413  

test<-cor.test(PSA, dH, method="spearman")
> test$p.value
[1] 0.0002876585
> 
> test$estimate
      rho 
0.4355443 

test<-cor.test(PSA, dH, method="kendall")
> test$p.value
[1] 0.006204218
> 
> test$estimate
      tau 
0.2342466 

plot(PSA, dH, pch=20, col='red', xlab="Polar Surface Area", text(300, 30, cex=0.8, "Pearson's corr. 0.3718413, p-val=0.00228934\nRho 0.4355443, p-val=0.0002876585\nTau 0.2342466, p-val=0.006204218"), ylab="Enthalpy", main="Enthalpy Vs Polar Surface Area")
abline(lm(dH~PSA), col="blue")
#####################################################################

#dHvsPolarizability
test<-cor.test(Polarizability, dH)
> test$p.value
[1] 0.0002731796
> test$estimate
      cor 
0.4401523  

test<-cor.test(Polarizability, dH, method="spearman")
> test$p.value
[1] 5.78618e-06
> test$estimate
      rho 
0.5329898 

test<-cor.test(Polarizability, dH, method="kendall")
> test$p.value
[1] 3.002823e-05
> test$estimate
     tau 
0.358837 

plot(Polarizability, dH, pch=20, col='red', xlab="Polarizability", text(58, 30, cex=0.8, "Pearson's corr. 0.4401523, p-val=0.0002731796\nRho 0.5329898, p-val=5.78618e-06\nTau 0.358837, p-val=3.002823e-05"), ylab="Enthalpy", main="Enthalpy Vs Polarizability")
abline(lm(dH~Polarizability), col="blue")

#####################################################################

#dHvsRefrIndex
test<-cor.test(RefrIndex, dH)
> test$p.value
[1] 9.080571e-07
> test$estimate
       cor 
-0.5694568 

test<-cor.test(RefrIndex, dH, method="spearman")
> test$p.value
[1] 5.165403e-08
> 
> test$estimate 
       rho 
-0.6184283 

test<-cor.test(RefrIndex, dH, method="kendall")
> test$p.value
[1] 1.381002e-07
> test$estimate
       tau 
-0.4524659 

plot(RefrIndex, dH, pch=20, col='red', xlab="Refraction Index", text(1.8, 30, cex=0.8, "Pearson's corr. -0.5694568, p-val=9.080571e-07\nRho -0.6184283, p-val=5.165403e-08\nTau -0.4524659, p-val=1.381002e-07"), ylab="Enthalpy", main="Enthalpy Vs Refraction Index")
abline(lm(dH~RefrIndex), col="blue")
#####################################################################

#dHvsMolarRefractivity
test<-cor.test(MolarRefractivity, dH)
> test$p.value
[1] 0.0002758053
> test$estimate
      cor 
0.4398853 

test<-cor.test(MolarRefractivity, dH, method="spearman")
> test$p.value
[1] 4.76566e-06
> test$estimate
      rho 
0.5370182 

test<-cor.test(MolarRefractivity, dH, method="kendall")
> test$p.value
[1] 2.396776e-05
> test$estimate 
      tau 
0.3625069  

plot(MolarRefractivity, dH, pch=20, col='red', xlab="Molar Refractivity", text(145, 30, cex=0.8, "Pearson's corr. 0.4398853, p-val=0.0002758053\nRho 0.5370182, p-val=4.76566e-06\nTau 0.3625069, p-val=2.396776e-05"), ylab="Enthalpy", main="Enthalpy Vs Molar Refractivity")
abline(lm(dH~MolarRefractivity), col="blue")
#####################################################################

#dHvsMolar_Volume
test<-cor.test(Molar_Volume, dH)
> test$p.value
[1] 7.329511e-06
> test$estimate
      cor 
0.5280102 

test<-cor.test(Molar_Volume, dH, method="spearman")
> test$p.value
[1] 2.36655e-06
> test$estimate
      rho 
0.5511328 

test<-cor.test(Molar_Volume, dH, method="kendall")
> test$p.value
[1] 6.722229e-06
> test$estimate
      tau 
0.3861833 
plot(Molar_Volume, dH, pch=20, col='red', xlab="Molar Volume", text(400, 30, cex=0.8, "Pearson's corr. 0.5280102, p-val=7.329511e-06\nRho 0.5511328, p-val=2.36655e-06\nTau 0.3861833, p-val=6.722229e-06"), ylab="Enthalpy", main="Enthalpy Vs Molar Volume")
abline(lm(dH~Molar_Volume), col="blue")
#####################################################################

dHvssurfTension
test<-cor.test(surfTension, dH)
> test$p.value
[1] 0.002943733
> test$estimate
       cor 
-0.3659223 

test<-cor.test(surfTension, dH, method="spearman")
> test$p.value
[1] 1.037559e-05
> test$estimate
       rho 
-0.5205445 

test<-cor.test(surfTension, dH, method="kendall")
> test$p.value
[1] 3.600421e-05
> test$estimate
       tau 
-0.3547275 

plot(surfTension, dH, pch=20, col='red', xlab="Surface Tension", text(200, 30, cex=0.8, "Pearson's corr. -0.3659223, p-val=0.002943733\nRho -0.5205445, p-val=1.037559e-05\nTau -0.3547275, p-val=3.600421e-05"), ylab="Enthalpy", main="Enthalpy Vs Surface Tension")
abline(lm(dH~surfTension), col="blue")
#####################################################################

