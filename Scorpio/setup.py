import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress'
    ]


tests_require = [
    'WebTest >= 1.3.1',  
    'pytest',
    'pytest-cov',
    ]


setup(name='scorpio',
      version='2.1.0',
      description='Structure-Calorimetry Of Reported Protein Interactions Online',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Demetriana Pandi',
      author_email='dp001@mail.bbk.ac.uk',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='template',
      install_requires=requires,
      extras_require={
        'testing': tests_require,
      },
      entry_points="""\
      [paste.app_factory]
      main = scorpio:main
      [console_scripts]
      initialize_db = scorpio.scripts.initializedb:main
      """,
      )
