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
test<-cor.test(HBondsNo, dH)
> test$estimate
      cor 
0.5546508 
> test$p.value 
[1] 1.977708e-06

test<-cor.test(HBondsNo, dH, method="spearman")
> test$estimate
      rho 
0.6032338 
> test$p.value
[1] 1.323793e-07

test<-cor.test(HBondsNo, dH, method="kendall")
> test$estimate
      tau 
0.4078079 
> test$p.value 
[1] 3.42107e-06 

plot(HBondsNo, dH, pch=20, col='red', xlab="No of Hydrogen Bonds", ylab="Enthalpy", text(18, 30, cex=0.8, "Pearson's corr. 0.5546508, p-val=1.977708e-06\nRho 0.6032338, p-val=1.323793e-07\nTau 0.4078079, p-val=3.42107e-06"), main="Enthalpy Vs Hydrogen Bonds")
abline(lm(dH~HBondsNo), col="blue")
#####################################################################

#dHvsPolar_Contacts
test<-cor.test(Polar_Contacts, dH)
> test$estimate
      cor 
0.3512668 
> test$p.value
[1] 0.00442653

test<-cor.test(Polar_Contacts, dH, method="spearman")
> test$estimate
      rho 
0.5199168 
> test$p.value 
[1] 1.067925e-05 

test<-cor.test(Polar_Contacts, dH, method="kendall")
> test$estimate
      tau 
0.3773264 
> test$p.value
[1] 1.890537e-05

plot(Polar_Contacts, dH, pch=20, col='red', xlab="No of Polar Contacts", ylab="Enthalpy", text(90, 30, cex=0.8, "Pearson's corr. 0.3512668, p-val=0.00442653\nRho 0.5199168, p-val=1.067925e-05\nTau 0.3773264, p-val=1.890537e-05"), main="Enthalpy Vs Polar Contacts")
abline(lm(dH~Polar_Contacts), col="blue")
#####################################################################

#dHvsApolar_Contacts
test<-cor.test(Apolar_Contacts, dH)
> test$estimate
      cor 
0.5191217 
> test$p.value
[1] 1.107582e-05

test<-cor.test(Apolar_Contacts, dH, method="spearman")
> test$estimate
      rho 
0.6051077 
> test$p.value
[1] 1.181858e-07  

test<-cor.test(Apolar_Contacts, dH, method="kendall")
> test$estimate
      tau 
0.4324017 
> test$p.value
[1] 5.314511e-07

plot(Apolar_Contacts, dH, pch=20, col='red', xlab="No of Apolar Contacts", ylab="Enthalpy", text(220, 30, cex=0.8, "Pearson's corr. 0.5191217, p-val=1.107582e-05\nRho 0.6051077, p-val=1.181858e-07\nTau 0.4324017, p-val=5.314511e-07"), main="Enthalpy Vs Apolar Contacts")
abline(lm(dH~Apolar_Contacts), col="blue")
#####################################################################

#dHvsPolar_Water_Contacts
test<-cor.test(Polar_Water_Contacts, dH)
> test$estimate
       cor 
-0.6069251 
> test$p.value 
[1] 1.058017e-07

test<-cor.test(Polar_Water_Contacts, dH, method="spearman")
> test$estimate
       rho 
-0.5715382 
> test$p.value
[1] 8.114478e-07  

test<-cor.test(Polar_Water_Contacts, dH, method="kendall")
> test$estimate
      tau 
-0.374721 
> test$p.value
[1] 1.279122e-05

plot(Polar_Water_Contacts, dH, pch=20, col='red', xlab="No of Polar Water Contacts", ylab="Enthalpy", text(-10, 30, cex=0.8, "Pearson's corr. -0.6069251, p-val=1.058017e-07\nRho -0.5715382, p-val=8.114478e-07\nTau -0.374721, p-val=1.279122e-05"), main="Enthalpy Vs Polar Water Contacts")
abline(lm(dH~Polar_Water_Contacts), col="blue")
#####################################################################

#dHvsApolar_Water_Contacts
test<-cor.test(Apolar_Water_Contacts, dH)
> test$estimate
       cor 
-0.4157907 
> test$p.value
[1] 0.0006334334

test<-cor.test(Apolar_Water_Contacts, dH, method="spearman")
> test$estimate
       rho 
-0.5462268 
> test$p.value
[1] 3.029382e-06

test<-cor.test(Apolar_Water_Contacts, dH, method="kendall")
> test$estimate
       tau 
-0.3946324 
> test$p.value
[1] 4.209657e-06

plot(Apolar_Water_Contacts, dH, pch=20, col='red', xlab="No of Apolar Water Contacts", ylab="Enthalpy", text(20, 30, cex=0.8, "Pearson's corr. -0.4157907, p-val=0.0006334334\nRho -0.5462268, p-val=3.029382e-06\nTau -0.3946324, p-val=4.209657e-06"), main="Enthalpy Vs Apolar Water Contacts")
abline(lm(dH~Apolar_Water_Contacts), col="blue")
#####################################################################

#dHvsSurface_Waters
test<-cor.test(Surface_Waters, dH)
> test$estimate
      cor 
0.1917059 
> test$p.value 
[1] 0.129132

test<-cor.test(Surface_Waters, dH, method="spearman")
> test$estimate
     rho 
0.183323 
> test$p.value
[1] 0.1470587 

test<-cor.test(Surface_Waters, dH, method="kendall")
> test$estimate
       tau 
0.09935421 
> test$p.value 
[1] 0.246521 

plot(Surface_Waters, dH, pch=20, col='red', xlab="No of Surface Waters", ylab="delta G", text(150, 30, cex=0.8, "Pearson's corr. 0.1917059, p-val=0.129132\nRho 0.183323, p-val=0.1470587\nTau 0.09935421, p-val=0.246521"), main="Enthalpy Vs Surface Waters")
abline(lm(dH~Surface_Waters), col="blue")

#####################################################################

#dHvsCleft_Waters
test<-cor.test(Cleft_Waters, dH)
> test$estimate
      cor 
0.5171983 
> test$p.value 
[1] 1.20925e-05

test<-cor.test(Cleft_Waters, dH, method="spearman")
> test$estimate
      rho 
0.6066611 
> test$p.value 
[1] 1.075214e-07

test<-cor.test(Cleft_Waters, dH, method="kendall")
> test$estimate
      tau 
0.4227975 
> test$p.value 
[1] 9.354604e-07

plot(Cleft_Waters, dH, pch=20, col='red', xlab="No of Cleft Waters", ylab="Enthalpy", text(20, 30, cex=0.8, "Pearson's corr. 0.5171983, p-val=1.20925e-05\nRho 0.6066611, p-val=1.075214e-07\nTau 0.4227975, p-val=9.354604e-07"), main="Enthalpy Vs Cleft Waters")
abline(lm(dH~Cleft_Waters), col="blue")

#####################################################################

#dHvsBuried_Waters
test<-cor.test(Buried_Waters, dH)
> test$estimate
      cor 
0.6296199 
> test$p.value 
[1] 7.081828e-08

test<-cor.test(Buried_Waters, dH, method="spearman")
> test$estimate
      rho 
0.6578089 
> test$p.value 
[1] 1.125929e-08 

test<-cor.test(Buried_Waters, dH, method="kendall")
> test$estimate
      tau 
0.4916851 
> test$p.value
[1] 8.717365e-08

plot(Buried_Waters, dH, pch=20, col='red', xlab="No of Buried Waters", ylab="Enthalpy", text(35, 30, cex=0.8, "Pearson's corr. 0.6296199, p-val=7.081828e-08\nRho 0.6578089, p-val=1.125929e-08\nTau 0.4916851, p-val=8.717365e-08"), main="Enthalpy Vs Buried Waters")
abline(lm(dH~Buried_Waters), col="blue")
#####################################################################
