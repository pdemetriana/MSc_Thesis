#!/usr/bin/env python

############################################################

import os
from os import listdir
from os.path import isfile,isdir
import shutil #allows files to be copied or moved between dirs
import sys # Allows exit for error messages

import re

## regular expressions 	##
pdb_code="^\d\w{3}$"
lig_name="[A-Z0-9]{2}"

mlc_ligands = open("mlc_ligands.txt", 'a+')

path = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"
os.chdir(path)

pdb_folders = [f for f in os.listdir(path) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

##########		Create directories		#############

for f in pdb_folders:
	
	os.chdir(f)
	pdb_code=os.path.basename(f)
	mlc_name=pdb_code+"[A-Z0-9]+\.pdb"
	
	contact_log=open("all_contacts.txt", "a+")
	
	PDB_file = os.getcwd()
	all_files=[f for f in os.listdir(PDB_file)]
	peptides = [p for p in os.listdir(PDB_file) if  p.endswith(".mol2")]
	
	###		for peptide ligands		###
	if len(peptides)>0:
		
		#step 3
		os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWDirectoryManagerTypeIII.py')
		
		#step 4
		os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWpro_CLic_runDirectories.py')
		os.chdir(PDB_file)
		
		if os.path.isfile(pdb_code+"_log.csv"):
			
			log_file=open((pdb_code+"_log.csv"), 'r')
			logRead=log_file.read()
			log_file.close()
			
			contact_log.write(logRead)	
		
		###		split chemical ligands		###
		#step 1
		os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChainSeparate2PDB_PtnLigUNIX_dir.py')
		os.chdir(PDB_file)
		#step 3 (ligand dir)
		all_files=[f for f in os.listdir(PDB_file)]
		
		# for ligands with multiple conformations
		mlc_list=[f for f in all_files if re.search(mlc_name, f) and f.endswith(".pdb")]
		if len(mlc_list)>0:
			mlc_ligands.write(pdb_code + "\n")
			print("PDB code "+pdb_code+" moved to mlc_ligands.txt")
			contact_log.close()		
			os.chdir(path)
			continue
			'''
			#step 1
			os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChainSeparate2PDB_PtnLigUNIX_dir.py')
			all_files=[f for f in os.listdir(PDB_file)]
			'''
		for i in all_files:
			if os.path.isdir(i):
				if re.search(lig_name, i):
					os.chdir(i)
					
					#step 3 (ligand dir)
					os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWDirectoryManagerTypeIII.py')
					
					#step 4 (ligand dir)
					os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWpro_CLic_runDirectories.py')
					
					if os.path.isfile(pdb_code+"_log.csv"):
						
						log_file= open ((pdb_code+"_log.csv"), 'r')
						logRead=log_file.read()
						log_file.close()
						
						contact_log.write(logRead)
					else:
						pass
					os.chdir("..")
	
	#if there are no peptide ligands
	else:
		# for ligands with multiple conformations
		mlc_list=[f for f in all_files if re.search(mlc_name, f) and f.endswith(".pdb")]
		if len(mlc_list)>0:
			'''mlc_ligands.write(pdb_code + "\n")
			print("PDB code "+pdb_code+" moved to mlc_ligands.txt")
			contact_log.close()		
			os.chdir(path)
			continue
			'''
			#step 1
			os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChainSeparate2PDB_PtnLigUNIX_dir.py')
			all_files=[f for f in os.listdir(PDB_file)]
			os.chdir(PDB_file)
			

		for i in all_files:
			#go to ligand dir
			if os.path.isdir(i):
				if re.search(lig_name, i):
					os.chdir(i)
					#step 3
					os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWDirectoryManagerTypeIII.py')
				
					#step4				
					os.system ('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWpro_CLic_runDirectories.py')
					
					if os.path.isfile(pdb_code+"_log.csv"):
						
						log_file= open ((pdb_code+"_log.csv"), 'r')
						logRead=log_file.read()
						log_file.close()
						
						contact_log.write(logRead)
					
					else:
						pass
					os.chdir("..")
	contact_log.close()		
	os.chdir(path)				
	
mlc_ligands.close()