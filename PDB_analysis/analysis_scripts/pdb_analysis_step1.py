#!/usr/bin/env python

############################################################

import os
from os import listdir

import re

path = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"
os.chdir(path)
## regular expressions 	##
pdb_code="\d\w{3}"
lig_name="[A-Z]{3}"
mlc_name="[A-Z]{4}\.pdb"

pdb_folders = [f for f in os.listdir(path) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

#############		Split complex		##################

for f in pdb_folders:
	
	os.chdir(f)
	pdb_code=os.path.basename(f)
	contact_log=open("all_contacts.txt", "a+")
	
	###		step 1, split protein chains		###
	os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWChainSeparate2PDB_PtnLigUNIX_dir.py')
	
	os.chdir(path)