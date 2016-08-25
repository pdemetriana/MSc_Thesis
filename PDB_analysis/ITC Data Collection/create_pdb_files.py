#!/usr/bin/env python

'''
MSc Bioinformatics 2015/16
MSc Thesis:
	"A Database of Thermodynamics and Structural Features of Protein-Ligand Interactions"
Author: Demetriana Pandi
Script Name: create_pdb_files


Purpose: 
		To create individual pdb sub-directories inside PDB_Files containing
		ligand information and the corresponding pdb file obtained by the 
		Protein Data Bank.
		
Steps:
	1. Read pdb_codes.txt.
	2. Create a list with the pdb codes from the file.
	3. Loop through the pdb list.
	4. Collect the pdb code, SMILES, name and Scorpio ID.
	5. Create a directory with the name of the pdb.
	6. Create "ligand_description.txt".
	7. Write the ligand name, SMILES and Scorpio ID in the file.
	8. Access Protein Data Bank by 
			http://files.rcsb.org/view/'pdb'.pdb.
	9. Copy the PDB file into the directory.

'''

import urllib
from urllib.request import urlopen

import os
import operator
import re, sys
import shutil

#######		Regular expressions		#######
line_regex="^(.*)\t(.*)\t(.*)\t(.*)"

if not os.path.exists('PDB_Files'):
    os.mkdir('PDB_Files')
	
# Retrieve the content of the file
pdb_codes = open("pdb_codes.txt", 'r')
pdbs=pdb_codes.readlines()
pdb_codes.close()

os.chdir('PDB_Files')

for code in pdbs:
	#Collect the pdb code, SMILES, name and Scorpio ID
	PDB_Code = re.search(line_regex, code).group(1)
	smi_string=re.search(line_regex, code).group(2)
	name=re.search(line_regex, code).group(3)
	id=re.search(line_regex, code).group(4)

	#Create a directory with the name of the pdb
	os.mkdir(PDB_Code)
	
	os.chdir(PDB_Code)
	
	smi_file=open("ligand_description.txt", 'w')
	smi_file.write(smi_string+"\n"+name+"\n"+id)
	smi_file.close()
	
	pdb_dir=os.getcwd()
	
	#find pdb file from Protein Data Bank
	pdb_url = 'http://files.rcsb.org/view/' + PDB_Code +'.pdb'
       
	pdb_file = pdb_dir + "/" + PDB_Code + ".pdb"
	
	pdb_write_file=open(pdb_file, 'w')
	
	req = urllib.request.Request(pdb_url)
	#Copy the pdb file into 'PDB_Code'.pdb
	with urllib.request.urlopen(req) as response:
		read_pdb = response.read()
		pdb_str=str(read_pdb,'UTF-8')
		pdb_write_file.write(pdb_str)
	
	pdb_write_file.close()
	
	os.chdir('..')