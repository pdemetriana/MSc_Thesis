#!/usr/bin/env python

############################################################

import os
from os import listdir
import re
import pyexcel

# R-data file
dataSet=open("Analysis_dataSet_ProACt.txt", 'w')
dataSet.write("PDB\tN\tDeltaG\tdeltaH\tTdeltaS\tKd\tHBondsNo\tPolar_Contacts\tApolar_Contacts\tPolar_Water_Contacts\tApolar_Water_Contacts\tSurface_Waters\tCleft_Waters\tBuried_Waters\t\n")

#"PDB	N	DeltaG(kJ/mol)	deltaH(kJ/mol)	TdeltaS(kJ/mol)	Kd(uM)"
my_data = pyexcel.get_sheet(file_name="itc_data.xlsx") 

my_contacts_file = pyexcel.get_sheet(file_name="ComplexContacts_table.xlsx")

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

my_contacts=[]
i=1
while i < len(my_contacts_file.column[0]):
	contacts_row=[]
	for l in my_contacts_file.row[i]:
		l=str(l)
		contacts_row.append(l)
	my_contacts.append(contacts_row)
	i=i+1

#################################################

#################################################
	
compl_data=[]
for l in my_contacts:
	pdb=l[0]
	for d in my_itc:
		pdb_d=d[0]
		if pdb_d == pdb:
			del l[0]
			compl_data.append([d, l])

			
for row in compl_data:
	itc, contacts=row
	for i in itc:
		dataSet.write(i+"\t")
	for i in contacts:
		dataSet.write(i+"\t")
	dataSet.write("\n")
dataSet.close()
	
	














