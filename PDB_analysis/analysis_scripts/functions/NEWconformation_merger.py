#!/usr/bin/env python

#Author: Dale Housler

#This programs creates the conformation files in the correct structure for the ProCLic_MENU.py MENU option 1. run
#See program ChainSeparate2PDB_PtnLigUNIX_dir.py
#def checkForConformations() for links to this program

### PROGRAM PROCEDURE ###
#1.  Copies all of the .pdb files for any folders that have the same name
#    because these are likely to be conformation files.
#    An initial match in the ChainSeparate2PDB_PtnLigUNIX_dir.py would have been done by:
#    Finding all 4 character folders, removing the first character and matching to a 3 char folder
#    If a match is found and the accepts the option to run this program script, then it is initiated.
#2.  New directories are created to keep multiple conformations separate.
#3.  Once the MAIN Ligand .pdb file and the conformation .pdb file is in the same directory
#4.  The lines from the short conformation .pdb is moved to the MAIN .pdb file
#5.  This MAIN .pdb file is then sorted to make sure the conformation lines are in the correct positions
#6.  This MAIN .pdb with the added conformation lines is moved to the PDB DIR
#7.  This MAIN .pdb is then renamed so that it can be re-run by the 'chain separate' program MENU option 1.
### ###

import os
import re
import shutil
import sys
import csv
import operator

try:
    import openbabel
except ImportError:
    print("Openbabel to be imported.")
    sys.exit(1)

start_directory = os.getcwd()

if not os.path.exists("conformation"):
    os.makedirs("conformation")

confDIR = (start_directory + "/" + "conformation")

conformation_dirs = []
mainConfdir = []
text = []

confDirs = []

### this is the NOT set only want directories NOT files remove by file type .XXX
notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa")

directories = [f for f in os.listdir(start_directory) if not  f.endswith(notFile)]
directories.sort()
#print(directories)

def moveLigPDBfiles():
    pdb_files = [g for g in os.listdir(cwd) if  g.endswith(".pdb")]
    #print("PDBFILES TO MOVE:" + str(pdb_files))
    ###moves only the pdb files of interest into the conformation folder for the merge
    for j in range(0,len(pdb_files)):
        #splits on _ and digit
        #underscore_split = re.split('\_|\d+',pdb_files[j])
        underscore_split = re.split('\_|\d+[A-Z]\.',pdb_files[j]) #*****NB
        #print(underscore_split)
        if len(underscore_split) == 4: #moves only the full ligand file
            shutil.copy2(pdb_files[j], confDIR)
            #sets the directory back to the start
    os.chdir(start_directory)
#END DEF

def AddConformationRows():
    PBD_lig_Files = [p for p in os.listdir(newConfDIR) if  p.endswith(".pdb")]
    #print(PBD_lig_Files)
    
    if len(PBD_lig_Files[0]) > len(PBD_lig_Files[1]):
        MAIN = PBD_lig_Files[1]
        CONF = PBD_lig_Files[0]
    else:
        MAIN = PBD_lig_Files[0]
        CONF = PBD_lig_Files[1]
    #print(MAIN)
    #print(CONF)

    #with open ()

    with open(CONF, 'r') as readfile:
        for line in readfile:
            # Checks for the conformation letter at pos 15 and replace with ''
            if line[16] != ' ':
                print(line[16])
                newline = line
                new = list(newline)
                new[16] = ' '
                newline = ''.join(new)
                print(newline)
                outfile = open(MAIN, 'a+')
                outfile.write(newline)

            readfile.close
            outfile.close
#END DEF

###SORT: Makes sure the PDB co-ordinates are in the correct order
def sort_file(IN):
    data = []

    try:
        with open(IN, 'r') as f:
            for row in csv.reader(f):
                data.append(row)
        data.sort(key=operator.itemgetter(0))
    except FileNotFoundError:
        print("Check conformation files are as expected.")

    try:
        with open(IN, 'w', newline='') as f:
            csv.writer(f).writerows(data)
    except FileNotFoundError:
        print("Check conformation files are as expected.")
    
    
###END DEF

def newMol2(pdb_file_to_convert):

    save_f = pdb_file_to_convert
    period_split = re.split('\.',save_f)
    name_ff = period_split[0]
    
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdb", "mol2")
    mol = openbabel.OBMol()
    obConversion.ReadFile(mol, save_f)
    name_ff_mol2 = name_ff  +  ".mol2"
    obConversion.WriteFile(mol, name_ff_mol2)

##END DEF

def copyOverFile():
    thisdir = os.getcwd()
    pdbFilesOnly =  [f for f in os.listdir(thisdir) if  f.endswith(".pdb")]#*
    pdbFilesOnly.sort()
    #print(pdbFilesOnly[0])
    
    filename = pdbFilesOnly[0]
    shutil.copy2(pdbFilesOnly[1], filename)
    os.remove(pdbFilesOnly[1])
    #move new file to main directory
    shutil.copy2(pdbFilesOnly[0], start_directory)

##END DEF

def remove_conformationDirs(conformation_dirs, mainConfdir):
    #for i in range(len(directories)):
    #    if len(directories[i]) == 4:
    #        conformation_dirs += [directories[i]]
    #        conformation_dirs_match = str(conformation_dirs[i])[1:]
    #        shutil.rmtree(directories[i])
    #    if (len(directories[i])) == 3 and (str(directories[i]) == conformation_dirs_match):
    #        shutil.rmtree(directories[i])

    for i in range(len(directories)):
        if len(directories[i]) == 4:
            #print(directories[i])
            conformation_dirs += [directories[i]]

    for i in range(len(conformation_dirs)):
        #print(conformation_dirs)
        conformation_dirs_match = str(conformation_dirs[0])[1:]
        #print(conformation_dirs_match)
        try:
            shutil.rmtree(conformation_dirs[i])
        except FileNotFoundError:
            pass

    for i in range(len(directories)):
        if (len(directories[i])) == 3 and (str(directories[i]) == conformation_dirs_match):
            mainConfdir += [directories[i]]
            #print(mainConfdir)

        for i in range(len(mainConfdir)):
            try:
                shutil.rmtree(mainConfdir[i])
            except FileNotFoundError:
                pass
            
def rename_startDIR_confFiles(start_directory):
    changedPDBFile = [s for s in os.listdir(start_directory) if  s.endswith(".pdb")]
    for j in range(0,len(changedPDBFile)):
        underscore_split = re.split('\_',changedPDBFile[j])
    
        if len(underscore_split) > 2:
            #print(underscore_split[2])
            newConfPDBname = underscore_split[0] + underscore_split[2] + ".pdb"
            print("\nCONFORMATION FILES CREATED:")
            print(newConfPDBname)

            os.rename(changedPDBFile[j], newConfPDBname)
###END DEF

def moveFINALConf_files(confDirs):

    start_directory = os.getcwd()
    
    pdbFilesOnly =  [f for f in os.listdir(start_directory) if  f.endswith(".pdb")]

    pdbFilesOnly.sort()
    
    for i in range(len(pdbFilesOnly)):
        #print(pdbFilesOnly)

        period_split = re.split('\.',pdbFilesOnly[i])
        
        if len(period_split[0]) == 8:
            dirname = list(period_split[0])
            dirname = dirname[-4:]
            dirname = ''.join(dirname)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            #print(dirname)

            shutil.copy2(pdbFilesOnly[i], dirname)

            confDirs += [dirname]
            #print(confDirs)

    for i in range(len(pdbFilesOnly)):
        if len(pdbFilesOnly[i]) > 13:

            for j in range(len(confDirs)):
                shutil.copy2(pdbFilesOnly[i], confDirs[j])

###END DEF

### MOVE ALL CONFORMATION FILE INTO CONFORMATION DIR FOR EDITING
'''for i in range(len(directories)):
    conformation_dirs += [directories[i]]
    #looks for the conformation dirs on lengthe =4 
    if len(directories[i]) == 4:
           print(directories[i])
           conformation_dirs += [directories[i]]
           conformation_dirs_match = str(conformation_dirs[i][1:])
           #print(conformation_dirs_match)
           cwd = os.chdir(start_directory + "/" + directories[i])
           #moves only the pdb files of interest into the conformation folder for the merge
           moveLigPDBfiles()
           
    # looks for the lig dir that matches the conformations    
    if (len(directories[i])) == 3 and (str(directories[i]) == conformation_dirs_match):
            main_lig_dir = directories[i]
            print(main_lig_dir)
            cwd = os.chdir(start_directory + "/" + directories[i])
            moveLigPDBfiles()
    i+= 1'''
###

##**
for i in range(len(directories)):
    if len(directories[i]) == 4:
        #print(directories[i])
        conformation_dirs += [directories[i]]

for i in range(len(conformation_dirs)):
    #print(conformation_dirs)
    conformation_dirs_match = str(conformation_dirs[0])[1:]
    #print(conformation_dirs_match)
    cwd = os.chdir(start_directory + "/" + directories[i])
    ###moves only the pdb files of interest into the conformation folder for the merge
    moveLigPDBfiles()

for i in range(len(directories)):
    if (len(directories[i])) == 3 and (str(directories[i]) == conformation_dirs_match):
        main_lig_dir = directories[i]
        #print(main_lig_dir)
        cwd = os.chdir(start_directory + "/" + directories[i])
        moveLigPDBfiles()


            
### MAKE NEW DIRECTORIES FOR CONFORMATION FILES, move and remove          
os.chdir(confDIR)
con_directories = [h for h in os.listdir(confDIR) if  h.endswith(".pdb")]
con_directories.sort()
#print(con_directories)
for i in range(len(con_directories)):
    underscore_split = re.split('\_',con_directories[i])
    New_conf_dir = (underscore_split[2])
    ###creates new conformation directories and moves the conformation files into the respective dir
    if len(New_conf_dir) == 4:
        if not os.path.exists(New_conf_dir):
            os.makedirs(New_conf_dir)
        shutil.copy2(con_directories[i], New_conf_dir)
        os.remove(con_directories[i])
        #moves the main lig file into both of the directories

notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa")
con_directories_new = [m for m in os.listdir(confDIR) if not m.endswith(notFile)]
con_directories_new.sort()
#print("NEW DIRS: " + str(con_directories))
for i in range(len(con_directories_new)):
    mainPDBlig_file = [l for l in os.listdir(confDIR) if  l.endswith(".pdb")]
    shutil.copy2(mainPDBlig_file[0], con_directories_new[i])


###MOVE INTO NEW DIRECTORY
###MERGE THE CONFORMATION FILE WITH THE MAIN LIG FILE (i.e., add ends)
notFile = ("pdb", "mol2", "csv", "txt", "py","kin","log","rsa")
con_directories_new2 = [q for q in os.listdir(confDIR) if not q.endswith(notFile)]
con_directories_new2.sort()
#print("****" + str(con_directories_new2))
#print("CONDIRS" + str(con_directories_new2))
for i in range(len(con_directories_new2)):
    newConfDIR = os.chdir(con_directories_new2[i])

    AddConformationRows()
    #***Check order incase conformation is not at the end but falls in the middle
    orderPDBFile = [r for r in os.listdir(confDIR) if  r.endswith(".pdb")]

    #sort
    for k in range(len(orderPDBFile)):
        IN = orderPDBFile[k]
        sort_file(IN)
        print(IN)

    ###
    #convert to .mol2
    #pdb_file_to_convert = orderPDBFile[0]
    #newMol2(pdb_file_to_convert)
    ###
        
    ###copy to conformation named file
    copyOverFile()

    os.chdir(confDIR)        

###DELETE ALL CONFORMATION FILES FOR RE RUN

os.chdir(start_directory)
shutil.rmtree(confDIR) # removes the conformation dir with files therein (switch off if want to see file separation for **errors)
remove_conformationDirs(conformation_dirs, mainConfdir) # removes all of the directories with conformation data

#renames conformation files in startDIR for chain_separate.py re-rerun
rename_startDIR_confFiles(start_directory)     

