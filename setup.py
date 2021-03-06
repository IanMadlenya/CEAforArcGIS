"""Installation script for the City Energy Analyst"""

import os
from setuptools import setup, find_packages

import cea

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas"]
__license__ = "MIT"
__version__ = cea.__version__
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = ['setuptools', 'SALib', 'deap', 'descartes', 'doit==0.29.0', 'ephem', 'fiona',
                    'geopandas', 'lxml', 'pandas', 'plotly', 'pycollada', 'pyproj', 'pysal', 'pyshp', 'requests',
                    'scikit-learn', 'shapely', 'simpledbf', 'xlrd', 'networkx', 'pyliburo>=0.1a8']

setup(name='cityenergyanalyst',
      version=__version__,
      description='City Energy Analyst',
      license='MIT',
      author='Architecture and Building Systems',
      author_email='cea@arch.ethz.ch',
      url='http://cityenergyanalyst.com',
      long_description=LONG_DESCRIPTION,
      py_modules=[''],
      packages=find_packages(),
      package_data={},
      dependency_links=['https://github.com/architecture-building-systems/pyliburo/tarball/master#egg=pyliburo-0.1a8'],
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      entry_points={
          'console_scripts': ['cea=cea.cli:main'],
      },
      extras_require={
          'dev': ['sphinx', 'twine']
      }
      )
