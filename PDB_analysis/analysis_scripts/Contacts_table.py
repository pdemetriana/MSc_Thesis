#!/usr/bin/env python

############################################################

import os
from os import listdir
from os.path import isfile,isdir
import xlsxwriter
import sys # Allows exit for error messages

import re

path = "C:/Users/demetriana/Documents/PDB_analysis/PDB_Files"

os.chdir(path)

## regular expressions 	##
pdb_code="\d\w{3}"
hydr_regex="^\#(0|1)[^\#]*\#(0|1).*"

polarC="Change in Polar Contacts: (\-?\d.*)"
apolarC="Change in Apolar Contacts: (\-?\d.*)"
polarW="Change in Polar Water Contacts: (\-?\d.*)"
apolarW="Change in Apolar Water Contacts: (\-?\d.*)"

surfW="Number surface waters: (\-?\d.*)"
cleftW="Number cleft waters: (\-?\d.*)"
buriedW="Number buried waters: (\-?\d.*)"

pdb_folders = [f for f in os.listdir(path) if re.search(pdb_code, os.path.basename(f))]

dirLength = len(pdb_folders)

#print (pdb_folders)
print ("There are", dirLength, "PDB files.")

#############		Split complex		##################

hbTable_xlsx=xlsxwriter.Workbook("C:/Users/demetriana/Documents/PDB_analysis/DATA/ComplexContacts_table.xlsx")
hbTable= hbTable_xlsx.add_worksheet()

hbTable.write_string(0,0, "PDB")
hbTable.write_string(0,1, "Number of HBonds")
hbTable.write_string(0,2, "Polar Contacts")
hbTable.write_string(0,3, "Apolar Contacts")
hbTable.write_string(0,4, "Polar Water Contacts")
hbTable.write_string(0,5, "Apolar Water Contacts")
hbTable.write_string(0,6, "Surface Waters")
hbTable.write_string(0,7, "Cleft Waters")
hbTable.write_string(0,8, "Buried Waters")


'''
hbTable.write_string(0,2, "Residue 1")
hbTable.write_string(0,3, "Residue 2")
hbTable.write_string(0,4, "Distance")
'''	
i=1
for f in pdb_folders:
	
	pdb=str(f)
	
	os.chdir(f)
	pdb_dir=os.getcwd()
	
	os.chdir("Conformation_Model")
	
	chimera_f=open("chimerafile.txt", 'r')
	chim_lines=chimera_f.readlines()
	chimera_f.close()

	hbond_list=[]
	for line in chim_lines:
		if re.search(hydr_regex, line):
			first_res=re.search(hydr_regex, line).group(1)
			sec_res=re.search(hydr_regex, line).group(2)
			#print(first_res, sec_res)
			if first_res!=sec_res:
				hbond_list.append(line)

	noOfBonds=str(len(hbond_list))
	
	'''
	hBonds=[]	
	for row in hbond_list:
		res1=re.search("^\#\d (\w*)", row).group(1)
		res2=re.search("^\#\d[^\#]*\#\d (\w*)", row).group(1)
		distance=re.search("  ([^\s]*)  [^\s]*$", row).group(1)
		hBonds.append([pdb, res1, res2, distance])
		hbTable.write_string(i,2, res1)
		hbTable.write_string(i,3, res2)
		hbTable.write_string(i,4, distance)
	'''
	if os.path.isfile(f+"_ContactChange_log.txt"):
		contacts_log=open(f+"_ContactChange_log.txt", 'r')
		log_lines=contacts_log.readlines()
		contacts_log.close()
	
	polContacts, apolContacts, polWcontacts, apolWcontacts=('', '', '', '')
	contacts_list=[]
	for line in log_lines:
		if re.search(polarC, line):
			polContacts=re.search(polarC, line).group(1)
		if re.search(apolarC, line):
			apolContacts=re.search(apolarC, line).group(1)
		if re.search(polarW, line):
			polWcontacts=re.search(polarW, line).group(1)
		if re.search(apolarW, line):
			apolWcontacts=re.search(apolarW, line).group(1)		

	os.chdir(pdb_dir +"/Conformation_with_water")
	
	if os.path.isfile(f+"_ContactChange_log.txt"):
		water_log=open(f+"_ContactChange_log.txt", 'r')
		water_lines=water_log.readlines()
		water_log.close()

	surfWaters, cleftWaters, buriedWaters=('','','')
	for line in water_lines:
		if re.search(surfW, line):
			surfWaters=re.search(surfW, line).group(1)
		if re.search(cleftW, line):
			cleftWaters=re.search(cleftW, line).group(1)	
		if re.search(buriedW, line):
			buriedWaters=re.search(buriedW, line).group(1)

	hbTable.write_string(i,0, pdb)
	hbTable.write_string(i,1, noOfBonds)
	hbTable.write_string(i,2, polContacts)
	hbTable.write_string(i,3, apolContacts)
	hbTable.write_string(i,4, polWcontacts)
	hbTable.write_string(i,5, apolWcontacts)
	hbTable.write_string(i,6, surfWaters)
	hbTable.write_string(i,7, cleftWaters)
	hbTable.write_string(i,8, buriedWaters)

	i=i+1
	
	os.chdir(path)

hbTable_xlsx.close()
