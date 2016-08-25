#!/usr/bin/env python

############################################################

import os
import re, sys, shutil

## regular expressions 	##
water_atom="HETATM\s.*\sHOH\s"
ligand_atom="HETATM\s.*\s[A-Z0-9]{2,}\s"

hetatmRow="HETATM\s\w+\s*\w+\s*\w+\s+\w+\s\w+\s*(\-?\d+\.?\d*)\s*(\-?\d+\.?\d*)\s*(\-?\d+\.?\d*)\s"

######### functions	#########
def atoms_distance(coordinates, ligandAtom_coordinates):
	x, y, z = coordinates
	x, y, z = (float(x), float(y), float(z))
	
	for ligand in ligandAtom_coordinates:
		a, b, c = ligand
		a, b, c = (float(a), float(b), float(c))
		distanceSqr = (x-a)**2 + (y-b)**2 + (z-c)**2
		distance=distanceSqr**(1/2)

		if distance < 10:
			return('y')
		else:
			continue
	return('n')


pdb_dir = os.getcwd()
pdb_code= os.path.basename(pdb_dir)

pdb_original = os.getcwd() + "/" + pdb_code + ".pdb"

#keep pdb lines for later
pdb_file=open(pdb_original, 'r')
pdb_lines=pdb_file.readlines()
pdb_file.close()

##### create new dir with chain files

os.mkdir("Conformation_with_water")
destination=pdb_dir + "/Conformation_with_water"

os.chdir("Conformation_Model")

chain=[f for f in os.listdir(os.getcwd()) if f.endswith(".pdb")]
ligand=[f for f in os.listdir(os.getcwd()) if f.endswith(".mol2")]

for i in chain:
	shutil.copy(os.getcwd()+"/"+i, destination)
for i in ligand:
	shutil.copy(os.getcwd()+"/"+i, destination)

os.chdir(destination)

chains=[f for f in os.listdir(os.getcwd()) if f.endswith(".pdb")]
new_chain_file=chains[0] 

## append files
######## add water atoms

new_chain=open(new_chain_file, 'a+')

waterAtom_list=[]
for line in pdb_lines:
	if re.search(water_atom, line):
		waterAtom_list.append(line)
		
ligandAtom_list=[]
for line in pdb_lines:
	if re.search(ligand_atom, line):
		if line not in waterAtom_list:
			ligandAtom_list.append(line)



ligandAtom_coordinates=[]
for atom in ligandAtom_list:
	x=re.search(hetatmRow, atom).group(1)
	y=re.search(hetatmRow, atom).group(2)
	z=re.search(hetatmRow, atom).group(3)
	ligandAtom_coordinates.append([x, y, z])
	

waterAtom_coordinates=[]
for atom in waterAtom_list:
	x=re.search(hetatmRow, atom).group(1)
	y=re.search(hetatmRow, atom).group(2)
	z=re.search(hetatmRow, atom).group(3)
	waterAtom_coordinates.append([x, y, z])
	
	is_close=atoms_distance([x, y, z], ligandAtom_coordinates)

	if is_close=='y':
		new_chain.write(atom)

os.chdir(pdb_dir)
sys.exit(1)		