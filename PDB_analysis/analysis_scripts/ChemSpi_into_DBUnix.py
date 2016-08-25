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
my_ligand_Unix=open("ligand_feature_table.txt", 'r')
my_ligand=my_ligand_Unix.readlines()
my_ligand_Unix.close()

ligands=[]
for row in my_ligand:
	lig_row = row.split("\t")
	scId, name, molWeight, hAcc, hDon, rotBonds, Polarizability=lig_row
	ligand_info = tables.Ligand_Characteristics(ligand_id=scId, name=name, molecular_weight=molWeight, Hacceptors=hAcc, Hdonors=hDon, rotatingBonds=rotBonds, polarizability=Polarizability)
	session.add(Alig)
	
session.commit()



