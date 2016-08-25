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
test<-cor.test(MW, TdS)
> test$estimate
      cor 
0.4990683 
> test$p.value
[1] 2.32016e-05


test<-cor.test(MW, TdS, method="spearman")
> test$p.valuetest$estimate
NULL
> test$p.value
[1] 9.061669e-08

test<-cor.test(MW, TdS, method="kendall")
> test$estimate
      tau 
0.3931586 
> test$p.value
[1] 3.829905e-06

plot(MW, TdS, pch=20, col='red', xlab="Molecular Weight", ylab="TdS", text(530, 65, cex=0.8, "Pearson's corr. 0.4990683 , p-val=2.32016e-05\nRho NULL, p-val=9.061669e-08\nTau 0.3931586, p-val=3.829905e-06"), main="Temperature*Entropy Vs Molecular Weight")
abline(lm(TdS~MW), col="blue")

#####################################################################

#TdSvsMM
test<-cor.test(MM, TdS)
> test$estimate
      cor 
0.4990755 
> test$p.value
[1] 2.319424e-05

test<-cor.test(MM, TdS, method="spearman")
> test$estimate
     rho 
0.605595 
> test$p.value
[1] 9.061669e-08

test<-cor.test(MM, TdS, method="kendall")
> test$estimate
      tau 
0.3931586 
> test$p.value
[1] 3.829905e-06

plot(MM, TdS, pch=20, col='red', xlab="Monoisotopic Mass", ylab="TdS", text(530, 65, cex=0.8, "Pearson's corr. 0.4990755, p-val=2.319424e-05\nRho 0.605595, p-val=9.061669e-08\nTau 0.3931586, p-val=3.829905e-06"), main="Temperature*Entropy Vs Monoisotopic Mass")
abline(lm(TdS~MM), col="blue")

#####################################################################

#TdSvsAlogP
test<-cor.test(AlogP, TdS)
> test$estimate
       cor 
-0.2495879 
> test$p.value
[1] 0.04495744

test<-cor.test(AlogP, TdS, method="spearman")
> test$estimate
       rho 
-0.2303142 
> test$p.value
[1] 0.06493255

test<-cor.test(AlogP, TdS, method="kendall")
> test$estimate
       tau 
-0.1886888 
> test$p.value
[1] 0.06362786

plot(AlogP, TdS, pch=20, col='red', xlab="AlogP", ylab="TdS", text(1.8, 50, cex=0.8, "Pearson's corr. -0.2495879, p-val=0.04495744\nRho -0.2303142, p-val=0.06493255\nTau -0.1886888, p-val=0.06362786"), main="Temperature*Entropy Vs AlogP")
abline(lm(TdS~AlogP), col="blue")

#####################################################################

#TdSvsXlogP
test<-cor.test(XlogP, TdS)
> test$estimate
      cor 
0.1664688 
> test$p.value
[1] 0.1850577

test<-cor.test(XlogP, TdS, method="spearman")
> test$estimate
     rho 
0.229081 
> test$p.value
[1] 0.06642169  

test<-cor.test(XlogP, TdS, method="kendall")
> test$estimate
      tau 
0.1708096 
> test$p.value 
[1] 0.05856151

plot(XlogP, TdS, pch=20, col='red', xlab="XlogP", ylab="TdS", text(3, 55, cex=0.8, "Pearson's corr. 0.1664688 , p-val=0.1850577\nRho 0.229081, p-val=0.06642169\nTau 0.1708096, p-val=0.05856151"), main="Temperature*Entropy Vs XlogP")
abline(lm(TdS~XlogP), col="blue")

#####################################################################

#TdSvsHacc
test<-cor.test(Hacc, TdS)
> test$estimate
      cor 
0.2879649 
> test$p.value
[1] 0.0200128

test<-cor.test(Hacc, TdS, method="spearman")
> test$estimate
      rho 
0.4515787 
> test$p.value 
[1] 0.0001595213

test<-cor.test(Hacc, TdS, method="kendall")
> test$estimate
      tau 
0.3184718 
> test$p.value
[1] 0.0003827889
 

plot(Hacc, TdS, pch=20, col='red', xlab="Hydrogen Acceptors", ylab="TdS", text(18, 60, cex=0.8, "Pearson's corr. 0.2879649, p-val=0.0200128\nRho 0.4515787, p-val=0.0001595213\nTau 0.3184718, p-val=0.0003827889"), main="Temperature*Entropy Vs Hydrogen Acceptors")
abline(lm(TdS~Hacc), col="blue")

#####################################################################

#TdSvsHd
test<-cor.test(Hd, TdS)
> test$estimate
      cor 
0.5743824 
> test$p.value
[1] 5.646268e-07

test<-cor.test(Hd, TdS, method="spearman")
> test$estimate
      rho 
0.5326142 
> test$p.value
[1] 4.949119e-06

test<-cor.test(Hd, TdS, method="kendall")
> test$estimate
      tau 
0.3497326 
> test$p.value 
[1] 9.386897e-05

plot(Hd, TdS, pch=20, col='red', xlab="Hydrogen Donors", ylab="TdS", text(11, 60, cex=0.8, "Pearson's corr. 0.5743824, p-val=5.646268e-07\nRho 0.5326142, p-val=4.949119e-06\nTau 0.3497326, p-val=9.386897e-05"), main="Temperature*Entropy Vs Hydrogen Donors")
abline(lm(TdS~Hd), col="blue")
#####################################################################

#TdSvsRotBonds
test<-cor.test(RotBonds, TdS)
> test$estimate
      cor 
0.7080317 
> test$p.value
[1] 4.224487e-11

test<-cor.test(RotBonds, TdS, method="spearman")
t> test$estimate
      rho 
0.7043739 
> test$p.value
[1] 5.87338e-11

test<-cor.test(RotBonds, TdS, method="kendall")
> test$estimate
      tau 
0.5348345 
> test$p.value
[1] 1.307422e-09

plot(RotBonds, TdS, pch=20, col='red', xlab="Rotating Bonds", ylab="TdS", text(15, 60, cex=0.8, "Pearson's corr. 0.7080317, p-val=4.224487e-11\nRho 0.7043739, p-val=5.87338e-11\nTau 0.5348345, p-val=1.307422e-09"), main="Temperature*Entropy Vs Rotating Bonds")
abline(lm(TdS~RotBonds), col="blue")
#####################################################################

#TdSvsViolLepinskiRule
test<-cor.test(violLepinskiRule, TdS)
> test$estimate
     cor 
0.295176 
> test$p.value
[1] 0.01698365

test<-cor.test(violLepinskiRule, TdS, method="spearman")
> test$estimate
      rho 
0.3821104 
> test$p.valu
[1] 0.001683637

test<-cor.test(violLepinskiRule, TdS, method="kendall")
> test$estimate
      tau 
0.2846327 
> test$p.value
[1] 0.003379829

plot(violLepinskiRule, TdS, pch=20, col='red', xlab="No of violations of 5 Rule", text(2.5, 60, cex=0.8, "Pearson's corr. 0.295176, p-val=0.01698365\nRho 0.3821104, p-val=0.001683637\nTau 0.2846327, p-val=0.003379829"), ylab="TdS", main="Temperature*Entropy Vs No of violations of 5 Rule")
abline(lm(TdS~violLepinskiRule), col="blue")

#####################################################################

#TdSvsPSA
test<-cor.test(PSA, TdS)
> test$estimate
      cor 
0.3826071 
> test$p.value 
[1] 0.001658383  

test<-cor.test(PSA, TdS, method="spearman")
> test$estimate
      rho 
0.4852117 
> test$p.value
[1] 4.194734e-05

test<-cor.test(PSA, TdS, method="kendall")
> test$estimate
      tau 
0.3017317 
> test$p.value
[1] 0.0004243631

plot(PSA, TdS, pch=20, col='red', xlab="Polar Surface Area", text(300, 60, cex=0.8, "Pearson's corr. 0.3826071, p-val=0.001658383\nRho 0.4852117, p-val=4.194734e-05\nTau 0.3017317, p-val=0.0004243631"), ylab="TdS", main="Temperature*Entropy Vs Polar Surface Area")
abline(lm(TdS~PSA), col="blue")
#####################################################################

#TdSvsPolarizability
test<-cor.test(Polarizability, TdS)
> test$estimate
      cor 
0.5565137 
> test$p.value 
[1] 1.796888e-06

test<-cor.test(Polarizability, TdS, method="spearman")
> test$estimate
      rho 
0.6575594 
> test$p.value
[1] 3.574694e-09

test<-cor.test(Polarizability, TdS, method="kendall")
> test$estimate
     tau 
0.443174 
> test$p.value
[1] 2.564984e-07

plot(Polarizability, TdS, pch=20, col='red', xlab="Polarizability", text(58, 60, cex=0.8, "Pearson's corr. 0.5565137, p-val=1.796888e-06\nRho 0.6575594, p-val=3.574694e-09\nTau 0.443174, p-val=2.564984e-07"), ylab="TdS", main="Temperature*Entropy Vs Polarizability")
abline(lm(TdS~Polarizability), col="blue")
#####################################################################

#TdSvsRefrIndex
test<-cor.test(RefrIndex, TdS)
> test$estimate
       cor 
-0.5975921 
> test$p.value
[1] 1.85444e-07 

test<-cor.test(RefrIndex, TdS, method="spearman")
> test$estimate
       rho 
-0.6057727 
> test$p.value 
[1] 1.135041e-07

test<-cor.test(RefrIndex, TdS, method="kendall")
> test$estimate
       tau 
-0.4331607 
> test$p.value
[1] 4.610949e-07

plot(RefrIndex, TdS, pch=20, col='red', xlab="Refraction Index", text(1.8, 60, cex=0.8, "Pearson's corr. -0.5975921, p-val=1.85444e-07\nRho -0.6057727, p-val=1.135041e-07\nTau -0.4331607, p-val=4.610949e-07"), ylab="TdS", main="Temperature*Entropy Vs Refraction Index")
abline(lm(TdS~RefrIndex), col="blue")
#####################################################################

#TdSvsMolarRefractivity
test<-cor.test(MolarRefractivity, TdS)
> test$estimate
      cor 
0.5563028 
> test$p.value
[1] 1.81656e-06

test<-cor.test(MolarRefractivity, TdS, method="spearman")
> test$estimate
      rho 
0.6611485 
> test$p.value
[1] 2.743457e-09

test<-cor.test(MolarRefractivity, TdS, method="kendall")
> test$estimate
      tau 
0.4476505 
> test$p.value 
[1] 1.835393e-07

plot(MolarRefractivity, TdS, pch=20, col='red', xlab="Molar Refractivity", text(150, 60, cex=0.8, "Pearson's corr. 0.5563028, p-val=1.81656e-06\nRho 0.6611485, p-val=2.743457e-09\nTau 0.4476505, p-val=1.835393e-07"), ylab="TdS", main="Temperature*Entropy Vs Molar Refractivity")
abline(lm(TdS~MolarRefractivity), col="blue")
#####################################################################

#TdSvsMolar_Volume
test<-cor.test(Molar_Volume, TdS)
> test$estimate
      cor 
0.6383007 
> test$p.value
[1] 1.394986e-08

test<-cor.test(Molar_Volume, TdS, method="spearman")
> test$estimate
      rho 
0.6697195 
> test$p.value
[1] 1.436917e-09

test<-cor.test(Molar_Volume, TdS, method="kendall")
> test$estimate
      tau 
0.4693019 
> test$p.value
[1] 4.498675e-08

plot(Molar_Volume, TdS, pch=20, col='red', xlab="Molar Volume", text(400, 60, cex=0.8, "Pearson's corr. 0.6383007, p-val=1.394986e-08\nRho 0.6697195, p-val=1.436917e-09\nTau 0.4693019, p-val=4.498675e-08"), ylab="TdS", main="Temperature*Entropy Vs Molar Volume")
abline(lm(TdS~Molar_Volume), col="blue")
#####################################################################

TdSvssurfTension
test<-cor.test(surfTension, TdS)
> test$estimate
       cor 
-0.4256947 
> test$p.value 
[1] 0.0004534264

test<-cor.test(surfTension, TdS, method="spearman")
> test$estimate
       rho 
-0.5491036 
> test$p.value
[1] 2.622271e-06

test<-cor.test(surfTension, TdS, method="kendall")
> test$estimate
      tau 
-0.369247 
> test$p.value
[1] 1.709113e-05

plot(surfTension, TdS, pch=20, col='red', xlab="Surface Tension", text(200, 60, cex=0.8, "Pearson's corr. -0.4256947, p-val=0.0004534264\nRho -0.5491036, p-val=2.622271e-06\nTau -0.369247, p-val=1.709113e-05"), ylab="TdS", main="Temperature*Entropy Vs Surface Tension")
abline(lm(TdS~surfTension), col="blue")
#####################################################################

