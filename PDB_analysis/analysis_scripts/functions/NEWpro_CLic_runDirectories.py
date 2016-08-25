#!/usr/bin/env python

#####
# Author: Dale Housler
# Creaton Date: 21-05-2014
# Name: pro-CLic (protein chain interaction counts)
# PROGRAM: pro-CLic_runDirectories
#####

'''
This program loops through all of the protein chain directories within the ligand directory
and runs proACT2 for each protein chain - ligand corss-reference.

And, alerts the user if proACT for some reason has not run and contact count details have therefore
not been obtained.
'''

import os # Operating system commands
import re # Regular expressions
import sys # Allows exit for error messages

def readLog():
    start_directory = os.getcwd()
    logfile = [f for f in os.listdir(start_directory) if f.endswith("log.csv")]
    ## Find the file name as a string
    logfile_str = str(logfile)
    logfile_str = re.sub('[\'\[\]]','',logfile_str) #uses re (regular expressions) to remove the ' and []

    try:
        a = open(logfile_str, "r")
    except FileNotFoundError:
        print("proAct has not run, no results to store in the log file")
        sys.exit(1)
    line = a.readline() 
    while line: 
        print (line) 
        line = a.readline() # Note that the content of line changes 
                            # here, resetting the loop
    a.close()

###END DEF

### START in the PDB folder
start_directory = os.getcwd()
notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa") # this is the NOT set only want directories NOT files remove by file type .XXX

### Get the protein chain directories
directories = [f for f in os.listdir(start_directory) if not f.endswith(notFile)]
directories.sort()
print(directories)

i=1

dirLength = len(directories)

### Loop through the protein chain directories
def LoopThroughChains(directories,dirLength):
    for i in range(0,len(directories)):
        ### Get the Chain_Ligand sub_directories
        os.chdir(directories[i]) # move into the chain directory
        next_directory = os.getcwd()
        #print(directories[i])
        sub_directories = [f for f in os.listdir(next_directory) if not f.endswith(notFile)]
        sub_directories.sort()
        print(sub_directories)

        ### Loop through the chain_sub_directories
        for j in range(0,len(sub_directories)):
            ### Get the .pdb and .mol2 files for proACT to use and run proACT2
            sub_dir=str(sub_directories[j])
            os.chdir(sub_dir) # move into the chain directory
            next_directory = os.getcwd()
            path = next_directory
            #print(directories[i])
            ### run pro_ACT
            ##Get the PDB file
            PDB_Chain = [f for f in os.listdir(next_directory) if f.endswith(".pdb")]
            PDB_Chain_file = PDB_Chain[0]
            print(PDB_Chain_file)
            PDB_ChainPath = path + "/" + PDB_Chain_file
            ##
            ##Get the mol2 file
            mol2_Chain = [f for f in os.listdir(next_directory) if f.endswith(".mol2")]

            try:
                mol2_Chain_file = mol2_Chain[0]
            except IndexError:
                print("No ligand file(s) found, check that the correct input has been entered.")

            print(mol2_Chain_file)
            LIG_ChainPath = path + "/" + mol2_Chain_file

            if os.path.isdir('proACT_run'): #need to check if exists otherwise will error
                pass
            else:
                os.mkdir('proACT_run')
            os.chdir('proACT_run')
            os.system('py C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/proACT2/proACT2.py --only_binding_site ' + PDB_ChainPath + " " + LIG_ChainPath)
            os.chdir("..")
            print("\nProACT2 run complete for: " + sub_directories[j] + "\n")
            ##
            ## RUN the contactsLogV1.py program
            os.system('python C:/Users/demetriana/Documents/PDB_analysis/analysis_scripts/functions/NEWContactLogv1.py')
            ##
            ###
            proACT_directory = [f for f in os.listdir(next_directory) if not f.endswith(notFile)]
            #print(proACT_directory)
            os.chdir("..")
    

        os.chdir("..") #go back up to the original chain directory
###END protein directory Loop

LoopThroughChains(directories,dirLength)

print("Counts complete!\n")
readLog()
sys.exit(1)


    
