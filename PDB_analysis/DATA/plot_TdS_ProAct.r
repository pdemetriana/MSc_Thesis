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

#####################################################################

#dGvsHBondsNo
test<-cor.test(HBondsNo, TdS)
> test$estimate
      cor 
0.5139717 
> test$p.value 
[1] 1.399519e-05 

test<-cor.test(HBondsNo, TdS, method="spearman")
> test$estimate
      rho 
0.5307535 
> test$p.value
[1] 6.437354e-06

test<-cor.test(HBondsNo, TdS, method="kendall")
> test$estimate
      tau 
0.3624725 
> test$p.value 
[1] 3.682129e-05

plot(HBondsNo, TdS, pch=20, col='red', xlab="Hydrogen Bonds", ylab="TdS", text(18, 60, cex=0.8, "Pearson's corr. 0.5139717, p-val=1.399519e-05\nRho 0.5307535, p-val=6.437354e-06\nTau 0.3624725, p-val=3.682129e-05"), main="Temperature*Entropy Vs Hydrogen Bonds")
abline(lm(TdS~HBondsNo), col="blue")
#####################################################################

#TdSvsPolar_Contacts
test<-cor.test(Polar_Contacts, TdS)
> test$estimate
      cor 
0.3089511 
> test$p.value
[1] 0.01299189

test<-cor.test(Polar_Contacts, TdS, method="spearman")
> test$estimate
      rho 
0.4358908 
> test$p.value 
[1] 0.0003179318

test<-cor.test(Polar_Contacts, TdS, method="kendall")
> test$estimate
      tau 
0.3317189 
> test$p.value
[1] 0.0001702178 

plot(Polar_Contacts, TdS, pch=20, col='red', xlab="Polar Contacts", ylab="TdS", text(90, 60, cex=0.8, "Pearson's corr. 0.3089511, p-val=0.01299189\nRho 0.4358908, p-val=0.0003179318\nTau 0.3317189, p-val=0.0001702178"), main="Temperature*Entropy Vs Polar Contacts")
abline(lm(TdS~Polar_Contacts), col="blue")

#####################################################################

#TdSvsApolar_Contacts
test<-cor.test(Apolar_Contacts, TdS)
> test$estimate
      cor 
0.5487082 
> test$p.value 
[1] 2.675008e-06

test<-cor.test(Apolar_Contacts, TdS, method="spearman")
> test$estimate
      rho 
0.6435141 
> test$p.value
[1] 9.740707e-09  

test<-cor.test(Apolar_Contacts, TdS, method="kendall")
> test$estimate
    tau 
0.47201 
> test$p.value 
[1] 4.433134e-08 

plot(Apolar_Contacts, TdS, pch=20, col='red', xlab="Apolar Contacts", ylab="TdS", text(220, 60, cex=0.8, "Pearson's corr. 0.5487082, p-val=2.675008e-06\nRho 0.6435141, p-val=9.740707e-09\nTau 0.47201, p-val=4.433134e-08"), main="Temperature*Entropy Vs Apolar Contacts")
abline(lm(TdS~Apolar_Contacts), col="blue")
#####################################################################

#TdSvsPolar_Water_Contacts
test<-cor.test(Polar_Water_Contacts, TdS)
> test$estimate
       cor 
-0.6030878 
> test$p.value 
[1] 1.335495e-07

test<-cor.test(Polar_Water_Contacts, TdS, method="spearman")
> test$estimate
       rho 
-0.5541308 
> test$p.value 
[1] 2.031145e-06  

test<-cor.test(Polar_Water_Contacts, TdS, method="kendall")
> test$estimate
       tau 
-0.3703342 
> test$p.value 
[1] 1.621043e-05

plot(Polar_Water_Contacts, TdS, pch=20, col='red', xlab="Polar Water Contacts", ylab="TdS", text(-10, 60, cex=0.8, "Pearson's corr. -0.6030878, p-val=1.335495e-07\nRho -0.5541308, p-val=2.031145e-06\nTau -0.3703342, p-val=1.621043e-05"), main="Temperature*Entropy Vs Polar Water Contacts")
abline(lm(TdS~Polar_Water_Contacts), col="blue")

#####################################################################

#TdSvsApolar_Water_Contacts
test<-cor.test(Apolar_Water_Contacts, TdS)
> test$estimate
       cor 
-0.4910356 
> test$p.value
[1] 3.79358e-05

test<-cor.test(Apolar_Water_Contacts, TdS, method="spearman")
> test$estimate
       rho 
-0.6535014 
> test$p.value
[1] 4.801216e-09

test<-cor.test(Apolar_Water_Contacts, TdS, method="kendall")
> test$estimate
       tau 
-0.4817302 
> test$p.value
[1] 1.967132e-08

plot(Apolar_Water_Contacts, TdS, pch=20, col='red', xlab="Apolar Water Contacts", ylab="TdS", text(20, 60, cex=0.8, "Pearson's corr. -0.4910356, p-val=3.79358e-05\nRho -0.6535014, p-val=4.801216e-09\nTau -0.4817302, p-val=1.967132e-08"), main="Temperature*Entropy Vs Apolar Water Contacts")
abline(lm(TdS~Apolar_Water_Contacts), col="blue")
#####################################################################

#TdSvsSurface_Waters
test<-cor.test(Surface_Waters, TdS)
> test$estimate
      cor 
0.2321054 
> test$p.value 
[1] 0.06495935

test<-cor.test(Surface_Waters, TdS, method="spearman")
> test$estimate
      rho 
0.2609641 
> test$p.value 
[1] 0.03726889

test<-cor.test(Surface_Waters, TdS, method="kendall")
> test$estimate
      tau 
0.1565217 
> test$p.value 
[1] 0.06797006 

plot(Surface_Waters, TdS, pch=20, col='red', xlab="Surface Waters", ylab="TdS", text(150, 60, cex=0.8, "Pearson's corr. 0.2321054, p-val=0.06495935\nRho 0.2609641, p-val=0.03726889\nTau 0.1565217, p-val=0.06797006"), main="Temperature*Entropy Vs Surface Waters")
abline(lm(TdS~Surface_Waters), col="blue")

#####################################################################

#TdSvsCleft_Waters
test<-cor.test(Cleft_Waters, TdS)
> test$estimate
      cor 
0.5135137 
> test$p.value 
[1] 1.428679e-05 

test<-cor.test(Cleft_Waters, TdS, method="spearman")
> test$estimate
      rho 
0.5915844 
> test$p.value
[1] 2.636615e-07 

test<-cor.test(Cleft_Waters, TdS, method="kendall")
> test$estimate
      tau 
0.4094056 
> test$p.value 
[1] 2.051388e-06

plot(Cleft_Waters, TdS, pch=20, col='red', xlab="Cleft Waters", ylab="TdS", text(20, 60, cex=0.8, "Pearson's corr. 0.5135137, p-val=1.428679e-05\nRho 0.5915844, p-val=2.636615e-07\nTau 0.4094056, p-val=2.051388e-06"), main="Temperature*Entropy Vs Cleft Waters")
abline(lm(TdS~Cleft_Waters), col="blue")
#####################################################################

#TdSvsBuried_Waters
test<-cor.test(Buried_Waters, TdS)
> test$estimate
      cor 
0.6079469 
> test$p.value
[1] 2.58092e-07

test<-cor.test(Buried_Waters, TdS, method="spearman")
> test$estimate
     rho 
0.600423 
> test$p.value  
[1] 3.954452e-07  

test<-cor.test(Buried_Waters, TdS, method="kendall")
> test$estimate
      tau 
0.4529585 
> test$p.value 
[1] 8.16402e-07

plot(Buried_Waters, TdS, pch=20, col='red', xlab="Buried Waters", ylab="TdS", text(35, 60, cex=0.8, "Pearson's corr. 0.6079469, p-val=2.58092e-07\nRho 0.600423, p-val=3.954452e-07\nTau 0.4529585, p-val=8.16402e-07"), main="Temperature*Entropy Vs Buried Waters")
abline(lm(TdS~Buried_Waters), col="blue")
#####################################################################
