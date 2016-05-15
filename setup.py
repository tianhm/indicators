#!/usr/bin/env python

from distutils.core import setup

setup(name='Indicators',
      version='1.0',
      description='Indicator code for common technical analysis indicators',
      author='Oliver Oberdorf',
      author_email='oly@barefootanalytics.com',
      url='http://www.barefootanalytics.com/',
      packages=['indicators'],
      package_dir={'': 'src'},
      requires=['stocklib', 'numpy'],
      )
