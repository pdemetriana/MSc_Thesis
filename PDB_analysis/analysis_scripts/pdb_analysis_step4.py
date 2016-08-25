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
pdb_code="\d\w{3}"
lig_name="[A-Z]{3}"
mlc_name="[A-Z]{4}\.pdb"

pdb_folders = [f for f in os.listdir(path) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

chimera="C:/Program Files/Chimera 1.10.2/bin"
os.chdir(chimera)
os.system("chimera.exe --gui C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/chimera_HBond.py")
os.chdir(path)
sys.exit(1)
