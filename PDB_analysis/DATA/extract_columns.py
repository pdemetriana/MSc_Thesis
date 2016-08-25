#!/usr/bin/env python

############################################################

import os
from os import listdir
import re
import pyexcel

# R-data file
dataSet=open("Analysis_dataSet.txt", 'w')
dataSet.write("PDB\tN\tDeltaG\tdeltaH\tTdeltaS\tKd\tMoleWeight\tAvMass\tMomoisMass\tNomMass\tAlogP\tXlogP\tH_acceptors\tH_donors\tFreelyRotBonds\tRuleOf5Violations\tPolarSurfaceArea\tPolarizability\tRefractionIndex\tMolarRefractivity\tSurface_Tension\tMolar_Volume\t\n")

#"PDB	N	DeltaG(kJ/mol)	deltaH(kJ/mol)	TdeltaS(kJ/mol)	Kd(uM)"
my_data = pyexcel.get_sheet(file_name="itc_data.xlsx") 

#"PDB	Molecular weight	Average Mass	Momoisotopic Mass	Nominal Mass	AlogP	XlogP	H-acceptors	H-donors	Freely Rotating Bonds	Rule of 5 Violations	Polar Surface Area(A^2)	Polarizability(+- 10.5 10^-24 cm^3)	Refraction Index	Molar Refractivity(cm^3)	Surface Tension(dyne/cm)	Molar Volume(cm^3)"
my_ligand = pyexcel.get_sheet(file_name="ligand_feature_table.xlsx")

my_itc=[]
i=1
while i < len(my_data.column[0]):
	itc_row=[]
	for l in my_data.row[i]:
		l=str(l)
		l=l.split(' ')[0]
		l=l.split('+-')[0]
		itc_row.append(l)
	my_itc.append(itc_row)
	i=i+1

my_ligFeat=[]
i=1
while i < len(my_ligand.column[0]):
	ligFeat_row=[]
	for l in my_ligand.row[i]:
		l=str(l)
		l=l.split(' ')[0]
		l=l.split('+-')[0]
		ligFeat_row.append(l)
	my_ligFeat.append(ligFeat_row)
	i=i+1

#################################################

#################################################
	
compl_data=[]
for l in my_ligFeat:
	pdb=l[0]
	for d in my_itc:
		pdb_d=d[0]
		if pdb_d == pdb:
			del l[0]
			compl_data.append([d, l])

			
for row in compl_data:
	itc, lig=row
	for i in itc:
		dataSet.write(i+"\t")
	for i in lig:
		dataSet.write(i+"\t")
	dataSet.write("\n")
dataSet.close()
	
	














