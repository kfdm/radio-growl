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
    py_modules=['AnimeNFO', 'AnimeNFO.cli'],
    install_requires=['BeautifulSoup', 'gntp'],
    dependency_links=[
        "https://github.com/kfdm/gntp/tarball/master#egg=gntp",
        "https://github.com/kfdm/pydefaults/tarball/master#egg=pydefaults",
    ],
    entry_points={
        'console_scripts': [
            'radio-growl = AnimeNFO.cli:main'
        ]
    }
)
