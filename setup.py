import sys
from setuptools import setup

install_requires = ['BeautifulSoup4', 'requests']
packages = ['AnimeNFO']
console_scripts = [
    'radio = AnimeNFO:simple',
    'radio-upcoming = AnimeNFO:main',
]

if '--extras' in sys.argv:
    sys.argv.remove('--extras')
    install_requires += ['gntp', 'clint', 'pillow']
    packages += ['AnimeNFO.cli']
    console_scripts += ['radio-growl = AnimeNFO.cli:main']


setup(
    name='AnimeNFO',
    description='AnimeNFO Radio Notifier',
    author='Paul Traylor',
    url='http://github.com/kfdm/radio-growl',
    version='0.2',
    packages=packages,
    install_requires=install_requires,
    entry_points={
        'console_scripts': console_scripts
    }
)
