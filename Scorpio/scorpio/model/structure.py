#!/usr/bin/env python

"""
This module contains classes for dealing with PDB structures.
"""

from ligand import Ligand
from protein import Protein
from citation import Citation

class Structure(object):
    """
    Structure class.

    Attributes:
      * pdb_code - Structure PDB code
      * protein - Protein in structure
      * ligand - Ligand in structure

    During initialisation any capitalised letters in PDB codes are converted
    to lower case.

    The PDB code is used when checking whether or not two structures are the
    same.

    Examples:
      >>> from structure import *
      >>> from protein import Protein
      >>> from ligand import Ligand
      >>>
      >>> lig = Ligand('Pyridine', 'c1cnccc1')
      >>> prot = Protein('Poly alanine', 'AAAAAA')
      >>> pdb = Structure('xxx1', prot, lig)
      >>> "%s %s %s" % (pdb.pdb_code, pdb.ligand.smiles, pdb.protein.name)
      'xxx1 c1cccnc1 Poly alanine'


    """
    
    def __init__(self,
                 pdb_code,
                 protein,
                 ligand,
                 citation=None,
                 resolution=None,
                 r_factor=None,
                 experimental_method=None):
        self._pdb_code = pdb_code.lower()
        self._protein = protein
        self._ligand = ligand
        self._citation = citation
        self._resolution = resolution
        self._r_factor = r_factor
        self._experimental_method = experimental_method

    def __repr__(self):
        return "<Structure('%s')>" % self._pdb_code

    def __eq__(self, other):
        return self.pdb_code == other.pdb_code

    def __ne__(self, other):
        return self.pdb_code != other.pdb_code
    
    def _get_pdb_code(self):
        return self._pdb_code
    def _set_pdb_code(self, pdb_code):
        self._pdb_code = pdb_code
    pdb_code = property(_get_pdb_code, _set_pdb_code)


    def _get_ligand(self):
        return self._ligand
    def _set_ligand(self, ligand):
        assert isinstance(ligand, Ligand), 'Supplied ligand is not a Ligand'
        self._ligand = ligand
    ligand = property(_get_ligand, _set_ligand)

    def _get_protein(self):
        return self._protein
    def _set_protein(self, protein):
        assert isinstance(protein, Protein), 'Supplied protein is not a Protein'
        self._protein = protein
    protein = property(_get_protein, _set_protein)

    def _get_citation(self):
        return self._citation
    def _set_citation(self, citation):
        assert isinstance(citation, Citation), 'Supplied citation is not a Citation'
        self._citation = citation
    citation = property(_get_citation, _set_citation)

    def _get_resolution(self):
        return self._resolution
    def _set_resolution(self, resolution):
        self._resolution = resolution
    resolution = property(_get_resolution, _set_resolution)

    def _get_r_factor(self):
        return self._r_factor
    def _set_r_factor(self, r_factor):
        self._r_factor = r_factor
    r_factor = property(_get_r_factor, _set_r_factor)

    def _get_experimental_method(self):
        return self._experimental_method
    def _set_experimental_method(self, experimental_method):
        self._experimental_method = experimental_method
    experimental_method = property(_get_experimental_method, _set_experimental_method)

class Contacts(object):

    def __init__(self, structure, pdb_code, Hbonds=None, polar_cont_changes=None, apolar_cont_changes=None, polar_water_cont_changes=None, apolar_water_cont_changes=None, surface_waters=None, cleft_waters=None, buried_waters=None):
        self._structure = structure
        self._Hbonds = Hbonds
        self._pdb_code = pdb_code
        self._polar_cont_changes = polar_cont_changes
        self._apolar_cont_changes = apolar_cont_changes
        self._polar_water_cont_changes = polar_water_cont_changes
        self._apolar_water_cont_changes = apolar_water_cont_changes
        self._surface_waters = surface_waters
        self._cleft_waters = cleft_waters
        self._buried_waters = buried_waters


    def __repr__(self):
         return "<Contacts('%s')>" % self._pdb_code


    def __eq__(self, other):
        return self.pdb_code == other.pdb_code

    def __ne__(self, other):
        return self.pdb_code != other.pdb_code


    def _get_pdb_code(self):
        return self._pdb_code

    def _set_pdb_code(self, pdb_code):
        self._pdb_code = pdb_code
    pdb_code = property(_get_pdb_code, _set_pdb_code)

    def _get_structure(self):
        return self._structure

    def _set_structure(self, structure):
        assert isinstance(structure, Structure)
        self._structure = structure
    structure = property(_get_structure, _set_structure)

############################################################################
    def _get_Hbonds(self):
        return self._Hbonds

    def _set_Hbonds(self, Hbonds):
        self._Hbonds = Hbonds
    Hbonds = property(_get_Hbonds, _set_Hbonds)

    def _get_polar_cont_changes(self):
        return self._polar_cont_changes

    def _set_polar_cont_changes(self, polar_cont_changes):
        self._polar_cont_changes = polar_cont_changes
    polar_cont_changes = property(_get_polar_cont_changes, _set_polar_cont_changes)
#######
    def _get_apolar_cont_changes(self):
        return self._apolar_cont_changes

    def _set_apolar_cont_changes(self, apolar_cont_changes):
        self._apolar_cont_changes = apolar_cont_changes
    apolar_cont_changes = property(_get_apolar_cont_changes, _set_apolar_cont_changes)
########
    def _get_polar_water_cont_changes(self):
        return self._polar_water_cont_changes

    def _set_polar_water_cont_changes(self, polar_water_cont_changes):
        self._polar_water_cont_changes = polar_water_cont_changes
    polar_water_cont_changes = property(_get_polar_water_cont_changes, _set_polar_water_cont_changes)
#########
    def _get_apolar_water_cont_changes(self):
        return self._apolar_water_cont_changes

    def _set_apolar_water_cont_changes(self, apolar_water_cont_changes):
        self._apolar_water_cont_changes = apolar_water_cont_changes
    apolar_water_cont_changes = property(_get_apolar_water_cont_changes, _set_apolar_water_cont_changes)
###########
    def _get_surface_waters(self):
        return self._surface_waters
    def _set_surface_waters(self, surface_waters):
        self._surface_waters = surface_waters
    surface_waters = property(_get_surface_waters, _set_surface_waters)

    def _get_cleft_waters(self):
        return self._cleft_waters
    def _set_cleft_waters(self, cleft_waters):
        self._cleft_waters = cleft_waters
    cleft_waters = property(_get_cleft_waters, _set_cleft_waters)

    def _get_buried_waters(self):
        return self._buried_waters
    def _set_buried_waters(self, buried_waters):
        self._buried_waters = buried_waters
    buried_waters = property(_get_buried_waters, _set_buried_waters)




if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    import unittest
    TEST_SUITE = doctest.DocFileSuite('tests/test_structure.txt',
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    unittest.TextTestRunner().run(TEST_SUITE)

