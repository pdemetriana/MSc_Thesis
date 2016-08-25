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
test<-cor.test(HBondsNo, dG)
 test$estimate
        cor 
-0.01388757 
> test$p.value 
[1] 0.913269


test<-cor.test(HBondsNo, dG, method="spearman")
> test$estimate
        rho 
-0.02759104 
> test$p.value
[1] 0.8286611

test<-cor.test(HBondsNo, dG, method="kendall")
> test$estimate
        tau 
-0.03525248 
> test$p.value 
[1] 0.6883817

plot(HBondsNo, dG, pch=20, col='red', xlab="No of Hydrogen Bonds", ylab="delta G", main="Gibb's energy Changes Vs Hydrogen Bonds")
abline(lm(dG~HBondsNo), col="blue")
text(19, -21, cex=0.8, "Pearson's corr. -0.01388757, p-val=-0.913269\nRho -0.02759104, p-val=0.8286611\nTau -0.03525248, p-val=0.6883817")
#####################################################################

#dGvsPolar_Contacts
test<-cor.test(Polar_Contacts, dG)
> test$estimate
       cor 
0.07033539 
> test$p.value
[1] 0.580758

test<-cor.test(Polar_Contacts, dG, method="spearman")
> test$estimate
       rho 
0.07139459 
> test$p.value 
[1] 0.5750594 

test<-cor.test(Polar_Contacts, dG, method="kendall")
> test$estimate
       tau 
0.05755453 
> test$p.value 
[1] 0.5145032

plot(Polar_Contacts, dG, pch=20, col='red', xlab="No of Polar Contacts", ylab="delta G", text(90, -21, cex=0.8, "Pearson's corr. 0.07033539, p-val=0.580758\nRho 0.07139459, p-val=0.5750594\nTau 0.05755453, p-val=0.5145032"), main="Gibb's energy Changes Vs Polar Contacts")
abline(lm(dG~Polar_Contacts), col="blue")

#####################################################################

#dGvsApolar_Contacts
test<-cor.test(Apolar_Contacts, dG)
> test$estimate
       cor 
-0.3233765 
> test$p.value
[1] 0.009148293

test<-cor.test(Apolar_Contacts, dG, method="spearman")
> test$estimate
       rho 
-0.3257135 
> test$p.value 
[1] 0.008629515   

test<-cor.test(Apolar_Contacts, dG, method="kendall")
> test$estimate
       tau 
-0.2036561 
> test$p.value 
[1] 0.01829341 

plot(Apolar_Contacts, dG, pch=20, col='red', xlab="No of Apolar Contacts", ylab="delta G", text(230, -21, cex=0.8, "Pearson's corr. -0.3233765, p-val=0.009148293\nRho -0.3257135, p-val=0.008629515\nTau -0.2036561, p-val=0.01829341"), main="Gibb's energy Changes Vs Apolar Contacts")
abline(lm(dG~Apolar_Contacts), col="blue")

#####################################################################

#dGvsPolar_Water_Contacts
test<-cor.test(Polar_Water_Contacts, dG)
> test$estimate
      cor 
0.2051684 
> test$p.value 
[1] 0.1038752

test<-cor.test(Polar_Water_Contacts, dG, method="spearman")
> test$estimate
      rho 
0.1702293 
> test$p.value
[1] 0.1786792  

test<-cor.test(Polar_Water_Contacts, dG, method="kendall")
> test$estimate
      tau 
0.1041097 
> test$p.value
[1] 0.2258038 

plot(Polar_Water_Contacts, dG, pch=20, col='red', xlab="No of Polar Water Contacts", ylab="delta G", text(-10, -21, cex=0.8, "Pearson's corr. 0.2051684, p-val=0.1038752\nRho 0.1702293, p-val=0.1786792\nTau 0.1041097, p-val=0.2258038"), main="Gibb's energy Changes Vs Polar Water Contacts")
abline(lm(dG~Polar_Water_Contacts), col="blue")

#####################################################################

#dGvsApolar_Water_Contacts
test<-cor.test(Apolar_Water_Contacts, dG)
> test$estimate
      cor 
0.4994473 
> test$p.value
[1] 2.65351e-05

test<-cor.test(Apolar_Water_Contacts, dG, method="spearman")
> test$estimate
      rho 
0.4784082 
> test$p.value
[1] 6.376419e-05

test<-cor.test(Apolar_Water_Contacts, dG, method="kendall")
> test$estimate
      tau 
0.3293532 
> test$p.value
[1] 0.0001249784

plot(Apolar_Water_Contacts, dG, pch=20, col='red', xlab="No of Apolar Water Contacts", ylab="delta G", text(18, -21, cex=0.8, "Pearson's corr. 0.4994473, p-val=2.65351e-05\nRho 0.4784082, p-val=6.376419e-05\nTau 0.3293532, p-val=0.0001249784"), main="Gibb's energy Changes Vs Apolar Water Contacts")
abline(lm(dG~Apolar_Water_Contacts), col="blue")

#####################################################################

#dGvsSurface_Waters
test<-cor.test(Surface_Waters, dG)
> test$estimate
       cor 
-0.2570376 
> test$p.value 
[1] 0.04032918 

test<-cor.test(Surface_Waters, dG, method="spearman")
> test$estimate
       rho 
-0.2929365 
> test$p.value 
[1] 0.01881936

test<-cor.test(Surface_Waters, dG, method="kendall")
> test$estimate
       tau 
-0.2038787 
> test$p.value 
[1] 0.01751174

plot(Surface_Waters, dG, pch=20, col='red', xlab="No of Surface Waters", ylab="delta G", text(150, -21, cex=0.8, "Pearson's corr. -0.2570376, p-val=0.04032918\nRho -0.2929365, p-val=0.01881936\nTau -0.2038787, p-val=0.01751174"), main="Gibb's energy Changes Vs Surface Waters")
abline(lm(dG~Surface_Waters), col="blue")

#####################################################################

#dGvsCleft_Waters
test<-cor.test(Cleft_Waters, dG)
> test$estimate
       cor 
-0.1671041 
> test$p.value
[1] 0.1869062

test<-cor.test(Cleft_Waters, dG, method="spearman")
> test$estimate
       rho 
-0.1564998 
> test$p.value
[1] 0.2168495  

test<-cor.test(Cleft_Waters, dG, method="kendall")
> test$estimate
       tau 
-0.1020526 
> test$p.value 
[1] 0.2368947

plot(Cleft_Waters, dG, pch=20, col='red', xlab="No of Cleft Waters", ylab="delta G", text(20, -21, cex=0.8, "Pearson's corr. -0.1671041, p-val=0.1869062\nRho -0.1564998, p-val=0.2168495\nTau -0.1020526, p-val=0.2368947"), main="Gibb's energy Changes Vs Cleft Waters")
abline(lm(dG~Cleft_Waters), col="blue")

#####################################################################

#dGvsBuried_Waters
test<-cor.test(Buried_Waters, dG)
> test$estimate
       cor 
-0.1172589 
> test$p.value
[1] 0.3722535 

test<-cor.test(Buried_Waters, dG, method="spearman")
> test$estimate
      rho 
-0.114663 
> test$p.value
[1] 0.3830044  

test<-cor.test(Buried_Waters, dG, method="kendall")
> test$estimate
        tau 
-0.08263487 
> test$p.value
[1] 0.3689367 

plot(Buried_Waters, dG, pch=20, col='red', xlab="No of Buried Waters", text(35, -21, cex=0.8, "Pearson's corr. -0.1172589, p-val=0.3722535\nRho -0.114663, p-val=0.3830044\nTau -0.08263487, p-val=0.3689367"), ylab="delta G", main="Gibb's energy Changes Vs Buried Waters")
abline(lm(dG~Buried_Waters), col="blue")

#####################################################################
