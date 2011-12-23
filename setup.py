#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='AnimeNFO',
    description='AnimeNFO Radio Notifier',
    author='Paul Traylor',
    url='http://github.com/kfdm/radio-growl',
    version='0.2',
    packages=['AnimeNFO'],
    install_requires=['BeautifulSoup']
)
