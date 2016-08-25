#!/usr/bin/env python

############################################################

import os
from chimera import runCommand # use 'rc' as shorthand for runCommand
from chimera import replyobj # for emitting status messages
import re

## regular expressions 	##
pdb_code="\d\w{3}"

main = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"

pdb_folders = [f for f in os.listdir(main) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

##########		Loop through files		#############

for f in pdb_folders:

	os.chdir(main + "/" + f + "/Conformation_Model")
	
	path=os.getcwd() 

	chimerafile=path+"/chimerafile.txt"
	
# gather the names of .pdb files in the folder

	pdbs=[fn for fn in os.listdir(path) if fn.endswith(".pdb")]

	ligand = [fn for fn in os.listdir(path) if fn.endswith(".mol2")]
	ligand_name=ligand[0]

	for i in pdbs:
		if i.split('.')[0] == ligand_name.split('.')[0]:
			pass
		else:
			chain_name=i

	runCommand("open " + ligand_name)
	runCommand("addh")
	runCommand("open " + chain_name)
	runCommand("select #all")
	runCommand("hbonds selRestrict #0 saveFile " + chimerafile)
	runCommand("close session")
	os.chdir(main)
runCommand("stop now")