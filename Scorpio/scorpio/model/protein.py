#!/usr/bin/env python

"""
Module containing classes for dealing with proteins.
"""

import re

WHITE_SPACE = re.compile(r'\W')
def normalise_aa_seq(aa_seq):
    return WHITE_SPACE.sub('', aa_seq.upper())


class ProteinRootName(object):
    """
    Protein root name class.

    E.g. SH2 as opposed to v-src SH2 and c-src SH2.
    Also useful to simplify protein names with point mutations.

    Attributes:
      * root_name - root name of protein

    Examples:
      >>> from protein import ProteinRootName
      >>> prn = ProteinRootName('SH2')
      >>> prn
      <ProteinRootName('SH2')>
      >>> prn.root_name
      'SH2'

    """
    def __init__(self, root_name):
        self._root_name = root_name

    def __repr__(self):
        return "<ProteinRootName('%s')>" % self._root_name

    def __eq__(self, other):
        return self.root_name == other.root_name

    def __ne__(self, other):
        return self.root_name != other.root_name

    def _get_root_name(self):
        """
        Return root_name.
        """
        return self._root_name

    def _set_root_name(self, root_name):
        """
        Set root_name name.
        """
        self._root_name = root_name

    root_name = property(_get_root_name, _set_root_name)


class ProteinSource(object):
    """
    Protein source class.

    E.g. Homo Sapiens

    Attributes:
      * source - protein source

    Examples:
      >>> from protein import ProteinSource
      >>> ps = ProteinSource('Homo Sapiens')
      >>> ps
      <ProteinSource('Homo Sapiens')>
      >>> ps.source
      'Homo Sapiens'

    """
    def __init__(self, source):
        self._source = source

    def __repr__(self):
        return "<ProteinSource('%s')>" % self._source

    def __eq__(self, other):
        return self.source == other.source

    def __ne__(self, other):
        return self.source != other.source

    def _get_source(self):
        """
        Return source.
        """
        return self._source

    def _set_source(self, source):
        """
        Set source name.
        """
        self._source = source
    source = property(_get_source, _set_source)

class ProteinClassification(object):
    """
    Protein classification class.

    E.g. HYDROLASE

    Attributes:
      * classification - protein classification

    Examples:
      >>> from protein import ProteinClassification
      >>> pc = ProteinClassification('HYDROLASE')
      >>> pc
      <ProteinClassification('HYDROLASE')>
      >>> pc.classification
      'HYDROLASE'

    """
    def __init__(self, classification):
        self._classification = classification

    def __repr__(self):
        return "<ProteinClassification('%s')>" % self._classification

    def __eq__(self, other):
        return self.classification == other.classification

    def __ne__(self, other):
        return self.classification != other.classification

    def _get_classification(self):
        """
        Return classification.
        """
        return self._classification

    def _set_classification(self, classification):
        """
        Set classification name.
        """
        self._classification = classification

    classification = property(_get_classification, _set_classification)

class ProteinECNumber(object):
    """
    Protein enzyme classification number class.

    E.g. 3.6.1.23

    Attributes:
      * ec_number - protein ec_number

    Examples:
      >>> from protein import ProteinECNumber
      >>> pecn = ProteinECNumber('3.6.1.23')
      >>> pecn
      <ProteinECNumber('3.6.1.23')>
      >>> pecn.ec_number
      '3.6.1.23'

    """
    def __init__(self, ec_number):
        self._ec_number = ec_number

    def __repr__(self):
        return "<ProteinECNumber('%s')>" % self._ec_number

    def __eq__(self, other):
        return self.ec_number == other.ec_number

    def __ne__(self, other):
        return self.ec_number != other.ec_number

    def _get_ec_number(self):
        """
        Return ec_number.
        """
        return self._ec_number

    def _set_ec_number(self, ec_number):
        """
        Set ec_number name.
        """
        self._ec_number = ec_number

    ec_number = property(_get_ec_number, _set_ec_number)

class Protein(object):
    """
    Protein class

    Attributes:
      * name   - name of the protein
      * aa_seq - amino acid sequence of the protein

    Any whitespace characters are removed from the amino acid sequence.

    The amino acid sequence string is used when checking whether or not two
    proteins are the same.

    Examples:
      >>> from protein import *
      >>> prot1 = Protein('Insulin',
      ...                 'MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTP\
      ...                  KTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQ\
      ...                  LENYCN')
      >>> prot1
      <Protein('Insulin')>
      >>> prot1.aa_seq
      'MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN'

    """
    
    def __init__(self,
                 name,
                 aa_seq,
                 root_name=None,
                 source=None,
                 classification=None,
                 ec_number=None):
        self._name = name
        self._aa_seq = normalise_aa_seq(aa_seq)
        self._root_name = root_name
        self._source = source
        self._classification = classification
        self._ec_number = ec_number

    def __repr__(self):
        return "<Protein('%s')>" % self._name

    def __eq__(self, other):
        return self.aa_seq == other.aa_seq

    def __ne__(self, other):
        return self.aa_seq != other.aa_seq

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
    name = property(get_name, set_name)

    def get_aa_seq(self):
        return self._aa_seq
    def set_aa_seq(self, aa_seq):
        self._aa_seq = normalise_aa_seq(aa_seq)
    aa_seq = property(get_aa_seq, set_aa_seq)

    def get_root_name(self):
        if self._root_name:
            return self._root_name
    def set_root_name(self, root_name):
        assert root_name, ProteinRootName
        self._root_name = root_name
    root_name = property(get_root_name, set_root_name)
        
    def get_source(self):
        if self._source:
            return self._source
    def set_source(self, source):
        assert source, ProteinSource
        self._source = source
    source = property(get_source, set_source)
        
    def get_classification(self):
        if self._classification:
            return self._classification
    def set_classification(self, classification):
        assert classification, ProteinClassification
        self._classification = classification
    classification = property(get_classification, set_classification)
        
    def get_ec_number(self):
        if self._ec_number:
            return self._ec_number
    def set_ec_number(self, ec_number):
        assert ec_number, ProteinECNumber
        self._ec_number = ec_number
    ec_number = property(get_ec_number, set_ec_number)
        
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    import unittest
    TEST_SUITE = doctest.DocFileSuite('tests/test_protein.txt',
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    unittest.TextTestRunner().run(TEST_SUITE)

