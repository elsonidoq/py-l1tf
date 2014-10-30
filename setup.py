#!/usr/bin/env python

from setuptools import setup

setup(name='l1tf',
      version='0.1',
      description='L1 trend filtering',
      author='Pablo Zivic',
      author_email='pablozivic@gmail.com',
      url='pablozivic.com.ar',
      packages=['l1tf'],
      install_requires=['pandas==0.13.1',
                'cvxopt==1.1.7']

     )
