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

#dGvsMW
# t = -3.7212, df = 63, p-value = 0.0004248
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.6056793 -0.2014443
#sample estimates:
#       cor 
#-0.4244874 

cor.test(MW, dG, method="spearman")
#S = 64202.22, p-value = 0.0008729
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#       rho 
#-0.4030205 

cor.test(MW, dG, method="kendall")
#z = -3.1426, p-value = 0.001675
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#     tau 
#-0.26747 
x<-test$p.value
plot(MW, dG, pch=20, col='red', xlab="Molecular Weight", ylab="delta G", main="Gibb's energy Changes Vs Molecular Weight")
abline(lm(dG~MW), col="blue")
text(430, -21, cex=0.8, "Pearson's corr. -0.4244874, p-val=-0.4244874\nRho -0.4030205, p-val=0.0008729\nTau -0.26747, p-val=0.001675")
#####################################################################

#dGvsMM
cor.test(MM, dG)
# t = -3.7202, df = 63, p-value = 0.0004262
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.6056098 -0.2013390
#sample estimates:
#       cor 
#-0.4243975 

cor.test(MM, dG, method="spearman")
#S = 64202.22, p-value = 0.0008729
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#       rho 
#-0.4030205 

cor.test(MM, dG, method="kendall")
#z = -3.1426, p-value = 0.001675
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#     tau 
#-0.26747 

plot(MM, dG, pch=20, col='red', xlab="Monoisotopic Mass", ylab="delta G", text(430, -21, cex=0.8, "Pearson's corr. -0.4243975, p-val=0.0004262\nRho -0.4030205, p-val=0.0008729\nTau -0.26747, p-val=0.001675"), main="Gibb's energy Changes Vs Monoisotopic Mass")
abline(lm(dG~MM), col="blue")

#####################################################################

#dGvsAlogP
cor.test(AlogP, dG)
#t = -0.7935, df = 63, p-value = 0.4305
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.3352428  0.1480128
#sample estimates:
#        cor 
#-0.09947749 

cor.test(AlogP, dG, method="spearman")
# S = 53500.02, p-value = 0.178
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
       # rho 
# -0.1691438  

cor.test(AlogP, dG, method="kendall")
# z = -1.3638, p-value = 0.1726
# alternative hypothesis: true tau is not equal to 0
# sample estimates:
       # tau 
# -0.1387752

plot(AlogP, dG, pch=20, col='red', xlab="AlogP", ylab="delta G", text(1.8, -21, cex=0.8, "Pearson's corr. -0.09947749, p-val=0.4305\nRho -0.1691438, p-val=0.178\nTau -0.1387752, p-val=0.1726"), main="Gibb's energy Changes Vs AlogP")
abline(lm(dG~AlogP), col="blue")

#####################################################################

#dGvsXlogP
cor.test(XlogP, dG)
# t = -2.4084, df = 63, p-value = 0.01896
# alternative hypothesis: true correlation is not equal to 0
# 95 percent confidence interval:
 # -0.49892087 -0.04999526
# sample estimates:
       # cor 
# -0.2903539 

cor.test(XlogP, dG, method="spearman")
# S = 58873.09, p-value = 0.02065
# alternative hypothesis: true rho is not equal to 0
# sample estimates:
       # rho 
# -0.2865624   

cor.test(XlogP, dG, method="kendall")
# z = -2.4235, p-value = 0.01537
# alternative hypothesis: true tau is not equal to 0
# sample estimates:
       # tau 
# -0.2189025 

plot(XlogP, dG, pch=20, col='red', xlab="XlogP", ylab="delta G", text(1.8, -21, cex=0.8, "Pearson's corr. -0.2903539 , p-val=0.01896\nRho -0.1691438, p-val=0.178\nTau -0.1387752, p-val=0.1726"), main="Gibb's energy Changes Vs XlogP")
abline(lm(dG~XlogP), col="blue")

#####################################################################

#dGvsHacc
cor.test(Hacc, dG)
#t = -0.8394, df = 63, p-value = 0.4044
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.3403375  0.1423831
#sample estimates:
#       cor 
#-0.1051681

cor.test(Hacc, dG, method="spearman")
#S = 51510.48, p-value = 0.3185
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#      rho 
#-0.125666 

cor.test(Hacc, dG, method="kendall")
#z = -0.9295, p-value = 0.3526
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#        tau 
#-0.08336809

plot(Hacc, dG, pch=20, col='red', xlab="Hydrogen Acceptors", ylab="delta G", text(18, -21, cex=0.8, "Pearson's corr. -0.1051681, p-val=0.4044\nRho -0.125666, p-val=0.3185\nTau -0.08336809, p-val=0.3526"), main="Gibb's energy Changes Vs Hydrogen Acceptors")
abline(lm(dG~Hacc), col="blue")

#####################################################################

#dGvsHd
cor.test(Hd, dG)
# t = 0.3097, df = 63, p-value = 0.7578
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.2068768  0.2802239
#sample estimates:
#       cor 
#0.03898957

cor.test(Hd, dG, method="spearman")
#S = 42800.82, p-value = 0.6088
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#      rho 
#0.0646674 

cor.test(Hd, dG, method="kendall")
#z = 0.4124, p-value = 0.6801
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#      tau 
#0.0369308

plot(Hd, dG, pch=20, col='red', xlab="Hydrogen Donors", ylab="delta G", text(10, -21, cex=0.8, "Pearson's corr. 0.03898957, p-val=0.4044\nRho 0.0646674, p-val=0.6088\nTau 0.0369308, p-val=0.6801"), main="Gibb's energy Changes Vs Hydrogen Donors")
abline(lm(dG~Hd), col="blue")

#####################################################################

#dGvsRotBonds
cor.test(RotBonds, dG)
# t = -1.9708, df = 63, p-value = 0.05314
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.457963741  0.003099767
#sample estimates:
#       cor 
#-0.2409815

cor.test(RotBonds, dG, method="spearman")
#S = 59045.42, p-value = 0.01897
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#       rho 
#-0.2903282 

cor.test(RotBonds, dG, method="kendall")
#z = -1.9404, p-value = 0.05233
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#       tau 
#-0.1711077

plot(RotBonds, dG, pch=20, col='red', xlab="Rotating Bonds", ylab="delta G", text(13, -21, cex=0.8, "Pearson's corr. -0.2409815, p-val=0.05314\nRho -0.2903282, p-val=0.01897\nTau -0.1711077, p-val=0.05233"), main="Gibb's energy Changes Vs Rotating Bonds")
abline(lm(dG~RotBonds), col="blue")

#####################################################################

#dGvsViolLepinskiRule
#cor.test(violLepinskiRule, dG)
# t = 0.3637, df = 63, p-value = 0.7173
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.2003675  0.2864696
#sample estimates:
#       cor 
#0.04576833

#cor.test(violLepinskiRule, dG, method="spearman")
#S = 41290.86, p-value = 0.4389
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#       rho 
#0.09766477 

#cor.test(violLepinskiRule, dG, method="kendall")
#z = 0.7844, p-value = 0.4328
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#       tau 
#0.07619596

plot(violLepinskiRule, dG, pch=20, col='red', xlab="No of violations of 5 Rule", text(2.5, -21, cex=0.8, "Pearson's corr. 0.04576833, p-val=0.7173\nRho 0.09766477, p-val=0.4389\nTau 0.07619596, p-val=0.4328"), ylab="delta G", main="Gibb's energy Changes Vs No of violations of 5 Rule")
abline(lm(dG~violLepinskiRule), col="blue")

#####################################################################

#dGvsPSA
cor.test(PSA, dG)
# t = -0.4921, df = 63, p-value = 0.6243
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.3012366  0.1848043
#sample estimates:
#        cor 
#-0.06188416 

#cor.test(PSA, dG, method="spearman")
#S = 51462.99, p-value = 0.3226
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#       rho 
#-0.1246283

#cor.test(PSA, dG, method="kendall")
#z = -0.867, p-value = 0.386
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#        tau 
#-0.07423804

plot(PSA, dG, pch=20, col='red', xlab="Polar Surface Area", ylab="delta G", text(300, -21, cex=0.8, "Pearson's corr. -0.06188416, p-val=0.6243\nRho -0.1246283, p-val=0.3226\nTau -0.07423804, p-val=0.386"), main="Gibb's energy Changes Vs Polar Surface Area")
abline(lm(dG~PSA), col="blue")

#####################################################################

#dGvsPolarizability
cor.test(Polarizability, dG)
  Polarizability and dG
t = -3.9768, df = 62, p-value = 0.0001852
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 -0.6271322 -0.2305591
sample estimates:
       cor 
-0.4508188 

cor.test(Polarizability, dG, method="spearman")
S = 61935.19, p-value = 0.0005898
alternative hypothesis: true rho is not equal to 0
sample estimates:
       rho 
-0.4179301 

cor.test(Polarizability, dG, method="kendall")
z = -3.2923, p-value = 0.0009936
alternative hypothesis: true tau is not equal to 0
sample estimates:
       tau 
-0.2832231 

plot(Polarizability, dG, pch=20, col='red', xlab="Polarizability", ylab="delta G", text(57, -21, cex=0.8, "Pearson's corr. -0.4508188, p-val=0.0001852\nRho -0.4179301, p-val=0.0005898\nTau -0.2832231, p-val=0.0009936"), main="Gibb's energy Changes Vs Polarizability")
abline(lm(dG~Polarizability), col="blue")

#####################################################################

#dGvsRefrIndex
cor.test(RefrIndex, dG)
# t = 0.9747, df = 62, p-value = 0.3335
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# -0.1267910  0.3578503
#sample estimates:
#     cor 
#0.122847

#cor.test(RefrIndex, dG, method="spearman")
#S = 38751.48, p-value = 0.3747
#alternative hypothesis: true rho is not equal to 0
#sample estimates:
#      rho 
#0.1128323 

#cor.test(RefrIndex, dG, method="kendall")
#z = 0.9446, p-value = 0.3448
#alternative hypothesis: true tau is not equal to 0
#sample estimates:
#       tau 
#0.08117555 

plot(RefrIndex, dG, pch=20, col='red', xlab="Refraction Index", ylab="delta G", text(1.8, -21, cex=0.8, "Pearson's corr. 0.122847, p-val=0.3335\nRho 0.1128323, p-val=0.3747\nTau 0.08117555, p-val=0.3448"), main="Gibb's energy Changes Vs Refraction Index")
abline(lm(dG~RefrIndex), col="blue")

#####################################################################
#####################################################################
#####################################################################
#dGvsMolarRefractivity
cor.test(MolarRefractivity, dG)
t = -3.979, df = 62, p-value = 0.0001838
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 -0.6272855 -0.2307984
sample estimates:
       cor 
-0.4510202

cor.test(MolarRefractivity, dG, method="spearman")
S = 61979.72, p-value = 0.00057
alternative hypothesis: true rho is not equal to 0
sample estimates:
       rho 
-0.4189497 

cor.test(MolarRefractivity, dG, method="kendall")
z = -3.3205, p-value = 0.0008987
alternative hypothesis: true tau is not equal to 0
sample estimates:
       tau 
-0.2850749 
 

plot(MolarRefractivity, dG, pch=20, col='red', xlab="Molar Refractivity", ylab="delta G", text(140, -21, cex=0.8, "Pearson's corr. -0.4510202, p-val=0.0001838\nRho -0.4189497, p-val=0.00057\nTau -0.2850749, p-val=0.0008987"), main="Gibb's energy Changes Vs Molar Refractivity")
abline(lm(dG~MolarRefractivity), col="blue")

#####################################################################

#dGvsMolar_Volume
cor.test(Molar_Volume, dG)
t = -3.7607, df = 62, p-value = 0.0003778
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 -0.6119561 -0.2071074
sample estimates:
       cor 
-0.4309761

cor.test(Molar_Volume, dG, method="spearman")
S = 62529.37, p-value = 0.0003705
alternative hypothesis: true rho is not equal to 0
sample estimates:
       rho 
-0.4315333 

cor.test(Molar_Volume, dG, method="kendall")
z = -3.3783, p-value = 0.0007294
alternative hypothesis: true tau is not equal to 0
sample estimates:
       tau 
-0.2899057 

plot(Molar_Volume, dG, pch=20, col='red', xlab="Molar Volume", ylab="delta G", text(390, -21, cex=0.8, "Pearson's corr. -0.4309761, p-val=0.0003778\nRho -0.4315333, p-val=0.0003705\nTau -0.2899057, p-val=0.0007294"), main="Gibb's energy Changes Vs Molar Volume")
abline(lm(dG~Molar_Volume), col="blue")

#####################################################################

#dGvssurfTension
cor.test(surfTension, dG)
t = 1.9088, df = 62, p-value = 0.06092
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 -0.01084656  0.45504811
sample estimates:
      cor 
0.2355909 

cor.test(surfTension, dG, method="spearman")
S = 32828.14, p-value = 0.04776
alternative hypothesis: true rho is not equal to 0
sample estimates:
      rho 
0.2484401  

cor.test(surfTension, dG, method="kendall")
z = 2.0804, p-value = 0.03749
alternative hypothesis: true tau is not equal to 0
sample estimates:
      tau 
0.1786962 

plot(surfTension, dG, pch=20, col='red', xlab="Surface Tension", ylab="delta G", text(200, -21, cex=0.8, "Pearson's corr. 0.2355909, p-val=0.06092\nRho 0.2484401, p-val=0.04776\nTau 0.1786962, p-val=0.03749"), main="Gibb's energy Changes Vs Surface Tension")
abline(lm(dG~surfTension), col="blue")

#####################################################################

