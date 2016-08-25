#!/usr/bin/env python
import doctest
import unittest
import os
import os.path

def get_filenames_from_dir(directory, all=False, prefix=None, suffix=None):
    """
    Get filenames from directory.

    Optional arguements:
    * all    - return hidden files as well (default False)
    * prefix - only get file names with prefix
    * suffix - only get file names with suffix
    """
    filenames = os.listdir(directory)
    if not all:
        filenames = [filename for filename in filenames
                     if not os.path.basename(filename).startswith('.')]
    if prefix:
        filenames = [filename for filename in filenames
                     if os.path.basename(filename).startswith(prefix)]
    if suffix:
        filenames = [filename for filename in filenames
                     if filename.endswith(suffix)]
    return [os.path.join(directory, filename) for filename in filenames]
suite = unittest.TestSuite()

def add_module_tests():
    for filename in get_filenames_from_dir('./', suffix='.py'):
        suite.addTest(doctest.DocFileSuite(filename,
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE
                      + doctest.REPORT_ONLY_FIRST_FAILURE))

def add_regression_tests():
    for filename in get_filenames_from_dir('./tests', suffix='.txt'):
        suite.addTest(doctest.DocFileSuite(filename,
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE
                      + doctest.REPORT_ONLY_FIRST_FAILURE))

def add_documentation_tests():
    for filename in get_filenames_from_dir('./doc', suffix='.rst'):
        suite.addTest(doctest.DocFileSuite(filename,
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE
                      + doctest.REPORT_ONLY_FIRST_FAILURE))

add_module_tests()
add_regression_tests()
add_documentation_tests()

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
