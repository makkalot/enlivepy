# -*- coding: utf-8 -*-
""" enlivepy setup.py script """


# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name="enlivepy",
    version='0.1.0',
    description='Html Tranformation Library',
    author='makkalot',
    author_email='makkalot@gmail.com',
    packages=['enlivepy','enlivepy.test'],
    url='https://github.com/makkalot/enlivepy',
    long_description=open('README.txt').read(),
    install_requires=['lxml'],
    test_suite='enlivepy.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
      ],
)
