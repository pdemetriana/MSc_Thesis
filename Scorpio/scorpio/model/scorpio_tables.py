#!/usr/bin/env python

"""
Module containing tables and mappers for the SCORPIO2 database. This module
defines the Object Relational Model (ORM).

Example:
  >>> from itc import ITC, ITCData, Affinity, DeltaG, DeltaH, DeltaS, Temperature
  >>> from ligand import Ligand
  >>> from protein import Protein
  >>> from structure import Structure
  >>> import sqlalchemy
  >>> print sqlalchemy.__version__
  0.5.8
  >>> from sqlalchemy import create_engine
  >>> engine = create_engine('sqlite:///:memory:', echo=False)
  >>> from scorpio_tables import METADATA
  >>> METADATA.create_all(engine)
  >>> from sqlalchemy.orm import sessionmaker
  >>> Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
  >>> session = Session()
  >>> lig1 = Ligand('Pyridine', 'c1cnccc1')
  >>> lig2 = Ligand('Propane', 'CCC')
  >>> prot1 = Protein('Poly alanine', 'AAAAAA')
  >>> prot2 = Protein('Poly proline', 'PPPPPP')
  >>> session.add(lig1)
  >>> session.add(lig2)
  >>> session.add(prot1)
  >>> session.add(prot2)
  >>> structure1 = Structure('xxx1', prot1, lig1)
  >>> structure2 = Structure('xxx2', prot2, lig2)
  >>> session.add(structure1)
  >>> session.add(structure2)
  >>> affinity1 = Affinity(10, 'uM')
  >>> delta_g1 = DeltaG(-28.54, 'kJ/mol')
  >>> delta_h1 = DeltaH(-10, 'kJ/mol')
  >>> delta_h2 = DeltaH(-20, 'kJ/mol')
  >>> itc_data = ITCData(affinity=affinity1, delta_g=delta_g1, delta_h=delta_h1)
  >>> itc1 = ITC(itc_data, protein=prot1, ligand=lig1)
  >>> itc_data = ITCData(affinity=affinity1, delta_g=delta_g1, delta_h=delta_h2)
  >>> itc2 = ITC(itc_data, protein=prot2, ligand=lig2)
  >>> print itc1
  <ITC(Kd=10.000, DG=-28.54, DH=-10.00, TDS=18.54, T=298.15)>
  >>> session.add(itc1)
  >>> session.add(itc2)
  >>> session.commit()
  >>> for lig in session.query(Ligand):
  ...     print "%i %s %.2f" % (lig._id, lig.smiles, lig.molecule.molwt)
  ...     print "lig strutures:", lig.structures
  ...     print "lig itc data:", lig.itc_data
  1 c1cccnc1 79.10
  lig strutures: [<Structure('xxx1')>]
  lig itc data: [<ITC(Kd=10.000, DG=-28.54, DH=-10.00, TDS=18.54,
  T=298.15)>] 
  2 CCC 44.10
  lig strutures: [<Structure('xxx2')>]
  lig itc data: [<ITC(Kd=10.000, DG=-28.54, DH=-20.00, TDS=8.54,
  T=298.15)>]
  >>> for prot in session.query(Protein):
  ...     print "%i %s %s" % (prot._id, prot.name, prot.aa_seq)
  ...     print "prot structures:", prot.structures
  ...     print "prot itc data:", prot.itc_data
  1 Poly alanine AAAAAA
  prot structures: [<Structure('xxx1')>]
  prot itc data: [<ITC(Kd=10.000, DG=-28.54, DH=-10.00, TDS=18.54,
  T=298.15)>]
  2 Poly proline PPPPPP
  prot structures: [<Structure('xxx2')>]
  prot itc data: [<ITC(Kd=10.000, DG=-28.54, DH=-20.00, TDS=8.54,
  T=298.15)>]
  >>> for pdb in session.query(Structure):
  ...     print "%s %s %s" % (pdb.pdb_code, pdb.ligand.smiles, pdb.protein.name)
  xxx1 c1cccnc1 Poly alanine
  xxx2 CCC Poly proline
  >>> for itc in session.query(ITC):
  ...     print "%s %s %.2f %.2f %.2f %.2f %.2f" % (itc.protein.name,
  ...     itc.ligand.smiles, itc.affinity, itc.delta_g, itc.delta_h,
  ...     itc.delta_s, itc.temperature)
  Poly alanine c1cccnc1 10.00 -28.54 -10.00 18.54 298.15
  Poly proline CCC 10.00 -28.54 -20.00 8.54 298.15
  >>>

"""

from sqlalchemy import Table, Column, Integer, Float, String, Text, Unicode
from sqlalchemy import Boolean
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import mapper, relation, backref, synonym

from .meta import Base

METADATA = MetaData()

from protein import Protein, ProteinRootName, ProteinSource, \
                    ProteinClassification, ProteinECNumber
from ligand import Ligand, LigandClassification, LigandHetnam, Ligand_Features
from structure import Structure, Contacts
from itc_helpers import ITCInstrument, ITCInteractionType, ITCBuffer
from itc_helpers import ITCCommentDefinition, ITCComment
from itc import ITC
from itc import ITCDeltaCp
from citation import Journal, Author, Citation
 
# Protein root name
PROTEIN_ROOT_NAME_TABLE = Table(
    'protein_root_name',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('root_name', String(255), unique=True, nullable=False)
)
mapper(
    ProteinRootName,
    PROTEIN_ROOT_NAME_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        root_name=synonym('_root_name'),
    )
)

# Protein source
PROTEIN_SOURCE_TABLE = Table(
    'protein_source',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('source', String(255), unique=True, nullable=False)
)
mapper(
    ProteinSource,
    PROTEIN_SOURCE_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        source=synonym('_source'),
    )
)

# Protein classification
PROTEIN_CLASSIFICATION_TABLE = Table(
    'protein_classification',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('classification', String(255), unique=True, nullable=False)
)
mapper(
    ProteinClassification,
    PROTEIN_CLASSIFICATION_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        classification=synonym('_classification'),
    )
)

# Protein enzyme classification number
PROTEIN_EC_NUMBER_TABLE = Table(
    'protein_ec_number',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('ec_number', String(255), unique=True, nullable=False)
)
mapper(
    ProteinECNumber,
    PROTEIN_EC_NUMBER_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        ec_number=synonym('_ec_number'),
    )
)

# Protein
PROTEIN_TABLE = Table(
    'protein',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('protein_root_name_id', ForeignKey('protein_root_name.id')),
    Column('protein_source_id', ForeignKey('protein_source.id')),
    Column('protein_classification_id',
           ForeignKey('protein_classification.id')),
    Column('protein_ec_number_id', ForeignKey('protein_ec_number.id')),
    Column('name', String(255), unique=True, nullable=False),
    Column('aa_seq', Text, unique=True, nullable=False)
)
mapper(
    Protein,
    PROTEIN_TABLE,
    column_prefix='_',
    properties=dict(
        _root_name=relation(
            ProteinRootName,
            uselist=False,
            backref=backref('proteins', uselist=True)),
        _source=relation(
            ProteinSource,
            uselist=False,
            backref=backref('proteins', uselist=True)),
        _classification=relation(
            ProteinClassification,
            uselist=False,
            backref=backref('proteins', uselist=True)),
        _ec_number=relation(
            ProteinECNumber,
            uselist=False,
            backref=backref('proteins', uselist=True)),
        id=synonym('_id'),
        name=synonym('_name'),
        aa_seq=synonym('_aa_seq'),
    )
)

# Ligand classification
LIGAND_CLASSIFICATION_TABLE = Table(
    'ligand_classification',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('classification', String(255), unique=True, nullable=False)
)
mapper(
    LigandClassification,
    LIGAND_CLASSIFICATION_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        classification=synonym('_classification'),
    )
)

# Hetnam
HETNAM_TABLE = Table(
    'hetnam',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('hetnam', String(6)),
)
mapper(
    LigandHetnam,
    HETNAM_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        hetnam=synonym('_hetnam'),
    )
)

# Ligand Hetnam (many-to-many)
LIGAND_HETNAM_TABLE = Table(
    'ligand_hetnam',
    METADATA,
    Column('ligand_id', Integer, ForeignKey('ligand.id')),
    Column('hetnam_id', Integer, ForeignKey('hetnam.id')),
)

# Ligand
LIGAND_TABLE = Table(
    'ligand',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('name', String(256), unique=True),
    Column('ligand_classification_id',
           ForeignKey('ligand_classification.id')),
    Column('smiles', Text, unique=True, nullable=False)
)
mapper(
   Ligand,
    LIGAND_TABLE,
    column_prefix='_',
    properties=dict(
        _classification=relation(
            LigandClassification,
            uselist=False,
            backref=backref('ligands', uselist=True)),
        _hetnams=relation(
            LigandHetnam,
            secondary=LIGAND_HETNAM_TABLE,
        ),
        id=synonym('_id'),
        name=synonym('_name'),
        smiles=synonym('_smiles'),
    )
)

################NEW

#ligand FEATURES
LIGAND_FEATURES_TABLE = Table(
    'Ligand_Features',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('ligand_id', Integer, ForeignKey(Ligand.id)),
    Column('name', String(256)),
    Column('molecular_weight', Float),
    Column('Hacceptors', Integer),
    Column('Hdonors', Integer),
    Column('rotatingBonds', Integer),
    Column('polarizability', String(10)),
)
mapper(
   Ligand_Features,
    LIGAND_FEATURES_TABLE,
    column_prefix='_',
    properties=dict(
        _ligand=relation(
            Ligand,
            uselist=False,
            backref=backref('ligands', uselist=True),
        ),
        id=synonym('_id'),
        name=synonym('_name'),
        molecular_weight=synonym('_molecular_weight'),
        Hacceptors=synonym('_Hacceptors'),
        Hdonors=synonym('_Hdonors'),
        rotatingBonds=synonym('_rotatingBonds'),
        polarizability=synonym('_polarizability'),
    )
)

# Structure
STRUCTURE_TABLE = Table(
    'structure',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('ligand_id', None, ForeignKey('ligand.id')),
    Column('protein_id', None, ForeignKey('protein.id')),
    Column('citation_id', None, ForeignKey('citation.id')),
    Column('pdb_code', String(255), unique=True, nullable=False),
    Column('resolution', Float),
    Column('r_factor', Float),
    Column('experimental_method', String(15))
)
mapper(
    Structure,
    STRUCTURE_TABLE,
    column_prefix='_',
    properties=dict(
        _ligand=relation(Ligand,
                         uselist=False,
                         backref=backref('structures', uselist=True)
        ),
        _protein=relation(Protein,
                          uselist=False,
                          backref=backref('structures', uselist=True)
        ),
        _citation=relation(Citation,
                          uselist=False,
                          backref=backref('structures', uselist=True)
        ),
        id=synonym('_id'),
        pdb_code=synonym('_pdb_code'),
        resolution=synonym('_resolution'),
        r_factor=synonym('_r_factor'),
        experimental_method=synonym('_experimental_method'),
    )
)

# Structure Contacts
CONTACTS_TABLE = Table(
    'contacts',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('structure_id', None, ForeignKey('structure.id')),
    Column('pdb_code', String(255), unique=True, nullable=False),
    Column('Hbonds', Integer),
    Column('polar_cont_changes', String(10)),
    Column('apolar_cont_changes', String(10)),
    Column('polar_water_cont_changes', String(10)),
    Column('apolar_water_cont_changes', String(10)),
    Column('surface_waters', String(10)),
    Column('cleft_waters', String(10)),
    Column('buried_waters', String(10))
)
mapper(
    Contacts,
    CONTACTS_TABLE,
    column_prefix='_',
    properties=dict(
        _structure=relation(Structure,
                          uselist=False,
                          backref=backref('structures', uselist=True)
        ),
        id=synonym('_id'),
        pdb_code=synonym('_pdb_code'),
        Hbonds=synonym('_Hbonds'),
        polar_cont_changes=synonym('_polar_cont_changes'),
        apolar_cont_changes=synonym('_apolar_cont_changes'),
        polar_water_cont_changes=synonym('_polar_water_cont_changes'),
        apolar_water_cont_changes=synonym('_apolar_water_cont_changes'),
        surface_waters=synonym('_surface_waters'),
        cleft_waters=synonym('_cleft_waters'),
        buried_waters=synonym('_buried_waters'),
    )
)

# ITC Instrument
ITC_INSTRUMENT_TABLE = Table(
    'itc_instrument',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), unique=True, nullable=False)
)
mapper(
    ITCInstrument,
    ITC_INSTRUMENT_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        name=synonym('_name'),
    )
)

# ITC Interaction type
ITC_INTERACTION_TYPE_TABLE = Table(
    'itc_interaction_type',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('interaction_type', String(255), unique=True, nullable=False)
)
mapper(
    ITCInteractionType,
    ITC_INTERACTION_TYPE_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        interaction_type=synonym('_interaction_type'),
    )
)

# ITC Buffer
BUFFER_TABLE = Table(
    'buffer',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('description', Text, unique=True, nullable=False)
)
mapper(
    ITCBuffer,
    BUFFER_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        description=synonym('_description'),
    )
)

# ITC Delta Cp
ITC_DELTA_CP_TABLE = Table(
    'itc_delta_cp',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('ligand_id', None, ForeignKey('ligand.id')),
    Column('protein_id', None, ForeignKey('protein.id')),
    Column('citation_id', None, ForeignKey('citation.id')),
    Column('buffer_id', None, ForeignKey('buffer.id')),
    Column('delta_cp', Float),
    Column('delta_cp_exp_err', Float),
    Column('delta_cp_unit', String(10)),
    Column('delta_cp_raw', Float),
    Column('delta_cp_exp_err_raw', Float),
    Column('delta_cp_unit_raw', String(10)),
    Column('ph', Float),
)
mapper(
    ITCDeltaCp,
    ITC_DELTA_CP_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        _ligand=relation(Ligand,
                         uselist=False,
                         backref=backref('itc_delta_cp', uselist=True)
                         ),
        _protein=relation(Protein,
                          uselist=False,
                          backref=backref('itc_delta_cp', uselist=True)),
        _citation=relation(Citation,
                          uselist=False,
                          backref=backref('itc_delta_cp', uselist=True)
        ),
        _buffer=relation(ITCBuffer,
                          uselist=False,
                          backref=backref('itc_delta_cp', uselist=True)
        ),
        delta_cp=synonym('_delta_cp'),
        delta_cp_exp_err=synonym('_delta_cp_exp_err'),
        delta_cp_unit=synonym('_delta_cp_unit'),
        delta_cp_raw=synonym('_delta_cp_raw'),
        delta_cp_exp_err_raw=synonym('_delta_cp_exp_err_raw'),
        delta_cp_unit_raw=synonym('_delta_cp_unit_raw'),
        ph=synonym('_ph'),
    )
)

# ITC Comment Definition
ITC_COMMENT_DEFINITION_TABLE = Table(
    'itc_comment_definition',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('definition', String(255), unique=True, nullable=False),
)
mapper(
    ITCCommentDefinition,
    ITC_COMMENT_DEFINITION_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        definition=synonym('_definition'),
    )
)

# ITC Comment
ITC_COMMENT_TABLE = Table(
    'itc_comment',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('itc_commment_definition_id', None,
           ForeignKey('itc_comment_definition.id')),
    Column('comment', Text, unique=True, nullable=False),
)
mapper(
    ITCComment,
    ITC_COMMENT_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        comment=synonym('_comment'),
        _definition=relation(ITCCommentDefinition,
                          uselist=False,
                          backref=backref('comments', uselist=True)
        ),
    )
)

# ITC ITC Comment (many-to-many)
ITC_ITC_COMMENT_TABLE = Table(
    'itc_itc_comment',
    METADATA,
    Column('itc_id', Integer, ForeignKey('itc.id')),
    Column('itc_comment_id', Integer, ForeignKey('itc_comment.id')),
)

# ITC
ITC_TABLE = Table(
    'itc',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('ligand_id', None, ForeignKey('ligand.id')),
    Column('protein_id', None, ForeignKey('protein.id')),
    Column('citation_id', None, ForeignKey('citation.id')),
    Column('instrument_id', None, ForeignKey('itc_instrument.id')),
    Column('interaction_type_id', None, ForeignKey('itc_interaction_type.id')),
    Column('buffer_id', None, ForeignKey('buffer.id')),
    Column('itc_delta_cp_id', None, ForeignKey('itc_delta_cp.id')),
    Column('affinity', Float),
    Column('affinity_exp_err', Float),
    Column('affinity_unit', String(2)),
    Column('delta_g', Float),
    Column('delta_g_exp_err', Float),
    Column('delta_g_unit', String(8)),
    Column('delta_h', Float),
    Column('delta_h_exp_err', Float),
    Column('delta_h_unit', String(8)),
    Column('delta_s', Float),
    Column('delta_s_exp_err', Float),
    Column('delta_s_unit', String(11)),
    Column('temperature', Float),
    Column('temperature_unit', String(1)),
    Column('affinity_raw', Float),
    Column('affinity_exp_err_raw', Float),
    Column('affinity_unit_raw', String(2)),
    Column('delta_g_raw', Float),
    Column('delta_g_exp_err_raw', Float),
    Column('delta_g_unit_raw', String(8)),
    Column('delta_h_raw', Float),
    Column('delta_h_exp_err_raw', Float),
    Column('delta_h_unit_raw', String(8)),
    Column('delta_s_raw', Float),
    Column('delta_s_exp_err_raw', Float),
    Column('delta_s_unit_raw', String(11)),
    Column('temperature_raw', Float),
    Column('temperature_unit_raw', String(1)),
    Column('ph', Float),
    Column('cell_content', String(7)),
    Column('stoich_param', Float),
    Column('stoich_param_exp_err', Float),
    Column('protonation_state_examined', Boolean),
)
mapper(
    ITC,
    ITC_TABLE,
    column_prefix='_',
    properties=dict(
        _ligand=relation(Ligand,
                         uselist=False,
                         backref=backref('itc_data', uselist=True)
                         ),
        _protein=relation(Protein,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)),
        _citation=relation(Citation,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)
        ),
        _instrument=relation(ITCInstrument,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)
        ),
        _interaction_type=relation(ITCInteractionType,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)
        ),
        _buffer=relation(ITCBuffer,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)
        ),
        _comments=relation(
            ITCComment,
            secondary=ITC_ITC_COMMENT_TABLE,
        ),
        _itc_delta_cp=relation(ITCDeltaCp,
                          uselist=False,
                          backref=backref('itc_data', uselist=True)
        ),
        id=synonym('_id'),
        affinity=synonym('_affinity'),
        affinity_exp_err=synonym('_affinity_exp_err'),
        affinity_unit=synonym('_affinity_unit'),
        delta_g=synonym('_delta_g'),
        delta_g_exp_err=synonym('_delta_g_exp_err'),
        delta_g_unit=synonym('_delta_g_unit'),
        delta_h=synonym('_delta_h'),
        delta_h_exp_err=synonym('_delta_h_exp_err'),
        delta_h_unit=synonym('_delta_h_unit'),
        delta_s=synonym('_delta_s'),
        delta_s_exp_err=synonym('_delta_s_exp_err'),
        delta_s_unit=synonym('_delta_s_unit'),
        temperature=synonym('_temperature'),
        temperature_unit=synonym('_temperature_unit'),
        affinity_raw=synonym('_affinity_raw'),
        affinity_exp_err_raw=synonym('_affinity_exp_err_raw'),
        affinity_unit_raw=synonym('_affinity_unit_raw'),
        delta_g_raw=synonym('_delta_g_raw'),
        delta_g_exp_err_raw=synonym('_delta_g_exp_err_raw'),
        delta_g_unit_raw=synonym('_delta_g_unit_raw'),
        delta_h_raw=synonym('_delta_h_raw'),
        delta_h_exp_err_raw=synonym('_delta_h_exp_err_raw'),
        delta_h_unit_raw=synonym('_delta_h_unit_raw'),
        delta_s_raw=synonym('_delta_s_raw'),
        delta_s_exp_err_raw=synonym('_delta_s_exp_err_raw'),
        delta_s_unit_raw=synonym('_delta_s_unit_raw'),
        temperature_raw=synonym('_temperature_raw'),
        temperature_unit_raw=synonym('_temperature_unit_raw'),
        ph=synonym('_ph'),
        cell_content=synonym('_cell_content'),
        stoich_param=synonym('_stoich_param'),
        stoich_param_exp_err=synonym('_stoich_param_exp_err'),
        protonation_state_examined=synonym('_protonation_state_examined'),
    )
)

# Journal
JOURNAL_TABLE = Table(
    'journal',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('abbreviation', String(50))
)
mapper(
    Journal,
    JOURNAL_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        name=synonym('_name'),
        abbreviation=synonym('_abbreviation'),
    )
)

# Author
AUTHOR_TABLE = Table(
    'author',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('first_name', Unicode(20)),
    Column('last_name', Unicode(20))
)
mapper(
    Author,
    AUTHOR_TABLE,
    column_prefix='_',
    properties=dict(
        id=synonym('_id'),
        first_name=synonym('_first_name'),
        last_name=synonym('_last_name'),
    )
)

# Citation Author (many-to-many)
CITATION_AUTHOR_TABLE = Table(
    'citation_author',
    METADATA,
    Column('citation_id', Integer, ForeignKey('citation.id')),
    Column('author_id', Integer, ForeignKey('author.id')),
)

# Citation
CITATION_TABLE = Table(
    'citation',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('journal_id', ForeignKey('journal.id')),
    Column('title', Unicode(255)),
    Column('volume', Integer),
    Column('first_page', Integer),
    Column('last_page', Integer),
    Column('year', Integer),
    Column('pubmed_id', String(20)),
)
mapper(
    Citation,
    CITATION_TABLE,
    column_prefix='_',
    properties=dict(
        _journal=relation(
            Journal,
            uselist=False,
            backref=backref('citations', uselist=True)
        ),
        _authors=relation(
            Author,
            secondary=CITATION_AUTHOR_TABLE,
        ),
        id=synonym('_id'),
        journal=synonym('_journal'),
        title=synonym('_title'),
        volume=synonym('_volume'),
        first_page=synonym('_first_page'),
        last_page=synonym('_last_page'),
        year=synonym('_year'),
        pubmed_id=synonym('_pubmed_id'),
    )
)

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

