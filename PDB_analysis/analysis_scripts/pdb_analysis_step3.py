#!/usr/bin/env python

############################################################

import os
from os import listdir
from os.path import isfile,isdir
import shutil #allows files to be copied or moved between dirs
import sys # Allows exit for error messages

import re

path = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"
os.chdir(path)
## regular expressions 	##
pdb_code="^\d\w{3}$"

mlc_name="[A-Z0-9]{4}\.pdb"

pdb_folders = [f for f in os.listdir(path) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

#########################

def get_optimal_complex_dir():
	max_contacts=0
	opt_complex=''
	os.mkdir("Conformation_Model")
	destination="Conformation_Model"
	with open ("all_contacts.txt", 'r') as log:
		lines=log.readlines()
		for line in lines:
			line=line.split(',')
			if re.match(r"pdb_ref", line[0]) :
				pass
			else:
				pdb, chain, ligand, polar_c, apolar_c, water_c, total_c=line
				if int(total_c) > max_contacts:
					max_contacts=int(total_c)
					opt_complex=ligand
					opt_line=pdb + "\t" + chain + "\t" + ligand + "\t" + polar_c + "\t" + apolar_c + "\t" + water_c + "\t" + total_c
		log.close()

	log=open("all_contacts.txt", 'a+')
	log.write("\nMax_Contacts\t"+opt_line)
	log.close()

	chain, ligand, dir=opt_complex.split('_')
	
	ligand_regex=r"_"+re.escape(ligand)+r".mol2"

	chain_regex=r"_PTNChain"+re.escape(chain)+r".pdb"
	
	chain_file=[f for f in os.listdir(os.getcwd()) if re.search(chain_regex, f)]
	chain_path=str(os.getcwd()+"/"+chain_file[0])
	
	if re.search(pdb_code, dir):
		ligand_file=[f for f in os.listdir(os.getcwd()) if re.search(ligand_regex, f)]
		ligand_path=str(os.getcwd()+"/"+ligand_file[0])
	else:
		os.chdir(dir)
		ligand_file=[f for f in os.listdir(os.getcwd()) if re.search(ligand_regex, f)]
		ligand_path=str(os.getcwd()+"/"+ligand_file[0])
		os.chdir("..")
	ligand_pdb=ligand_path.split('.')[0]  + r".pdb"
	shutil.copy(chain_path, destination)
	shutil.copy(ligand_path, destination)


##########		Find optimal ligand		#############

for f in pdb_folders:
	
	os.chdir(f)
	top_dir=os.getcwd()
	pdb_code=os.path.basename(f)
	
	get_optimal_complex_dir()
	
	os.chdir("Conformation_Model")
	
	###		step 5, run ProAct for water		###
	os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChangeInContactsLog.py')
	
	## repeat including water
	os.chdir(top_dir)
	os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWAnalysisWithWaterMolecules.py')
	
	os.chdir("Conformation_with_water")

	###		step 5, run ProAct for water		###
	print(os.getcwd())
	os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChangeInContactsLogV2.py')
	
	os.chdir(path)