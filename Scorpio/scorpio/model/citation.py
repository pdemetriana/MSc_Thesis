#!/usr/bin/env python

"""
The citation module has classes for dealing with publications.
"""

class Journal(object):
    """
    Journal class.

    Attributes:
      * name - journal name
      * abbreviation - journal abbreviation

    Examples:
      >>> from citation import Journal
      >>> j = Journal("Journal of Molecular Biology", "JMB")
      >>> j
      <Journal('JMB')>
      >>> j.name
      'Journal of Molecular Biology'
      >>> j.abbreviation
      'JMB'

    """

    def __init__(self, name, abb):
        self._name = name
        self._abbreviation = abb

    def __repr__(self):
        return "<Journal('%s')>" % self._abbreviation
    
    def __eq__(self, other):
        name1 = self.name.lower()
        name2 = other.name.lower()
        abb1 = self.abbreviation.lower()
        abb2 = other.abbreviation.lower()
        if (name1 == name2 or abb1 == abb2):
            return True
        else:
            return False

    def __ne__(self, other):
        name1 = self.name.lower()
        name2 = other.name.lower()
        abb1 = self.abbreviation.lower()
        abb2 = other.abbreviation.lower()
        if (name1 == name2 or abb1 == abb2):
            return False
        else:
            return True
    
    def set_name(self, name):
        self._name = name
    def get_name(self):
        return self._name
    name = property(get_name, set_name)

    def set_abbreviation(self, abbreviation):
        self._abbreviation = abbreviation
    def get_abbreviation(self):
        return self._abbreviation
    abbreviation = property(get_abbreviation, set_abbreviation)

class Author(object):
    """
    Author class.

    Attributes:
      * first_name - authors first name
      * last_name  - authors last name
    
    Examples:
      >>> from citation import Author
      >>> a = Author('Tjelvar S. G.', 'Olsson')
      >>> a
      <Author(u'Tjelvar S. G.' u'Olsson')>
      >>> a.first_name
      u'Tjelvar S. G.'
      >>> a.last_name
      u'Olsson'

    """

    def __init__(self, first_name, last_name):
        self._first_name = unicode(first_name)
        self._last_name = unicode(last_name)

    def __repr__(self):
        return u"<Author(%r %r)>" % (self._first_name, self._last_name)

    def __str__(self):
        return u"%s %s" % (self._first_name, self._last_name)

    def __eq__(self, other):
        fn1 = self.first_name.lower()
        fn2 = other.first_name.lower()
        sn1 = self.last_name.lower()
        sn2 = other.last_name.lower()
        if (fn1 == fn2 and sn1 == sn2):
            return True
        else:
            return False

    def __ne__(self, other):
        fn1 = self.first_name.lower()
        fn2 = other.first_name.lower()
        sn1 = self.last_name.lower()
        sn2 = other.last_name.lower()
        if (fn1 == fn2 and sn1 == sn2):
            return False
        else:
            return True
    
    def set_first_name(self, first_name):
        self._first_name = first_name
    def get_first_name(self):
        return self._first_name
    first_name = property(get_first_name, set_first_name)

    def set_last_name(self, last_name):
        self._last_name = last_name
    def get_last_name(self):
        return self._last_name
    last_name = property(get_last_name, set_last_name)

    @property
    def full_name(self):
        return '%s %s' % (self._first_name, self._last_name)

class Citation(object):
    """
    Citation class.

    Attributes:
      * journal - a :class:`Journal` instance
      * authors - list of :class:`Author` instances
      * title - title of the paper
      * volume - volume in which the paper was published
      * first_page - first page of the paper
      * last_page - last page of the paper
      * year - year in which the paper was published
      * pubmed_id - pubmed id

    Examples:
      >>> from citation import Journal
      >>> j = Journal("Journal of Molecular Biology", "JMB")
      >>> from citation import Author
      >>> auths = [Author('Tjelvar S. G.', 'Olsson')]
      >>> from citation import Citation
      >>> c = Citation(j, auths,             # journal, authors
      ...              'Title of the paper', # title 
      ...              256,                  # volume
      ...              2156,                 # first page
      ...              2170,                 # last page
      ...              2009,                 # year
      ...              'PM12345678')         # pubmed id
      >>> c
      <Citation('JMB[2009]256,2156-2170')>

    """

    def __init__(self,
                 journal,
                 authors,
                 title,
                 volume,
                 first_page,
                 last_page,
                 year,
                 pubmed_id):
        self._journal = journal
        self._authors = authors
        self._title = title
        self._volume = volume
        self._first_page = first_page
        self._last_page = last_page
        self._year = year
        self._pubmed_id = pubmed_id

    def __repr__(self):
        return "<Citation('%s[%i]%i,%i-%i')>" % (self._journal.abbreviation,
                                                 self._year,
                                                 self._volume,
                                                 self._first_page,
                                                 self._last_page)

    def __str__(self):
        return "%s [%i] %i, %i-%i" % (self._journal.abbreviation,
                                      self._year,
                                      self._volume,
                                      self._first_page,
                                      self._last_page)

    def __eq__(self, other):
        """
        Returns true if the journal, year, volume and first page are the same.
        """
        if (    self.journal == other.journal
            and self.year == other.year
            and self.volume == other.volume
            and self.first_page == other.first_page):
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Returns false if the journal, year, volume and first page are the
        same.
        """
        if (    self.journal == other.journal
            and self.year == other.year
            and self.volume == other.volume
            and self.first_page == other.first_page):
            return False
        else:
            return True

    def set_journal(self, journal):
        self._journal = journal
    def get_journal(self):
        return self._journal
    journal = property(get_journal, set_journal)

    def set_authors(self, authors):
        self._authors = authors
    def get_authors(self):
        return self._authors
    authors = property(get_authors, set_authors)

    def set_title(self, title):
        self._title = title
    def get_title(self):
        return self._title
    title = property(get_title, set_title)

    def set_volume(self, volume):
        self._volume = volume
    def get_volume(self):
        return self._volume
    volume = property(get_volume, set_volume)

    def set_first_page(self, first_page):
        self._first_page = first_page
    def get_first_page(self):
        return self._first_page
    first_page = property(get_first_page, set_first_page)

    def set_last_page(self, last_page):
        self._last_page = last_page
    def get_last_page(self):
        return self._last_page
    last_page = property(get_last_page, set_last_page)

    def set_year(self, year):
        self._year = year
    def get_year(self):
        return self._year
    year = property(get_year, set_year)

    def set_pubmed_id(self, pubmed_id):
        self._pubmed_id = pubmed_id
    def get_pubmed_id(self):
        return self._pubmed_id
    pubmed_id = property(get_pubmed_id, set_pubmed_id)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import unittest
    TEST_SUITE = doctest.DocFileSuite('tests/test_citation.txt',
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    unittest.TextTestRunner().run(TEST_SUITE)
