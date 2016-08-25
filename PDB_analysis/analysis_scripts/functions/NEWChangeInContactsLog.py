#!/usr/bin/env python

# Original ProCLic script with the addition in lines 29-42 by
# Demetriana Pandi, July 2016

# Author: Dale Housler
# Date: 16-08-2014
# Python: 3.3
# ChangeInContactsLog.py

'''
This program:
1. User inputs the protein chain .pdb file to use and ligand .mol2 file
2. A directory called 'complex_run' is created
3. proACT2 is run to obtain the change in contacts all_runs.csv file
4. This all_runs.csv file is saved to a dictionary structure
5. The change in polar, apolar and water polar and apolar contacts is saved.
6. The info. in 5. above is saved in 'pdb_ContactChange_log.txt' file
'''

import os   #Allows for operating system commands
import shutil # Allows for files to be moved between directories
import csv
from collections import defaultdict #Allows dictionary set-up

#Get the starting directory 
start_directory = os.getcwd()

########################## New Section 	######################################
#																			 #
# To collect chain and ligand instead of inputing them using the Menu.		 #
#																			 #
##############################################################################

chain_file=[f for f in os.listdir(start_directory) if f.endswith(".pdb")]
ligand_file=[f for f in os.listdir(start_directory) if f.endswith(".mol2")]

#User enters the files to use, as there can be manu options
ptn_chain_file = chain_file[0]
lig_chain_file = ligand_file[0]

##############################################################################

def runProACT2_complex_Formation(ptn_chain_file,lig_chain_file):

    #make the complex run directory to store the proACT2 complex run files in
    if os.path.isdir('complex_run'): #need to check if exists otherwise will error
        pass
    else:
        os.mkdir('complex_run')

    complex_dir = start_directory + "/" + "complex_run/"

    #move the protein .pdb file and the .mol2 file into the complex_run folder
    shutil.copy2(ptn_chain_file, complex_dir) #moves .pdb file
    shutil.copy2(lig_chain_file, complex_dir)#moves .mol2 file

    #move into the new complex_run directory so that the command can be run
    os.chdir('complex_run')
	
    #Run the proACT2 complex formation command
    #print("python /root/proACT2/proACT2.py --only_binding_site --complex_formation " + ptn_chain_file + " " + lig_chain_file + " --no_naccess --no_water_pdb --no_cavity_pdb") 
    ### remove " --no_naccess --no_water_pdb --no_cavity_pdb" if all files are to be run, so that solvation files can be used for Chimera viewing)
    os.system("py C:/Users/demetriana/Documents/Uni/MSc_Bioinformatics/Term_3/proCLic_package/proACT2/proACT2.py --only_binding_site --complex_formation " + ptn_chain_file + " " + lig_chain_file + " --no_naccess --no_water_pdb --no_cavity_pdb --runs=10")
    
    

def Get_ChangeInContacts(ptn_chain_file,lig_chain_file):
    
    columns = defaultdict(list) # each value in each column is appended to a list

    FileInput = "all_runs.csv"

    with open(FileInput) as f:
        reader = csv.DictReader(f)      # read rows into a dictionary format
        for row in reader:              # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items():   # go over each column name and value 
                columns[k].append(v)    # append the value into the appropriate list
                                        # based on column name k

    polar_contacts =(columns['polar_contacts'])
    apolar_contacts = (columns['apolar_contacts'])
    polar_water_contacts =(columns['polar_water_contacts'])
    apolar_water_contacts = (columns['apolar_water_contacts'])

    print("Change in Polar Contacts: " + polar_contacts[-1])
    print("Change in Apolar Contacts: " + apolar_contacts[-1])
    print("Change in Polar Water Contacts: " + polar_water_contacts[-1])
    print("Change in Apolar Water Contacts: " + apolar_water_contacts[-1])

    #Get the PDB reference
    structure =(columns['structure'])
    structure_str = str(structure[3])
    pdb_ref = structure_str[0:4]
    #print(pdb_ref)

    ### Create the Log file
    os.chdir ('..') # moves the log file to the pdb top directory
    save_f = (pdb_ref + '_ContactChange_log.txt')
    g = open(save_f, 'a+')
    g.close()#Closes PDB File
   
    ### Write the data to the 'pdb_ContactChange_log.txt' File ###
    g = open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears

    ### Write the protein and ligand files used ###
    g.write("---------------------------------------------------------\n\n")
    g.write("Protein Chain File: " + ptn_chain_file + "\n")
    g.write("Ligand File: " + lig_chain_file + "\n\n")

    ### Write the data obtained ###
    g.write("---------- Change in Polar and Apolar Contacts ----------\n\n")
    g.write("Change in Polar Contacts: " + polar_contacts[-1] + "\n")
    g.write("Change in Apolar Contacts: " + apolar_contacts[-1] + "\n")
    g.write("Change in Polar Water Contacts: " + polar_water_contacts[-1] + "\n")
    g.write("Change in Apolar Water Contacts: " + apolar_water_contacts[-1] + "\n")
    g.write('\n')
	
    g.close()#Closes PDB File

    ### End def

##### Run the functions #####
runProACT2_complex_Formation(ptn_chain_file,lig_chain_file)
Get_ChangeInContacts(ptn_chain_file,lig_chain_file)


