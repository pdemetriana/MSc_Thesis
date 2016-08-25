#!/usr/bin/env python

"""
Module containing classes for dealing with ligands.
"""

import pybel

class LigandClassification(object):
    """
    Ligand classification class.

    E.g. Peptide

    Attributes:
      * classification - ligand classification

    Examples:
      >>> from ligand import LigandClassification
      >>> lc = LigandClassification('Peptide')
      >>> lc
      <LigandClassification('Peptide')>
      >>> lc.classification
      'Peptide'

    """
    def __init__(self, classification):
        self._classification = classification

    def __repr__(self):
        return "<LigandClassification('%s')>" % self._classification

    def __eq__(self, other):
        return self.classification == other.classification

    def __ne__(self, other):
        return self.classification != other.classification

    def _get_classification(self):
        return self._classification
    def _set_classification(self, classification):
        self._classification = classification
    classification = property(_get_classification, _set_classification)

class LigandHetnam(object):
    """
    Hetnam class.

    Attributes:
      * hetnam - PDB HETNAM
    
    Examples:
      >>> from ligand import LigandHetnam
      >>> h = LigandHetnam('GLN')
      >>> h
      <LigandHetnam('GLN')>

    """

    def __init__(self, hetnam):
        self._hetnam = hetnam

    def __repr__(self):
        return u"<LigandHetnam('%s')>" % self._hetnam

    def __eq__(self, other):
        return self.hetnam == other.hetnam

    def __ne__(self, other):
        return self.hetnam != other.hetnam
    
    @property
    def hetnam(self):
        """
        Return PDB HETNAM.
        """
        return self._hetnam
    def _get_hetnam(self):
        return self._hetnam
    def _set_hetnam(self, hetnam):
        self._hetnam = hetnam
    hetnam = property(_get_hetnam, _set_hetnam)


class Ligand(object):
    """
    Ligand class.

    Attributes:
      * name - ligand name
      * smiles  - canonical SMILES string representation of the ligand
      * molecule - pybel instance of the ligand, which can be used to generate
                   chemical properties

    During the initialisation of a ligand the SMILES string provided is
    converted to its canonical form.

    The canonical SMILES string is used when checking whether or not two
    ligands are the same.

    Examples:
      >>> from ligand import *
      >>> lig1 = Ligand('Pyridine', 'c1ncccc1')
      >>> lig1
      <Ligand('c1cccnc1')>
      >>> lig2 = Ligand('Also pyridine', 'c1ccncc1')
      >>> lig1 == lig2
      True
      >>> '%s molwt %.2f' % (lig1.smiles, lig1.molecule.molwt)
      'c1cccnc1 molwt 79.10'
    
    """
    
    def __init__(self, name, smiles, classification=None, hetnams=None):
        self._name = name
        self._smiles = None
        self._classification = classification
        if not hetnams:
            self._hetnams = []
        else:
            self._hetnams = hetnams
        self._generate_chemical_attributes(smiles)

    def __repr__(self):
        return "<Ligand('%s')>" % self._smiles

    def __eq__(self, other):
        if not isinstance(other, Ligand):
            return False
        return self.smiles == other.smiles

    def __ne__(self, other):
        if not isinstance(other, Ligand):
            return True
        return self.smiles != other.smiles

    def _generate_chemical_attributes(self, smiles):
        """
        Generate the chemical attributes using a pybel molecule.
        """
        tmp_mol = pybel.readstring('smi', smiles)
        self._smiles = tmp_mol.write('can').split()[0]  # Use canonical smiles

    def _get_name(self):
        return self._name
    def _set_name(self, name):
        self._name = name
    name = property(_get_name, _set_name)

    def _get_smiles(self):
        return self._smiles
    def _set_smiles(self, smiles):
        self._generate_chemical_attributes(smiles)
    smiles = property(_get_smiles, _set_smiles)

    def _get_classification(self):
        return self._classification
    def _set_classification(self, classification):
        assert isinstance(classification, LigandClassification)
        self._classification = classification
    classification = property(_get_classification, _set_classification)

    def _get_hetnams(self):
        return self._hetnams
    def _set_hetnams(self, hetnams):
        self._hetnams = hetnams
    hetnams = property(_get_hetnams, _set_hetnams)

    @property
    def molecule(self):
        """
        Return a pyble molecule that can be used to calculate properties etc.
        """
        return pybel.readstring('smi', str(self._smiles))

########	NEW TABLE	########

class Ligand_Features(object):

    def __init__(self, ligand_id, name, molecular_weight=None, Hacceptors=None, Hdonors=None, rotatingBonds=None, polarizability=None):
        self._name = name
        self._ligand_id = ligand_id
        self._molecular_weight = molecular_weight
        self._Hacceptors = Hacceptors
        self._Hdonors = Hdonors
        self._rotatingBonds = rotatingBonds
        self._polarizability = polarizability


    def __repr__(self):
         return "<Ligand_Features('%s')>" % self._name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name


    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name
    name = property(_get_name, _set_name)

    def _get_ligand_id(self):
        return self._ligand_id

    def _set_ligand_id(self, ligand_id):
        assert isinstance(ligand, Ligand)
        self._ligand_id = ligand
    ligand_id = property(_get_ligand_id, _set_ligand_id)

    def _get_molecular_weight(self):
        return self._molecular_weight

    def _set_molecular_weight(self, molecular_weight):
        self._molecular_weight = molecular_weight
    molecular_weight = property(_get_molecular_weight, _set_molecular_weight)

    def _get_Hacceptors(self):
        return self._Hacceptors

    def _set_Hacceptors(self, Hacceptors):
        self._Hacceptors = Hacceptors
    Hacceptors = property(_get_Hacceptors, _set_Hacceptors)

    def _get_Hdonors(self):
        return self._Hdonors

    def _set_Hdonors(self, Hdonors):
        self._Hdonors = Hdonors
    Hdonors = property(_get_Hdonors, _set_Hdonors)

    def _get_rotatingBonds(self):
        return self._rotatingBonds

    def _set_rotatingBonds(self, rotatingBonds):
        self._rotatingBonds = rotatingBonds
    rotatingBonds = property(_get_rotatingBonds, _set_rotatingBonds)

    def _get_polarizability(self):
        return self._polarizability
    def _set_polarizability(self, polarizability):
        self._polarizability = polarizability
    polarizability = property(_get_polarizability, _set_polarizability)



##########################

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    import unittest
    TEST_SUITE = doctest.DocFileSuite('tests/test_ligand.txt',
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    unittest.TextTestRunner().run(TEST_SUITE)

