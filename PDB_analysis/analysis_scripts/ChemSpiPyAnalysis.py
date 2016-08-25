#!/usr/bin/env python

'''
MSc Bioinformatics 2015/16
MSc Thesis:
	"A Database of Thermodynamics and Structural Features of Protein-Ligand Interactions"
Author: Demetriana Pandi
Script Name: NEWAnalysisWithWaterMolecules.py'


Purpose: 
	To collect all ligand information from the ChemSpider Database. From the SMILES string that already exists 
	in the "ligand_description.txt", the ChemSpider Id is obtained using ChemSpiPy. mol_weight, av_mass, 
	monois_mass, nomin_mass, alogP, xlogP are also available from the ChemSpider wrapper, ChemSpiPy.
	All other features are retrieved by parsing the source code of the ligand page, which is accessed using the 
	ChemSpider id.
	
Steps:
	1. Access ChemSpider from ChemSpiPy. 
		If the ligand is not available from the database, continue to the next pdb file.
	2. Collect all the information that can be collected using ChemSpiPy, mol_weight, av_mass, 
	monois_mass, nomin_mass, alogP, xlogP.
	3. Access the ChemSpider ligand page, http://www.chemspider.com/Chemical-Structure.'ligand ID'.html.
	4. Copy source code in chemSpiData.txt
	5. Collect all other information of interest, hb_acceptors, hb_donors, rotating_bonds, ruleOf5_violations,
	polarSurA, Polarizability, RefrIndex, MolarRefr, SurfTension, MolarV
	6. Print all data in an excel file, "ligand_feature_table.xlsx"
		
'''


import os
import re
import sys

import urllib
import xlsxwriter
from chemspipy import ChemSpider

path = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"
analysis_dir=os.getcwd()
cs = ChemSpider('aa2df0d7-32cf-4f0f-8904-d3c413280413')

## regular expressions 	##
pdb_code="\d\w{3}"

hb_acceptors_regex="\#H bond acceptors\:\<\/td\>[^\<]*\<td class[^\>]*\>[^\d]*(\d*)[^\d]*\<\/td\>"
hb_donors_regex="\#H bond donors\:\<\/td\>[^\<]*\<td class[^\>]*\>[^\d]*(\d*)[^\d]*\<\/td\>"
rotating_bonds_regex="\#Freely Rotating Bonds\:\<\/td\>[^\<]*\<td class[^\>]*\>[^\d]*(\d*)[^\d]*\<\/td\>"
ruleOf5_violations_regex="\#Rule of 5 Violations\:\<\/td\>[^\<]*\<td class[^\>]*\>[^\d]*(\d*)[^\d]*\<\/td\>"

polarSurA_regex="Polar Surface Area\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"
Polarizability_regex="Polarizability\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"
RefrIndex_regex="Index of Refraction\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"
MolarRefr_regex="Molar Refractivity\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"

SurfTension_regex="Surface Tension\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"
MolarV_regex="Molar Volume\:\<\/td\>[^\<]*\<td class[^\>]*\>(.*)\<\/td\>"

####################################################

def html_to_string(string):

	new=string.replace('<sup>', '^')
	new=new.replace('</sup>', ' ')
	new=new.replace("\\xc2\\xb",'+-')
	new=new.replace('  ','')
	new=new.replace('\\r','')
	new=new.replace('\\n','')
	new=new.replace('&#8491;', 'A')
	return(new)

####################################################

pdb_folders = [f for f in os.listdir(path) if re.match(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

print ("There are", dirLength, "PDB files.")

LigFeatTable_xlsx=xlsxwriter.Workbook(analysis_dir+"/ligand_feature_table.xlsx")
LigFeatTable= LigFeatTable_xlsx.add_worksheet()

LigFeatTable.write_string(0,0, "PDB")
LigFeatTable.write_string(0,1, "Scorpio ID")
LigFeatTable.write_string(0,2, "Name")
LigFeatTable.write_string(0,3,'Molecular weight')
LigFeatTable.write_string(0,4,'Average Mass')
LigFeatTable.write_string(0,5, 'Momoisotopic Mass')
LigFeatTable.write_string(0,6, 'Nominal Mass')
LigFeatTable.write_string(0,7, 'AlogP')
LigFeatTable.write_string(0,8, 'XlogP')
LigFeatTable.write_string(0,9,'H-acceptors')
LigFeatTable.write_string(0,10,'H-donors')
LigFeatTable.write_string(0,11, 'Freely Rotating Bonds')
LigFeatTable.write_string(0,12, 'Rule of 5 Violations')
LigFeatTable.write_string(0,13, 'Polar Surface Area')
LigFeatTable.write_string(0,14, 'Polarizability')
LigFeatTable.write_string(0,15, 'Refraction Index')
LigFeatTable.write_string(0,16, 'Molar Refractivity')
LigFeatTable.write_string(0,17, 'Surface Tension')
LigFeatTable.write_string(0,18, 'Molar Volume')

##########		Loop through files		#############
ind=1

for f in pdb_folders:
	
	os.chdir(path+"/"+f)
	
	main=os.getcwd()

	lines=[]
	smile=''
	csid=''
	mol_weight, av_mass, monois_mass, nomin_mass, alogP, xlogP=('', '', '', '', '', '')
	hb_acceptors, hb_donors, rotating_bonds, ruleOf5_violations=('', '', '', '')
	polarSurA, Polarizability, RefrIndex, MolarRefr, SurfTension, MolarV=('', '', '', '', '', '')
	
	pdb=os.path.basename(main)
	
	ligand_file_name=main + "/ligand_description.txt"
	ligand_desc = open (ligand_file_name, 'r')
	ligand_description=ligand_desc.readlines()
	smile=ligand_description[0].split("\n")[0]
	lig_name=ligand_description[1].split("\n")[0]
	scorpioId=ligand_description[2].split("\n")[0]
	ligand_desc.close()

	result=cs.search(smile)
	
	for i in result:
		csid=i.csid

	if csid =='':
		result=cs.search(lig_name)
		for i in result:
			csid=i.csid
		if csid =='':
			print (pdb + ": Ligand "+ lig_name +" not in the ChemSpider database.")
			continue
	
	LigFeatTable.write_string(ind,0, pdb)
	LigFeatTable.write_string(ind,1, scorpioId)
	LigFeatTable.write_string(ind,2, lig_name)

	ligand=cs.get_compound(csid)

	mol_weight=str(ligand.molecular_weight)
	av_mass=str(ligand.average_mass)
	monois_mass=str(ligand.monoisotopic_mass)
	nomin_mass=str(ligand.nominal_mass)
	alogP=str(ligand.alogp)
	xlogP=str(ligand.xlogp)

	LigFeatTable.write_string(ind,3, mol_weight)
	LigFeatTable.write_string(ind,4, av_mass)
	LigFeatTable.write_string(ind,5, monois_mass)
	LigFeatTable.write_string(ind,6, nomin_mass)
	LigFeatTable.write_string(ind,7, alogP)
	LigFeatTable.write_string(ind,8, xlogP)

	comp_url="http://www.chemspider.com/Chemical-Structure." + str(csid) + ".html"
	
	response = urllib.request.urlopen(comp_url)
	html_b = response.read()
	
	chemFile = open ("chemSpiData.txt", 'w', encoding='utf-8')
	print(html_b, file=chemFile)
	chemFile.close()
	
	complete_text=''

	chemFile=open("chemSpiData.txt", "r")
	source_line=chemFile.read()
	chemFile.close()

	lines=re.search("(\<table.*\<\/table\>)", source_line).group(1)
	table=lines.split('</tr>')

	chemData=open("chemSpiData.txt", "w")

	chemData.write("Molecular Weight\t" + mol_weight + "\n")
	chemData.write("Average Mass\t" + av_mass + "\n")
	chemData.write("Momoisotopic Mass\t" + monois_mass + "\n")
	chemData.write("Nominal Mass\t" + nomin_mass + "\n")
	chemData.write("AlogP\t" + alogP + "\n")
	chemData.write("XlogP\t" + xlogP + "\n\n")


	for i in table:	
		if re.search(hb_acceptors_regex, i):
			hb_acceptors=re.search(hb_acceptors_regex, i).group(1)
			hb_acceptors=html_to_string(hb_acceptors)
			chemData.write("H-acceptors\t" + hb_acceptors + "\n")
		if re.search(hb_donors_regex, i):
			hb_donors=re.search(hb_donors_regex, i).group(1)
			hb_donors=html_to_string(hb_donors)
			chemData.write("H-donors\t" + hb_donors + "\n")
		if re.search(rotating_bonds_regex, i):
			rotating_bonds=re.search(rotating_bonds_regex, i).group(1)
			rotating_bonds=html_to_string(rotating_bonds)
			chemData.write("Freely Rotating Bonds\t" + rotating_bonds + "\n")
		if re.search(ruleOf5_violations_regex, i):
			ruleOf5_violations=re.search(ruleOf5_violations_regex, i).group(1)
			ruleOf5_violations=html_to_string(ruleOf5_violations)		
			chemData.write("Rule of 5 Violations\t" + ruleOf5_violations + "\n\n")
	
		if re.search(polarSurA_regex, i):
			polarSurA=re.search(polarSurA_regex, i).group(1)
			polarSurA=html_to_string(polarSurA)
			chemData.write("Polar Surface Area\t" + polarSurA + "\n")
		if re.search(Polarizability_regex, i):
			Polarizability=re.search(Polarizability_regex, i).group(1)
			Polarizability=html_to_string(Polarizability)
			chemData.write("Polarizability\t" + Polarizability + "\n")
		if re.search(RefrIndex_regex, i):
			RefrIndex=re.search(RefrIndex_regex, i).group(1)
			RefrIndex=html_to_string(RefrIndex)
			chemData.write("Refraction Index\t" + RefrIndex + "\n")
		if re.search(MolarRefr_regex, i):
			MolarRefr=re.search(MolarRefr_regex, i).group(1)
			MolarRefr=html_to_string(MolarRefr)
			chemData.write("Molar Refractivity\t" + MolarRefr + "\n")
		if re.search(SurfTension_regex, i):
			SurfTension=re.search(SurfTension_regex, i).group(1)
			SurfTension=html_to_string(SurfTension)
			chemData.write("Surface Tension\t" + SurfTension + "\n")
		if re.search(MolarV_regex, i):
			MolarV=re.search(MolarV_regex, i).group(1)
			MolarV=html_to_string(MolarV)
			chemData.write("Molar Volume\t" + MolarV + "\n")

	chemFile.close()

	LigFeatTable.write_string(ind,9,hb_acceptors)
	LigFeatTable.write_string(ind,10,hb_donors)
	LigFeatTable.write_string(ind,11, rotating_bonds)
	LigFeatTable.write_string(ind,12, ruleOf5_violations)
	LigFeatTable.write_string(ind,13, polarSurA)
	LigFeatTable.write_string(ind,14, Polarizability)
	LigFeatTable.write_string(ind,15, RefrIndex)
	LigFeatTable.write_string(ind,16, MolarRefr)
	LigFeatTable.write_string(ind,17, SurfTension)
	LigFeatTable.write_string(ind,18, MolarV)

	ind=ind+1

	os.chdir(path)

LigFeatTable_xlsx.close()
sys.exit(1)	
