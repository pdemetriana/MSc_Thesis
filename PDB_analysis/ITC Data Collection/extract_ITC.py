#!/usr/bin/env python

'''
MSc Bioinformatics 2015/16
MSc Thesis:
	"A Database of Thermodynamics and Structural Features of Protein-Ligand Interactions"
Author: Demetriana Pandi
Script Name: create_pdb_files


Purpose: 
		To collect pdb structures from Scorpio WebSite including
		ligand information, name, SMILES, Scorpio ID for the ligand
		of each pdb structure. This information is printed in "pdb_codes.txt"
		ITC data for each complex are also collected and placed 
		in "itc_data.xlsx".
		
		*Since html parsing is necessary many times, functions use an
		intermediate file "source_html.txt" where the source code is
		placed.
		
Steps:
	1. Collect source code from 'structure' page.
	2. From source code collect ligand Scorpio ID and the ITC-page link.
		The ligand information including the pdb code are printed in "pdb_codes.txt".
	3. Access ligand page using the ligand Scorpio ID and collect ligand name and SMILES.
	4. Access ITC page and collect raw table data for each structure.
	5. Loop through the obtained list.
	6. If the temperature of the ITC experiment was 25C, 
		collect ITC data and print into "itc_data.xlsx".
'''

import urllib
from urllib import request
import os
import re
import sys
import xlsxwriter

path=os.getcwd()

###		Regular Expressions		###

view_pdb_regex="\/structure\/view\/(\d+)\"\>Link\<\/a\>\<\/td\>[^\>]*\<td\>\<[^\>]*\>(\w{4})\<"
table_regex="\<table(.+)\<\/table\>"

itc_link_regex="\<td\>\<a href\=\"\/itc\/view\/(\d+)\"\>Link\<\/a\>"
ligand_link_regex="\<a class\=\"thumbnail\" href\=\"\/ligand\/view\/(\d+)\"\>"
smi_regex="\<th\>SMILES\<\/th\>[^\<]*\<td\>(.*)"
lig_name_regex="\<th\>Name<\/th\>[^\<]*\<td\>(.*)"

temp_regex="\<th\>Temp\. \((\w)\)\<\/th\>[^\<]*\<td\>[^\d]*(\d*\.?\d*)[^\<\d]*\<\/td\>"
pH_regex="\<th\>pH\<\/th\>[^\<]*\<td\>[^\d]*(\d*\.?\d*)[^\<\d]*\<\/td\>"

####################################


######### functions for collecting source code #########
def collect_structure_source():

	'''
	This function reads the 6 structure pages of Scorpio, a list of pdb codes with protein and ligand names,
	and collects the source code into "source_html.txt".
	The aim is to collect the structure list in order to retrieve structure information
	later on.
	'''
	source_code=open("source_html.txt", 'w', encoding='utf-8')
	serial=1
	while serial < 7:
		source_code.write("\nPage no " + str(serial) + "\n")
		url="http://scorpio2.biophysics.ismb.lon.ac.uk/structure/browse?page=" + str(serial)
		req = urllib.request.Request(url)	
		with urllib.request.urlopen(req) as response:
			the_page = response.read()
		print(the_page, file=source_code)
		
		serial =serial +1
	
	source_code.close()


def collect_source(list, url_base):

	'''
	The input of this function is a url base, eg "http://scorpio2.biophysics.ismb.lon.ac.uk/ligand/view/".
	and a list of ids with their corresponding pdb code that refer to a specific page, 
	eg "http://scorpio2.biophysics.ismb.lon.ac.uk/ligand/view/12".
	The fuction collects the source code for each of these pages and prints it in "source_html.txt"
	including the Id and pdb code.
	'''
	source_code=open("source_html.txt", 'w', encoding='utf-8')

	for row in list:
		pdb, num =row
	
		source_code.write("\nNumber " + num + " PDB Code " + pdb + "\n")
		url=url_base + num
		req = urllib.request.Request(url)
		
		with urllib.request.urlopen(req) as response:
			the_page = response.read()
		print(the_page, file=source_code)

	source_code.close()
		
	source_code=open("source_html.txt", 'r')
	source_lines=source_code.readlines()
	source_code.close()
	
	return(source_lines)
	
###################################################################

def collect_temp_and_pH(table):

	'''
	From raw table data, this function extracts the experimental temperature.
	It converts the temperature to Celcius and returns 'y' if it's 25 and 
	'n' if it's not.
	'''
	unit=re.search(temp_regex, table).group(1)
	temp=re.search(temp_regex, table).group(2)
	
	pH=re.search(pH_regex, table).group(1)

	if unit == 'K':
		temp = round(float(temp) - 273.15)
	if str(temp) == '25':
		#print(temp)
		return('y')
	else:
		#print(temp)
		return('n')

######################################

def collect_VIEW_PDB():

	'''
	The function reads the "source_html.txt" and extracts a list of pdb codes
	with their structure ids(view_no)
	'''
	
	collect_structure_source()

	source_code=open("source_html.txt", 'r')
	lines=source_code.readlines()
	source_code.close()

	pages=[]
	for line in lines:
		if re.search(r"DOCTYPE HTML", line):
			pages.append(line)

	structures=[]
	for line in pages:
		classes=line.split(str('<tr class='))
		for i in classes:
			if i == classes[0]:
				pass
			else:
				structures.append(i)

	struc_details=[]			
	for s in structures:
		view_no=re.search(view_pdb_regex, s).group(1)
		pdb=re.search(view_pdb_regex, s).group(2)
		struc_details.append([pdb, view_no])
	
	return(struc_details)
#####################################################

def collect_table_raw(list):

	'''
	The input is a list containing the pdb code of the structure and the source code of a page.
	The function is used to isolate table information from a source code and return it in a list with the pdb code.
	'''
	tables=[]
	for row in list:
		if re.search("PDB Code (\w+)", row):
			pdb=re.search("PDB Code (\w+)", row).group(1)
		if re.search(r'DOCTYPE HTML', row):
			if re.search(table_regex, row):
				table_data=re.search(table_regex, row).group(1)
				tables.append([pdb, table_data])
			else:
				print ("No data for structure with pdb code "+pdb+".")
	return(tables)

def collect_Links_Ligand_no(tables):

	'''
	From the table extracted from the structure source code, it collects the ligadn number - Scorpio ID
	and the link leading to the ITC information of the complex.
	'''
	
	links=[]
	ligands=[]
	for i in tables:
		pdb, data = i
		lines=data.split('</td>')
		for l in lines:
			if re.search(itc_link_regex, l):
				link_no=re.search(itc_link_regex, l).group(1)
				links.append([pdb, link_no])
		ligand_no=re.search(ligand_link_regex, lines[2]).group(1)
		ligands.append([pdb, ligand_no])
	return(ligands, links)

def collect_SMILES(list):

	'''
	The input is a list containing the pdb and Scorpio ID(number) and also the source code
	of the ligand page.
	The function creates the "pdb_codes.txt" and after extracting the pdb, id, SMILES string and name,
	it prints them in the file separated by tabs. 
	'''
	pdb_codes=open("pdb_codes.txt", 'w')
	
	smiles=[]
	for row in list:
		if re.search("PDB Code ", row):
			pdb=re.search("PDB Code (\w+)", row).group(1)
			id=re.search("Number (\d+)", row).group(1)
		if re.search(r'DOCTYPE HTML', row):
			split_r=row.split('</td>')
			for i in split_r:
				if re.search(smi_regex, i):
					smi=re.search(smi_regex, i).group(1)
				if re.search(lig_name_regex, i):
					name=re.search(lig_name_regex, i).group(1)
			smiles.append([pdb, smi, name, id])
			pdb_codes.write(pdb + "\t" + smi + "\t" + name + "\t" + id + "\n")	
					
	pdb_codes.close()
	
##################################################################

def get_ITC_table_values(column):

	'''
	Given a table column with the ITC value, it extracts the actual
	value as V and the error as v_2, if it exists. It returns a string 
	V =str(V + " +- " + v_2) and the unit of the measurement eg. 'KJ/mol'.
	'''
	V, v_2, unit=('', '', '')

	list=column.split('</td>')
	if re.search("(\<a[^\>]+\>)?(\-?\d+\.?\d+)", list[0]):
		V=re.search("(\<a[^\>]+\>)?(\-?\d+\.?\d+)", list[0]).group(2)
	if re.search("(\<a[^\>]+\>)?(\-?\d+\.?\d+)", list[1]):
		v_2=re.search("(\<a[^\>]+\>)?(\d+\.?\d+)", list[1]).group(2)
	if re.search("\<td\>[^\;]*$", list[2]):
		unit=re.search("\<td\>(.*)", list[2]).group(1)
	if V != '':
		if v_2!= '':
			V =str(V + " +- " + v_2)
	
	return (V, unit)

def collect_itc_data(table_row):

	'''
	The function collects all ITC data, N, delta_G, delta_H, Tdelta_S, Kd, delta_C
	for a pdb structure, given in the form of html table that was extracted from the
	source code of the ITC page.
	'''
	data=[]
	
	pdb, table=table_row
	rows=table.split('</tr>')
	N, delta_G, delta_H, Tdelta_S, Kd, delta_C=[rows[7], rows[8], rows[9], rows[10], rows[11], rows[12]]
	
	n, Nunit=get_ITC_table_values(N)
	data.append([n, Nunit])
	
	dG, dGunit=get_ITC_table_values(delta_G)
	data.append([dG, dGunit])
	
	dH, dHunit=get_ITC_table_values(delta_H)
	data.append([dH, dHunit])
	
	TdS, TdSunit=get_ITC_table_values(Tdelta_S)
	data.append([TdS, TdSunit])
	
	Kd, Kdunit=get_ITC_table_values(Kd)
	data.append([Kd, Kdunit])

	dC, dCunit=get_ITC_table_values(delta_C)
	data.append([dC, dCunit])

	return(data)
############################################


####################   Collect structure page HTML   ######################
struc_details=collect_VIEW_PDB()

##############    Isolate table information   ##################
url_itc_list="http://scorpio2.biophysics.ismb.lon.ac.uk/structure/itc_data/"
source_itc_list=collect_source(struc_details, url_itc_list)

tables=collect_table_raw(source_itc_list)


###########       Collect links and ligand-links    ###########
ligands, links=collect_Links_Ligand_no(tables)

##############        Collect SMILES   ###############
url_ligand="http://scorpio2.biophysics.ismb.lon.ac.uk/ligand/view/"
source_ligand=collect_source(ligands, url_ligand)

collect_SMILES(source_ligand)

##############        Collect ITC data   ###############

url_itc="http://scorpio2.biophysics.ismb.lon.ac.uk/itc/view/"
source_itc=collect_source(links, url_itc)
tables=collect_table_raw(source_itc)

##############        Create ITC file   ###############

itc_data_xlsx=xlsxwriter.Workbook("itc_data.xlsx")
itc_data= itc_data_xlsx.add_worksheet()

itc_data.write_string(0,0, "PDB")
itc_data.write_string(0,2,'N')
itc_data.write_string(0,3,'unit')
itc_data.write_string(0,5, 'DeltaG')
itc_data.write_string(0,6, 'unit')
itc_data.write_string(0,8, 'deltaH')
itc_data.write_string(0,9, 'unit')
itc_data.write_string(0,11,'TdeltaS')
itc_data.write_string(0,12,'unit')
itc_data.write_string(0,14, 'Kd')
itc_data.write_string(0,15, 'unit')
itc_data.write_string(0,17, 'deltaC')
itc_data.write_string(0,18, 'unit')

# if the temperature of the expirement is 25C, write the pdb data into itc_data
i=1
for t in tables:
	pdb, table=t
	is_temp_25=collect_temp_and_pH(table)
	if is_temp_25 == 'y':
		data=collect_itc_data(t)#collect itc
		N, dG, dH, TdS, Kd, dC=data
		itc_data.write_string(i, 0, pdb)
		itc_data.write_string(i, 2, N[0])
		itc_data.write_string(i, 3, N[1])
		itc_data.write_string(i, 5, dG[0])
		itc_data.write_string(i, 6, dG[1])
		itc_data.write_string(i, 8, dH[0])
		itc_data.write_string(i, 9, dH[1])
		itc_data.write_string(i, 11, TdS[0])
		itc_data.write_string(i, 12, TdS[1])
		itc_data.write_string(i, 14, Kd[0])
		itc_data.write_string(i, 15, Kd[1])
		itc_data.write_string(i, 17, dC[0])
		itc_data.write_string(i, 18, dC[1])
		i=i+1
	else:
		continue

itc_data_xlsx.close()
