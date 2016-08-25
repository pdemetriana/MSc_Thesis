#!/usr/bin/env python

#Author: Dale Housler
#OS: UNIX
#Program Description: A saved PDB file is accessed using the Saved PDB Files location pathway
#The PDB file is separated into a protein file and a set of ligand files .mol2 dependant on choice.

###### REFERENCES #####
#OPENBABEL: http://open-babel.readthedocs.org/en/latest/UseTheLibrary/PythonDoc.html#examples
#PDB:       http://www.wwpdb.org/policy.html, January 2014 version 3.5


'''
1. Enter PDB File location pathway.
2. Enter File location for separated Protein and ligands to be stored.
3. Choose way to separate file
'''

#NOTE: python2 users:
#Replace: url = urllib.urlopen(geturl)
#Replace 'input' with 'rawinput'
#Do not need to use print with brackets

### 'Open file' and 'Save in' location ###
'''
1. Enter PDB file location pathway
2. Enter File location for separated Protein and ligands to be stored.

Checks are made if no path is entered or just enter is pressed
'''

import sys # Allows exit for error messages

try:
    import openbabel
except ImportError:
    print("Unable to open Openbabel")
    sys.exit(1)
    
import os
#import glob
import re
import shutil

#DECLARED ARRAYS#
chain_array = []
chain_array_set = []
ligand_array = []
ligand_array_all = []
ligand_array_set = []
ligand_arrayname = []
ligand_arrayname_set = []
ligand_array_number = []
myarrayligN_chain = []
myarrayligN_chainAll = []
myarrayligN_chainSet = []

conformation_dirs = []
conformation_dirs_match = ""
mergeDecision = ""


#COMMON VARIABLES#
#str_char_del = ["[","]","(",")","'",";","\"",","]
str_char_del = ["[","]","(",")",";","\"",","]

##PARTS:
'''
1. Show protein chains and ligands present
2. Choose protein chains to save and separated or together
3. Choose ligand chains to save
'''
Lig_convert=''
PDB_fileloc = os.getcwd()
save_loc = os.getcwd()
start_directory=os.getcwd()
TS=''

PDB_ref=os.path.basename(PDB_fileloc)

##### Finds the PDB file of interest, if there are more than one relies on user entry #####

## regular expressions ##
mlc_name=PDB_ref+"[A-Z0-9]+\.pdb"	

PDB_dir=[p for p in os.listdir(PDB_fileloc) if  p.endswith(".pdb")]

path=[]

if len(PDB_dir) >1:
	TS='n'
	Lig_convert='y'
	mlc_list=[l for l in PDB_dir if re.search(mlc_name, l) and l.endswith(".pdb")]
	if len(mlc_list)>0:
		for i in mlc_list:
			path.append(PDB_fileloc + "/" + i)
	else:
		path.append(PDB_fileloc + "/" + PDB_ref + ".pdb")
else:
	TS='p'
	path.append(PDB_fileloc + "/" + PDB_ref + ".pdb")



def LookPDBHeader():
    for line in f:
        ###extracts PDB reference from the first line
        line_1 = str(line)
        s = "".join(line_1.split())
        pdb_ref = s[-4:]
        #print(pdb_ref[::-1]) #prints the reverse
        print("\n" + "----- PROTEIN LIGAND DETAILS FOR: "+ pdb_ref + " -----\n")
        ###

    #### FINDS CHAIN
        for column in [raw.strip().split() for raw in f]: #strips and makes into columns
            if 'MOLECULE:' in column[2:]:
                print (' '.join(column[2:]))
            
            if 'CHAIN:' in column[2:]:
                print (' '.join(column[2:]) + "\n")

            if 'HETNAM' in column[0:] and ("REMARK" not in column[0:]):
                print (' '.join(column[1:]))

    f.close()

########## Subroutines ##########
def SaveAllPTNChains(chain_array, chain_array_set):        
    with open(path) as h:
        print("\nProcessing 'PROTEIN' chains ...")
        print("Please wait for the process to complete ...\n")
        h.readline(0)
        #for column in [raw.strip().split() for raw in h]:
        for column in h:
            #-----Get the Protein chains from the pdb files-----#
            if ("ATOM" in column[0:]) and ("REMARK" not in column[0:]) and ("HETNAM" not in column[0:]) and ("REVDAT" not in column[0:]) and ("MDLTYP" not in column[0:]):
                chain_array_all = (column [:]) # Gets each line
                chain_array += (chain_array_all[21:]) # Gets all chains
                chain_array_set = sorted(set(chain_array)) #Finds unique chains
                chain_match = str(chain_array_all)
                for ch in str_char_del:
                    chain_match = chain_match.replace(ch,"")#Removes all of the characters stored in the Array
                chain_match = ''.join(chain_match)
                save_f = (save_loc + "/" + PDB_ref + "_ALL_PTNChains.pdb")#Writes as individual chains
                g = open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
                g.write(chain_match)#Writes pdb file data to txt file
                g.close()#Closes PDB File
            else:
                pass #This skips all lines that are not valid
    h.close()
#####
    
def SavePTNChainsSeperately(chain_array, chain_array_set):
    with open(path) as h:
        print("\nProcessing 'PROTEIN' chains ...")
        print("Please wait for the process to complete ...\n")
        h.readline(0)
        #for column in [raw.strip().split() for raw in h]:
        for column in h:
            #-----Get the Protein chains from the pdb files-----#
            if ("ATOM" in column[0:]) and ("REMARK" not in column[0:]) and ("HETNAM" not in column[0:]) and ("REVDAT" not in column[0:]) and ("MDLTYP" not in column[0:]):
                chain_array_all = (column [:]) # Gets each line
                chain_array += (chain_array_all[21:]) # Gets all chains
                chain_array_set = sorted(set(chain_array)) #Finds unique chains
                for i in range(len(chain_array_set)):#Collected all chains, hence length of this array to capture all chains
                    if (chain_array_set[i]) == (chain_array_all[21]):#Loops for chain check
                        chain_match = str(chain_array_all)#Sets to a string
                        for ch in str_char_del:
                            chain_match = chain_match.replace(ch,"")#Removes all of the characters stored in the Array
                        chain_match = ''.join(chain_match)
                        save_f = (save_loc + "/" + PDB_ref + "_PTNChain" + str(chain_array_set[i]) + ".pdb")#Writes as individual chains
                        g= open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
                        #g.write(chain_match + '\n')#Writes pdb file data to txt file
                        g.write(chain_match)#Writes pdb file data to txt file
                        g.close()#Closes PDB File
                            
            else:
                pass #This skips all lines that are not valid
    h.close()
#####
        
def SavePTNChainsPTNLigs(chain_array,chain_array_set):
    
    with open(path) as h:
        print("\nProcessing 'PROTEIN' chains ...")
        print("Please wait for the process to complete ...\n")
        h.readline(0)
        #for column in [raw.strip().split() for raw in h]:
        for column in h:
            #-----Get the Protein chains from the pdb files-----#
            if ("ATOM" in column[0:]) and ("REMARK" not in column[0:]) and ("HETNAM" not in column[0:]) and ("REVDAT" not in column[0:]) and ("MDLTYP" not in column[0:]):
                chain_array_all = (column [:]) # Gets each line
                chain_array += (chain_array_all[21:]) # Gets all chains
                chain_array_set = sorted(set(chain_array)) #Finds unique chains
                for i in range(len(chain_array_set)):#Collected all chains, hence length of this array to capture all chains
                    if (chain_array_set[i]) == (chain_array_all[21]):#Loops for chain check
                        chain_match = str(chain_array_all)#Sets to a string
                        for ch in str_char_del:
                            chain_match = chain_match.replace(ch,"")#Removes all of the characters stored in the Array
                        chain_match = ''.join(chain_match)
                        save_f = (save_loc + "/" + PDB_ref + "_PTNChain" + str(chain_array_set[i]) + ".pdb")#Writes as individual chains
                        name_ff = (save_loc + "/" + PDB_ref + "_PTNChain" + str(chain_array_set[i]))
                        g= open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
                        #g.write(chain_match + '\n')#Writes pdb file data to txt file
                        g.write(chain_match)#Writes pdb file data to txt file
                        g.close()#Closes PDB File

                        #---Change the HETATM Files to Mol2 Files---#
                        #07-04-2014 added funct to convert to mol2, in case ptn ligand
                        
                        obConversion = openbabel.OBConversion()
                        obConversion.SetInAndOutFormats("pdb", "mol2")
                        mol = openbabel.OBMol()
                        #obConversion.ReadFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\1mui_HETATMChainB_AAB1.pdb")   # Open Babel will uncompress automatically
                        obConversion.ReadFile(mol, save_f)
                        #obConversion.WriteFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\AAB1x1.mol2")
                        name_ff_mol2 = name_ff  +  ".mol2"
                        obConversion.WriteFile(mol, name_ff_mol2)
            else:
                pass #This skips all lines that are not valid
    h.close()
#####

def convertOnCount_PTNLigsMol2():
    start_directory = os.getcwd()

    directories = [f for f in os.listdir(start_directory) if  f.endswith(".pdb")]
    print("PDB Files present in current directory: \n")

    i = 1
    count = 0

    #prints pdb files in the directory
    for i in range(0,len(directories)):
        print(str(directories[i]))

    
    print("\nResidue count per pdb file: ")
    #Shows line count per pdb file and converts at least 24 to .mol2
    #prints the count and converts to mol2 if at least 24 residues else just prints file line count
    #This rule is as per PDB input criteria:
    #Non-biological synthetic peptides with at least 24 residues within a polymer chain
    #January 2014 version 3.5
    #http://www.wwpdb.org/policy.html
    for i in range(0,len(directories)): #loops per file in directory
        pdb_files = (directories[i])
        mol_f = re.sub('.pdb','',pdb_files)#removed.pdb file format for mol2 naming

    ###way 1 Count all alpha carbons
        with open(pdb_files) as h: #counts each line per pdb file
            for line in h:
                if ("ATOM" in line) and ("REMARK" not in line) and ("HETNAM" not in line) and ("REVDAT" not in line) and ("MDLTYP" not in line):
                    line_array = re.split('\s+', line) #split on the space to find the columns
                    if "CA" in line_array[2]: #USE CA not N as other side chain N's picked up 
                        count += 1

        #prints the count and converts to mol2 if at least 24 residues else just prints file line count     
        if count <= 24:
            print(str(pdb_files) + ": [" + str(count) + "] Possible **peptide ligands converted to .mol2 files")
        ####convert protein ligand chains to .mol2 files
            obConversion = openbabel.OBConversion()
            obConversion.SetInAndOutFormats("pdb", "mol2")
            mol = openbabel.OBMol()
            obConversion.ReadFile(mol, pdb_files)
            name_f_mol2 = mol_f + ".mol2"
            obConversion.WriteFile(mol, name_f_mol2)
        else:
            print(str(pdb_files) + ": [" + str(count) + "]")
       
        count = 0 #set count back to zero for next file count
#####

def countResidues():
    start_directory = os.getcwd()

    directories = [f for f in os.listdir(start_directory) if  f.endswith(".pdb")]
    print("PDB Files present in current directory: \n")

    i = 1
    count = 0

    #prints pdb files in the directory
    for i in range(0,len(directories)):
        print(str(directories[i]))

    print("\nResidue count per pdb file: ")
    #Shows line count per pdb file and converts at least 24 to .mol2
    
    for i in range(0,len(directories)): #loops per file in directory
        pdb_files = (directories[i])
        mol_f = re.sub('.pdb','',pdb_files)#removed.pdb file format for mol2 naming

    ###way 1 Count all alpha carbons
        with open(pdb_files) as h: #counts each line per pdb file
            for line in h:
                if ("ATOM" in line) and ("REMARK" not in line) and ("HETNAM" not in line) and ("REVDAT" not in line) and ("MDLTYP" not in line):
                    line_array = re.split('\s+', line) #split on the space to find the columns
                    if "CA" in line_array[2]: #USE CA not N as other side chain N's picked up 
                        count += 1

        #prints the count    
        if count <= 24:
            print(str(pdb_files) + ": [" + str(count) + "] Possible **peptide ligands converted to .mol2 files")
        else:
            print(str(pdb_files) + ": [" + str(count) + "]")
       
        count = 0 #set count back to zero for next file count
###END DEF
def ConvertLigFiles(
    Lig_convert,
    ligand_array,
    ligand_array_all,
    ligand_array_set,
    ligand_arrayname,
    ligand_arrayname_set,
    myarrayligN_chain,
    myarrayligN_chainAll,
    myarrayligN_chainSet):
    
    with open(path) as k:
        print("Processing 'HETATM' chains ...")
        print("Please wait for the process to complete ...\n")
        k.readline(0)
        #for column in [raw.strip().split() for raw in k]:
        for column in k:
            if ("HETATM" in column[0:]) and ("HOH" not in column[3:]) and ("REMARK" not in column[0:]) and ("HETNAM" not in column[0:]) and ("REVDAT" not in column[0:]):
                #---Finds Chain Ligands Attached To---#
                ligand_array_all = (column [:]) # Gets each line
                ligand_array += (column[21:22]).strip().split() # Gets all chains
                ligand_array_set = sorted(list(set(ligand_array)))#Finds unique chains
                #---Finds Unique Ligand Reference---#
                myarrayligN_chain += (column[16:21]).strip().split()
                #myarrayligN_chainAll += ''.join(myarrayligN_chain)
                myarrayligN_chainSet = sorted(list(set(myarrayligN_chain)))
                for i in range(len(myarrayligN_chainSet)): # Loops through all chains
                    if (myarrayligN_chainSet[i]) == ((ligand_array_all[16:21]).strip()): #Prints line if = to ligand[i]
                        for j in range(len(ligand_array_set)):# Loops through all Ligand Types
                            if (ligand_array_set[j]) == ((ligand_array_all[21:22]).strip()):#Prints line if = to chain[i] type[i]
                                ligand_match = str(ligand_array_all) #Sets to a string
                                for ch in str_char_del:
                                    ligand_match = ligand_match.replace(ch,"")#Removes all of the characters stored in the Array
                                ligand_match = ''.join(ligand_match)
                                ### makes ligand directory
                                if not os.path.exists(str(myarrayligN_chainSet[i])):
                                    os.makedirs(str(myarrayligN_chainSet[i]))
                                ###
                                save_f = (save_loc + "/" + str(myarrayligN_chainSet[i]) + "/" + PDB_ref + "_LigandChain" + "_" + str(myarrayligN_chainSet[i]) + "_" + str(ligand_array_set[j]) + ".pdb") #Saves Specific chain and Ligand
                                name_f = (save_loc + "/" + str(myarrayligN_chainSet[i]) + "/" + PDB_ref + "_LigandChain" + "_" + str(myarrayligN_chainSet[i]) + "_" + str(ligand_array_set[j]))
                                g = open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
                                #g.write(ligand_match + '\n')#Writes pdb file data to txt file DO NOT USE \n otherwise wont convert to MOL2 format for ligands
                                g.write(ligand_match)#Writes pdb file data to txt file
                                g.close()#Closes PDB File

                                #---Change the HETATM Files to Mol2 Files---#
                                obConversion = openbabel.OBConversion()
                                obConversion.SetInAndOutFormats("pdb", "mol2")
                                mol = openbabel.OBMol()
                                #obConversion.ReadFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\1mui_HETATMChainB_AAB1.pdb")   # Open Babel will uncompress automatically
                                obConversion.ReadFile(mol, save_f)
                                #obConversion.WriteFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\AAB1x1.mol2")
                                name_f_mol2 = name_f + ".mol2"
                                obConversion.WriteFile(mol, name_f_mol2)
                    #shutil.copy2(str(myarrayligN_chainSet[i]), str(myarrayligN_chainSet[i])) #moves files that end in a specific terminus

            else:
                pass #This skips all lines that are not valid
    k.close()
#####
    
###Splits the ligand files up if there are multiple forms
def ConvertLigFiles_OnID(
    Lig_convert,
    ligand_array,
    ligand_array_all,
    ligand_array_set,
    ligand_arrayname,
    ligand_arrayname_set,
    myarrayligN_chain,
    myarrayligN_chainAll,
    myarrayligN_chainSet,
    ligand_array_number):
    
    with open(path) as k:
        print("Processing 'HETATM' chains ...")
        print("Please wait for the process to complete ...\n")
        k.readline(0)
        #for column in [raw.strip().split() for raw in k]:
        for column in k:
            if ("HETATM" in column[0:]) and ("HOH" not in column[3:]) and ("REMARK" not in column[0:]) and ("HETNAM" not in column[0:]) and ("REVDAT" not in column[0:]):
                #---Finds Chain Ligands Attached To---#
                ligand_array_all = (column [:]) # Gets each line
                ligand_array += (column[21:22]).strip().split() # Gets all chains
                ligand_array_set = sorted(list(set(ligand_array)))#Finds unique chains
                #
                ligand_array_number += (column[22:31]).strip().split() #Checks for more than one ligand on lig reference
                #
                #---Finds Unique Ligand Number Reference---#
                myarrayligN_chain += (column[16:21]).strip().split()
                myarrayligN_chainSet = sorted(list(set(myarrayligN_chain)))
                #
                ligand_array_numberSet = sorted(list(set(ligand_array_number)))
                ##print(ligand_array_numberSet)
                #
                for i in range(len(myarrayligN_chainSet)): # Loops through all chains
                    if (myarrayligN_chainSet[i]) == ((ligand_array_all[16:21]).strip()): #Prints line if = to ligand[i]
                        for v in range(len(ligand_array_numberSet)):
                            if (ligand_array_numberSet[v]) == ((ligand_array_all[22:31]).strip()):
                                for j in range(len(ligand_array_set)):# Loops through all Ligand Types
                                    if (ligand_array_set[j]) == ((ligand_array_all[21:22]).strip()):#Prints line if = to chain[i] type[i]
                                        ligand_match = str(ligand_array_all) #Sets to a string
                                        #ligand_match_number = str(ligand_array_number)
                                        for ch in str_char_del:
                                            ligand_match = ligand_match.replace(ch,"")#Removes all of the characters stored in the Array
                                            ligand_match = ''.join(ligand_match)
                                            #ligand_match_number = ligand_array_number.replace(ch,"")
                                        ### makes ligand directory
                                        if not os.path.exists(str(myarrayligN_chainSet[i])):
                                            os.makedirs(str(myarrayligN_chainSet[i])) #MAKES THE DIRECTORIES FOR THE LIGANDS
                                        ###
                                        save_f = (save_loc + "/" + str(myarrayligN_chainSet[i]) + "/" + PDB_ref + "_LigandChain" + "_" + str(myarrayligN_chainSet[i]) + "_" + str(ligand_array_set[j]) + str(ligand_array_numberSet[v]) + ".pdb") #Saves Specific chain and Ligand
                                        name_f = (save_loc + "/" + str(myarrayligN_chainSet[i]) + "/" + PDB_ref + "_LigandChain" + "_" + str(myarrayligN_chainSet[i]) + "_" + str(ligand_array_set[j]) + str(ligand_array_numberSet[v]))
                                        g = open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
                                        #g.write(ligand_match + '\n')#Writes pdb file data to txt file DO NOT USE \n otherwise wont convert to MOL2 format for ligands
                                        g.write(ligand_match)#Writes pdb file data to txt file
                                        g.close()#Closes PDB File

                                        #---Change the HETATM Files to Mol2 Files---#
                                        obConversion = openbabel.OBConversion()
                                        obConversion.SetInAndOutFormats("pdb", "mol2")
                                        mol = openbabel.OBMol()
                                        #obConversion.ReadFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\1mui_HETATMChainB_AAB1.pdb")   # Open Babel will uncompress automatically
                                        obConversion.ReadFile(mol, save_f)
                                        #obConversion.WriteFile(mol, "C:\\Dale\\Python\\Project\\WorkingScripts\\Chains\\1mui\\AAB1x1.mol2")
                                        name_f_mol2 = name_f + ".mol2"
                                        obConversion.WriteFile(mol, name_f_mol2)
                    #shutil.copy2(str(myarrayligN_chainSet[i]), str(myarrayligN_chainSet[i])) #moves files that end in a specific terminus

            else:
                pass #This skips all lines that are not valid

    k.close()
#####

ligandDir = []
new_fileName = []
fileType = ["pdb", "mol2"]

def suffixLabel(ligandDir, new_fileName, fileType):

    suffix_allowed = ['Z','Y','X','W','V','U','T','S','R','Q',
                      'P','O','N','M','L','K','J','I','H','G',
                      'F','E','D','C','B','A']

    start_directory = os.getcwd()

    # this is the NOT set only want directories NOT files remove by file type .XXX
    notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa")

    directories = [f for f in os.listdir(start_directory) if not  f.endswith(notFile)]

    #print(directories)

    
    
    for i in range(len(directories)):

        k = 0
        
        if (len(directories[i])) >= 2: #don't want to relabel any files in the peptide ligand dir(Most Ligands will be labelled XX or XXX)
            #print(directories[i])
            
            os.chdir(directories[i])   

            ligandDir = os.getcwd()
            pdb_files = [g for g in os.listdir(ligandDir) if g.endswith(fileType)]
            
            pdb_files = sorted(pdb_files)
            #print(pdb_files)

            
            for j in range(len(pdb_files)):
                
                file_split = re.split('\_|\.',pdb_files[j])
                #print(file_split)

                #Adds the suffix allowed reference
                if len(file_split[-2]) >= 2: #Checks not a chain by being >2 as chain will be 1 character
                    #print(file_split[-2])
                    file_split.insert(-1,suffix_allowed[k])
                    k += 1
                #Makes sure non-numbered files have _ separator between lig ref and chain
                elif len(file_split[-2]) == 1: 
                    file_split.insert(-2,"")

                del file_split[-1] # removes the .pdb 
                #print(file_split)
                
                new_fileName = "_".join(file_split)
                #print(new_fileName)

                #removes the "_" between the inserted suffix and the ligand molecule #ref
                s = list(new_fileName)
                s[-2] = ""
                
                final_filename = "".join(s)
                final_filename = final_filename + "." + fileType #adds the .pdb ref back
                #print(final_filename) 
                                            
                try:
                    shutil.copy2(pdb_files[j], final_filename) #copies file without suffix to file with new suffix
                    os.remove(pdb_files[j]) #removes old file
                except shutil.Error:
                    pass

                
        os.chdir(start_directory)


###END DEF


def CopyPDBFiles():
    ### START in the PDB folder
    start_directory = os.getcwd()
    notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa") # this is the NOT set only want directories NOT files remove by file type .XXX

    ### Get the protein chain directories
    directories = [f for f in os.listdir(start_directory) if not f.endswith(notFile)]
    directories.sort()
    #print(directories)
    print("Files moved to directories: \n")
    i=0

    ### Loop through the protein chain directories
    for i in range(0,len(directories)):
        ### Get the Chain_Ligand sub_directories
        print(directories[i])

        ### Loop through the chain_sub_directories
        PDB_Chain = [f for f in os.listdir(start_directory) if f.endswith(".pdb")]
        print(PDB_Chain)
        for j in range(0,len(PDB_Chain)):
            ### Get the .pdbfiles
            
            shutil.copy2(PDB_Chain[j], directories[i])    

###END DEF
def checkForConformations(conformation_dirs,conformation_dirs_match, mergeDecision):

    start_directory = os.getcwd()

    # this is the NOT set only want directories NOT files remove by file type .XXX
    notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa")

    directories = [f for f in os.listdir(start_directory) if not  f.endswith(notFile)]
    #print(directories)
    for i in range(len(directories)):
        if len(directories[i]) == 4:
            #print(directories[i])
            conformation_dirs += [directories[i]]

    for i in range(len(conformation_dirs)):
        #print(conformation_dirs)
        conformation_dirs_match = str(conformation_dirs[0])[1:]
        #print(conformation_dirs_match)

    for i in range(len(directories)):#Checks for a dir with only 3 letters to match the four letter conf dir if the first letter is ignored
        if (len(directories[i])) == 3 and (str(directories[i]) == conformation_dirs_match):
            main_lig_dir = directories[i]
            print("\nIMPORTANT MESSAGE:\nThere are multiple conformations of the ligand: " + main_lig_dir)
            mergeDecision = 'y'

        if (mergeDecision == 'y'):
            os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWconformation_merger.py')

            print("\n----- IMPORTANT: -----\n")
            print("\nThe conformation files have been created")
            sys.exit(1)
        else:
            pass
               
            
#END DEF
##########

### PDB header shown on screen for protein ligand file decisions


for path in path:
	print(path)

	f = open(path)
	LookPDBHeader()
###
#-----Get the PROTEIN CHAINS from the pdb files-----#
    
	if TS == 'p':
		SavePTNChainsSeperately(chain_array, chain_array_set)
		convertOnCount_PTNLigsMol2()
		print ("\n**Peptide Ligands: Non-biological synthetic peptides with at least 24 residues within the polymer chain.\n")
		upd_file=os.getcwd()
		peptides = [p for p in os.listdir(upd_file) if  p.endswith(".mol2")]
		if len(peptides)<1:
			Lig_convert ='y'
		else:
			sys.exit(1)

#-----Get the HETATM (Ligand chains) from the pdb files-----#
	if Lig_convert == 'y':
    
     ##Convert PDB ligands to mol2##
		ConvertLigFiles(
		Lig_convert,
		ligand_array,
		ligand_array_all,
		ligand_array_set,
		ligand_arrayname,
		ligand_arrayname_set,
		myarrayligN_chain,
		myarrayligN_chainAll,
		myarrayligN_chainSet)

    ## Copy the pdb chain files to each ligand directory
    #CopyPDBFiles()

		ConvertLigFiles_OnID(
		Lig_convert,
		ligand_array,
		ligand_array_all,
		ligand_array_set,
		ligand_arrayname,
		ligand_arrayname_set,
		myarrayligN_chain,
		myarrayligN_chainAll,
		myarrayligN_chainSet,
		ligand_array_number)


    ## Add the suffix Labels to the ligand files
		for i in range(len(fileType)):
			suffixLabel(ligandDir, new_fileName, fileType[i])
    ##

    ## Copy the pdb chain files to each ligand directory
		CopyPDBFiles()

    #print("Please change to the correct ligand directory and run the menu options for each ligand in the associated directory.")

    #-----CHECK FOR MULTIPL CONFORMATIONS-----#
		#checkForConformations(conformation_dirs,conformation_dirs_match, mergeDecision)
		mergedecision = checkForConformations(conformation_dirs,conformation_dirs_match, mergeDecision)
    
	else:
		print("Ligand files have not been converted.")

#--Print where all files are saved---#
	print("All files have been saved in: \n" + save_loc + "\n\nComplete!\n")
###Shows files in folder ###
os.system('dir')
os.chdir(start_directory)
sys.exit(1)
