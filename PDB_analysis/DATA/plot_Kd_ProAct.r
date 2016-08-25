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
test<-cor.test(HBondsNo, K)
> test$estimate
       cor 
-0.1713153 
> test$p.value 
[1] 0.1758829

test<-cor.test(HBondsNo, K, method="spearman")
> test$estimate
        rho 
-0.02494925 
> test$p.value
[1] 0.8448524

test<-cor.test(HBondsNo, K, method="kendall")
> test$estimate
        tau 
-0.03441089 
> test$p.value 
[1] 0.6968245

plot(HBondsNo, K, pch=20, col='red', xlab="No of Hydrogen Bonds", ylab="delta G", main="Affinity Vs Hydrogen Bonds")
abline(lm(K~HBondsNo), col="blue")
text(15, 400, cex=0.8, "Pearson's corr. -0.1713153, p-val=-0.1758829\nRho -0.02494925, p-val=0.8448524\nTau -0.03441089, p-val=0.6968245")
#####################################################################

#KvsPolar_Contacts
test<-cor.test(Polar_Contacts, K)
        cor 
-0.07499209 
> test$p.value
[1] 0.5558997


test<-cor.test(Polar_Contacts, K, method="spearman")
> test$estimate
       tau 
0.05940733 
> test$p.value 
[1] 0.5031034

test<-cor.test(Polar_Contacts, K, method="kendall")
       tau 
0.05940733 
> test$p.value
[1] 0.5031034

plot(Polar_Contacts, K, pch=20, col='red', xlab="No of Polar Contacts", ylab="delta G", text(90, 400, cex=0.8, "Pearson's corr. -0.07499209, p-val=0.5558997\nRho 0.05940733, p-val=0.5031034\nTau 0.05940733 , p-val=0.5031034"), main="Affinity Vs Polar Contacts")
abline(lm(K~Polar_Contacts), col="blue")

#####################################################################

#KvsApolar_Contacts
test<-cor.test(Apolar_Contacts, K)
> test$estimate
       cor 
-0.2599834 
> test$p.value  
[1] 0.03801461 

test<-cor.test(Apolar_Contacts, K, method="spearman")
> test$estimate
       tau 
-0.2132797 
> test$p.value 
[1] 0.01391808  

test<-cor.test(Apolar_Contacts, K, method="kendall")
> test$estimate
       tau 
-0.2132797 
> test$p.value 
[1] 0.01391808

plot(Apolar_Contacts, K, pch=20, col='red', xlab="No of Apolar Contacts", ylab="delta G", text(220, 400, cex=0.8, "Pearson's corr. -0.2599834, p-val=0.03801461\nRho -0.2132797, p-val=0.01391808\nTau -0.2132797, p-val=0.01391808"), main="Affinity Vs Apolar Contacts")
abline(lm(K~Apolar_Contacts), col="blue")

#####################################################################

#KvsPolar_Water_Contacts
test<-cor.test(Polar_Water_Contacts, K)
> test$estimate
      cor 
0.3429675 
> test$p.value
[1] 0.005531203

test<-cor.test(Polar_Water_Contacts, K, method="spearman")
> test$estimate
      rho 
0.1781166 
> test$p.value
[1] 0.1590907 

test<-cor.test(Polar_Water_Contacts, K, method="kendall")
> test$estimate
      tau 
0.1086639 
> test$p.value 
[1] 0.2083148

plot(Polar_Water_Contacts, K, pch=20, col='red', xlab="No of Polar Water Contacts", ylab="delta G", text(-10, 400, cex=0.8, "Pearson's corr. 0.3429675, p-val=0.005531203\nRho 0.1781166, p-val=0.1590907\nTau 0.1086639, p-val=0.2083148"), main="Affinity Vs Polar Water Contacts")
abline(lm(K~Polar_Water_Contacts), col="blue")

#####################################################################

#KvsApolar_Water_Contacts
test<-cor.test(Apolar_Water_Contacts, K)
> test$estimate
      cor 
0.3228371 
> test$p.value
[1] 0.009271805

test<-cor.test(Apolar_Water_Contacts, K, method="spearman")
> test$estimate
      rho 
0.4870068 
> test$p.value
[1] 4.487116e-05

test<-cor.test(Apolar_Water_Contacts, K, method="kendall")
> test$estimate
      tau 
0.3365888 
> test$p.value
[1] 9.548468e-05

#####################################################################

#KvsSurface_Waters
test<-cor.test(Surface_Waters, K)
> test$estimate
       cor 
0.01032057 
> test$p.value
[1] 0.9354901

test<-cor.test(Surface_Waters, K, method="spearman")
> test$estimate
       rho 
-0.2923257 
> test$p.value 
[1] 0.01907991 

test<-cor.test(Surface_Waters, K, method="kendall")
> test$estimate
      tau 
-0.201453 
> test$p.value 
[1] 0.01947262

plot(Surface_Waters, K, pch=20, col='red', xlab="No of Surface Waters", ylab="delta G", text(150, 400, cex=0.8, "Pearson's corr. 0.01032057, p-val=0.9354901\nRho -0.2923257, p-val=0.01907991\nTau -0.201453, p-val=0.01947262"), main="Affinity Vs Surface Waters")
abline(lm(K~Surface_Waters), col="blue")

#####################################################################

#KvsCleft_Waters
test<-cor.test(Cleft_Waters, K)
> test$estimate
       cor 
-0.1539361 
> test$p.value 
[1] 0.2245679

test<-cor.test(Cleft_Waters, K, method="spearman")
> test$estimate
       rho 
-0.1687386 
> test$p.value  
[1] 0.1825701 

test<-cor.test(Cleft_Waters, K, method="kendall")
> test$estimate
       tau 
-0.1091275 
> test$p.value 
[1] 0.2081151

plot(Cleft_Waters, K, pch=20, col='red', xlab="No of Cleft Waters", ylab="delta G", text(20, 400, cex=0.8, "Pearson's corr. -0.1539361, p-val=0.2245679\nRho -0.1687386, p-val=0.1825701\nTau -0.1091275, p-val=0.2081151"), main="Affinity Vs Cleft Waters")
abline(lm(K~Cleft_Waters), col="blue")

#####################################################################

#KvsBuried_Waters
test<-cor.test(Buried_Waters, K)
> test$estimate
       cor 
-0.1932024 
> test$p.value
[1] 0.1391315

test<-cor.test(Buried_Waters, K, method="spearman")
> test$estimate
       rho 
-0.1148845 
> test$p.value 
[1] 0.3820799 

test<-cor.test(Buried_Waters, K, method="kendall")
> test$estimate
        tau 
-0.08372924 
> test$p.value 
[1] 0.3652329

plot(Buried_Waters, K, pch=20, col='red', xlab="No of Buried Waters", text(30, 400, cex=0.8, "Pearson's corr. -0.1932024, p-val=0.1391315\nRho -0.1148845, p-val=0.3820799\nTau -0.08372924, p-val=0.3652329"), ylab="delta G", main="Affinity Vs Buried Waters")
abline(lm(K~Buried_Waters), col="blue")

#####################################################################
