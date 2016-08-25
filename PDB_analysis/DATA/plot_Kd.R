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
test<-cor.test(MW, K)
> test$estimate
       cor 
-0.1524996 
> test$p.value
[1] 0.2488825


test<-cor.test(MW, K, method="spearman")
> test$estimate
      rho 
-0.232187 
> test$p.value
[1] 0.0767982

test<-cor.test(MW, K, method="kendall")
> test$estimate
       tau 
-0.1433609 
> test$p.value
[1] 0.1104182

plot(MW, K, pch=20, col='red', xlab="Molecular Weight", ylab="delta G", text(530, 400, cex=0.8, "Pearson's corr. -0.1524996 , p-val=0.2488825\nRho -0.232187, p-val=0767982\nTau -0.1433609, p-val=0.1104182"), main="Affinity Vs Molecular Weight")
abline(lm(K~MW), col="blue")

#####################################################################

#KvsMM
test<-cor.test(MM, K)
> test$estimate
       cor 
-0.1525066 
> test$p.value
[1] 0.2488605

test<-cor.test(MM, K, method="spearman")
> test$estimate
      rho 
-0.232187 
> test$p.value
[1] 0.0767982

test<-cor.test(MM, K, method="kendall")
> test$estimate
       tau 
-0.1433609 
> test$p.value
[1] 0.1104182

plot(MM, K, pch=20, col='red', xlab="Monoisotopic Mass", ylab="delta G", text(430, 400, cex=0.8, "Pearson's corr. -0.1525066, p-val=0.2488605\nRho -0.232187, p-val=0.0767982\nTau -0.1433609, p-val=0.1104182"), main="Affinity Vs Monoisotopic Mass")
abline(lm(K~MM), col="blue")

#####################################################################

#KvsAlogP
test<-cor.test(AlogP, K)
> test$estimate
       cor 
0.02942518 
> test$p.value 
[1] 0.8249126

test<-cor.test(AlogP, K, method="spearman")
> test$estimate
        rho 
-0.06277138 
> test$p.value
[1] 0.6367083

test<-cor.test(AlogP, K, method="kendall")
> test$estimate
        tau 
-0.05162634 
> test$p.value
[1] 0.6297795

plot(AlogP, K, pch=20, col='red', xlab="AlogP", ylab="delta G", text(1.8, 400, cex=0.8, "Pearson's corr. 0.02942518, p-val=0.8249126\nRho -0.06277138, p-val=0.6367083\nTau -0.05162634, p-val=0.6297795"), main="Affinity Vs AlogP")
abline(lm(K~AlogP), col="blue")

#####################################################################

#KvsXlogP
test<-cor.test(XlogP, K)
> test$estimate
       cor 
0.08272298 
> test$p.value
[1] 0.5333627

test<-cor.test(XlogP, K, method="spearman")
> test$estimate
       rho 
0.01285509 
> test$p.value 
[1] 0.9230178   

test<-cor.test(XlogP, K, method="kendall")
> test$estimate
        tau 
0.002618185 
> test$p.value 
[1] 0.9781352

plot(XlogP, K, pch=20, col='red', xlab="XlogP", ylab="delta G", text(1.8, 400, cex=0.8, "Pearson's corr. 0.08272298 , p-val=0.5333627\nRho 0.01285509, p-val=0.9230178\nTau 0.002618185, p-val=0.9781352"), main="Affinity Vs XlogP")
abline(lm(K~XlogP), col="blue")

#####################################################################

#KvsHacc
test<-cor.test(Hacc, K)
> test$estimate
       cor 
-0.1058782 
> test$p.value
[1] 0.4248055

test<-cor.test(Hacc, K, method="spearman")
> test$estimate
       rho 
-0.1621649 
> test$p.value 
[1] 0.2197841
 
test<-cor.test(Hacc, K, method="kendall")
       tau 
-0.1086633 
> test$p.value 
[1] 0.2510509

plot(Hacc, K, pch=20, col='red', xlab="Hydrogen Acceptors", ylab="delta G", text(18, 400, cex=0.8, "Pearson's corr. -0.1058782, p-val=0.4248055\nRho -0.1621649, p-val=0.2197841\nTau -0.1086633, p-val=0.2510509"), main="Affinity Vs Hydrogen Acceptors")
abline(lm(K~Hacc), col="blue")

#####################################################################

#KvsHd
test<-cor.test(Hd, K)
> test$estimate
       cor 
-0.1648076 
> test$p.value
[1] 0.2122596

test<-cor.test(Hd, K, method="spearman")
> test$estimate
       rho 
-0.1710661 
> test$p.value
[1] 0.1951675

test<-cor.test(Hd, K, method="kendall")
> test$estimate
       tau 
-0.1257873 
> test$p.value 
[1] 0.1831095

plot(Hd, K, pch=20, col='red', xlab="Hydrogen Donors", ylab="delta G", text(10, 400, cex=0.8, "Pearson's corr. -0.1648076, p-val=0.2122596\nRho -0.1710661, p-val=0.1951675\nTau -0.1257873, p-val=0.1831095"), main="Affinity Vs Hydrogen Donors")
abline(lm(K~Hd), col="blue")

#####################################################################

#KvsRotBonds
test<-cor.test(RotBonds, K)
> test$estimate
       cor 
-0.2095898 
> test$p.value
[1] 0.1111163

test<-cor.test(RotBonds, K, method="spearman")
> test$estimate
       rho 
-0.2389453 
> test$p.value
[1] 0.06836331

test<-cor.test(RotBonds, K, method="kendall")
> test$estimate
      tau 
-0.148041 
> test$p.value 
[1] 0.1127898 

plot(RotBonds, K, pch=20, col='red', xlab="Rotating Bonds", ylab="delta G", text(13, 400, cex=0.8, "Pearson's corr. -0.2095898, p-val=0.1111163\nRho -0.2389453, p-val=0.06836331\nTau -0.148041, p-val=0.1127898"), main="Affinity Vs Rotating Bonds")
abline(lm(K~RotBonds), col="blue")

#####################################################################

#KvsViolLepinskiRule
test<-cor.test(violLepinskiRule, K)
> test$estimate
         cor 
-0.003536533 
> test$p.value
[1] 0.978792

test<-cor.test(violLepinskiRule, K, method="spearman")
> test$estimate
       rho 
0.01119955 
> test$p.value 
[1] 0.9329074

test<-cor.test(violLepinskiRule, K, method="kendall")
> test$estimate
       tau 
0.01076549 
> test$p.value
[1] 0.9161256

plot(violLepinskiRule, K, pch=20, col='red', xlab="No of violations of 5 Rule", text(2.5, 400, cex=0.8, "Pearson's corr. -0.003536533, p-val=0.978792\nRho 0.01119955, p-val=0.9329074\nTau 0.01076549, p-val=0.9161256"), ylab="delta G", main="Affinity Vs No of violations of 5 Rule")
abline(lm(K~violLepinskiRule), col="blue")

#####################################################################

#KvsPSA
test<-cor.test(PSA, K)
> test$estimate
       cor 
-0.1310937 
> test$p.value 
[1] 0.3223282  

test<-cor.test(PSA, K, method="spearman")
> test$estimate
       rho 
-0.1946436 
> test$p.value
[1] 0.1396042

test<-cor.test(PSA, K, method="kendall")
> test$estimate
       tau 
-0.1332972 
> test$p.value
[1] 0.1406388

plot(PSA, K, pch=20, col='red', xlab="Polar Surface Area", ylab="delta G", text(300, 400, cex=0.8, "Pearson's corr. -0.1310937, p-val=0.3223282\nRho -0.1946436, p-val=0.1396042\nTau -0.1332972, p-val=0.1406388"), main="Affinity Vs Polar Surface Area")
abline(lm(K~PSA), col="blue")

#####################################################################

#KvsPolarizability
test<-cor.test(Polarizability, K)
> test$estimate
       cor 
-0.1765363 
> test$p.value 
[1] 0.1810529

test<-cor.test(Polarizability, K, method="spearman")
> test$estimate
       rho 
-0.2137197 
> test$p.value
[1] 0.1040927

test<-cor.test(Polarizability, K, method="kendall")
> test$estimate
       tau 
-0.1373419 
> test$p.value
[1] 0.1272777

plot(Polarizability, K, pch=20, col='red', xlab="Polarizability", ylab="delta G", text(55, 400, cex=0.8, "Pearson's corr. -0.1765363, p-val=0.1810529\nRho -0.2137197, p-val=0.1040927\nTau -0.1373419, p-val=0.1272777"), main="Affinity Vs Polarizability")
abline(lm(K~Polarizability), col="blue")

#####################################################################

#KvsRefrIndex
test<-cor.test(RefrIndex, K)
> test$estimate
       cor 
0.09093652 
> test$p.value
[1] 0.4933611 

test<-cor.test(RefrIndex, K, method="spearman")
> test$estimate
      rho 
0.1248027 
> test$p.value 
[1] 0.3462922 

test<-cor.test(RefrIndex, K, method="kendall")
> test$estimate
     tau 
0.101236 
> test$p.value
[1] 0.2604061

plot(RefrIndex, K, pch=20, col='red', xlab="Refraction Index", ylab="delta G", text(1.8, 400, cex=0.8, "Pearson's corr. 0.09093652, p-val=0.4933611\nRho 0.1248027, p-val=0.3462922\nTau 0.101236, p-val=0.2604061"), main="Affinity Vs Refraction Index")
abline(lm(K~RefrIndex), col="blue")

#####################################################################

#KvsMolarRefractivity
test<-cor.test(MolarRefractivity, K)
> test$estimate
       cor 
-0.1767581 
> test$p.value
[1] 0.1804967

test<-cor.test(MolarRefractivity, K, method="spearman")
> test$estimate
       rho 
-0.2155897 
> test$p.value
[1] 0.1010276

test<-cor.test(MolarRefractivity, K, method="kendall")
> test$estimate
       tau 
-0.1399177 
> test$p.value
[1] 0.1194399  

plot(MolarRefractivity, K, pch=20, col='red', xlab="Molar Refractivity", ylab="delta G", text(140, 400, cex=0.8, "Pearson's corr. -0.1767581, p-val=0.1804967\nRho -0.2155897, p-val=0.1010276\nTau -0.1399177, p-val=0.1194399"), main="Affinity Vs Molar Refractivity")
abline(lm(K~MolarRefractivity), col="blue")

#####################################################################

#KvsMolar_Volume
test<-cor.test(Molar_Volume, K)
> test$estimate
       cor 
-0.1859521 
> test$p.value
[1] 0.1585111

test<-cor.test(Molar_Volume, K, method="spearman")
> test$estimate
       rho 
-0.2136541 
> test$p.value
[1] 0.1042015

test<-cor.test(Molar_Volume, K, method="kendall")
> test$estimate
       tau 
-0.1292598 
> test$p.value
[1] 0.1500651

plot(Molar_Volume, K, pch=20, col='red', xlab="Molar Volume", ylab="delta G", text(400, 400, cex=0.8, "Pearson's corr. -0.1859521, p-val=0.1585111\nRho -0.2136541, p-val=0.1042015\nTau -0.1292598, p-val=0.1500651"), main="Affinity Vs Molar Volume")
abline(lm(K~Molar_Volume), col="blue")

#####################################################################

KvssurfTension
test<-cor.test(surfTension, K)
> test$estimate
      cor 
0.0853384 
> test$p.value
[1] 0.5204541

test<-cor.test(surfTension, K, method="spearman")
> test$estimate
      rho 
0.1048585 
> test$p.value
[1] 0.4293042

test<-cor.test(surfTension, K, method="kendall")
> test$estimate
       tau 
0.08762129 
> test$p.value
[1] 0.3296288

plot(surfTension, K, pch=20, col='red', xlab="Surface Tension", ylab="delta G", text(200, 400, cex=0.8, "Pearson's corr. 0.0853384, p-val=0.5204541\nRho 0.1048585, p-val=0.4293042\nTau 0.08762129, p-val=0.3296288"), main="Affinity Vs Surface Tension")
abline(lm(K~surfTension), col="blue")

#####################################################################

