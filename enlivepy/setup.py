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
    version='0.1.3',
    description='Html Tranformation Library',
    author='makkalot',
    author_email='makkalot@gmail.com',
    packages=['enlivepy','enlivepy.test'],
    url='https://github.com/makkalot/enlivepy',
    install_requires=['lxml', 'cssselect'],
    test_suite='enlivepy.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
      ],
    keywords=['templating', 'html', 'transformation']
)
