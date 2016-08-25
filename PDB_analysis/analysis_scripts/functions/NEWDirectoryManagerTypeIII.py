#!/usr/bin/env python

#####
# Author: Dale Housler
# Creaton Date: 17-05-2014
# PROGRAM: DirectoryManagerTypeIII
#####

##### PROGRAM DESCRIPTION #####
# This program takes:
#       the number of protein chains entered by a user
#       the number if ligand chains entered by a user
# checks these
# Then allows each chain to be entered as a SINGLE alphabetical letter
# converts the inputed chains to capitals
# creates x number of directories
# inside x directories it makes further directories for the protein chain linked to the ligands
# moves the appropriate files into each directory
#####

##### EXAMPLE #####
#
# User inputs protein chain number = 3
# User inputs ligand chain number = 2
# User inputs protein chain types = A B C
# User inputs ligand chain types = A Z
# 
#
# Creates directories according to protein chains:      dir: A
#                                                       dir: B
#                                                       dir: C
#
# Protein ligands chains:                       dir: A -drill down-> dir: A_ligA + A_ligZ
#                                               dir: B -drill down-> dir: B_ligA + B_ligZ
#                                               dir: C -drill down-> dir: C_ligA + C_ligZ
#
# pdb and mol2 files from the level above the chain directory level are then moved into
# each directory A, B, C and then matches made to the sub-directory and moved accordingly
#####

##### TEST CASES #####
#
# i     - 1 protein chain   :   1 ligand chain
# ii    - 2 protein chains  :   2 ligand chains
# iii   - 3 protein chains  :   2 ligand chains
# iv    - 2 protein chains  :   3 ligand chains
#   
# v     - protein ligand files only
# vi    - chemical ligand files only
# vii   - a mix of protein and chemical ligands
#
# viii  - an invalid protein chain entered
# ix    - an invalid ligand chain entered
# x     - the same protein chain entered twice
# xi    - the same ligand chain entered twice
#
# xii   - a series of invalid user inputs (e.g., any chain entry > 1 [AA], non-numeric chain number entry etc.)
#
#####

##### CAVEAT #####
#
# 3 chains 2 ligand chains scenario, ligand is the inner loop so list index is out of bounds
# Work areound is a try except for this error to skip if the ligands are complete
# Would be the same issue if the ligand chains ran the external loop and everythin was swapped around
# Could have another similar program where one runs the protein chains and the other the ligand chains
# Decided on the internal Try except and pass function instead to allow the process to complete
#
# This allows all files to be transferred correctly
#####

##### PITFALLS #####
#
# 1.    If a protein and a chemical ligand with the same chain reference appear in the same directory
#       e.g., 1a1b_ChainA.mol2 and 1a1e_LigandChain_PTR_A.mol2
#       ERROR displayed: "Protein and chemical ligands cannot exist within the same folder"
#       A BREAK is set in this instance because the correct files in the directory need to be decided upon
#       
#       EXCEPTION:
#       If a protein and chemical ligand exist in the same directory but for different chains
#       e.g., 1a1b_ChainA.mol2 and 1a1e_LigandChain_PTR_X.mol2
#
# 2.    If a ligand chain is entered more than once
#       All directories are still created, hence a PASS is set.
#       WARNING displayed: "The same ligand has been entered twice."
#
# 3.    If a protein MAIN chain has been entered and no chain file for the entry exists
#       No pdb files can be transferred, hence a BREAK is set.
#       ERROR displayed: "A protein file ending in:  __.pdb doesn't exist. (The invalid chain entered is defined)
#
# 4.    If a ligand has been entered and no ligand file for the entry exists
#       All files are transferred for valid finds, hence a PASS is set.
#       ERROR displayed: "A ligand file ending in:  __.mo12 doesn't exist. (The invalid chain entered is defined)
#####

import os
import shutil
import re
import sys

start_directory = os.getcwd()

#	regular expressions#
chain_regex="PTNChain.\.pdb"

#print (start_directory)

chain_list=[0]
ligand_list=[0]
chain_full_names=[]
ligands_full_names=[]

pdf_file_list=[f for f in os.listdir(start_directory) if re.search(chain_regex, f) and f.endswith(".pdb")]
ligand_files=[f for f in os.listdir(start_directory) if f.endswith(".mol2")]

for f in ligand_files:
	lig_name=re.sub('.mol2','',f)
	ligands_full_names.append(lig_name)
	last_letter_place=len(lig_name)-1
	lig_letter=lig_name[last_letter_place]
	ligand_list.append(lig_letter)

#print ("ligands: ", ligand_list)	
for f in pdf_file_list:
	file_name=re.sub('.pdb','',f)
	if file_name not in ligands_full_names:
		if "Chain" in file_name:
			chain_full_names.append(file_name)
			last_letter_place=len(file_name)-1
			ch_letter=file_name[last_letter_place]
			chain_list.append(ch_letter)
	
#print ("chains: ", chain_list)
#print (ligands_full_names)

##### Make directories #####

def MakeDirectories(ptn_chains_count,lig_chains_count,chains,lig_chains):
    ptn_chain_number = int(ptn_chains_count)
    lig_chain_number = int(lig_chains_count)
    length = len(chains)
    length_lig = len(lig_chains)
    warning = 0
    i = 1
    while (i <= ptn_chain_number) and (i <= length):
        #print(chains[i])
        if (not os.path.isfile(chains[i])) and (not os.path.isdir(chains[i])):
            os.mkdir(chains[i])
            os.chdir(chains[i])
       
            ### Ligand Loop - creates same chain with diff ligands dir###
            j = 1
            while (j <= lig_chain_number) and (j <= length_lig):
                if (not os.path.isfile(lig_chains[j])) and (not os.path.isdir(lig_chains[j])):
                    try:    #skip if the same ligand is entered twice
                        os.mkdir(chains[i] + '_lig' + lig_chains[j])
                    except FileExistsError:
                        warning += 1
                        if warning <= 1:
                            print("\nWARNING: The same ligand has been entered twice")
                            pass #still want the process to be completed regardless of the repeat
                j += 1
            ### End Ligand Loop ###
           
            os.chdir(start_directory)
       
        i+= 1
    ### End of While loop ###
    #print('All files can be found in: ' + start_directory)
#####END

##### MoveChainFiles_TypeI #####
def MoveChainFiles_TypeIII(ptn_chains_count,lig_chains_count,chains,lig_chains):
    start_directory = os.getcwd()
    chain_number = int(ptn_chains_count)
    lig_chain_number = int(lig_chains_count)

    #print("\nFiles copied successfuly!")

    ### Make directories - Beginning of while ###
    i = 1
    for i in range(1,chain_number+1):
        fileToFind = 'Chain' + chains[i] + '.pdb'
        #print(fileToFind)
        chain_files = [f for f in os.listdir(start_directory) if f.endswith(fileToFind)] # collects all files ending with fileToFind details

        ## Find the file name as a string
        chain_files_str = str(chain_files)
        chain_files_str = re.sub('[\'\[\]]','',chain_files_str) #uses re (regular expressions) to remove the ' and []
        print ('\nDirectory ' + chains[i] + ':')
        print(chain_files_str)
        ## end
   
        saveToDir = chains[i]
        try:
            shutil.copy2(chain_files_str, saveToDir) #moves files that end in a specific terminus
        except FileNotFoundError:
                print("ERROR: A protein file ending in: " + chains[i] + ".pdb doesn't exist.")
                break #pass so continues with all valid files
        ### Ligand Loop - creates same chain with diff ligands dir###
        j = 1
        for j in range(1,lig_chain_number+1):
            lig_fileToFind = lig_chains[j] + '.mol2'
          
            lig_chain_files = [f for f in os.listdir(start_directory) if f.endswith(lig_fileToFind)]
            if len(lig_chain_files) > 1:
                print("\nERROR: Protein and Chemical ligand files cannot exist in the same file")
                break #break because unsure if which mol2 file to use
            #print(lig_chain_files)

            ## Find the file name as a string
            lig_chain_files_str = str(lig_chain_files)
            lig_chain_files_str = re.sub('[\'\[\]]','',lig_chain_files_str)
            print(lig_chain_files_str)
            ## end
       
            lig_saveToDir = chains[i]   #set to i NOT j so copies each file in i's directory
                                        #(otherwise will move files each time and overwrite)
            try:
                shutil.copy2(lig_chain_files_str, lig_saveToDir) #moves files that end in a specific terminus  
            except FileNotFoundError:
                print("ERROR: A ligand file ending in: " + lig_chains[j] + ".mo12 doesn't exist.")
                pass #pass so continues with all valid files
        j += 1
            ### End Ligand Loop ###        
    i+= 1
    ### End of While loop ###
   
    #print("\nFiles copied successfuly!\n")

##### end #####

##### MoveLigandFiles_TypeI#####

def MoveLigandFiles_TypeIII(ptn_chains_count,lig_chains_count,chains,lig_chains):
   
    start_directory = os.getcwd()
    chain_number = int(ptn_chains_count)
    lig_chain_number = int(lig_chains_count)

    print("\nAll files can be found in the following directories: \n")
    k = 1
    for k in range(1,chain_number+1): #upper directory so must match chain number
        path = start_directory + '/' + chains[k]
        print(path)
        os.chdir(path)
        chain = chains[k]

        ##### Make directories - Beginning of while #####

       
        ### Find the largest chain number
        if chain_number > lig_chain_number:
            maxChain = chain_number
        elif lig_chain_number > chain_number:
            maxChain = lig_chain_number
        else:
            maxChain = chain_number
           
        i = 1
        for i in range(1,maxChain+1):
            fileToFind = 'Chain' + chain + '.pdb'
            #print(fileToFind)
            chain_files = [f for f in os.listdir(start_directory) if f.endswith(fileToFind)] # collects all files ending with fileToFind details
            ## Find the file name as a string
            chain_files_str = str(chain_files)
            chain_files_str = re.sub('[\'\[\]]','',chain_files_str) #uses re (regular expressions) to remove the ' and []
            #print ('\nDirectory ' + chains[i] + ':')
            #print(chain_files_str)
            ## end
            ### determines which array ptn chains or ligand chains is larger and sends protein files accordingly
            if chain_number > lig_chain_number:
                try:
                    saveToDir = chain + '_lig' + lig_chains[i] #defined by protein chains #******* Problem is case 3 ptns 2 ligs looks for additional ptn chain hence pass
                except IndexError:
                    pass
            if lig_chain_number > chain_number:
                saveToDir = chain + '_lig' + lig_chains[i] #defined by ligand chains
            if chain_number == lig_chain_number:
                saveToDir = chain + '_lig' + lig_chains[i] #if they are equal defined by ligand chains
            try:   
                shutil.copy2(chain_files_str, saveToDir) #moves files that end in a specific terminus
            except FileNotFoundError:
                pass #*** ERROR already displayed for pdb file not found in def above ***
            ### Ligand Loop - creates same chain with diff ligands dir###
            j = 1
            for j in range(1,lig_chain_number+1):
                lig_fileToFind = lig_chains[j] + '.mol2'
               
                lig_chain_files = [f for f in os.listdir(start_directory) if f.endswith(lig_fileToFind)]
                #print(lig_chain_files)

                ## Find the file name as a string
                lig_chain_files_str = str(lig_chain_files)
                lig_chain_files_str = re.sub('[\'\[\]]','',lig_chain_files_str)
                #print(lig_chain_files_str)
                ## end
                ### determines which array ptn chains or ligand chains is larger and sends ligand files accordingly
                if chain_number > lig_chain_number:
                    lig_saveToDir = chain + '_lig' + lig_chains[j] #defined by protein chains
                elif lig_chain_number > chain_number:   
                    lig_saveToDir = chain + '_lig' + lig_chains[j]  #defined by ligand chains #set to j NOT i so copies specific file in i's directory
                else:
                    lig_saveToDir = chain + '_lig' + lig_chains[j]  #if they are equal defined by ligand chains
                try:   
                    shutil.copy2(lig_chain_files_str, lig_saveToDir) #moves files that end in a specific terminus  
                except FileNotFoundError:
                    pass
            j += 1
            ### End Ligand Loop ###
           
        i+= 1

        ### End of While loop ###
    k += 1
    os.chdir(start_directory) #otherwise will start to create next set of files in this directory
    #print("\nFiles moved successful!\n")
##### end #####

## Check counts are correct
chains = chain_list
lig_chains = ligand_list
ptn_chains_count=len(chains)-1
lig_chains_count=len(lig_chains)-1

MakeDirectories(ptn_chains_count,lig_chains_count,chains,lig_chains)

### Move Protein and Ligand chain files into chain X sub-directory
MoveChainFiles_TypeIII(ptn_chains_count,lig_chains_count,chains,lig_chains)
### Move specific Protein and Ligand chain files into chain X_ligX secondary sub-directory
MoveLigandFiles_TypeIII(ptn_chains_count,lig_chains_count,chains,lig_chains)

os.chdir(start_directory)
sys.exit(1)
