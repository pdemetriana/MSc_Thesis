#!/usr/bin/env python

# Author: Dale Housler
# Date: 13-05-2014
# Python: 3.3
# ContactLogv1.py

'''
This program calculates the Polar, Apolar and Binding water contact count details
from the proACT2 created file residue_contacts.csv
It also created the .txt files in which these contact count runs are stored as well as
the final ligand log.csv file containing a summary of all of the protein chain - ligand cross-referenced data.
'''


import os   #Allows for operating system commands
import re   #Regular expressions
import csv  #Imports read csv commands
import operator #Additional csv functionality
import sys  #Allows exit for error messages

start_directory = os.getcwd()

########## Subroutines ##########

##### Finds the current directory for multiple ligands and log file naming #####
def GetCurrentDir():
    directory = start_directory.split(os.sep) # splits on /
    n = len(directory) # gets length of directories

    return (str(directory[n-3])) # returns the correct folder (important for named ligands)


#####End

##### Finds the ligand chain from the files in the directory #####
def GetLigandChain_ref():
    ligChain_files = [f for f in os.listdir(start_directory) if f.endswith('.mol2')]

    chain_files_str = str(ligChain_files)
    chain_files_str = re.sub('[\'\[\]]','',chain_files_str)
    chain_files_str = re.sub('.mol2','',chain_files_str) # removes the file type

    underscore_split = re.split('\_',chain_files_str)
    fileType_len = len(underscore_split)
    #print(len(underscore_split))
    ## Checks the length of the file split to determine if a PTN mol2 or a lig mol2 file
    if fileType_len == 2:
        return underscore_split[1] #PDB_PTNChainX.mol2 file
    else:
        return underscore_split[3] #PDB_LigandChain_XXX_x.mol2 file
        
        
    
    
    
#####End

##### Finds the PDB reference from the files in the directory #####
def GetPDB_ref():
    ligChain_files = [f for f in os.listdir(start_directory) if f.endswith('.mol2')]

    chain_files_str = str(ligChain_files)
    chain_files_str = re.sub('[\'\[\]]','',chain_files_str)
    chain_files_str = re.sub('.mol2','',chain_files_str) # removes the file type

    underscore_split = re.split('\_',chain_files_str)

    return (underscore_split[0])
#####End

##### Finds the protein chain from the files in the directory #####
def GetPTNChain_ref():
    Chain_files = [f for f in os.listdir(start_directory) if f.endswith('.pdb')]

    chain_files_str = str(Chain_files)
    chain_files_str = re.sub('[\'\[\]]','',chain_files_str)
    chain_files_str = re.sub('.pdb','',chain_files_str) # removes the file type
    chain_files_str = re.sub('Chain','',chain_files_str)# removes word 'Chain' from file name
    chain_files_str = re.sub('PTN','',chain_files_str)# removes word 'PTN' from file name
    underscore_split = re.split('\_',chain_files_str)
    #print (underscore_split)
    #return (underscore_split[2])
    return (underscore_split[1])
#####End

##### Get Polar + Apolar Contacts #####

def GetPAPContacts(pdb_ref):
    ##Checks that proACT file is in the directory
    path = start_directory + '/proACT_run/'
    try:
        os.chdir(path)
    except FileNotFoundError as err:
        print ("proACT_run directory does not exist.\nPlease run the directory creator program or make this directory.")
    ##
    contact_file = [f for f in os.listdir(path) if f.endswith('contacts.csv')]
    contact_file_str = str(contact_file)
    contact_file_str = re.sub('[\'\[\]]','',contact_file_str)
    print("\n__________CONTACTS CALCULATED__________ " + "\n\nFile used: " + contact_file_str + "\n\n" + "----- POLAR and APOLAR CONTACTS -----\n")

##########################################
    file_loc = os.getcwd()
    CSV = contact_file_str
    path = (file_loc + "/" + CSV)
    #-----Get the info from the CSV file-----#
    chain_array = []
    chain_array_FULL = []
    chain_array_SET = []
    chain_final = []

    lig_array = []
    lig_arrayReversed = []
    new_lig_array = []
    lig_array_FULL = []
    SET_lig_array = []
    p_count = []
    p_count_ptn = []
    p_count_lig = []
    M_tag = []
    P = []
    AP = []
    M_tag_FULL = []
    P_FULL = []
    AP_FULL = []
    ALL_FULL = []

    chain_char_del = ["\""," ","'","[","]",","]
    str_char_del = ["[","]","(",")","'",";","\"",","]
    bracket_del = ["[],","[","]","'"]
    Comma_replace = [", "]
    colon_replace = [":"]

    p_add = 0
    ap_add = 0
    p_add_ptn = 0
    ap_add_ptn = 0
    p_add_lig = 0
    ap_add_lig = 0


    #----- Shows Total number of contacts -----
    with open(path) as h:
        for i, line in enumerate(h):
            for line in h:
                #for line in [raw.strip().split() for raw in h]:
                chain_array = line.strip().split(",")
                chains = chain_array[2]
                chain_array_FULL += [chains[:i]]
                chains_str = str(chain_array_FULL)
                for ch in chain_char_del:
                    chains_str = chains_str.replace(ch,"")#.strip(" ")
                chain_array_SET = sorted(set(chains_str))
                chain_array_other = sorted(set(chain_array_FULL))
                #chain_FINAL = chain_array_SET
                chain_FINAL = chain_array_SET
                i += 1
    h.close()

    if ((file_loc != ("")) or (file_loc != (" ")) or (file_loc != ("\n"))):
        #save_g = (file_loc + "\\" + CSV + "_Contacts.txt")
        contacts_file = (pdb_ref + '_PolarApolar_contacts.txt')
        ##same_file = raw_input("Enter the file name for the contacts to be saved under\n")
        #save_g = (file_loc + same_file + "_Contacts.txt")
        #save_g = (file_loc + "_" + contacts_file + "_Contacts.txt")
        os.chdir("..")
        save_g = (contacts_file)
        #save_g = (contacts_file + "_Contacts.txt")
        g = open(save_g, 'a+')
        g.write("                        CHAIN     " + "POLAR     " + "APOLAR\n\n")
        for p in range(len(chain_FINAL)):
            #note: reset count variables otherwise all chains are counted.
            p_add_ptn = 0
            ap_add_ptn = 0
            p_add_lig = 0
            ap_add_lig = 0
            with open(path) as h:
                for i, line in enumerate(h):
                    for line in h:
                        #for line in [raw.strip().split() for raw in h]:
                        if ("Z" in line) and ("HOH" not in line) and ("PPP" not in line):
                            lig_array = line.strip().split(",") # strip removes /n & split: this splits at the comma
                            #print (list(line)) 
                            if ((lig_array[0] != "9999") and (lig_array[2] == ("\"" +(chain_FINAL[p]+ "\"")))):
                                if (int(lig_array[6]) >= 0) or (int(lig_array[7]) >= 0):
                                    p_count_ptn = (int(lig_array[6]))
                                    p_add_ptn = p_count_ptn + p_add_ptn
                                    ap_count_ptn = (int(lig_array[7]))
                                    ap_add_ptn = ap_count_ptn + ap_add_ptn
                            if ((lig_array[0] == "9999")and (lig_array[2] == ("\"" +(chain_FINAL[p]+ "\"")))):
                                if (int(lig_array[6]) >= 0) or (int(lig_array[7]) >= 0):
                                    p_count_lig = (int(lig_array[6]))
                                    p_add_lig = p_count_lig + p_add_lig
                                    ap_count_lig = (int(lig_array[7]))
                                    ap_add_lig = ap_count_lig + ap_add_lig
                        i += 1
       
                print("                        CHAIN     " + "POLAR     " + "APOLAR\n")
                print("ALL CONTACTS:     " + "        " + (str(chain_FINAL[p]))+ "         " + (str(p_add_ptn + p_add_lig)) + "         " + (str(ap_add_ptn + ap_add_lig)) + "\n")
                print ("PTN TO LIG CONTACTS: " + "     " + (str(chain_FINAL[p])) + "         " + (str(p_add_ptn)) + "         " + (str(ap_add_ptn))+ "\n") 
                print ("LIG TO PTN CONTACTS:" + "      " + (str(chain_FINAL[p])) + "         " + (str(p_add_lig)) + "         " + (str(ap_add_lig))+ "\n")
        
                g.write("ALL CONTACTS:     " + "        " + (str(chain_FINAL[p]))+ "         " + (str(p_add_ptn + p_add_lig)) + "         " + (str(ap_add_ptn + ap_add_lig)) + "\n")
                g.write("PTN TO LIG CONTACTS: " + "     " + (str(chain_FINAL[p])) + "         " + (str(p_add_ptn)) + "         " + (str(ap_add_ptn))+ "\n")
                g.write("LIG TO PTN CONTACTS:" + "      " + (str(chain_FINAL[p])) + "         " + (str(p_add_lig)) + "         " + (str(ap_add_lig))+ "\n\n")
            h.close()
        #print ("File saved: " + save_g)
        g.close()

        return (str(p_add_lig) + ',' + str(ap_add_lig)) #returns the polar and apolar bonds to be stored to the main log file
        
##########################################

def GetWaterContacts(pdb_ref):
    path = start_directory + '/proACT_run/'
    os.chdir(path)
    water_contact_file = [f for f in os.listdir(path) if f.endswith('contacts.csv')]
    contact_file_str = str(water_contact_file)
    contact_file_str = re.sub('[\'\[\]]','',contact_file_str)
    print("----- BINDING WATER CONTACTS -----")

##########################################
    FileInput = contact_file_str
    OpenFile = open(FileInput, 'r')
    #OpenFile = open('/root/Scorpio2_PDB_Files/CSVruns/1a1e/1a1e_ALL_PTNChains_run1_residue_contacts.csv', 'r')

    os.chdir("..")
    contacts_file = (pdb_ref + '_bindingWater_contacts.txt')

    if ((contacts_file != ("")) or (contacts_file != (" ")) or (contacts_file != ("\n"))):
        path = os.getcwd()
        #print (path)
        save_g = (contacts_file)
        g = open(save_g, 'a+')
        g.write("\n")
    else:
        print("File not saved")
        conti = 'n'

    csvFile = csv.reader(OpenFile, delimiter=',' , quotechar=' ') # remove quotechar if want to remove double quotes around string values
    sort = sorted(csvFile, key=operator.itemgetter(int(x=3))) #int(x=3) sets the col value to an integer

    store_HOH = []
    store_HOH1 = []
    storeHOH1 = []
    store_HOH2 = []
    storeHOH2 = []

    #print ('Check water order\n')
    for line in sort: # can change to csvFile if waters pre-sorted
        #print(line)
        if (('"HOH"' in line) or ('HOH' in line)):
            #print(line)
            ##print(line[1:5])
            store_HOH += [line[1:5]] # if you want this to be individual strings use () instead of []

    chain_store = []
    bindingWater_positions = []
    count_bridgingWaters = 0
    bridgingWater_positions = []
    count_bridgingWaters_withZ = 0
    count_bindingWaters = 0

    for i,line in enumerate(store_HOH): #skips the header line
        store_HOH1 = store_HOH[i]
        ##print (store_HOH[i])
        store_HOH2 = store_HOH[i-1] #set to i-1 NOT i+1 because want 1 less as skipped the first to make the comparison
        ##print (store_HOH[i])
    
        if ((store_HOH1[1] != store_HOH2[1]) and (store_HOH1[2] == store_HOH2[2])):
            ##print (store_HOH1)
            ##print (store_HOH2)
            store_chain1 = store_HOH1[1]
            store_chain2 = store_HOH2[1]
        
            if ((store_chain1 in ('Z','"Z"')) and (store_chain2 != store_chain1)):
                ## this if checks scenario AB Z
                print (store_HOH1)
                g.write(str(store_HOH1)+ "\n")
                print (store_HOH2)
                g.write(str(store_HOH2)+ "\n")
                count_bindingWaters +=1
                #if store_HOH1[2] not in bindingWater_positions:
                   #bindingWater_positions += [store_HOH1[2]] #get position to determine if a binding or bridging water
                 
    ##print(bindingWater_positions)
    #length_binding = len(bindingWater_positions)

    print ("\nBinding water count = ", count_bindingWaters) #'{Considers multi-chain bridge and counts as 1}')
    g.write ("\nBinding water count = " + str(count_bindingWaters) + "\n")
    g.close()

    return str(count_bindingWaters)
#####END

def CalcTotalContacts(P_AP_contacts,water_contacts):
    ### Split PAP return for totalling ###
    PAP_split = re.split(',',P_AP_contacts)
    polar_contacts = int(PAP_split[0])
    apolar_contacts = int(PAP_split[1])
    ### Calculate Total ###
    Total_contacts = polar_contacts + apolar_contacts + int(water_contacts)

    return Total_contacts
    

########## End Subroutines ##########

### Check for a proACT_run Directory ###


### Return Values from subroutines ###
pdb_ref = GetPDB_ref()
chain_ref = GetPTNChain_ref()
ligand_ref = GetLigandChain_ref()

try:
    P_AP_contacts = GetPAPContacts(pdb_ref)
except IsADirectoryError:
    print("ProAct has not completed. No CSV file to use for contact runs.")
    sys.exit(1)

water_contacts = GetWaterContacts(pdb_ref)

TOTAL_contacts = CalcTotalContacts(P_AP_contacts,water_contacts)

    
LigDir = GetCurrentDir()

### Change directory to top level
os.chdir ('../..') # moves the log file to the pdb top directory

### Create the Log file
save_f = (pdb_ref + '_log.csv')
g = open(save_f, 'a+')
g.close()#Closes PDB File

### Check if log file is empty, if empty writes heading else no header only body data is written

header = 'pdb_ref,Protein Chain,Ligand,Polar Count, Apolar Count, Binding Water Count, Total Count'

if os.stat(save_f).st_size==0: #Checks if file is empty
   
    ### Print to File ###
    g = open(save_f, 'a+') #Writes to file by adding (w overwrites but then the last line only appears
    g.write(header)
    g.write('\n') #Skips header if found
    g.write(pdb_ref + ','  + chain_ref  + ',' + chain_ref  + '_' + ligand_ref  + '_' + LigDir + ',' + P_AP_contacts + ',' + water_contacts + ',' + str(TOTAL_contacts))
    g.write('\n')
    g.close()#Closes PDB File
else:
    g = open(save_f, 'a+')
    g.write(pdb_ref + ','  + chain_ref  + ',' + chain_ref  + '_' + ligand_ref  + '_' + LigDir  + ',' + P_AP_contacts + ',' + water_contacts + ',' + str(TOTAL_contacts))
    g.write('\n')
    g.close()#Closes PDB File

### Print to Screen ###

logfile_directory = os.getcwd()
print("\n----- Details written to file ----- \n\n" + logfile_directory + "/" + save_f + "\n")
