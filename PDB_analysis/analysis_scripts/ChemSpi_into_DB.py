#!/usr/bin/env python

############################################################
'''
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

from scorpio.model import scorpio_tables as tables
'''
import os
import pyexcel
'''
engine = create_engine('sqlite:///production.db', echo=True)
Base = declarative_base()


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
'''

#"PDB	id	name	Molecular weight	Average Mass	Momoisotopic Mass	Nominal Mass	AlogP	XlogP	H-acceptors	H-donors	Freely Rotating Bonds	Rule of 5 Violations	Polar Surface Area(A^2)	Polarizability(+- 10.5 10^-24 cm^3)	Refraction Index	Molar Refractivity(cm^3)	Surface Tension(dyne/cm)	Molar Volume(cm^3)"
my_ligand = pyexcel.get_sheet(file_name="ligand_feature_table.xlsx")
my_ligand_Unix=open("ligand_feature_table.txt", 'w')

i=1
while i < len(my_ligand.column[0]):
	lig_row = my_ligand.row[i]
	scId, name, molWeight, hAcc, hDon, rotBonds, Polarizability=(lig_row[1], lig_row[2], lig_row[3], lig_row[9], lig_row[10], lig_row[11], lig_row[14].split('+')[0])
	my_ligand_Unix.write(scId+"\t"+name+"\t"+molWeight+"\t"+hAcc+"\t"+hDon+"\t"+rotBonds+"\t"+Polarizability+"\t"+"\n")
	i=i+1

my_ligand_Unix.close()




